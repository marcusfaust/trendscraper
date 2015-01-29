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



print "hello"