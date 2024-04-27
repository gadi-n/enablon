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


def test_homepage_structure(browser, open_url):
    # verify header
    header_text = browser.find_element(By.CSS_SELECTOR, "h1").text
    assert header_text == "todos", f'Error! Header text is {header_text} and not "todos"'
    # verify placeholder
    placeholder_text = browser.find_element(By.ID, "todo-input").get_attribute("placeholder")
    assert placeholder_text == 'What needs to be done?', f'Error! Place holder text is {placeholder_text} and not "What needs to be done"?'
    # verify footer
    footer_text = browser.find_element(By.CLASS_NAME, "info").text
    assert footer_text == "Double-click to edit a todo\nCreated by the TodoMVC Team\nPart of TodoMVC", \
        f'Error! footer text text is {footer_text} and not "Double-click to edit a todo\nCreated by the TodoMVC Team\nPart of TodoMVC"'
    # verify link
    href_value = browser.find_element(By.LINK_TEXT, "TodoMVC").get_attribute("href")
    assert href_value == "http://todomvc.com/", f'link leads to {href_value} and not to "http://todomvc.com/"'


def test_create_several_tasks(browser, open_url):
    textbox_element = browser.find_element(By.ID, "todo-input")
    for idx, _ in enumerate(range(5)):
        # create task
        textbox_element.send_keys(f"task{idx + 1}")
        textbox_element.send_keys(Keys.ENTER)
        # validate creation
        browser.find_element(By.XPATH, f"//label[@data-testid='todo-item-label' and text()='task{idx + 1}']")
