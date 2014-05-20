# -*- coding: utf-8 -*-
"""
Acceptance tests for Video grading functionality.
"""
from ...pages.lms.progress import ProgressPage
from .test_video_module import VideoBaseTest


# @TODO
# start-end time:
## 1) scored_on_end on entTime
# 2) scored_on_end is not scored if we seek it to the end of the video
# 3) scored_on_end is scored if we seek it at the endTime point and video is not playing
## 4) scored_on_end is scored if we click download video button
## 5) scored_on_percent is scored at 50% of start-end time interval
## 6) scored_on_percent with saved position
## 7) basic_grader is scored when we click play button
## 8) basic_grader is scored when we click download video button


class VideoGradedTest(VideoBaseTest):
    """ Test Video Player """

    def setUp(self):
        super(VideoGradedTest, self).setUp()
        self.progress_page = ProgressPage(self.browser, self.course_id)

    def _assert_video_is_not_scored(self, weight=1.0):
        self.assertEquals(self.video.progress_message_text(), '({} points possible)'.format(weight))
        self.assertFalse(self.video.is_status_message_shown())

    def _assert_video_is_scored_successfully(self, weight=1.0):
        self.assertEquals(self.video.progress_message_text(), '({} / {} points)'.format(weight, weight))
        self.assertEquals(self.video.status_message_text(), 'You\'ve received credit for viewing this video.')

    def _assert_video_is_graded_successfully(self, weight=1.0):
        self.tab_nav.go_to_tab('Progress')
        actual_scores = self.progress_page.scores('Test Chapter', 'Test Section')
        self.assertEqual(actual_scores, [(int(weight), int(weight))])


