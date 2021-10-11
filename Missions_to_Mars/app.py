from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_dictionary")

@app.route("/")
def main():
    mars_dictionary = mongo.db.mars_dictionary.find_one()
    return render_template("main.html", mars_dictionary=mars_dictionary)

@app.route("/scrape")
def scraper():
    mars_dictionary = mongo.db.mars_dictionary
    mars_dictionary_data = scrape_mars.scrape()
    mars_dictionary.update({}, mars_dictionary_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
