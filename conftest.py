import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


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


@pytest.fixture
def action_chains(browser):
    yield ActionChains(browser)