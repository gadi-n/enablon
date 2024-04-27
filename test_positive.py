import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def open_url(browser):
    url = "https://todomvc.com/examples/react/dist/"
    browser.get(url)


@pytest.fixture
def textbox_element(browser):
    yield browser.find_element(By.ID, "todo-input")


def create_tasks(browser, num_of_tasks, text, textbox_element, verify_creation=False):
    """
    Create tasks
    :param browser: Selenium WebDriver instance, browser element
    :param num_of_tasks: int, how many tasks to create
    :param text: str, text of the task
    :param textbox_element: Selenium WebDriver instance, task textbox element
    :param verify_creation: bool, should creation be verified
    """
    for idx, _ in enumerate(range(num_of_tasks)):
        # create tasks
        textbox_element.send_keys(f"{text}{idx + 1}")
        textbox_element.send_keys(Keys.ENTER)
        if verify_creation:
            browser.find_element(By.XPATH, f"//label[@data-testid='todo-item-label' and text()='{text}{idx + 1}']")


def validate_task_appears(text, num_list, task_list):
    """
    Validates that the expected tasks appear
    :param text: str, the task text
    :param num_list: list, the index number of the task
    :param task_list: list, the list of the tasks
    """
    for idx, task in enumerate(task_list):
        assert task.text == f'{text}{num_list[idx]}', \
            f"Error! Task text is {task[idx].text} and not f'{text}{num_list[idx]}'"


def test_homepage_structure(browser, open_url, textbox_element):
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
    create_tasks(browser, 5, 'task', textbox_element, verify_creation=True)


def test_complete_task_and_display_by_status(browser, open_url, textbox_element):
    # preconditions - create tasks
    create_tasks(browser, 5, 'task', textbox_element)
    checkboxes = (browser.find_elements
                  (By.XPATH, "//input[@class='toggle' and @type='checkbox' and @data-testid='todo-item-toggle']"))
    # complete tasks
    checkboxes[0].click()
    checkboxes[2].click()
    # show only completed
    browser.find_element(By.LINK_TEXT, "Completed").click()
    completed_tasks = browser.find_elements(By.XPATH, "//*[@data-testid='todo-item-label']")
    assert len(completed_tasks) == 2, f'Error! there are {len(completed_tasks)} completed tasks but there should be 2'
    validate_task_appears('task', [1, 3], completed_tasks)
    # show only active
    browser.find_element(By.LINK_TEXT, "Active").click()
    active_tasks = browser.find_elements(By.XPATH, "//*[@data-testid='todo-item-label']")
    assert len(active_tasks) == 3, f'Error! there are {len(active_tasks)} active tasks but there should be 3'
    validate_task_appears('task', [2, 4, 5], active_tasks)
    # show all tasks
    browser.find_element(By.LINK_TEXT, "All").click()
    all_tasks = browser.find_elements(By.XPATH, "//*[@data-testid='todo-item-label']")
    assert len(all_tasks) == 5, f'Error! there are {len(all_tasks)} tasks but there should be 5'
    validate_task_appears('task', [1, 2, 3, 4, 5], all_tasks)
