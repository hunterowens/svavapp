from flask import Flask, render_template, request, redirect, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Review, Bathroom
import json


app = Flask(__name__)
engine = create_engine("mysql://root:scav@localhost/Scav")

SessionMkr = sessionmaker()
SessionMkr.configure(bind=engine)
session = SessionMkr()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list_reviews():
    locations = [instance.location for instance in session.query(Bathroom)]
    bathrooms = session.query(Bathroom).all()
    return render_template('list.html', locs=locations, baths=bathrooms)

@app.route('/bath/<bath>')
def show_bath(bath):
    print "showing bath " + str(bath)
    reviews = session.query(Review).filter(Review.bathroom_id==bath).all()
    bath = session.query(Bathroom).filter(Bathroom.id == bath).first()
    print reviews
    return render_template('bath.html', reviews=reviews, bath=bath)

@app.route('/addBath',methods=['GET','POST'])
def add_bath():
    if request.method == 'POST':
        data = request.data
        bathroom = json.loads(data)
        loc = bathroom['location']
        floor = bathroom['floor']
        gender = bathroom['gender']
        bathrooms = session.query(Bathroom).filter(Bathroom.location == loc, Bathroom.floor == floor, Bathroom.gender == gender).all()
        bathroom_new = Bathroom(location=bathroom['location'], floor=bathroom['floor'], gender=bathroom['gender'])
        if len(bathrooms) == 0:
            print len(bathrooms)
            session.add(bathroom_new)
            session.commit()
        return make_response(render_template('bathroomAdded.html'),200)
    else:
        return render_template('addBathroomForm.html')

@app.route('/addReview',methods=['GET','POST'])
def add_review():
    if request.method == 'POST':
        data = request.data
        review = json.loads(data)
        review_new = Review(content=review['content'], rating=int(review['rating']))
        bath = session.query(Bathroom).filter(Bathroom.id == int(review['bathroom'])).first()
        review_new.bathroom = bath
        session.add(review_new)
        session.commit()
        return make_response(render_template('reviewAdded.html'), 200)
    else:
        baths = session.query(Bathroom).all()
        return render_template('addReviewForm.html', baths=baths)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',80)
