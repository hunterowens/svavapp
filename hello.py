from flask import Flask, render_template, request, redirect, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Review, Bathroom
import json


app = Flask(__name__)
engine = create_engine("mysql://root:@localhost/Scav")

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
    print "showing bath " + str(bath)
    reviews = session.query(Review).filter(Review.bathroom_id==bath).all()
    print reviews
    return render_template('bath.html', reviews=reviews)

@app.route('/addBath',methods=['GET','POST'])
def add_bath():
    if request.method == 'POST':
        data = request.data
        bathroom = json.loads(data)
        bathroom_new = Bathroom(location=bathroom['location'], floor=bathroom['floor'], gender=bathroom['gender'])
        session.add(bathroom_new)
        session.commit()
        return make_response(render_template('bathroomAdded.html'),200)
    else:
        return render_template('addBathroomForm.html')

@app.route('/addReview',methods=['GET','POST'])
def add_review():
    if request.method = 'POST':
        data = request.data
        review = json.loads(data)
        review_new = Review(content=review['content'], rating=review['rating'])
        bath = session.query(Bathroom).filter(Bathroom.id == review['bathroom']).all().head()
        review_new.bathroom = bath
        session.add(review_new)
        session.commit()
        return make_response(render_template('reviewAdded.html'), 200)
    else:
        return render_template('addReviewForm.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
