from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def create_single_task(textbox_element, text):
    """
    :param textbox_element: Selenium WebDriver instance, task textbox element
    :param text: str, text of the task
    """
    textbox_element.send_keys(text)
    textbox_element.send_keys(Keys.ENTER)


def create_tasks(browser, num_of_tasks, text, textbox_element, verify_creation=False):
    """
    Create tasks
    :param browser: Selenium WebDriver instance, browser element
    :param num_of_tasks: int, how many tasks to create
    :param text: str, text of the task
    :param textbox_element: Selenium WebDriver instance, task textbox element
    :param verify_creation: bool, should creation be verified
    """
    # create the tasks
    for idx, _ in enumerate(range(num_of_tasks)):
        create_single_task(textbox_element, f"{text}{idx + 1}")
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


def delete_task_text(browser, textbox_element, action_chains, task_text, config):
    """
    Edit and delete existing task text
    :param browser: Selenium WebDriver instance, browser element
    :param textbox_element: Selenium WebDriver instance, task textbox element
    :param action_chains: Selenium WebDriver instance, action chains
    :param task_text: str, the text to delete
    :param config: dict, elements config file
    :return: list, the text input boxes
    """
    create_single_task(textbox_element, task_text)
    task = browser.find_elements(By.XPATH, config['task_element'])
    action_chains.double_click(task[0]).perform()
    input_tasks = browser.find_elements(By.CLASS_NAME, "new-todo")
    # delete all the characters in the box
    while len(input_tasks[1].get_attribute("value")) > 0:
        input_tasks[1].send_keys(Keys.BACKSPACE)
    return input_tasks


def get_task_elements_by_status(browser, status, config):
    """
    Get all task elements by their status
    :param browser: Selenium WebDriver instance, browser element
    :param status: str, the status of the task
    :param config: dict, elements config file
    :return: list, the task elements with the expected status
    """
    browser.find_element(By.LINK_TEXT, status).click()
    return browser.find_elements(By.XPATH, config['task_element'])
