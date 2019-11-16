from abc import ABCMeta, abstractmethod

from paul6325106.actionexpect.expected_conditions import WindowHandle, Url


class Dialog(metaclass=ABCMeta):
    """
    Page model implementation of a UI element.
    This hypothetical UI element appears in several implementations of a system.
    Additionally, this UI element can have different behaviour depending on the test.
    """

    @abstractmethod
    def get_text(self) -> str:
        pass

    @abstractmethod
    def click_button(self, label: str) -> 'Action':
        pass


class Action:
    """
    A builder-like page model object, where the build step describes the expected outcome.
    """

    @abstractmethod
    def and_expect_dialog_closed(self) -> None:
        pass

    @abstractmethod
    def and_expect_page_redirected(self) -> Url:
        pass

    @abstractmethod
    def and_expect_new_window_opened(self) -> WindowHandle:
        pass
