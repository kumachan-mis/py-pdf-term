from abc import ABCMeta, abstractmethod
from py_pdf_term.tokenizer import Token


class BaseTokenClassifier(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def inscope(self, token: Token) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_symbol(self, token: Token) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_symbol()")

    @abstractmethod
    def is_connector_symbol(self, token: Token) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_connector_symbol()")

    @abstractmethod
    def is_connector_term(self, token: Token) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_connector_term()")

    def is_meaningless(self, token: Token) -> bool:
        return (
            self.is_symbol(token)
            or self.is_connector_symbol(token)
            or self.is_connector_term(token)
        )

    def is_connector(self, token: Token) -> bool:
        return self.is_connector_symbol(token) or self.is_connector_term(token)
