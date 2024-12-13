from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

print(client.list_database_names())

db = client['servant_chatbot']  # replace with your database name

# Create the CivilComplaints collection with schema validation and uniqueness constraint on '_id'
def create_civil_complaints_collection():
    try:
        db.create_collection(
            'CivilComplaints',
            validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["Gu", "doc_id", "date", "dept", "state"],
                    "properties": {
                        "Gu" : {
                            "bsonType": "string",
                            "description": "Gu must be a string."
                        },
                        "doc_id": {
                            "bsonType": "int",
                            "description": "doc_id should be a unique integer."
                        },
                        "answer_url": {
                            "bsonType": ["string", "null"],
                            "description": "answer_url must be a string or null."
                        },
                        "title": {
                            "bsonType": ["string", "null"],
                            "description": "title must be a string or null."
                        },
                        "request_content": {
                            "bsonType": ["string", "null"],
                            "description": "request_content must be a string or null."
                        },
                        "attached_file": {
                            "bsonType": ["binData","null", "array"],
                            "description": "attached_file must be binary data (e.g., file)."
                        },
                        "answer": {
                            "bsonType": ["string", "null"],
                            "description": "answer must be a string or null."
                        },
                        "answer_summary": {
                            "bsonType": ["string", "null"],
                            "description": "answer_summary must be a string or null."
                        },
                        "extracted_reference": {
                            "bsonType": ["array", "null"],
                            "description": "extracted_reference must be an array or null."
                        },
                        "date": {
                            "bsonType": "date",
                            "description": "date must be a date."
                        },
                        "dept": {
                            "bsonType": "string",
                            "description": "dept must be a string."
                        },
                        "state": {
                            "bsonType": "string",
                            "description": "state must be a string."
                        },
                        "note": {
                            "enum": ["조례", "법률", "이관", None],  # JavaScript의 null 대신 Python의 None 사용
                            "description": "note must be one of '조례', '법률', '이관', or null."
                        }
                    }
                }
            }
        )
        # Create a unique index on the '_id' field (This is automatic for _id, but here to demonstrate uniqueness of the _id)
        db.CivilComplaints.create_index([("doc_id", 1)], unique=True)
        print("CivilComplaints collection created with schema and constraints!")
    except Exception as e:
        print(f"Error creating CivilComplaints collection: {e}")

# Create the GuOffice collection
def create_gu_office_collection():
    try:
        db.create_collection('GuOffice', validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["Gu", "url", "depts"],
                "properties": {
                    "Gu": {
                        "bsonType": "string",
                        "description": "Gu should be a string."
                    },
                    "url": {
                        "bsonType": "string",
                        "description": "url should be a string."
                    },
                    "depts": {
                        "bsonType": "object",
                        "description": "depts should be an object containing category and deptcode pairs."
                    }
                }
            }
        })
        print("GuOffice collection created with schema!")
    except Exception as e:
        print(f"Error creating GuOffice collection: {e}")

# Example usage
if __name__ == '__main__':
    create_civil_complaints_collection()
    create_gu_office_collection()
