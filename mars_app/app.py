from flask import Flask, render_template, redirect, Markup, url_for
from flask_pymongo import PyMongo
from scrape_mars import scrape_info
from mars_facts_table import scrape_table
from mars_rover import scrape_rover
import os
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True

app.config['MONGO_URI'] = os.environ['MONGODB_URI'] or "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app, config_prefix='MONGO')
db = mongo.db.collection.find_one()

# uri = 'mongodb://user:pass@host:port/db' 


# client = pymongo.MongoClient(uri)

# db = client.get_default_database()


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()
    table_string = scrape_table()
    rover_string = scrape_rover()

    # Return template and data
    print(destination_data)
    return render_template("index.html", mars=destination_data, table=table_string, rover=rover_string)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()
    print(mars_data)
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)
    test_data = mongo.db.collection.find_one()
    print(test_data)
    # Redirect back to home page
    return redirect("/")

@app.route("/status_spirit.html#recient")
def redir1():
    return redirect(url_for("https://mars.nasa.gov/mer/mission/status_spirit.html#recient"))

if __name__ == "__main__":
    app.run(host='192.168.1.118', port='5000', debug=True)

# why does database only update when test_data and print statements are uncommented..?
# and then sometimes it won't even update... lol