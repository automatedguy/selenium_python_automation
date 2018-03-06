import json
import logging

import requests

from base.constants import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Apikeys:
    def __init__(self):
        raw_channels_info = requests.get(ABS_ALMUNDO_IT)
        self.json_channels_info = json.loads(raw_channels_info.text)

    def get_apikey(self, channel_name):
        # logger.info('Looking for apikey corresponding to Site: [' + BASE_URL + ']')
        for channel in self.json_channels_info:
            if channel['name'] == channel_name:
                logger.info('Apikey for [' + channel_name + '] found [' + channel['value'] + ']')
                break
        return channel['value']


class Autocomplete:
    def __init__(self, place, entity_type):
        self.autocomplete_url = APIST_ALMUNDO_COM \
                                + '/api/autocomplete/suggestions/es?' \
                                + 'q=' + place \
                                + '&entityType=' + entity_type

    def get_entity_id(self, apikey, location_name):
        raw_autocomplete_suggestions = requests.get(self.autocomplete_url, headers={'X-Apikey': apikey})
        json_autocomplete_suggestions = json.loads(raw_autocomplete_suggestions.text)
        for entities in json_autocomplete_suggestions['suggestions'][0]['entities']:
            if location_name in entities['label']:
                logger.info('Location Found:' + entities['label'])
                break
        return entities['id']


class HotelsAvailabilities:
    def __init__(self, entity_id, entity_type, checkin, checkout, room, language, site):
        self.hotel_availabilities_url = APIST_ALMUNDO_COM \
                                        + '/api/hotels/v2/availabilities?' \
                                        + 'entityId=' + entity_id \
                                        + '&entityType=' + entity_type \
                                        + '&checkin=' + checkin \
                                        + '&test_checkout=' + checkout \
                                        + '&room=' + room \
                                        + '&language=' + language \
                                        + '&site=' + site

    def get_hotel_id(self, apikey):
        raw_hotels_availabilities = requests.get(self.hotel_availabilities_url, headers={'X-Apikey': apikey})
        json_hotels_availabilities = json.loads(raw_hotels_availabilities.text)
        return json_hotels_availabilities['availabilities'][0]['id']


class HotelsDetails:
    def __init__(self, hotel_id, checkin, checkout, room, language, site):
        self.hotels_details_url = APIST_ALMUNDO_COM \
                                  + '/api/hotels/v2/detail?' \
                                  + 'hotelId=' + hotel_id \
                                  + '&checkin=' + checkin \
                                  + '&test_checkout=' + checkout \
                                  + '&room=' + room \
                                  + '&language=' + language \
                                  + '&site=' + site

    def get_hotel_id(self, apikey):
        raw_hotel_details = requests.get(self.hotels_details_url, headers={'X-Apikey': apikey})
        json_hotel_details = json.loads(raw_hotel_details.text)
        return json_hotel_details


class FlightsClusters:
    def __init__(self, api_host, origin, destination, departure_date, return_date, site, language, adults, children, infants):
        self.flights_clusters_url = api_host \
                                    + '/api/flights/clusters?' \
                                    + 'from=' + origin + ',' + destination + '&to=' + destination + ',' + origin \
                                    + '&departure=' + departure_date + ',' + return_date \
                                    + '&site=' + site \
                                    + '&language=' + language \
                                    + '&adults=' + adults \
                                    + '&children=' + children \
                                    + '&infants=' + infants

        logger.info('Flight Cluster URL: [' + self.flights_clusters_url + ']')

    def get_flight_id(self, apikey):
        raw_flights_clusters = requests.get(self.flights_clusters_url, headers={'X-Apikey': apikey})
        json_flights_clusters = json.loads(raw_flights_clusters.text)
        try:
            return str(json_flights_clusters['clusters'][0]['segments'][0]['choices'][0]['id']) \
                + '*' + str(json_flights_clusters['clusters'][0]['segments'][1]['choices'][0]['id'])
        except IndexError as no_availability:
            logger.error(ERR_NO_AVAILABILITY + str(no_availability))


class InputDefinitions:
    def __init__(self, input_def_host, cart_id, country, language):
        self.input_def_url = input_def_host \
                             + '/api/v3/cart/' + cart_id \
                             + '/input-definitions?site=' + country \
                             + '&language=' + language
        self.json_input_definitions = None

    def get_input_definitions(self, apikey):
        logger.info('Getting input definitions...')
        raw_input_definitions = requests.get(self.input_def_url, headers={'X-Apikey': apikey, 'Version': 'v3'})
        self.json_input_definitions = json.loads(raw_input_definitions.text)
        logger.info("Input definitions retrieved!" + str(self.json_input_definitions))
        return self.json_input_definitions


class Cart:
    def __init__(self, api_host, site, language):
        self.book_url = api_host \
                        + '/api/v3/cart/' \
                        + '?site=' + site \
                        + '&language=' + language
        logger.info('Cart Book URL: [' + self.book_url + ']')

    def get_cart_id(self, apikey, flight_id):
        data = {"products": [{"type": "FLIGHT", "id": flight_id}]}
        raw_cart_book_id = requests.post(self.book_url, headers={'X-Apikey': apikey}, json=data)
        json_cart_book_id = json.loads(raw_cart_book_id.text)
        return json_cart_book_id['cart_id']


class AbRouterUrl:
    def __init__(self, api_host, site, language):
        self.book_url = api_host \
                        + 'chkabrouter/cart' \
                        + '?site=' + site \
                        + '&language=' + language
        logger.info('Ab Router Book URL: [' + self.book_url + ']')

    def get_ab_router_cart_id(self, apikey, flight_id):
        data = {"products": [{"type": "FLIGHT", "id": flight_id}]}
        raw_cart_book_id = requests.post(self.book_url, headers={'X-Apikey': apikey}, json=data)
        json_cart_book_id = json.loads(raw_cart_book_id.text)
        return json_cart_book_id['urlToRedirect']


# HOTEL THINGS
# autocomplete = Autocomplete('MIA', 'CITY')
# location_entity_id = autocomplete.get_entity_id(channel_apikey, 'Miami')
# logger.info(location_entity_id)
# hotels_availabilities = HotelsAvailabilities(location_entity_id, 'CITY', '2018-03-18', '2018-04-02', '2', 'es', 'ARG')
# selected_hotel_id = hotels_availabilities.get_hotel_id(channel_apikey)
