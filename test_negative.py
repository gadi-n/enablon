from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import utils

TASK_ELEMENT = "//*[@data-testid='todo-item-label']"
CHECKBOX_ELEMENT = "//input[@class='toggle' and @type='checkbox' and @data-testid='todo-item-toggle']"
LEFT_ITEMS_TEXT_ELEMENT = 'todo-count'


def test_fail_to_create_empty_task(browser, open_url, textbox_element):
    utils.create_single_task(textbox_element, '   ')
    all_tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(all_tasks) == 0, f'Error! there are {len(all_tasks)} tasks but there should be 0'


def test_fail_to_create_1_char_task(browser, open_url, textbox_element):
    utils.create_single_task(textbox_element, 'a')
    all_tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(all_tasks) == 0, f'Error! there are {len(all_tasks)} tasks but there should be 0'


def test_tasks_not_save_after_refresh(browser, open_url, textbox_element):
    utils.create_tasks(browser, 3, 'task', textbox_element)
    browser.refresh()
    all_tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(all_tasks) == 0, f'Error! there are {len(all_tasks)} tasks but there should be 0'


def test_fail_to_edit_to_empty_task(browser, open_url, textbox_element, action_chains):
    input_tasks = utils.delete_task_text(browser, textbox_element, action_chains, 'task')
    input_tasks[1].send_keys(Keys.ENTER)
    tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(tasks) == 0, f"Error! Task created with text '{tasks[0].text}'"


def test_fail_to_edit_to_1_char_task(browser, open_url, textbox_element, action_chains):
    input_tasks = utils.delete_task_text(browser, textbox_element, action_chains, 'task')
    input_tasks[1].send_keys('a')
    input_tasks[1].send_keys(Keys.ENTER)
    tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(tasks) == 0, f"Error! Task created with text '{tasks[0].text}'"
