import requests  # potrzebne do połączenia z api
import pandas as pd  # potrzebne do formatowania danych
from util import exception_handler  # dodatkowy plik obsługujący błędy


class Output:
    endpoint = "https://analytics.algolia.com/2"  # adres api - tam mieszkają dane analityczne

    def __init__(self, api_key, application_id):
        """ Inicjalizacja obiektu i stworzenie nagłówków API """
        self.headers = {'X-Algolia-API-Key': api_key,
                        'X-Algolia-Application-Id': application_id}

    # funkcje, które zwracają poszczególne raporty:
    def number_of_users(self, **kwargs):
        """Raport o liczbie użytkowników """
        end_point_type = 'users'
        metric = 'count'
        indices = '?index=dev_SPRYKER'
        url = self._construct_url(end_point_type, metric, indices)
        result = self._call_algolia(url, params=kwargs)

        return result

    def number_of_searches(self, **kwargs):
        """Raport o liczbie wyszukań """
        end_point_type = 'searches'
        metric = 'count'
        indices = '?index=dev_SPRYKER'
        url = self._construct_url(end_point_type, metric, indices)
        result = self._call_algolia(url, params=kwargs)

        return result

    def no_results(self, **kwargs):
        """Raport o liczbie wyszukań, które nie zwróciły wyniku """
        end_point_type = 'searches'
        metric = 'noResultRate'
        indices = '?index=dev_SPRYKER'
        url = self._construct_url(end_point_type, metric, indices)
        result = self._call_algolia(url, params=kwargs)

        return result

    def avg_click_position(self, **kwargs):
        """Raport o średniej z kolejności produktów klikniętych na wyniku wyszukiwania """
        end_point_type = 'clicks'
        metric = 'averageClickPosition'
        indices = '?index=dev_SPRYKER'
        url = self._construct_url(end_point_type, metric, indices)
        result = self._call_algolia(url, params=kwargs)

        return result

    def _construct_url(self, end_point_type, metric, indices='index=dev_SPRYKER'):
        """Funkcja pomocnicza, która buduje url dla api """
        url = [self.endpoint, end_point_type, metric]
        return '/'.join(url) + indices

    def _call_algolia(self, url, **kwargs):
        """ Funkcja pomocnicza, która buduje zapytanie do api """
        result = requests.get(url, headers=self.headers, **kwargs)

        if result.status_code >= 300:
            exception_handler(result)

        return result


# stworzenie obiektu w klasie, który zawiera ID aplikacji i klucz potrzebne do połączenia z api:
raport_obj = Output("d5f16de86b17c8cd0105d7b14450004b", "NNWYKHZ90Y")

# wywołanie wyników raportów dla każdej z funkcji:
users = raport_obj.number_of_users()
users = users.json()
print(users)

searches = raport_obj.number_of_searches()
searches = searches.json()
print(searches)

no_results_rate = raport_obj.no_results()
no_results_rate = no_results_rate.json()
print(no_results_rate)

click_position = raport_obj.avg_click_position()
click_position = click_position.json()
print(click_position)

# zamiana JSONa na data frame oraz eksport do pliku excel

# no_results_rate_df = pd.DataFrame(no_results_rate)
# no_results_rate_df.to_excel('no_results_rate.xlsx')

pd.DataFrame(users).to_excel('users.xlsx')
pd.DataFrame(searches).to_excel('searches.xlsx')
pd.DataFrame(no_results_rate).to_excel('no_results_rate.xlsx')
pd.DataFrame(click_position).to_excel('click_position.xlsx')
