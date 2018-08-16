#!/usr/bin/env python
import json
import logging

from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler
import webapp2

import lyric_engine


client = Client('https://841e64cb97c948bd98d7a85ed1e4862f:ac524529e2ea4be09b424ebfbe9cfe5e@sentry.io/1244452')
handler = SentryHandler(client)
handler.setLevel(logging.WARNING)
setup_logging(handler)

class MainHandler(webapp2.RequestHandler):
    def handler(self):
        url = self.request.get('url')

        if url:
            try:
                engine = lyric_engine.Lyric(url)
                lyric = engine.get_lyric()
                output = json.dumps({'lyric': lyric})
                if not lyric:
                    client.captureMessage('lyric content is empty', {'url': url})
            except IOError:
                output = json.dumps({'lyric': 'IO error!'})
                client.captureException()
            except TypeError:
                output = json.dumps({'lyric': 'aType error!'})
                client.captureException()
            except IndexError:
                output = json.dumps({'lyric': 'Index error!'})
                client.captureException()
        else:
            output = json.dumps({'lyric': 'error!'})

        self.response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.response.headers.add('Access-Control-Allow-Methods', 'GET,POST')

        self.response.write(output)
        
    def get(self):
        self.handler()

    def post(self):
        self.handler()


class NotFound(webapp2.RequestHandler):
    def get(self):
        self.redirect('http://franks543.blogspot.com/')

    def post(self):
        self.redirect('http://franks543.blogspot.com/')

app = webapp2.WSGIApplication([
    ('/app', MainHandler),
    ('/.*', NotFound)
], debug=True)
