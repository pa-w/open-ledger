# encoding: utf-8

import logging

requests_log = logging.getLogger("flickrapi")
requests_log.propagate = False

import flickrapi

from django.conf import settings
from imageledger.licenses import license_match

log = logging.getLogger(__name__)

LICENSES = {
    "BY": 4,
    "BY-NC": 2,
    "BY-ND": 6,
    "BY-SA": 5,
    "BY-NC-ND": 3,
    "BY-NC-SA": 1,
    "PDM": 7,
    "CC0": 9,
}
LICENSE_VERSION = "2.0"

LICENSE_LOOKUP = {v: k for k, v in LICENSES.items()}

def auth():
    return flickrapi.FlickrAPI(settings.FLICKR_KEY,
                               settings.FLICKR_SECRET,
                               format='parsed-json',
                               store_token=False,
                               cache=True)

def photos(search=None, licenses=["ALL"], page=1, per_page=20, **kwargs):
    flickr = auth()
    photos = flickr.photos.search(safe_search=1,  # safe-search on
                         content_type=1,  # Photos only, no screenshots
                         license=license_match(licenses, LICENSES),
                         text=search,
                         extras='url_l,url_m,url_s,owner_name,license',
                         sort='relevance',
                         page=page,
                         per_page=per_page)
    photos['photos']['total'] = int(photos['photos']['total'])  # seriously why is this a string
    photos['photos']['pages'] = int(photos['photos']['pages'])
    for p in photos['photos']['photo']:
        p['url'] = p.get('url_l') or p.get('url_m') or p.get('url_s') or ""
        p['thumbnail'] = p.get('url_s') or ""
    return photos
