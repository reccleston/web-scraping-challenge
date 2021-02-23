import pymongo
from flask import Flask, jsonify, make_response, render_template
from scrape_mars import scrape

# mars_data = scrape()
app = Flask(__name__)
client = pymongo.MongoClient('mongodb//:localhost:27017')

db = client.mars_mission_db