# -*- coding: utf8 -*-
import logging
import re

# fetch function of google.appengine.api.urlfetch
# fetch(url, payload=None, method=GET, headers={}, allow_truncated=False)

class URL:
    def __init__(self, url, data=None, headers=None):
        self.google = False

        method = 'get'

        if headers is None:
            headers = {
                'User-Agent': 'Google-urlfetch',
            }

        if data:
            method = 'post'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        try:
            # if under Google App Engine (we cannot use urllib)
            from google.appengine.api import urlfetch

            self.handle = urlfetch.fetch(url, data, method, headers)
            self.google = True
        except ImportError:
            # not in Google App Engine environment, then use traditional urllib2
            import urllib2

            req = urllib2.Request(url, data, headers)
            self.handle = urllib2.urlopen(req)

    def get_content(self):
        if self.google:
            return self.handle.content
        else:
            return self.handle.read()

    def get_info(self):
        if self.google:
            return self.handle.headers
        else:
            return self.handle.info()

def get_url_content(url, data=None, headers=None):
    obj = URL(url, data, headers)

    return obj.get_content()

def half2full(input):
    import re

    ascii = 'a-zA-Z0-9,\' \!\?'
    pattern = '(?<=[^%s]) | (?=[^%s])' % (ascii, ascii)

    return re.sub(pattern, u'　', input)

def unicode2string(input):
    import re

    def point2string(match_obj):
        if match_obj and match_obj.group(1):
            return unichr(int(match_obj.group(1)))

    def hex2dec(match_obj):
        if match_obj and match_obj.group(1):
            return unichr(int('0' + match_obj.group(1), 16))

    input = input.replace('&hellip;', u'…')

    pattern = r'&#x([0-9a-fA-F]+);'
    input = re.sub(pattern, hex2dec, input)

    pattern = r'&#([0-9]+);'
    return re.sub(pattern, point2string, input)

def strip_tags(input):
    return re.sub('<[^>]+>', '', input)

def strip_slash(input):
    return re.sub(r'\\(.)', r'\1', input)

def get_first_group_by_pattern(input, pattern):
    output = ''
    logging.debug('pattern [%s]' % (pattern, ))
    regex = re.compile(pattern).search(input)
    if regex:
        output = regex.group(1)
    else:
        logging.debug('Failed to find pattern [%s]', pattern)
    return output

def get_string_by_start_end_string(startStr, endStr, input):
    start = input.find(startStr)
    if start == -1:
        return None

    end = input.find(endStr, start)
    if end == -1:
        return None

    result = input[start:end + len(endStr)]
    return result

def find_string_by_prefix_suffix(input, prefix, suffix, including=True):
    start = input.find(prefix)
    if start == -1:
        return None

    end = input.find(suffix, start + len(prefix))
    if end == -1:
        return None

    if including:
        result = input[start:end + len(suffix)]
    else:
        result = input[start + len(prefix):end]
    return result


import htmlentitydefs
def htmlspecialchars_decode_func(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0) # use as is

def htmlspecialchars_decode(string):
    pattern = re.compile("&(\w+?);")
    if isinstance(string, unicode):
        return pattern.sub(htmlspecialchars_decode_func, string.encode('utf8')).decode('utf8', 'ignore')
    return pattern.sub(htmlspecialchars_decode_func, string)

if __name__ == '__main__':
    text = """
&#26085;&#12418;<br />
<br />
"""
    print(unicode2string(text))
