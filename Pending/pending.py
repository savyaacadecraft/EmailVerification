from validate_email_own import verifying2, PatternCheck

from json import load
from pymongo import MongoClient
from urllib.parse import quote_plus
from sys import exit, argv
from datetime import datetime, timedelta
from time import sleep
from threading import Thread


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

START_ID = None
ID_MAX = None

DAILY_LIMIT = 1000
LIMIT_CHECKER = 0

def update_pattern_file(ptrn:str) -> None:

    pattern_list = list()

    with open("../patterns.txt", "r") as file:
        for line in file:
            pattern_list.append(line.split("\n")[0])

    pattern_list.pop(pattern_list.index(ptrn))
    pattern_list.append(ptrn)
    print("\n".join(pattern_list), file=open("../patterns.txt", "w"))

def printf(*args):
    print(*args, file=open(f"New_logic_pending_Logs.txt", "a"))

def get_file_data(file_name:str) -> list:
    data_list = list()

    with open(file_name, "r") as file:
        for line in file:
            data_list.append(line.split("\n")[0])
    
    return data_list

def data_insertion(firm: str, emp_id: int, email: str) -> None:
    printf(firm, emp_id, email)

    collection.find_one_and_update({"Company": firm, "data_dict": {"$elemMatch": {"id": emp_id}}},
                                        { "$set":
                                            {
                                                "data_dict.$.email": email,
                                                "data_dict.$.Verification": True,
                                                "data_dict.$.Checked24": datetime.now()
                                            
                                            }})

def initial_pattern_check(firm: str, pattern_dict: dict = None) -> dict:
    global START_ID, ID_MAX, DAILY_LIMIT

    # data = collection.aggregate(
    #     [
    #     {
    #         '$match': {
    #             'Company': firm
    #         }
    #     }, {
    #         '$unwind': {
    #             'path': '$data_dict'
    #         }
    #     }, {
    #         '$match': {
    #             'data_dict.Verification': "pending"
    #         }
    #     }
    #     ]
    # )
    data = collection.find_one({"Company": firm}, {"Domain": 1, "data_dict": 1})
    
    ptrn_list = None

    if pattern_dict:

        pattern_map = pattern_dict
        for i in pattern_map.keys():
            pattern_map[i] = 0
        ptrn_list = list(pattern_dict.keys())
    else:
        pattern_map = dict.fromkeys(get_file_data("../patterns.txt"), 0)

    init = 0
    for i in data["data_dict"]:
        if init == 10:
            break

        if i["Verification"] == "pending":

            name = i["first"] +" "+ i["last"]
            pattern, email, lmt = PatternCheck(full_name=name, domain=data["Domain"], _idnum=START_ID, pattern_list=ptrn_list)


            if lmt >= DAILY_LIMIT:
                START_ID += 1

            if pattern:
                pattern_map[pattern] += 1
                init += 1
                Thread(target=data_insertion, args=(firm, int(i["id"]), email)).start()
                # data_insertion(firm, int(i["id"]), email)
                update_pattern_file(pattern)

    return pattern_map

def get_count(firm:str) -> int:
    result = list(collection.aggregate([
        {
            '$match': {
                'Company': firm
            }
        }, {
            '$unwind': {
                'path': '$data_dict'
            }
        }, {
            '$match': {
                'data_dict.Verification': {
                    '$ne': True
                }
            }
        }, {
            '$count': 'count'
        }
    ]))


    return result[0]["count"]
        
def create_email_from_pattern(first_name, last_name, domain, pattern) -> str:
    
    if "//" in domain:
        domain = ".".join(" ".join(domain.split("//")[1:]).replace("/","").replace("www.","").replace("-", "").split(".")[0:2])
    else:
        domain = domain.replace("www.","").replace("-", "").replace("/", "")

    email = pattern.replace('firstname', first_name).replace('lastname', last_name).replace('firstinitial', first_name[0]).replace('lastinitial', last_name[0]).lower()

    email = email.replace("(", "").replace(")", "").replace("..", ".").replace(".@", "@").replace(",", "").replace("%", "").replace("$", "").replace("#", "").replace("/", "").replace("<", "").replace(">", "").replace("?", "")

    return email+"@"+domain
    
def has_only_one_max_value(d):

    if not d:
        return False

    max_value = max(d.values())
    if max_value < 1:
        return False

    count_max_value = sum(1 for value in d.values() if value == max_value)
    return count_max_value == 1

def email_finder(firm: str, _pattern:dict = None, turn:bool = False):
    global START_ID, ID_MAX, DAILY_LIMIT, LIMIT_CHECKER

    if turn:
        if has_only_one_max_value(_pattern):
            pattern_dict = _pattern
        else:
            pattern_dict = initial_pattern_check(firm, pattern_dict= _pattern)
        
    else:
        pattern_dict = initial_pattern_check(firm)
    
    

    count = get_count(firm)
    printf(len(pattern_dict.keys()), ":|:|:|:", count)

    if count or (len(pattern_dict.keys()) > 2):

        pattern = max(pattern_dict, key= lambda x: pattern_dict[x])

        data = collection.find_one({"Company": firm}, {"_id": 0, "Domain": 1, "data_dict": 1})
        for i in data["data_dict"]:
            if i["Verification"] == "pending":

                if LIMIT_CHECKER >= DAILY_LIMIT: 
                    START_ID += 1
                    LIMIT_CHECKER = 0

                email = create_email_from_pattern(i["first"], i["last"], data["Domain"], pattern)
                LIMIT_CHECKER += 1
                try:
                    if verifying2(recipient_email=email, id_num=START_ID):
                        Thread(target=data_insertion, args=(firm, int(i["id"]), email)).start()
                        # data_insertion(firm, int(i["id"]), email)
                except Exception as E:
                    printf("Exception ::::: ", E)
        
        if get_count(firm):
            del pattern_dict[pattern]
            email_finder(firm, pattern_dict, turn=True)


    else:
        if count < 1:
            return True
        else:
            return False
    


if __name__ == "__main__":

    data = load(open("Data.json", "r"))
    printf("start....")


    START_ID = data['pending']["start"]
    ID_MAX = data['pending']["max"]



    companies = collection.find({"data_dict.Verification": {"$eq": "pending"}}, {"Company":1, "_id": 0})
    try:
        for company in companies:
                       
            try:
                email_finder(company["Company"])
            except Exception as E:
                printf(E)

            
            # except KeyboardInterrupt as KE:
            #     print(company["Company"], "\n", file=open("firm_list.csv", "a"))
    
    except Exception as E:
        pass