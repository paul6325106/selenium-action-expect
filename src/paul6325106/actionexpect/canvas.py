from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from paul6325106.actionexpect.expected_conditions import new_window_is_opened, WindowHandle, url_changes, Url
from paul6325106.actionexpect.interface import Dialog, Action


class CanvasDialog(Dialog):
    """
    UI elements inside a canvas will likely require an api for proper test automation.
    """

    def __init__(self, driver: WebDriver, wait: WebDriverWait) -> None:
        self.__driver = driver
        self.__wait = wait

    def get_text(self) -> str:
        return self.__driver.execute_script('return testApi.getDialogText()')

    def click_button(self, label: str) -> 'Action':
        return CanvasAction(self.__driver, self.__wait, label)


class CanvasAction(Action):
    """
    Closing the dialog requires a JavaScript-side callback to confirm success and correct timing. However, the other
    conditions are still Selenium based.

    Some notes:

     * The use of both an async script and a WebDriverWait means that we cannot easily combine the conditions (unlike
       the DOM implementation which only required WebDriverWait).

     * A new window opening would leave the callback in an unknown state, which means a different implementation of the
       script (without the callback) is required for this outcome.

     * A page redirect will cause an async script to error, which is something to be aware of if all api calls are
       asynchronous.
    """

    def __init__(self, driver: WebDriver, wait: WebDriverWait, label: str) -> None:
        self.__driver = driver
        self.__wait = wait
        self.__label = label

    def and_expect_dialog_closed(self) -> None:
        self.__driver.execute_async_script(f'''
            testApi.onDialogClosed(arguments[0]);
            testApi.clickDialogButton({self.__label});
        ''')

    def and_expect_page_redirected(self) -> Url:
        current_url = self.__driver.current_url
        self.__driver.execute_script(f'testApi.clickDialogButton({self.__label})')
        return self.__wait.until(url_changes(current_url))

    def and_expect_new_window_opened(self) -> WindowHandle:
        window_handles = set(self.__driver.window_handles)
        self.__driver.execute_script(f'testApi.clickDialogButton({self.__label})')
        return self.__wait.until(new_window_is_opened(window_handles))
