#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request, Response
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()     
mime = {
    "json": "application/json",
    "html": "text/html",
} 

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    return flask.redirect('/static/index.html', code=301)

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    body = flask_post_json()

    #Entity = client (i.e person drawing), key = coordinate-pair, value = coordinates (dict) ?
    for key, value in body.items():
        myWorld.update(entity, key, value)

    updated_entity = myWorld.get(entity)

    res = Response(response=updated_entity, status=200, mimetype=mime["json"])
    return res

@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    world = json.dumps(myWorld.world())

    res = Response(response=world, status=200, mimetype=mime["json"])
    return res

@app.route("/entity/<entity>")    
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    entity = json.dumps(myWorld.get(entity))
    #Returns an empty dict if no entity (client will have to decide what to do with this)
    return Response(response=entity, status=200)

@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    myWorld.clear()
    world = json.dumps(myWorld.world())

    res = Response(response=world, status=200, mimetype=mime["json"])
    return res

if __name__ == "__main__":
    app.run(debug=True)
