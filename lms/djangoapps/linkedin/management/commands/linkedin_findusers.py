"""
Provides a command to use with Django's `manage.py` that uses LinkedIn's API to
find edX users that are also users on LinkedIn.
"""
import datetime
import pytz
import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from optparse import make_option

from util.query import use_read_replica_if_available
from linkedin.models import LinkedIn
from . import LinkedInAPI

FRIDAY = 4


def get_call_limits(force_unlimited=False):
    """
    Returns a tuple of: (max_checks, checks_per_call, time_between_calls)

    Here are the parameters provided by LinkedIn:

    Please note: in order to ensure a successful call, please run the calls
    between Friday 6pm PST and Monday 5am PST.

    During the week, calls are limited to very low volume (500 profiles/day)
    and must be run after 6pm and before 5am. This should only be used to do
    subsequent trigger emails. Please contact the developer support alias for
    more information.

    Use 80 emails per API call and 1 call per second.
    """
    now = timezone.now().astimezone(pytz.timezone('US/Pacific'))
    lastfriday = now
    while lastfriday.weekday() != FRIDAY:
        lastfriday -= datetime.timedelta(days=1)
    safeharbor_begin = lastfriday.replace(hour=18, minute=0)
    safeharbor_end = safeharbor_begin + datetime.timedelta(days=2, hours=11)
    if force_unlimited or (safeharbor_begin < now < safeharbor_end):
        return -1, 80, 1
    elif now.hour >= 18 or now.hour < 5:
        return 500, 80, 1
    else:
        return 0, 0, 0


class Command(BaseCommand):
    """
    Provides a command to use with Django's `manage.py` that uses LinkedIn's
    API to find edX users that are also users on LinkedIn.
    """
    args = ''
    help = 'Checks LinkedIn for students that are on LinkedIn'
    option_list = BaseCommand.option_list + (
        make_option(
            '--recheck',
            action='store_true',
            dest='recheck',
            default=False,
            help='Check users that have been checked in the past to see if '
                 'they have joined or left LinkedIn since the last check'
        ),
        make_option(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Disregard the parameters provided by LinkedIn about when it '
                 'is appropriate to make API calls.'
        )
    )

    def handle(self, *args, **options):
        """
        Check users.
        """
        api = LinkedInAPI(self)
        recheck = options.get('recheck', False)
        force = options.get('force', False)
        max_checks, checks_per_call, time_between_calls = get_call_limits(force)

        if not max_checks:
            raise CommandError("No checks allowed during this time.")

        def user_batches_to_check():
            """Generate batches of users we should query against LinkedIn."""
            count = 0
            batch = []

            users = use_read_replica_if_available(
                None
            )
            for user in User.objects.all():
                if not hasattr(user, 'linkedin'):
                    LinkedIn(user=user).save()
                checked = user.linkedin.has_linkedin_account is not None
                if recheck or not checked:
                    batch.append(user)
                    if len(batch) == checks_per_call:
                        yield batch
                        batch = []

                    count += 1
                    if max_checks != -1 and count >= max_checks:
                        self.stderr.write(
                            "WARNING: limited to checking only %d users today."
                            % max_checks)
                        break
            if batch:
                yield batch

        def update_linkedin_account_status(users):
            """
            Given a an iterable of User objects, check their email addresses
            to see if they have LinkedIn email addresses and save that
            information to our database.
            """
            emails = (u.email for u in users)
            for user, has_account in zip(users, api.batch(emails)):
                linkedin = user.linkedin
                if linkedin.has_linkedin_account != has_account:
                    linkedin.has_linkedin_account = has_account
                    linkedin.save()

        for i, user_batch in enumerate(user_batches_to_check()):
            if i > 0:
                # Sleep between LinkedIn API web service calls
                time.sleep(time_between_calls)
            update_linkedin_account_status(user_batch)