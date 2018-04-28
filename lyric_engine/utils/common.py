import html
import logging
import re


def get_url_content(url, data=None, headers=None, encoding="utf-8"):
    try:
        import requests_toolbelt.adapters.appengine
        # Use the App Engine Requests adapter. This makes sure that Requests uses
        # URLFetch.
        requests_toolbelt.adapters.appengine.monkeypatch()
    except:
        pass

    import requests

    if data:
        r = requests.post(url, data=data, headers=headers)
    else:
        r = requests.get(url, headers=headers)
    
    r.encoding = encoding

    return r.text

def half2full(input):
    ascii = 'a-zA-Z0-9,\'& \!\?'
    pattern = '(?<=[^%s]) | (?=[^%s])' % (ascii, ascii)

    return re.sub(pattern, '　', input)

def unicode2string(input):
    def point2string(match_obj):
        if match_obj and match_obj.group(1):
            return chr(int(match_obj.group(1)))

    def hex2dec(match_obj):
        if match_obj and match_obj.group(1):
            return chr(int('0' + match_obj.group(1), 16))

    input = input.replace('&hellip;', '…')

    pattern = r'&#x([0-9a-fA-F]+);'
    input = re.sub(pattern, hex2dec, input)

    pattern = r'&#([0-9]+);'
    return re.sub(pattern, point2string, input)

def strip_tags(input):
    return re.sub('<[^>]+>', '', input)

def strip_slash(input):
    return re.sub(r'\\(.)', r'\1', input)

def to_one_line(input):
    return re.sub(r'[\r\n]', '', input)

def get_first_group_by_pattern(input, pattern):
    output = ''
    logging.debug('pattern [%s]' % (pattern, ))
    regex = re.compile(pattern).search(input)
    if regex:
        output = regex.group(1)
    else:
        logging.debug('Failed to find pattern [%s]', pattern)
    return output

def get_matches_by_pattern(input, pattern):
    logging.debug('pattern [%s]' % (pattern, ))
    regex = re.compile(pattern).search(input)
    if regex:
        return regex
    else:
        logging.debug('Failed to find pattern [%s]', pattern)
    return None

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


def htmlspecialchars_decode(string):
    return html.unescape(string)

if __name__ == '__main__':
    text = """
&#26085;&#12418;<br />
<br />
I&#039;m so lonely.
R &amp; B
&quot;NO&quot;
&lt;hr&gt;
"""
    print((unicode2string(text)))

    text = 'I&#039;m so lonely. R &amp; B'
    print((half2full(htmlspecialchars_decode(text))))

