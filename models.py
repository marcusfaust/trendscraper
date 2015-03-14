import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.engine.url import URL


Base = declarative_base()


class Summary(Base):
    __tablename__ = 'summary'

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=True), primary_key=False, nullable=False, default=datetime.datetime.now)
    customer = Column(String)
    serial_no = Column(String)
    percent_read = Column(String)
    iops_avg = Column(String)
    iops_95th = Column(String)
    iops_max = Column(String)
    model = Column(String)
    avg_io_size = Column(String)

    def __init__(self, customer, percent_read, iops_avg, iops_95th, iops_max, model, avg_io_size):
        self.customer = customer
        self.percent_read = percent_read
        self.iops_avg = iops_avg
        self.iops_95th = iops_95th
        self.iops_max = iops_max
        self.model = model
        self.avg_io_size = avg_io_size


class RefreshToken(Base):
    __tablename__ = 'rtokens'

    id = Column(Integer(), primary_key=True)
    token = Column(String())

    def __repr__(self):
        return '<token {}>'.format(self.token)


