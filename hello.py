from flask import Flask, render_template, request
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
    print "showing bath " + str(bath)
    reviews = session.query(Review).filter(Review.bathroom_id==bath).all()
    print reviews
    return render_template('bath.html', reviews=reviews)

@app.route('/addBath',methods=['POST', 'GET'])
def add_bath():
	if request.method == 'POST':
		location = request.form['location']
		floor = request.form['floor']
		gender = request.form['gender']
		bathroom_new = Bathroom(location=location, floor=floor, gender=gender)
		session.add(bathroom_new)
		session.commit()
		return render_template('bathroomAdded.html')
	else:
		return render_template('addBathroomForm.html')

@app.route('/addReview')
def add_review():
    pass

if __name__ == '__main__':
    app.run()
