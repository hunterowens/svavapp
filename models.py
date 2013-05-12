from sqlalchemy import Column, Integer, String, Sequence, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from EnumSymbol import DeclEnum

Base = declarative_base()

class GenderType(DeclEnum):
    female = "female", "Female"
    male = "male", "Male"
    either = "either", "Either"
    neither = "neither", "Neither"
    what = "what", "what?"

class Bathroom(Base):
    __tablename__ = "bathrooms"

    id = Column(Integer, Sequence("bathroom_id_seq"), primary_key=True)
    location = Column(String(128))
    floor = Column(String(128))
    gender = Column(GenderType.db_type())

    def __init__(self, location, floor, gender):
        self.location = location
        self.floor = floor
        self.gender = gender

    def __repr__(self):
        return "<Bathroom('%s', '%s', '%s')>" % (self.location, \
                self.floor, self.gender)

def Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, Sequence("review_id_seq"), primary_key=True)
    bathroom_id = Column(Integer, ForeignKey('bathrooms.id'))
    rating = Column(Integer)
    comment = Column(String(1024))

    bathroom = relationship("Bathroom", backref=backref('reviews', order_by=id))

    def __init__(self, rating, comment):
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return "<Review('%d', '%s')>" % (self.rating, self.comment)
