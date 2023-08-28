
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timedelta


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

# myTime = "2023-06-03T15:51:47.005"

# Compny = collection.find_one({"Company": "Bauer Media"})
# comp = Compny["Company"]
# for employee in Compny["data_dict"]:
#     if employee["Verification"] == "Not Found":
#         id = employee["id"]
#         collection.update_one({"Company": comp, "data_dict" :{"$elemMatch" : {"id": id}} }, {'$set': {"data_dict.$.Verification": "pending" }})



Company = collection.find_one({"Company": "Webedia"})

for employee in Company["data_dict"]:
    if employee['Verification'] == "Not Found":   
        print(employee["id"])     
        collection.update_one({"Company": "Webedia", "data_dict" :{"$elemMatch" : {"id": employee["id"]}} }, 
                      {'$set': 
                         {
                            "data_dict.$.Verification": "pending"
                          }
                        })

# str_date = "2023-06-16T18:20:53.118"
collection.update_one({"Company": "N3TWORK", "data_dict" :{"$elemMatch" : {"id": 4}} }, 
                      {'$set': 
                         {
                            "data_dict.$.Checked24": datetime.now() - timedelta(days=1, hours=6)
                          }
                        })

# today = datetime.now()
# the_day_before_yesterday = today - timedelta(days=1)
# yesterday = today - timedelta(days=0)

# results = [
#         {
#             '$match': {
#                 'data_dict.Checked24': {
#                     '$gte': the_day_before_yesterday.replace(hour=0, minute=0, second=0, microsecond=0),
#                     '$lte': yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
#                 }
#             }
#         },
#         {
#             '$project': {
#                 '_id': 0,
#                 'num_occurrences': {
#                     '$size': {
#                         '$filter': {
#                             'input': '$data_dict.Checked24',
#                             'as': 'checked',
#                             'cond': {
#                                 '$and': [
#                                     {'$gte': ['$$checked', the_day_before_yesterday.replace(
#                                         hour=0, minute=0, second=0, microsecond=0)]},
#                                     {'$lte': ['$$checked', yesterday.replace(
#                                         hour=0, minute=0, second=0, microsecond=0)]}
#                                 ]
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     ]
# Allresults = list(collection.aggregate(results))


# print(Allresults)