class YouTubeVideoGradedTest(VideoGradedTest):
    """ Test YouTube Video Player """

    def setUp(self):
        super(YouTubeVideoGradedTest, self).setUp()

    def test_video_is_scored_by_percent_to_view(self):
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
        data = {'has_score': True, 'scored_on_percent': 1, 'grade_videos': True}
        self.metadata = self.metadata_for_mode('youtube', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_not_scored()
        self.video.click_player_button('play')
        self.video.wait_for_status_message()
        self._assert_video_is_scored_successfully()
        self._assert_video_is_graded_successfully()

    def test_video_basic_grader_on_play(self):
        """
        Scenario: Video Basic Grader
        Given the course has a Video component in "Youtube" mode:
        |has_score|
        |True     |
        And I see progress message is "1.0 points possible"
        And I do not see status message
        And I click video button "play"
        Then I see status and progress messages are visible
        And I see progress message is "(1.0 / 1.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "1/1"
        """
        data = {'has_score': True, 'grade_videos': True}
        self.metadata = self.metadata_for_mode('youtube', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_not_scored()
        self.video.click_player_button('play')
        self.video.wait_for_status_message()
        self._assert_video_is_scored_successfully()
        self._assert_video_is_graded_successfully()

    def test_video_basic_grader_on_download_video_button(self):
        """
        Scenario: Video Basic Grader
        Given the course has a Video component in "Youtube" mode:
        |has_score|
        |True     |
        And I see progress message is "1.0 points possible"
        And I do not see status message
        And I click video button "play"
        Then I see status and progress messages are visible
        And I see progress message is "(1.0 / 1.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "1/1"
        """
        data = {'has_score': True, 'grade_videos': True}
        self.metadata = self.metadata_for_mode('youtube', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_not_scored()
        self.video.click_player_button('download_video')
        self.video.wait_for_status_message()
        self._assert_video_is_scored_successfully()
        self._assert_video_is_graded_successfully()

    def test_video_is_scored_by_on_end_andclick_download_video_button(self):
        """
        Scenario: Video component is scored by percent viewed
        Given the course has a Video component in "Youtube" mode:
        |has_score|scored_on_end|weight|
        |True     |True         |15    |
        And I see progress message is "15.0 points possible"
        And I do not see status message
        And I click video button "play"
        And I click video button "Download Video"
        Then I see status and progress messages are visible
        And I see progress message is "(15.0 / 15.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "15/15"
        """
        data = {
            'has_score': True,
            'scored_on_end': True,
            'weight': 15.0,
            'grade_videos': True,
        }
        self.metadata = self.metadata_for_mode('youtube', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_not_scored(weight=15.0)
        self.video.click_player_button('play')
        self.video.click_player_button('download_video')
        self.video.wait_for_status_message()
        self._assert_video_is_scored_successfully(weight=15.0)
        self._assert_video_is_graded_successfully(weight=15.0)


class Html5VideoGradedTest(VideoGradedTest):
    """ Test Html5 Video Player """

    def setUp(self):
        super(Html5VideoGradedTest, self).setUp()

    def test_video_is_scored_by_on_end(self):
        """
        Scenario: Video component is scored by percent viewed
        Given the course has a Video component in "Html5" mode:
        |has_score|scored_on_end|weight|
        |True     |True         |15    |
        And I see progress message is "15.0 points possible"
        And I do not see status message
        And I click video button "play"
        Then I see status and progress messages are visible
        And I see progress message is "(15.0 / 15.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "15/15"
        """
        data = {
            'has_score': True,
            'scored_on_end': True,
            'weight': 15.0,
            'grade_videos': True,
        }
        self.metadata = self.metadata_for_mode('html5', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_not_scored(weight=15.0)
        self.video.click_player_button('play')

        # Play the video until the end.
        self.video.wait_for_state('finished');

        self._assert_video_is_scored_successfully(weight=15.0)
        self._assert_video_is_graded_successfully(weight=15.0)

    def test_video_is_scored_when_all_graders_are_enabled(self):
        """
        Scenario: Video component is scored by percent viewed
        Given the course has a Video component in "Html5" mode:
        |has_score|scored_on_end|scored_on_percent|
        |True     |True         |20%              |
        And I click video button "play"
        And the video is playing up to "0:02" seconds
        And I click video button "pause"
        And I see progress message is still "1.0 points possible"
        And I still do not see status message
        Then I reload the page
        And I click video button "play"
        And the video is playing up to the end
        Then I see status and progress messages are visible
        And I see progress message is "(1.0 / 1.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "1/1"
        """
        data = {'has_score': True, 'scored_on_end': True, 'scored_on_percent': 40, 'grade_videos': True}
        self.metadata = self.metadata_for_mode('html5', additional_data=data)
        self.navigate_to_video()

        self.video.click_player_button('play')
        self.video.wait_for_position('0:03')
        # Video total time is 5 sec.
        # So 100 * 3/5 = 60% of video is played and it means that
        # `scored_on_percent` grader is passed. So, we pause the video and
        # verify that status and progress messages are still the same.
        self.video.click_player_button('pause')
        self._assert_video_is_not_scored()

        # Reloads the page and waits for content loading.
        self.browser.refresh()
        self.video.wait_for_page()

        self.video.click_player_button('play')

        # Play the video until the end.
        self.video.wait_for_state('finished');

        self._assert_video_is_scored_successfully()
        self._assert_video_is_graded_successfully()


    def test_video_score_messages_are_saved_between_seq_switch(self):
        """
        Same as test_video_is_scored_by_on_end,
        but after that navigate to other position of sequential and back,
        and same message should still appear.
        """
        data = {'has_score': True, 'scored_on_end': True, 'grade_videos': True}
        a_metadata = self.metadata_for_mode('html5', additional_data=data)
        b_metadata = self.metadata_for_mode('html5')

        self.verticals = [
            [{'display_name': 'A', 'metadata': a_metadata}],
            [{'display_name': 'B', 'metadata': b_metadata}],
        ]

        # open the section with videos (open video "A")
        self.navigate_to_video()
        self._assert_video_is_not_scored()
        self.video.click_player_button('play')

        # Play the video until the end.
        self.video.wait_for_state('finished');

        self._assert_video_is_scored_successfully()

        self.course_nav.go_to_sequential('B')
        self.course_nav.go_to_sequential('A')

        self._assert_video_is_scored_successfully()


class VideoGradedWithStartEndTimesTest(VideoGradedTest):
    """ Test YouTube Video Player """

    def setUp(self):
        super(VideoGradedWithStartEndTimesTest, self).setUp()

    def test_video_is_scored_by_percent_to_view(self):
        """
        Scenario: Video Percent to View
        Given the course has a Video component in "Youtube" mode:
        |has_score|scored_on_percent|start_time|end_time|
        |True     |50%              |0:10      |0:20    |
        And I see progress message is "1.0 points possible"
        And I do not see status message
        And I click video button "play"
        Then I see status and progress messages are visible
        And I see progress message is "(1.0 / 1.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "1/1"
        """
        data = {
            'has_score': True,
            'scored_on_percent': 50,
            'grade_videos': True,
            'start_time': '0:10',
            'end_time': '0:20',
        }
        self.metadata = self.metadata_for_mode('youtube', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_not_scored()
        self.video.click_player_button('play')
        self.video.wait_for_status_message()
        self._assert_video_is_scored_successfully()
        self._assert_video_is_graded_successfully()

    def test_video_is_scored_by_on_end(self):
        """
        Scenario: Video component is scored by percent viewed
        Given the course has a Video component in "Youtube" mode:
        |has_score|scored_on_end|weight|
        |True     |True         |15    |
        And I see progress message is "15.0 points possible"
        And I do not see status message
        And I click video button "play"
        Then I see status and progress messages are visible
        And I see progress message is "(15.0 / 15.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "15/15"
        """
        data = {
            'has_score': True,
            'scored_on_end': True,
            'grade_videos': True,
            'weight': 15.0,
            'start_time': '0:10',
            'end_time': '0:20',
        }
        self.metadata = self.metadata_for_mode('youtube', additional_data=data)
        self.navigate_to_video()
        self._assert_video_is_not_scored(weight=15.0)
        self.video.click_player_button('play')

        # Play the video until the end.
        self.video.wait_for_state('paused');

        self._assert_video_is_scored_successfully(weight=15.0)
        self._assert_video_is_graded_successfully(weight=15.0)

    def test_video_is_scored_by_percent_with_stored_position(self):
        """
        Scenario: Video component is scored by percent viewed
        Given the course has a Video component in "Youtube" mode:
        |has_score|scored_on_percent|start_time|end_time|
        |True     |50%              |0:10      |0:20    |
        And I click video button "play"
        And the video is playing up to "0:13" seconds
        And I click video button "pause"
        And I see progress message is still "1.0 points possible"
        And I still do not see status message
        Then I reload the page
        And I see the video position is "0:13"
        And I click video button "play"
        And the video is playing up to the position "0:15"
        Then I see status and progress messages are visible
        And I see progress message is "(1.0 / 1.0 points)"
        And I see status message is "You've received credit for viewing this video."
        When I open progress page
        Then I see current scores are "1/1"
        """
        data = {
            'has_score': True,
            'scored_on_percent': 50,
            'grade_videos': True,
            'start_time': '0:10',
            'end_time': '0:20',
            }
        self.metadata = self.metadata_for_mode('youtube', additional_data=data)
        self.navigate_to_video()

        self.video.click_player_button('play')
        self.video.wait_for_position('0:13')
        # Video total time is 5 sec.
        # So 100 * 3/5 = 60% of video is played and it means that
        # `scored_on_percent` grader is passed. So, we pause the video and
        # verify that status and progress messages are still the same.
        self.video.click_player_button('pause')
        self._assert_video_is_not_scored()

        # Reloads the page and waits for content loading.
        self.browser.refresh()
        self.video.wait_for_page()

        self.assertEquals(self.video.position(), '0:13')
        self.video.click_player_button('play')

        # Play the video until the end.
        self.video.wait_for_position('0:15')
        self.video.click_player_button('pause')
        self.video.wait_for_status_message()

        self._assert_video_is_scored_successfully()
        self._assert_video_is_graded_successfully()

