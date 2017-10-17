import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PHANTOMJS_PATH = './node_modules/phantomjs-prebuilt/bin/phantomjs'
CREATE_USER_URL = 'http://atomicboard.devman.org/create_test_user/'
URL = 'http://atomicboard.devman.org/'
TEXT_FOR_TEST = 'test_test_test'
TEST_TASK_HEADING = 'test_task_heading'


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

    def test_edit_existing_task(self):
        self.driver.find_element(By.CSS_SELECTOR, 'span.editable').click()
        task_input = self.driver.find_element(By.CLASS_NAME, 'editable-input')
        task_input.clear()
        task_input.send_keys(TEXT_FOR_TEST)
        self.driver.find_element(By.CLASS_NAME, 'glyphicon-ok').click()
        tasks = self.driver.find_elements(By.CLASS_NAME, 'editable')
        assert any([task.text for task in tasks if task.text == TEXT_FOR_TEST])

    def test_mark_task_closed(self):
        tasks = self.driver.find_elements(By.CLASS_NAME, 'ticket_status')
        open_task = [task for task in tasks if task.text == 'open'][0]
        open_task.click()
        WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CLASS_NAME,
                                        'change-status-form__button')))
        self.driver.find_element(
            By.CSS_SELECTOR,
            'button.btn-primary.change-status-form__button').click()
        assert open_task.text == 'closed'

    def test_add_new_task(self):
        self.driver.find_element(By.CLASS_NAME,
                                 'add-ticket-block_button').click()
        input_field = self.driver.find_element(By.CLASS_NAME, 'editable-input')
        input_field.send_keys(TEST_TASK_HEADING)
        self.driver.find_element(By.CLASS_NAME, 'glyphicon-ok').click()
        WebDriverWait(self.driver, 25).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR,
                                                'input.editable-input')))
        tasks = self.driver.find_elements(By.CLASS_NAME, 'editable')
        assert any([task for task in tasks if task.text == TEST_TASK_HEADING])

    def test_drag_and_drop_task(self):
        # This test running with drug_n_drop_helper.js script
        # check the SO answer https://stackoverflow.com/a/29381532/3355831
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
