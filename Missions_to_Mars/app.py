import pymongo
from flask import Flask, jsonify, make_response, render_template, redirect
from scrape_mars import scrape

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_mission
db.mars_mission.drop()
db.mars_mission.insert_many(scrape()['mars_data'])

@app.route('/') 
def index():
    data = list(db.mars_mission.find())
    return render_template('index.html', mars_data=data)

# scrape new data
@app.route('/scrape')
def marsScrape():

    print('scrape from app.py')
    mars_data = scrape()
    db.mars_mission.insert_many(mars_data['mars_data'])

    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)