from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from paul6325106.actionexpect.expected_conditions import new_window_is_opened, WindowHandle, url_changes, Url, \
    any_condition
from paul6325106.actionexpect.interface import Dialog, Action


class DOMDialog(Dialog):
    """
    Fairly standard page model implementation, except that an action is returned for the button click.
    """

    def __init__(self, driver: WebDriver, wait: WebDriverWait, element: WebElement) -> None:
        self.__driver = driver
        self.__wait = wait
        self.__element = element

    def get_text(self) -> str:
        return self.__element.text

    def click_button(self, label: str) -> 'Action':
        buttons = self.__element.find_elements(By.TAG_NAME, 'button')

        for button in buttons:
            if button.text == label:
                return DOMAction(self.__driver, self.__wait, button)

        raise NoSuchElementException(f'Unable to find button with label {label}')


class DOMAction(Action):
    """
    Fairly standard page model implementation, except that an action is returned for the button click.
    """

    def __init__(self, driver: WebDriver, wait: WebDriverWait, element: WebElement) -> None:
        self.__driver = driver
        self.__wait = wait
        self.__element = element

    def __execute(self) -> None:
        self.__element.click()

    def and_expect_dialog_closed(self) -> None:
        self.__execute()
        self.__wait.until(staleness_of(self.__element))

    def and_expect_page_redirected(self) -> Url:
        current_url = self.__driver.current_url
        self.__execute()
        return self.__wait.until(url_changes(current_url))

    def and_expect_new_window_opened(self) -> WindowHandle:
        window_handles = set(self.__driver.window_handles)
        self.__execute()
        return self.__wait.until(new_window_is_opened(window_handles))


class DOMDialogWithoutAction:
    """
    A combined condition can be used when you only care about outcomes for the purposes of timing/general success.
    """

    def __init__(self, driver: WebDriver, wait: WebDriverWait, element: WebElement) -> None:
        self.__driver = driver
        self.__wait = wait
        self.__element = element

    def get_text(self) -> str:
        return self.__element.text

    def click_button(self) -> None:
        current_url = self.__driver.current_url
        window_handles = set(self.__driver.window_handles)

        self.__element.click()

        self.__wait.until(any_condition(
            staleness_of(self.__element),
            url_changes(current_url),
            new_window_is_opened(window_handles)
        ))
