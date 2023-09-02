from pprint import pprint
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



# Company = collection.find_one({"Company": "Webedia"})

# for employee in Company["data_dict"]:
#     if employee['Verification'] == "Not Found":   
#         print(employee["id"])     
#         collection.update_one({"Company": "Webedia", "data_dict" :{"$elemMatch" : {"id": employee["id"]}} }, 
#                       {'$set': 
#                          {
#                             "data_dict.$.Verification": "pending"
#                           }
#                         })

# # str_date = "2023-06-16T18:20:53.118"
# collection.update_one({"Company": "N3TWORK", "data_dict" :{"$elemMatch" : {"id": 4}} }, 
#                       {'$set': 
#                          {
#                             "data_dict.$.Checked24": datetime.now() - timedelta(days=1, hours=6)
#                           }
#                         })

# today = datetime.now()
# the_day_before_yesterday = today - timedelta(days=2)
# yesterday = today - timedelta(days=1)

# hourly_dict = dict()

# for i in range(24):
#     greater_time = (today - timedelta(hours=i)).replace(minute=0, second=0)
#     lower_time = (today - timedelta(hours=i+1)).replace(minute=0, second=0)
    
#     key = greater_time.strftime('%H')+" to "+lower_time.strftime('%H')
#     print(greater_time, lower_time, key, sep=" | ")
#     hourly_dict[key] = 0
#     try:
#         results = [
#                 {
#                     '$match': {
#                         'data_dict.Checked24': {
#                             '$gte': lower_time,
#                             '$lte': greater_time
#                         }
#                     }
#                 },
#                 {
#                     '$project': {
#                         '_id': 0,
#                         'num_occurrences': {
#                             '$size': {
#                                 '$filter': {
#                                     'input': '$data_dict.Checked24',
#                                     'as': 'checked',
#                                     'cond': {
#                                         '$and': [
#                                             {'$gte': ['$$checked', lower_time]},
#                                             {'$lte': ['$$checked', greater_time]}
#                                         ]
#                                     }
#                                 }
#                             }
#                         }
#                     }
#                 },
#                 {
#                     '$group': {
#                         '_id': None,
#                         'total_checked24_sum': {
#                             '$sum': '$num_occurrences'
#                         }
#                     }
#                 }
#             ]
#         data = list(collection.aggregate(results))
#     except Exception as E:
#         print("Iteration Count: ", i)
#         print(E)

#     try:
#         hourly_dict[key] = data[0]["total_checked24_sum"]
#     except Exception as EX:
#         print("Count: ", i)
#         print(EX)
#         print(data)
# pprint(hourly_dict)


# # print("YesterDay Total: ", Allresults[0]["total_checked24_sum"])



data = collection.aggregate([
  {
    "$unwind": "$data_dict"
  },
  {
    "$match": {
      "data_dict.Verification": "pending"
    }
  },
  {
    "$group": {
      "_id": "$_id",
      "itemCount": { "$sum": 1 },
      "specificValueCount": {
        "$sum": {
          "$cond": [
            { "$eq": ["$data_dict", "pending"] },
            1,
            0
          ]
        }
      }
    }
  },
  {
    "$group": {
      "_id": None,
      "totalItemCount": { "$sum": "$itemCount" },
      "totalSpecificValueCount": { "$sum": "$specificValueCount" }
    }
  }
])


print(data)
for i in data:
    print(i)
