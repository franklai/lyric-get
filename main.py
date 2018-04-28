import json
import logging

import flask

import lyric_engine

app = flask.Flask(__name__, template_folder='static')

@app.route('/')
def home():
    """index page"""
    return flask.render_template('index.html')

@app.route('/app')
def main():
    """Main lyric get handler"""
    url = flask.request.args.get('url')

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

    response = flask.make_response(output)
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'

    return response

    self.response.write(output)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=3000, debug=True)
# [END app]
