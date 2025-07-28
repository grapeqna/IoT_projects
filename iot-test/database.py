from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://ilievayana:iylfRpWikjic485Y@cluster0.ij9wh5k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

DATABASE_NAME = "iot_exam"

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client[DATABASE_NAME]

