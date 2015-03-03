from models import *
import config

if __name__ == '__main__':
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)

