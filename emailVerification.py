# # If i have 1000 Emails then i have to check first 10 each with 16 pattern until i get the True Point else pass
# #

from validate_email_own import PatternCheck
from pymongo import MongoClient
from urllib.parse import quote_plus
import ast
from sys import exit
from os.path import exists
from datetime import datetime, timedelta


DAILY_LIMIT = 800

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

def printf(*args):
    print(*args, file=open("All_Print_Logs.txt", "a"))

def update_pattern_list(ptrn):
   
    with open("patterns.txt", "r") as file:
        patterns = file.readlines()

    patterns = [pattern.strip() for pattern in patterns]

    if ptrn in patterns:
        patterns.remove(ptrn)
        patterns.insert(0, ptrn)

    with open("patterns.txt", "w") as file:
        for pattern in patterns:
            file.write( pattern + "\n")

def patternCatcher(Company):
    if exists(f'Companies/{Company}.csv'):
        with open(f'{Company}.csv','r',encoding='utf-8') as f:
            first_line = f.readlines()[1]
            
    # Convert the string to a dictionary
            dictionary = ast.literal_eval(first_line)

            # Access and work with the dictionary
            printf(dictionary)
            return dictionary
    else:
        printf("File not found")
        return dict()
        

def CompanyEmailPatrn(Company, start_id):
    try:
        idnum = start_id
        correctness = {"correct": 0, "incorrect": 0}
        

        try:
            patternSuc = patternCatcher(Company)
        except Exception:
            patternSuc = {}
        
        Emails = []
        data = collection.find_one({"Company": Company,}, {"Domain": 1, "data_dict": 1})

        for i in data["data_dict"]:

            # i['Verification'] in (False, "pending")
            domain = data['Domain']

            if i['Verification'] == "pending":
                printf("Checking:",i["id"])
                id = i['id']
                fname = i['first']
                lname = i['last']

                fullName = f'{fname} {lname}'.replace(".","").replace(",","").replace("(","").replace(")","")
                printf(fullName)

                while (idnum <= 30):
                    ptrn = None
                    EMail = None
                    counter = 0
                    try:
                        
                        printf(f"Email[{id}] ==", fullName,'\n-------------------------')
                        ptrn, EMail, counter = PatternCheck(fullName, domain, idnum)
                        break

                    except Exception as E:
                        printf("Exception: ",E)
                        printf(f"ID Value is :::: {idnum}")
                        idnum += 1


                if counter > DAILY_LIMIT:
                    printf(f"******** Daily Limit Reached for ID: {idnum} ********")
                    idnum += 1

                if EMail:
                    correctness["correct"] += 1
                    collection.update_one({
                        "Company": Company,
                        "data_dict" :{"$elemMatch" : {"id": id}}
                        }, 
                        {'$set': 
                         {
                            "data_dict.$.email": EMail,
                            "data_dict.$.Verification": True,
                            "data_dict.$.Checked24": datetime.now()
                          
                          }})
                    
                else:
                    correctness["incorrect"] += 1

                    # collection.update_one(
                    #     {"Company": Company, "data_dict" :{"$elemMatch" : {"id": id}}}, 
                    #     {'$set': {
                    #         "data_dict.$.Verification": "Not Found",
                    #         "data_dict.$.Checked24": datetime.now()
                    #         }}
                    #     )

                    collection.update_one(
                        {"Company": Company, "data_dict" :{"$elemMatch" : {"id": id}}}, 
                        {'$set': {
                            "data_dict.$.Verification": "pending"
                            }}
                        )
                    
                    if correctness["correct"] < correctness["incorrect"] and correctness["correct"] != 0 and correctness["incorrect"] != 0: 
                        return False


                printf(f'Email Found[{id}] ~ {EMail}\n--------------------------')
                
                try:
                    update_pattern_list(ptrn)
                    printf(f'{ptrn} Listed first on patterns.txt')
                except Exception:
                    pass

                if ptrn in patternSuc.keys():
                    patternSuc[ptrn] = int(patternSuc[ptrn])+1
                else:
                    patternSuc[ptrn] = 1

                Emails.append(EMail)

        item_with_highest_value = max(patternSuc, key=lambda x: patternSuc[x])
        printf("Item with highest value:", item_with_highest_value)

    except Exception as e:
        printf(e)

    

    try:
        with open(f"Company/{Company}.csv", 'a', encoding='utf-8') as f:
            f.write(f'{Company}:\n{patternSuc}\n')
            f.write(', '.join(Emails))
            f.close()
        collection.update_one(
            {"Company": Company},
            {
                '$set': {
                    'pattern': item_with_highest_value
                }
            }
        )
    except Exception:
        pass


if __name__ == "__main__":
    
    tomorrow = ((datetime.now()) + timedelta(days=1)).strftime("%Y-%m-%d")
    printf(tomorrow)

    companies = collection.find({"data_dict.Verification": "pending"}, {"Company":1})
    
    for company in companies:

        if tomorrow == datetime.now().strftime("%Y-%m-%d"):
            exit("Next Day Has Started ........")

        printf("################################################################################")

        printf("Company Name :::: ", company["Company"])
        try:
            CompanyEmailPatrn(company["Company"], 15)
            
        except Exception as E:
            printf(E)
            break

        except KeyboardInterrupt as KE:
            printf("Generated KeyBoard Interrupt ::::::")
            break

        

    

































    # companies = collection.find({"status": "PC Completed", "data_dict.Verification": {"$in": [False, "pending"]}}, {"Domain":1, "data_dict":1})
    
    # for company in companies:
    #     # printf(company["Company"], company["totalProfiles"])
    #     for i in company.keys():
    #         printf(i, company[i], sep=": ")
    #     break
        
    
    # data = collection.find(
    #         {
    #             "Company": Company,
    #             "data_dict.Verification": {"$in": [False, "pending"]}
    #         },
    #         {"Domain": 1, "data_dict": {"$slice": totalProfiles}}
    #     )

    # for i in range(totalProfiles):
    #     Verification = (data[0]['data_dict'][i]['Verification'])
    #     if Verification == False or Verification == "pending":
    #         printf("Checking:",i)
    #         id = (data[0]['data_dict'][i]['id'])
    #         fname = (data[0]['data_dict'][i]['first'])
    #         lname = (data[0]['data_dict'][i]['last'])
    #         domain = (data[0]['Domain'])
