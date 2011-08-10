# encoding=utf-8

import datetime, json, itertools

from urlparse import urlparse, parse_qs

from flask import (request, flash, url_for, redirect, 
    render_template, abort, session, jsonify, g)
    
from .app import app

from instagram import InstagramAPI
from instagram.models import ApiModel
# from .models import Person, Photo

TAG_NAME = 'gummiognina'
PAGE_COUNT = 5

def get_photos(max_tag_id=None):
    
    api = InstagramAPI(client_id=g.instagram_id, 
                       client_secret=g.instagram_secret, 
                       redirect_uri='http://www.gummiognina.com/')
                       
    data, next_url = api.tag_recent_media(tag_name=TAG_NAME, 
                                          count=PAGE_COUNT, 
                                          max_tag_id=max_tag_id)
    
    def _to_dict(obj):
        d = dict()
        if not isinstance(obj, dict):
            obj = obj.__dict__
        for key, value in obj.iteritems():
            if isinstance(value, (ApiModel, dict)):
                d[key] = _to_dict(value)
            elif isinstance(value, list):
                d[key] = map(unicode, value)
            else:
                d[key] = unicode(value)
        return d
    
    def yield_images():
        for obj in data:
            yield _to_dict(obj)
    
    qs = urlparse(next_url).query
    max_tag_id = parse_qs(qs).get('max_tag_id', [None])[0]
    
    return (_to_dict(obj) for obj in data), max_tag_id
    

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/photos', methods=['GET'])
@app.route('/photos/page-<page>', methods=['GET'])
def photos(page=None):
    photos, max_tag_id = get_photos(page)
    return jsonify(photos=list(photos), max_tag_id=max_tag_id)
