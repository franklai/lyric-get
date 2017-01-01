#!/usr/bin/env python
import json
import lyric_engine
import webapp2

class MainHandler(webapp2.RequestHandler):
    def handler(self):
        url = self.request.get('url')

        if url:
            try:
                engine = lyric_engine.Lyric(url)
                lyric = engine.get_lyric()
                output = json.dumps({'lyric': lyric})
            except IOError:
                output = json.dumps({'lyric': 'IO error!'})
            except TypeError:
                output = json.dumps({'lyric': 'Type error!'})
            except IndexError:
                output = json.dumps({'lyric': 'Index error!'})
            except StandardError:
                output = json.dumps({'lyric': 'Standard Error!'})
        else:
            output = json.dumps({'lyric': 'error!'})

        self.response.headers.add('Access-Control-Allow-Origin', 'http://localhost')
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
