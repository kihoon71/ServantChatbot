from pymongo import MongoClient
# test_insert_GU_data.py 파일에서
import sys
import os
import requests

# 프로젝트 디렉토리를 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
print(sys.path)

# 이제 절대 임포트를 사용하여 임포트
from utils.crawl import get_dept_code


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['servant_chatbot']  # replace with your database name

url = 'https://www.yangcheon.go.kr/site/mayor/ex/bbs/List.do?cbIdx=414'
response = requests.get(url)


# get the department code
dept_codes = get_dept_code(response.text)

# Insert the GU data
db.GuOffice.insert_one({
    'Gu': '양천구',
    'url' : url,
    'depts' : dept_codes
})

