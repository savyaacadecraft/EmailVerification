
from pymongo import MongoClient
from urllib.parse import quote_plus


username = "manojtomar326"
password = "Tomar@@##123"
cluster_url = "cluster0.ldghyxl.mongodb.net"

# Encode the username and password using quote_plus()
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Create the MongoDB Atlas connection string with the encoded credentials
connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster_url}/test?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(connection_string)

# Query all documents in the collection
db = client['mydatabase']
collection = db['my_collection']


#  Compny = collection.find_one({"status":"Checked"})
#             print("Comapany --> ",Compny["Company"])
#             print("TotalProfiles -> ", Compny["totalProfiles"])


data = collection.find(
            {"data_dict.Verification": {"$in": [False, "pending"]}},
            {"Company": 1,"Domain": 1, "data_dict": 1}
        )

for company in data:
    print(company["Company"])
    for employee in company["data_dict"]:
        if employee["Verification"] in [False, "pending"]:
            print(employee["first"])
            print(employee["last"])
            print(employee["id"])
            print(employee["email"])

            
        break
    break
100/0

# barrett.sheridan@nytimes.com

collection.update_one({"Company": company["Company"], "data_dict" :{"$elemMatch" : {"id": employee["id"]}}}, 
                                  {'$set': {"data_dict.$.email": "barrett.sheridan@nytimes.com"}})


