import bs4
import requests
import re
from pprint import pprint
import os
import sys
import traceback
from datetime import datetime

from pymongo import MongoClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import utils.crawl as crawl
import utils.dataSchema as schema

def make_civil_complaints(body):

    bulks = []
    for row in body:
        doc_id = row[0]
        answer_url = row[1]
        date = datetime.strptime(row[2], "%Y.%m.%d") # date : '2024.09.25'
        dept = row[3]
        state = row[4]

        civil_complaints = schema.CivilComplaints(
            Gu='양천구',
            doc_id = int(doc_id),
            answer_url= answer_url,
            answer_summary=None,
            extraced_reference=None,
            date = date,
            dept = dept,
            state = state,
            title = None,
            request_content = None,
            attached_file = [],
            answer = None,
            note = None
        )

        bulks.append(civil_complaints.dict())

    return bulks

if __name__=="__main__":

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['servant_chatbot']  # replace with your database name

    # get the url and depts code from GU office
    yangcheon_gu = db.GuOffice.find_one({'Gu': '양천구'})
    url = yangcheon_gu['url']
    dept_codes = yangcheon_gu['depts']['교통']

    # make the url for the department
    dept_url = url + "&depts=" + dept_codes

    response = requests.get(dept_url)
    page_links = crawl.get_page_indices(response.text)
    
    first_page = page_links[0] # to use later for the range
    last_page = page_links[-1] # to use later for the range

    page_range = [ dept_url + '&pageIndex=' + str(i) for i in range(1, 10)]

    pprint(page_range)
    try:
        session = client.start_session()
        session.start_transaction()
        # get the data from the pages

        for page in page_range:
            response = requests.get(page) 
            if response.status_code == 200:
                tables = crawl.get_table(response.text)
                body = crawl.get_body_rows(tables)
                bulk = make_civil_complaints(body)
                db.CivilComplaints.insert_many(bulk)
            
    except Exception as e:
        print(traceback.format_exc())
        session.abort_transaction()
    else:
        session.commit_transaction()
        print("Success in the request")

    
    