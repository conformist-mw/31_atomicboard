import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PHANTOMJS_PATH = './node_modules/phantomjs-prebuilt/bin/phantomjs'
CREATE_USER_URL = 'http://atomicboard.devman.org/create_test_user/'
URL = 'http://atomicboard.devman.org/'
TEXT_FOR_TEST = 'test_test_test'


class AtomicBoardTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS(PHANTOMJS_PATH)
        self.driver.set_window_size(1366, 768)
        self.driver.get(CREATE_USER_URL)
        self.driver.find_element(By.TAG_NAME, 'button').click()
        self.driver.get(URL)
        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tickets-column')))

    def test_whole_page_loaded(self):
        assert self.driver.find_element(By.CLASS_NAME, 'js-tickets-column')

    def test_edit_exist_task(self):
        self.driver.find_element(By.CSS_SELECTOR, 'span.editable').click()
        task_input = self.driver.find_element(By.CLASS_NAME, 'editable-input')
        task_input.clear()
        task_input.send_keys(TEXT_FOR_TEST)
        self.driver.find_element(By.CLASS_NAME, 'glyphicon-ok').click()
        tasks = self.driver.find_elements(By.CLASS_NAME, 'editable')
        test_text = [x.text for x in tasks if x.text == TEXT_FOR_TEST][0]
        assert test_text == TEXT_FOR_TEST

    def test_mark_task_closed(self):
        tasks = self.driver.find_elements(By.CLASS_NAME, 'ticket_status')
        open_task = [e for e in tasks if e.text == 'open'][0]
        open_task.click()
        sleep(5)
        buttons = self.driver.find_elements(By.CLASS_NAME,
                                            'change-status-form__button')
        [b for b in buttons if b.text == 'closed'][0].click()
        assert open_task.text == 'closed'

    def test_add_new_task(self):
        add_span = self.driver.find_element(By.CLASS_NAME,
                                            'add-ticket-block_button')
        add_span.click()
        input_field = self.driver.find_element(By.CLASS_NAME, 'editable-input')
        input_field.send_keys('new_task_added')
        self.driver.find_element(By.CLASS_NAME, 'glyphicon-ok').click()
        sleep(5)
        tasks = self.driver.find_elements(By.CLASS_NAME, 'editable')
        assert len([t for t in tasks if t.text == 'new_task_added']) == 1

    def test_drag_and_drop_task(self):
        cols = self.driver.find_elements(By.CLASS_NAME, 'tickets-column')
        task = cols[0].find_element(By.CLASS_NAME, 'js-ticket')
        task_text = task.text
        with open("drag_and_drop_helper.js") as drag_and_drop_file:
            drag_and_drop_js = drag_and_drop_file.read()
        self.driver.execute_script(
            drag_and_drop_js + ('$("div.js-ticket:eq(0)").simulateDragDrop('
                                '{dropTarget: "span.tickets-column:eq(1)"});'))

        target_text = cols[1].find_element(By.CLASS_NAME, 'js-ticket').text
        assert task_text == target_text

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
