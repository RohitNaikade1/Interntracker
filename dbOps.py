from pymongo import MongoClient
import urllib.parse

client=MongoClient("mongodb+srv://GSLab:"+urllib.parse.quote("gslab@123")+"@cluster0.v2mwo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db=client.get_database("InterTracker")
intern=db.Interns

