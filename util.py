class BaseError(Exception):
    """Wyjątki do Algolia API """

    message = u"Pojawił się nieznany błąd dla '{url}'. Odpowiedź: '{content}'"

    def __init__(self, url, status, resource_name, content):
        self.url = url
        self.status = status
        self.resource_name = resource_name
        self.content = content

    def __str__(self):
        return self.message.format(url=self.url, content=self.content)

    def __unicode__(self):
        return self.__str__()


class CredentialError(BaseError):
    """
    Error Code: 403
    Nieprawidłowe dane dostępowe
    """
    message = u"Błąd danych dostępowych dla: '{url}'. Odpowiedź: '{content}'"


class InternalError(BaseError):
    """
    Error Code: 500
    Błąd serwera
    """
    message = u"Błąd serwera dla: '{url}'. Odpowiedź: '{content}'"


def exception_handler(result, name=""):
    """ Obsługa wyjątków. Określa, który błąd zgłosić, gdy kod nie działa """
    try:
        response_content = result.json()
    except Exception:
        response_content = result.text

    exception_map = {403: CredentialError, 500: InternalError}
    exception_class = exception_map.get(result.status_code, BaseError)

    raise exception_class(result.url, result.status_code, name, response_content)

