#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from pprint import pprint

import urllib2
import json
import sys

IP_ADDR = '192.168.0.1'
REFERER = 'google.com'

gnewstopics = {
     'headlines'     : 'h',
      'world'         : 'w',
      'business'      : 'b',
      'nation'        : 'n',
      'scitech'       : 't',
      'election'      : 'el',
      'politics'      : 'p',
      'entertainment' : 'e',
      'sports'        : 's',
      'health'        : 'm'
}

class GnewsSearchResults:
    """
    Wraps the JSON results from the Google News API into a class.
    """

    def __init__(self, json_result):
        if not json_result:
            raise Exception("Empty json_object")

        for k, v in json_result.items():

            if k == 'relatedStories' and (k in json_result):
                self.relatedStories = [RelatedStory(rs) for rs in json_result[k]]
                continue

            if k == 'image' and (k in json_result):
                self.image = Image(json_result[k])

            # skip unknown dicts and lists
            if (k in json_result) and\
               type(json_result[k]) is dict or\
               type(json_result[k]) is list:
                    continue

            # set the key/value for all attributes
            setattr(self, k, v)


class RelatedStory:
    """
    Wraps the JSON results of the related news story from the results of a query.
    """
    def __init__(self, rs_json):
        for k, v in rs_json.items():
            setattr(self, k, v)


class Image:
    """
    Wraps the JSON results of the image data from the results of a query.
    """
    def __init__(self, img_json):
        for k, v in img_json.items():
            setattr(self, k, v)


class GnewsSearch:
    """
    Provides access to the Google News API
    """
    def __init__(self):
        self.ipaddr = IP_ADDR
        self.referer = REFERER
        self.url = ('https://ajax.googleapis.com/ajax/services/search/news?' +
                    'v=1.0&userip={0}&rsz=8'.format(self.ipaddr))


        def make_topic_func(x):
            return lambda : self._call_api(self.url, {'topic':x})

        for k, v in gnewstopics.items():
            setattr(self, 'get_{}'.format(k), make_topic_func(v))


    def get_query(self, query):
        params = {'q': urllib2.quote(query)}
        return self._call_api(self.url, params)


    def _call_api(self, url, params):
        """
        Calls the Google News API and returns the results as a list of
        JSON data used to create GoogleNewsResults objects
        """
        paramlist = ["{}={}".format(k,v) for k, v in params.items()]
        queryurl = '{0}&{1}'.format(url, '&'.join(paramlist))
        if sys.flags.debug:
            pprint(queryurl)
            pprint(url)

        try:
            req = urllib2.Request(queryurl, None, {'Referer': REFERER})
            opened_req = urllib2.urlopen(req)
            resp = opened_req.read()

            # Process the JSON string.
            resp_obj = json.loads(resp)
            if sys.flags.debug:
                pprint(resp_obj)

            if resp_obj and\
                ('responseData' in resp_obj) and\
                ('results' in resp_obj['responseData']):
                return resp_obj['responseData']['results']
            else:
                raise Exception('Could not retrieve result for query')

        except Exception as e:
            pprint(e)
