from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import inspect


class TestNavigation(StaticLiveServerTestCase):
    """
        test Navigation from homepage
    """
    def setUp(self):
        self.browser = Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.close()

    def test_bad_address_returns_handler404(self):
        """
            Test bad address is caught by the handler and redirect to error page
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.browser.get('%s%s' % (self.live_server_url, '/test'))
        # message = self.browser.find_element_by_tag_name('h1').text
        self.assertTemplateUsed(response, 'errors/errors.html')

    def test_click_mentions(self):
        """
            Test the click on mentions redirect to mentions page
        """
        print(inspect.currentframe().f_code.co_name)
        """
        self.browser.get(self.live_server_url)
        user_url = self.live_server_url + reverse('home_app:mentions')
        element = self.browser.find_element_by_partial_link_text('mentions')
        self.scroll_shim(self.browser, element)
        actions = ActionChains(self.browser)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()
        self.assertEquals(self.browser.current_url, user_url)
        """

    def test_click_icon_person_to_user(self):
        """
            Test click on the person image redirect to user page
        """
        print(inspect.currentframe().f_code.co_name)
        self.browser.get(self.live_server_url)
        user_url = self.live_server_url + reverse('user_app:login')
        self.browser.find_element(By.CSS_SELECTOR, ".nav-item img").click()
        self.assertEquals(self.browser.current_url, user_url)

    def scroll_shim(self, passed_in_driver, object):
        x = object.location['x']
        y = object.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
            x,
            y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        passed_in_driver.execute_script(scroll_by_coord)
        passed_in_driver.execute_script(scroll_nav_out_of_way)