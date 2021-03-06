import json
import logging

from flask import Flask, Response, redirect
from flask import request
from flask_cors import CORS

from gplz.demo import shorten

demo = Flask(__name__)
demo.config.from_object('flask_config')
CORS(demo)

logging.getLogger('flask_cors').level = logging.DEBUG


@demo.route('/ops/shorten', methods=['POST'])
def handle_shorten():
    data = request.get_json()
    url = data.get('url', 'NO URL')
    res = shorten.shorten(url)
    return Response(json.dumps(res), mimetype='application/json')


@demo.route('/ops/custom', methods=['POST'])
def handle_custom():
    data = request.get_json()
    url = data.get('url', 'NO URL')
    shortcode = data.get('shortcode', 'NO SHORTCODE')
    res = shorten.custom(url, shortcode)
    return Response(json.dumps(res), mimetype='application/json')


@demo.route('/ops/lookup', methods=['POST'])
def handle_lookup():
    data = request.get_json()
    url = data.get('shortcode', 'NO URL')
    res = shorten.lookup(url)
    return Response(json.dumps(res['url']),
                    mimetype='application/json')


@demo.route('/ops/dump', methods=['GET'])
def handle_dump():
    res = [dict(e) for e in shorten.dump()]
    return Response(json.dumps(res), mimetype='application/json')


@demo.route('/<path>', methods=['GET'])
def handle_redirect(path):
    res = shorten.lookup(path)
    url = res['url']
    return redirect(url)


if __name__ == "__main__":
    demo.run()
