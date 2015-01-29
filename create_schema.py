from models import *
import config

if __name__ == '__main__':
    engine = create_engine(URL(**config.DATABASE))
    Base.metadata.create_all(engine)

