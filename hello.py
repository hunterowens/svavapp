from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine("mysql://root:scavhunt@localhost/Scav")

SessionMkr = sessionmaker()
SessionMkr.configure(bind=engine)
session = SessionMkr()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list_reviews():
    locations = session.query(Bathroom.location).all()
    reviewsByLoc = {}
    for location in locations:
        reviewsByLoc[location] = session.query(Review).filter(Review.bathroom.location == location).all()

    return render_template('list.html', locations=locations, reviews=reviewsByLoc)

if __name__ == '__main__':
    app.run()
