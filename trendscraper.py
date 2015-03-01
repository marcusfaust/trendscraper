"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
"""

import argparse, requests, re
import httplib2
from pptx import Presentation
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets, AccessTokenCredentials
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.discovery import build
from oauth2client.tools import run_flow
from models import *
from sqlalchemy.orm import sessionmaker
import os
import config
import base64


from apiclient import errors

ftplinks = []

class GmailSession:


    def __init__(self , session):
        self.refresh_token = session.query(RefreshToken).filter_by(id=1).first()


    gmail_client_id = os.environ.get('GMAIL_CLIENT_ID')
    gmail_client_secret = os.environ.get('GMAIL_CLIENT_SECRET')

    """
    flow = OAuth2WebServerFlow(client_id=gmail_client_id,
                               client_secret=gmail_client_secret,
                               scope='https://www.googleapis.com/auth/gmail.readonly',
                               redirect_uri='https://www.example.com/oauth2callback',
                               access_type='offline',
                               approval_prompt='force')

    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flags = parser.parse_args()

    storage = Storage('Trendscraper.json')

    credentials = run_flow(flow, storage, flags)
    """

    def getAccessToken(self, session):

        tokenURL = "https://www.googleapis.com/oauth2/v3/token"

        params = {"client_id": self.gmail_client_id,
                  "client_secret": self.gmail_client_secret,
                  "refresh_token": str(self.refresh_token.token),
                  "grant_type": "refresh_token"}

        r = requests.post(tokenURL, params=params)
        results = r.json()
        atoken = results['access_token']

        # Store refresh_token
        #session.query(RefreshToken.filter_by(id=1).update(dict(token=rtoken))
        #db.session.commit()


        return atoken

    def get_mail(self):
        pass

engine = create_engine(URL(**config.DATABASE))
Session = sessionmaker(bind=engine)
session = Session()

gmailsession = GmailSession(session)
access_token = gmailsession.getAccessToken(session)
new_credentials = AccessTokenCredentials(access_token, '', '')

print "hello"

def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
              page_token = response['nextPageToken']
              response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
              messages.extend(response['messages'])

        return messages

    except errors.HttpError, error:
        print 'An error occurred: %s' % error

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'Trendscraper.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

# Location of the credentials storage file
#STORAGE = Storage('gmail.storage')

#HTTP object
http = httplib2.Http()
http = new_credentials.authorize(http)

#Gmail Service
gmail_service = build('gmail', 'v1', http=http)

# Retrieve a list of all messages
messages = gmail_service.users().messages().list(userId='me').execute()

#Get Contents of Each Message and Populate ftpdict
for message in messages['messages']:
    message_text = gmail_service.users().messages().get(id=message['id'], userId='me', format='full').execute()
    for part in message_text['payload']['parts']:
        print "hello"
        if part.has_key('body') and part['body'].has_key('data'):
            msg = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
            ftpmatches = re.findall('\r\n(.*assessment_download.*.zip)\r\n', msg)
            for link in ftpmatches:
                ftplinks.append(link)

print "hello"



#Download any new emails from service account
#new_messages = ListMessagesMatchingQuery(gmail_service, 'me', 'from:mfaust@fusionstorm.com')
#response = gmail_service.users().messages().list(userId='me', q='').execute(http=http_auth)

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



