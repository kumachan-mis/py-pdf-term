from abc import ABCMeta, abstractmethod

from py_pdf_term.tokenizers import Token


class BaseTokenClassifier(metaclass=ABCMeta):
    """Base class for token classifiers. A token classifier is used to classify a token
    into a specific category.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def inscope(self, token: Token) -> bool:
        """Test whether a token is in the scope of this classifier or not.

        Args
        ----
            token:
                Token to be tested.

        Returns
        -------
            bool:
                True if the token is in the scope of this classifier, False otherwise.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_symbol(self, token: Token) -> bool:
        """Test whether a token is a symbol or not.

        Args
        ----
            token:
               Token to be tested.

        Returns
        -------
            bool:
                True if the token is a symbol, False otherwise.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.is_symbol()")

    @abstractmethod
    def is_connector_symbol(self, token: Token) -> bool:
        """Test whether a token is a connector symbol or not. A connector symbol is a
        symbol that is used to connect two terms such as - and ・.
        If this method returns True, is_symbol() must also return True.

        Args
        ----
            token:
                Token to be tested.

        Returns
        -------
            bool:
                True if the token is a connector symbol, False otherwise.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.is_connector_symbol()")

    @abstractmethod
    def is_connector_term(self, token: Token) -> bool:
        """Test whether a token is a connector term or not. A connector term is a term
        that is used to connect two terms such as "of" and "in" in English, and "の" in
        Japanese.

        Args
        ----
            token:
                Token to be tested.

        Returns
        -------
            bool:
                True if the token is a connector term, False otherwise.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.is_connector_term()")

    def is_meaningless(self, token: Token) -> bool:
        """Test whether a token is meaningless or not. A meaningless token is a token
        that does not have any meaning such as a symbol and a connector term.

        Args
        ----
            token:
                Token to be tested.

        Returns
        -------
            bool:
                True if the token is meaningless, False otherwise.
        """

        return (
            self.is_symbol(token)
            or self.is_connector_symbol(token)
            or self.is_connector_term(token)
        )

    def is_connector(self, token: Token) -> bool:
        """Test whether a token is a connector or not. A connector is a token that is
        used to connect two terms such as a connector symbol and a connector term.

        Args
        ----
            token:
                Token to be tested.

        Returns
        -------
            bool:
                True if the token is a connector, False otherwise.
        """

        return self.is_connector_symbol(token) or self.is_connector_term(token)
