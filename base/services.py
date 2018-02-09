import json

import requests

from base.constants import ABS_ALMUNDO_IT, APIST_ALMUNDO_COM


class Apikeys:
    raw_channels_info = requests.get(ABS_ALMUNDO_IT)
    json_channels_info = json.loads(raw_channels_info.text)
    apikey_name = 'almundo-web'

    def get_apikey(self):
        print('Looking for apikey corresponding to channel: [' + self.apikey_name + ']')
        for channel in self.json_channels_info:
            if channel['name'] == self.apikey_name:
                print('Apikey found, awesome!')
                break
        return channel['value']


class FlightsClusters:
    def __init__(self, origin, destination, departure_date, return_date, site, language, adults, children, infants):
        self.flights_clusters_url = APIST_ALMUNDO_COM \
                                    + '/api/flights/clusters?' \
                                    + 'from=' + origin + ',' + destination + '&to=' + destination + ',' + origin \
                                    + '&departure=' + departure_date + ',' + return_date \
                                    + '&site=' + site \
                                    + '&language=' + language \
                                    + '&adults=' + adults \
                                    + '&children=' + children \
                                    + '&infants=' + infants

        print('Flight Cluster URl: [' + self.flights_clusters_url + ']')

    @classmethod
    def get_flight_id(cls, apikey, flights_clusters_url):
        raw_flights_clusters = requests.get(flights_clusters_url, headers={'X-Apikey': apikey})
        json_flights_clusters = json.loads(raw_flights_clusters.text)
        return str(json_flights_clusters['clusters'][0]['segments'][0]['choices'][0]['id']) \
            + '*' + str(json_flights_clusters['clusters'][0]['segments'][1]['choices'][0]['id'])


class Cart:
    def __init__(self, site, language):
        self.book_url = APIST_ALMUNDO_COM \
                        + '/api/v3/cart/' \
                        + '?site=' + site \
                        + '&language=' + language
        print('Cart Book URL: [' + self.book_url + ']')

    @classmethod
    def get_cart_id(cls, apikey, flight_id, book_url):
        data = {"products": [{"type": "FLIGHT", "id": flight_id}]}
        raw_cart_book_id = requests.post(book_url, headers={'X-Apikey': apikey}, json=data)
        json_cart_book_id = json.loads(raw_cart_book_id.text)
        return json_cart_book_id['cart_id']


apikeys = Apikeys()
channel_apikey = apikeys.get_apikey()
print('X-apikey: [' + channel_apikey + ']')

flights_clusters = FlightsClusters('BUE', 'MIA', '2018-03-18', '2018-04-02', 'ARG', 'es', '2', '1', '0')
product_id = flights_clusters.get_flight_id(channel_apikey, flights_clusters.flights_clusters_url)
print('Flight ID: [' + product_id + ']')


cart = Cart('ARG', 'es')
cart_id = cart.get_cart_id(channel_apikey, product_id, cart.book_url)
print('Cart ID: [' + cart_id + ']')
