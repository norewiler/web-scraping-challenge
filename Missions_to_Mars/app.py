# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# # identify the collection and drop any existing data for this demonstration
# mars_info = mongo.db.mars_info
# mars_info.drop()



@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    if mars_info is None:
        return render_template("blank.html")
    else:
        return render_template("index.html", mars_info = mars_info)

@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    info = scrape_mars.scrape()
    mars_info.update({}, info, upsert = True)

    return redirect("/")











if __name__ == "__main__":
    app.run(debug=True)