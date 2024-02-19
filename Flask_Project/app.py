from flask import Flask                 # also import render template, request..
from flask_sqlalchemy import SQLAlchemy
#import sql queries and other funtions from relevant directories

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ArchGenome.db'    # Ensure correct path to database is here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define routes for backend here: 

#@app.route("/")
#@app.route("/home")
#def home():
    #return render_template("index.html")


#if __name__ == '__main__':
    #app.run(debug=True)





