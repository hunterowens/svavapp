from models import Base
from hello import engine

Base.metadata.create_all(engine)
