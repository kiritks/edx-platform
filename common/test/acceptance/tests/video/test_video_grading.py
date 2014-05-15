# -*- coding: utf-8 -*-

"""
Acceptance tests for Video grading functionality.
"""

# @TODO
# 1) Verify if grading on percentage works correctly and progress is shown.
# 2) Verify if grading on video finish works correctly and progress is shown.
# 3) Verify if both graders work well.
# 4) Verify if video messages are stored when user navigates between sequentials.
# 5) Verify error message and score is not stored (reload page and check progress message).


from ...pages.lms.progress import ProgressPage
from .test_video_module import VideoBaseTest


class VideoGradedTest(VideoBaseTest):
    """ Test Video Player """

    def setUp(self):
        super(VideoGradedTest, self).setUp()
        self.progress_page = ProgressPage(self.browser, self.course_id)

    def _assert_video_is_scored_successfully(self):
        self.assertEquals(self.video.progress_message_text(), '(1.0 points possible)')
        self.assertFalse(self.video.is_status_message_shown())

        self.video.click_player_button('play')
        self.video.wait_for_status_message();

        self.assertEquals(self.video.progress_message_text(), '(1.0 / 1.0 points)')
        self.assertEquals(self.video.status_message_text(), 'You\'ve received credit for viewing this video.')

        self.tab_nav.go_to_tab('Progress')

        EXPECTED_SCORES = [(1, 1)]
        actual_scores = self.progress_page.scores('Test Chapter', 'Test Section')
        self.assertEqual(actual_scores, EXPECTED_SCORES)


class YouTubeVideoGradedTest(VideoGradedTest):
    """ Test YouTube Video Player """

    def setUp(self):
        super(YouTubeVideoGradedTest, self).setUp()

    def test_video_percent_to_view(self):
        """
        Scenario: Video Percent to View
        Given the course has a Video component in "Youtube" mode:
        |has_score|scored_on_percent|
        |True     |1%               |
        And I see progress message is "1.0 points possible"
        And I do not see status message
        And I click video button "play"
        Then I see status and progress messages are visible
        And I see progress message is "(1.0 / 1.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "1/1"
        """
        data = {'has_score': True, 'scored_on_percent': 1}
        self.metadata = self.metadata_for_mode('html5', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_scored_successfully()


class Html5VideoGradedTest(VideoGradedTest):
    """ Test Html5 Video Player """

    def setUp(self):
        super(Html5VideoGradedTest, self).setUp()

    def test_video_is_scored_by_percent_viewed(self):
        """
        Scenario: Video component is scored by percent viewed
        Given the course has a Video component in "Youtube" mode:
        |has_score|scored_on_end|
        |True     |True         |
        And I see progress message is "1.0 points possible"
        And I do not see status message
        And I click video button "play"
        Then I see status and progress messages are visible
        And I see progress message is "(1.0 / 1.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "1/1"
        """
        data = {'has_score': True, 'scored_on_end': True}
        self.metadata = self.metadata_for_mode('html5', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_scored_successfully()

