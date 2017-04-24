import unittest
from time import sleep
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
        self.driver.find_element_by_xpath(
            '//body/form/button[@type="submit"]').click()
        self.driver.get(URL)
        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tickets-column')))

    def test_whole_page_loaded(self):
        assert self.driver.find_element_by_xpath(
            '//*[contains(@class, "js-tickets-column")]')

    def test_edit_exist_task(self):
        self.driver.find_element_by_xpath(
            '//span[@editable-text="ticket.title"]').click()
        task_input = self.driver.find_element_by_xpath(
            '//input[contains(@class, "editable-input")]')
        task_input.clear()
        task_input.send_keys('test_task_edit')
        self.driver.find_element_by_xpath(
            '//span[@class="glyphicon glyphicon-ok"]').click()
        assert self.driver.find_element_by_xpath(
            '//*[contains(text(), "test_task_edit")]')

    def test_mark_task_closed(self):
        task = self.driver.find_element_by_xpath(
            '//span[contains(@class, "js-tickets-column")][1]/div[contains(@class, "js-ticket")]')
        task.find_element_by_xpath(
            '//span[contains(@class, "ticket_status") and contains(text(), "open")]').click()
        sleep(5)
        self.driver.find_element_by_xpath(
            '//button[contains(@class, "change-status-form__button") and contains(text(), "closed")]').click()
        assert task.find_element_by_xpath(
            '//span[contains(@class, "ticket_status") and contains(text(), "closed")]')

    def test_add_new_task(self):
        add_span = self.driver.find_element_by_xpath(
            '//span[contains(@class, "add-ticket-block_button")]')
        add_span.click()
        input_field = add_span.find_element_by_xpath(
            '//following-sibling::form/div/input')
        input_field.send_keys('new_task_added')
        input_field.find_element_by_xpath(
            '//following-sibling::span/button/span[@class="glyphicon glyphicon-ok"]').click()
        sleep(5)
        assert self.driver.find_element_by_xpath(
            '//span[contains(text(), "new_task_added")]')

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
