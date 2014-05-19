
from bok_choy.web_app_test import WebAppTest
from ..pages.lms.edge_homepage import EdgeHomePage


class EdgeHomePageTest(WebAppTest):
    """
    Test edge homepage.
    """

    def setUp(self):
        super(EdgeHomePageTest, self).setUp()
        self.homepage = EdgeHomePage(self.browser)

    def test_register_button(self):
        """
        Test register button on edge homepage.
        """

        self.homepage.visit()
        modal_page = self.homepage.open_register_modal()

        # Should be True.
        self.assertTrue(modal_page.check_modal_visible())
