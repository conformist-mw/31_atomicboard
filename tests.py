import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

PHANTOMJS_PATH = './node_modules/phantomjs/bin/phantomjs'
CREATE_USER_URL = 'http://atomicboard.devman.org/create_test_user/'
URL = 'http://atomicboard.devman.org/'


class AtomicBoardTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS(PHANTOMJS_PATH)
        self.driver.set_window_size(1366, 768)
        self.driver.get(CREATE_USER_URL)
        self.driver.find_element_by_xpath('//body/form/button[@type="submit"]').click()
        self.driver.get(URL)
        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tickets-column')))

    def test_whole_page_loaded(self):
        assert self.driver.find_element_by_xpath('//*[contains(@class, "js-tickets-column")]')

    def test_edit_exist_task(self):
        task_span = self.driver.find_element_by_xpath('//span[@editable-text="ticket.title"]')
        task_span.click()
        task_input = self.driver.find_element_by_xpath('//input[contains(@class, "editable-input")]')
        task_input.clear()
        task_input.send_keys('test_task_edit')
        ok_button = self.driver.find_element_by_xpath('//span[@class="glyphicon glyphicon-ok"]')
        ok_button.click()
        assert self.driver.find_element_by_xpath('//*[contains(text(), "test_task_edit")]')

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
