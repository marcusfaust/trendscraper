"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
"""

from pptx import Presentation
from models import *
from sqlalchemy.orm import sessionmaker
import config

prs = Presentation('/Users/mxf7/PycharmProjects/trendscraper/vnx.pptx')

summary_found = False
ARRAYSUMMARY = {}
for slide in prs.slides:
    for shape in slide.shapes:
        if (shape.has_text_frame and shape.text == 'System Summary'):
            summary_found = True
            continue

        if (shape.has_table and summary_found):
            for row in range(0,len(shape.table.rows._tbl.tr_lst)):
                ARRAYSUMMARY[shape.table.cell(row,0).text_frame.text] = shape.table.cell(row,1).text_frame.text
                summary_found = False


print "hello"
#INSERT Summary information into db

engine = create_engine(URL(**config.DATABASE))
Session = sessionmaker(bind=engine)
session = Session()

summ = Summary(ARRAYSUMMARY['% Reads'],
               ARRAYSUMMARY['Front End IOPS - avg'],
               ARRAYSUMMARY['Front End IOPS - 95th'],
               ARRAYSUMMARY['Front End IOPS - max'],
               ARRAYSUMMARY['Model'],
               ARRAYSUMMARY['Avg IO Size (KB)'])

session.add(summ)
session.commit()

print "hello"



