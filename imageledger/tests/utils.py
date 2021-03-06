import json
import os

import jinja2
from django.test import TestCase
import html5lib
from lxml.html import tostring, html5parser
import responses

from imageledger import models

TESTING_CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.py')

class TestImageledgerApp(TestCase):
    """Setup/teardown for app test cases"""
    def setUp(self):
        activate_all_provider_mocks()

def activate_all_provider_mocks():
    """Mock all the responses we know about from all the providers"""
    activate_500px_mocks()
    activate_rijks_mocks()
    activate_flickr_mocks()
    activate_wikimedia_mocks()

def activate_flickr_mocks():
    from imageledger.handlers.handler_flickr import auth
    flickr = auth()
    responses.add(responses.POST, flickr.REST_URL, status=200, content_type='application/json',
                      json=load_json_data('flickr-response.json'))

def activate_500px_mocks():
    from imageledger.handlers.handler_500px import ENDPOINT_PHOTOS
    responses.add(responses.GET, ENDPOINT_PHOTOS, status=200, content_type='application/json',
                  json=load_json_data('500px-response.json'))

def activate_rijks_mocks():
    from imageledger.handlers.handler_rijks import ENDPOINT_PHOTOS
    responses.add(responses.GET, ENDPOINT_PHOTOS, status=200, content_type='application/json',
                  json=load_json_data('rijks-response.json'))

def activate_wikimedia_mocks():
    from imageledger.handlers.handler_wikimedia import BASE_URL, WIKIDATA_URL
    entities_template = load_json_data('wikimedia-entities-response.json')
    wikidata_template = load_json_data('wikimedia-data-response.json')
    responses.add(responses.GET, BASE_URL, status=200, content_type='application/json',
                  json=entities_template)
    responses.add(responses.GET, WIKIDATA_URL, status=200, content_type='application/json',
                  json=wikidata_template)

def load_json_data(datafile):
    """Load testing data in JSON format relative to the path where the test lives"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return json.loads(open(os.path.join(dir_path, datafile)).read())

def select_node(resp, selector):
    """Give a response from the app, return just the HTML fragment defined by `selector`.
    Guaranteed to return one node or None"""
    r = select_nodes(resp, selector)
    if r and len(r) > 0:
        return r[0]
    return None

def select_nodes(resp, selector):
    """Give a response from the app, return just the HTML fragment defined by `selector`"""
    h = html5lib.parse(resp.content.decode('utf-8'), treebuilder='lxml', namespaceHTMLElements=False)
    return h.getroot().cssselect(selector)
