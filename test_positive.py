from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import utils

TASK_ELEMENT = "//*[@data-testid='todo-item-label']"
CHECKBOX_ELEMENT = "//input[@class='toggle' and @type='checkbox' and @data-testid='todo-item-toggle']"
LEFT_ITEMS_TEXT_ELEMENT = 'todo-count'


def test_homepage_content(browser, open_url, textbox_element):
    # verify header
    header_text = browser.find_element(By.CSS_SELECTOR, "h1").text
    assert header_text == "todos", f'Error! Header text is {header_text} and not "todos"'
    # verify placeholder
    placeholder_text = textbox_element.get_attribute("placeholder")
    assert placeholder_text == 'What needs to be done?', (f'Error! Place holder text is '
                                                          f'{placeholder_text} and not "What needs to be done"?')
    # verify footer
    footer_text = browser.find_element(By.CLASS_NAME, "info").text
    assert footer_text == "Double-click to edit a todo\nCreated by the TodoMVC Team\nPart of TodoMVC", \
        (f'Error! footer text text is {footer_text} '
         f'and not "Double-click to edit a todo\nCreated by the TodoMVC Team\nPart of TodoMVC"')
    # verify link
    href_value = browser.find_element(By.LINK_TEXT, "TodoMVC").get_attribute("href")
    assert href_value == "http://todomvc.com/", f'link leads to {href_value} and not to "http://todomvc.com/"'


def test_create_several_tasks(browser, open_url, textbox_element):
    utils.create_tasks(browser, 5, 'task', textbox_element, verify_creation=True)


def test_edit_task(browser, open_url, textbox_element, action_chains):
    input_tasks = utils.delete_task_text(browser, textbox_element, action_chains, 'old task')
    for char in 'new task':
        input_tasks[1].send_keys(char)
    input_tasks[1].send_keys(Keys.ENTER)
    task = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert task[0].text == f'new task', f"Error! Task text is {task[0].text} and not 'new task'"


def test_complete_task_and_display_by_status(browser, open_url, textbox_element):
    # preconditions - create tasks
    utils.create_tasks(browser, 5, 'task', textbox_element)
    checkboxes = (browser.find_elements(By.XPATH, CHECKBOX_ELEMENT))
    # complete tasks
    checkboxes[0].click()
    checkboxes[2].click()
    # show only completed
    browser.find_element(By.LINK_TEXT, "Completed").click()
    completed_tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(completed_tasks) == 2, f'Error! there are {len(completed_tasks)} completed tasks but there should be 2'
    utils.validate_task_appears('task', [1, 3], completed_tasks)
    # show only active
    browser.find_element(By.LINK_TEXT, "Active").click()
    active_tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(active_tasks) == 3, f'Error! there are {len(active_tasks)} active tasks but there should be 3'
    utils.validate_task_appears('task', [2, 4, 5], active_tasks)
    # show all tasks
    browser.find_element(By.LINK_TEXT, "All").click()
    all_tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(all_tasks) == 5, f'Error! there are {len(all_tasks)} tasks but there should be 5'
    utils.validate_task_appears('task', [1, 2, 3, 4, 5], all_tasks)


def test_clear_completed_tasks(browser, open_url, textbox_element):
    # preconditions - create and complete tasks
    utils.create_tasks(browser, 3, 'task', textbox_element)
    checkboxes = (browser.find_elements(By.XPATH, CHECKBOX_ELEMENT))
    for checkbox in checkboxes:
        checkbox.click()
    # clear completed tasks
    browser.find_element(By.CLASS_NAME, "clear-completed").click()
    # validate tasks cleared
    all_tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(all_tasks) == 0, f'Error! there are {len(all_tasks)} tasks but there should be 0'


def test_left_items(browser, open_url, textbox_element):
    # preconditions - create tasks
    utils.create_tasks(browser, 3, 'task', textbox_element)
    left_items_element = browser.find_elements(By.CLASS_NAME, LEFT_ITEMS_TEXT_ELEMENT)[0].text
    # validate text
    assert left_items_element == '3 items left!'
    browser.find_elements(By.XPATH, CHECKBOX_ELEMENT)[0].click()
    assert browser.find_elements(By.CLASS_NAME, LEFT_ITEMS_TEXT_ELEMENT)[0].text == '2 items left!'
    browser.find_elements(By.XPATH, CHECKBOX_ELEMENT)[1].click()
    assert browser.find_elements(By.CLASS_NAME, LEFT_ITEMS_TEXT_ELEMENT)[0].text == '1 item left!'
    browser.find_elements(By.XPATH, CHECKBOX_ELEMENT)[0].click()
    assert browser.find_elements(By.CLASS_NAME, LEFT_ITEMS_TEXT_ELEMENT)[0].text == '2 items left!'
    checkboxes = (browser.find_elements(By.XPATH, CHECKBOX_ELEMENT))
    # click all unchecked tasks
    for checkbox in checkboxes:
        flag = False
        try:
            checkbox.find_element(By.XPATH, "./ancestor::li[contains(@class, 'completed')]")
        except NoSuchElementException:
            flag = True
        if flag:
            checkbox.click()
    # validate text
    assert browser.find_elements(By.CLASS_NAME, LEFT_ITEMS_TEXT_ELEMENT)[0].text == '0 items left!'


def test_create_1000_tasks(browser, open_url, textbox_element):
    utils.create_tasks(browser, 1000, 'task', textbox_element)
    all_tasks = browser.find_elements(By.XPATH, TASK_ELEMENT)
    assert len(all_tasks) == 1000, f'Error! there are {len(all_tasks)} tasks but there should be 1000'


def test_mark_all_tasks_as_completed(browser, open_url, textbox_element):
    # preconditions - create tasks
    utils.create_tasks(browser, 3, 'task', textbox_element)
    # mark as done
    browser.find_element(By.CLASS_NAME, "toggle-all").click()
    # validate text
    assert browser.find_elements(By.CLASS_NAME, LEFT_ITEMS_TEXT_ELEMENT)[0].text == '0 items left!'
    # validate checkboxes checked
    checkboxes = (browser.find_elements(By.XPATH, CHECKBOX_ELEMENT))
    for checkbox in checkboxes:
        try:
            checkbox.find_element(By.XPATH, "./ancestor::li[contains(@class, 'completed')]")
        except NoSuchElementException:
            raise NoSuchElementException("Found an uncompleted task")
