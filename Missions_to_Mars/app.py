from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Return template and data
    return render_template("index.html")


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect to the scraped data page
    return redirect("/data")

# Route to render data.html template using data from Mongo
@app.route("/data")
def data():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("data.html", info=mars_info)

if __name__ == "__main__":
    app.run(debug=True)
