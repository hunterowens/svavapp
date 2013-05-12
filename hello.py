from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Review, Bathroom

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
    locations = [instance.location for instance in session.query(Bathroom)]
    print locations
    bathrooms = session.query(Bathroom).all()
    print bathrooms
    return render_template('list.html', locs=locations, baths=bathrooms)

@app.route('/bath/<bath>')
def show_bath(bath):
    reviews = [instance for instance in session.query(Review).filter(Review.bathroom.id == bath)]
    return render_template('bath.html', reviews=reviews)

if __name__ == '__main__':
    app.run()
