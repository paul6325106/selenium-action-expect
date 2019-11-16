from typing import Any, Callable, Dict, NewType, Optional, Tuple, TypeVar

from selenium.webdriver.remote.webdriver import WebDriver

T = TypeVar('T')
Condition = Callable[[WebDriver], Optional[T]]
Url = NewType('Url', str)
WindowHandle = NewType('WindowHandle', str)


def new_window_is_opened(window_handles) -> Condition[WindowHandle]:
    """
    Modification of actionexpect.webdriver.support.expected_conditions.new_window_is_opened to return the new handle.
    """

    old_window_handles = set(window_handles)

    def condition(web_driver: WebDriver) -> Optional[WindowHandle]:
        new_window_handles = set(web_driver.window_handles)
        diff = new_window_handles - old_window_handles
        return diff.pop() if diff else None

    return condition


def url_changes(current_url) -> Condition[Url]:
    """
    Modification of actionexpect.webdriver.support.expected_conditions.url_changes to return the new url.
    """

    def condition(web_driver: WebDriver) -> Optional[Url]:
        new_url = web_driver.current_url
        return new_url if new_url != current_url else None

    return condition


def any_condition(*conditions: Condition[Any]) -> Any:
    """
    Combines several conditions.
    """

    def condition(web_driver: WebDriver) -> Any:
        for func in conditions:
            result = func(web_driver)
            if result:
                return result

        return None

    return condition


def any_condition_identified(conditions: Dict[str, Condition[Any]]) -> Condition[Tuple[str, Any]]:
    """
    Combines several conditions, and identifies the passing condition.
    """

    def condition(web_driver: WebDriver) -> Optional[Tuple[str, Any]]:
        for key, func in conditions.items():
            result = func(web_driver)
            if result:
                return key, result

        return None

    return condition
