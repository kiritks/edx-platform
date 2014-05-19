"""
Edge homepage
"""
from . import BASE_URL
from bok_choy.page_object import PageObject


class EdgeHomePage(PageObject):
    """
    Edge Home page.
    """

    @property
    def url(self):
        return "{0}/?edge=True".format(BASE_URL)

    def is_browser_on_page(self):
        return self.q(css='body.edge-landing').present

    def open_register_modal(self):
        """
        Open register modal and return page object for it.
        """

        self.q(css='a.register-button').first.click()
        register_modal = EdgeRegisterPage(self.browser)
        return register_modal


class EdgeRegisterPage(PageObject):
    """
    Edge Register Modal Page.
    """

    url = None

    def is_browser_on_page(self):
        return self.q(css='section.signup-modal').present

    def check_modal_visible(self):
        """
        Check signup modal is visible.
        """
        return self.q(css='section.signup-modal').visible