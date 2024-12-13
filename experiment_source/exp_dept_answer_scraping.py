import bs4
import requests
import re
from pprint import pprint
import os
import sys
import traceback
from datetime import datetime

from pymongo import MongoClient


if __name__=="__main__":

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['servant_chatbot'] 
    

    # get the urls and doc_id from CivilComplaints collection
    civil_complaints = db.CivilComplaints.find()
    doc_id_and_url = [(complaint['doc_id'], complaint['answer_url']) for complaint in civil_complaints]

    pprint(len(doc_id_and_url))
    
    # request to the answer url
    for doc_id, url in doc_id_and_url[1:]:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        title = soup.find('td', id='bbsTitle').text.strip()
        content = soup.find('div', {"class" :"txt-area"}).text.strip()
        answer = soup.find('dd', {"class" :"detail"}).text.strip()

        # update the CivilComplaints collection

        db.CivilComplaints.update_one(
            {'doc_id': doc_id},
            {
                '$set': {
                    'title': title,
                    'request_content': content,
                    'answer': answer
                }
            }
        )
        print(doc_id)
        # print(title)
        # print(content)
        # print('---')
        # print(answer)
        


    # parse the answer page