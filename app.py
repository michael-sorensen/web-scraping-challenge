from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)



# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_dictionary = mongo.db.collection.find_one({})
    return render_template("index.html", mars=mars_dictionary)

@app.route("/scrape_mars")
def scrape():
    mars_dictionary = mongo.db.mars_dictionary
    mars_dictionary_data = scrape_mars.scraper()
    mongo.db.collection.update({}, mars_dictionary_data, upsert=True)
    return redirect("/")
    print(mars_dictionary, flush=True)

if __name__ == '__main__':
    app.run(debug=True)
