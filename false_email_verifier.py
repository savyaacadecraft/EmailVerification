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

idnum = None

def printf(*args):
    print(*args, file=open("All_Print_Logs.txt", "a"))

def get_file_data(file_name):
    Company_list = list()

    with open(file_name, "r") as file:
        for line in file:
            Company_list.append(line.split("\n")[0])
    
    return Company_list

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

def pattern_matcher(first_name, last_name, domain, email, pattern_list) -> str:
    
    for i in pattern_list:
        ptrn = i.replace('firstname', first_name).replace('lastname', last_name).replace('firstinitial', first_name[0]).replace('lastinitial', last_name[0]).lower()
        mail = f'{ptrn}@{domain}'

        if email == mail:
            return i

def get_pattern(Domain, True_Data) -> dict:
    
    pattern_dict = dict()
    pattern_list = get_file_data("patterns.txt")

    if "//" in Domain:
        Domain = ".".join(" ".join(Domain.split("//")[1:]).replace("/","").replace("www.","").replace("-", "").split(".")[0:2])
    else:
        Domain = Domain.replace("www.","").replace("-", "").replace("/", "")


    for i in True_Data:
        ptrn = pattern_matcher(first_name=i["first"], last_name=i["last"], domain=Domain, email=i["email"], pattern_list=pattern_list)

        if not ptrn: continue

        if ptrn in pattern_dict.keys():
            pattern_dict[ptrn] += 1
        else:
            pattern_dict[ptrn] = 1
        
    final_list = sorted(pattern_dict, key=lambda k: pattern_dict[k])
    for i in final_list:
        if i in pattern_list:
            index = pattern_list.index(i)
            pattern_list.pop(index)
    
    return final_list + pattern_list

def get_company_pattern_list(company, domain):

    data =  collection.find({"Company": company, "data_dict.Verification": True}, {"data_dict.first": 1, "data_dict.last": 1, "data_dict.email": 1, "_id": 0})
    
    try:
        data = list(data)[0]       
        pattern_collection = get_pattern(Domain=domain, True_Data=data["data_dict"])
        # print(company["Company"], pattern_collection, sep="\n", file=open(f"Company/{company['Company']}.csv", "w"))
        printf(pattern_collection)
        printf(":::::Company Pattern List Created:::::")
        return pattern_collection
    except Exception as E:
        printf(":::::Company Pattern List Not Found:::::")
        printf("Exception: ", E, company["Company"])
        return get_file_data("patterns.txt")

def CompanyEmailPatrn(Company, start_id, condition=False, pattern=None):
    global idnum

    Company_Bool = False
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

            if i['Verification'] == condition:
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
                        ptrn, EMail, counter = PatternCheck(fullName, domain, idnum, pattern_list=pattern)
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
                    if not Company_Bool: Company_Bool = True
                    
                else:
                    correctness["incorrect"] += 1

                    collection.update_one(
                        {"Company": Company, "data_dict" :{"$elemMatch" : {"id": id}}}, 
                        {'$set': {
                            "data_dict.$.Verification": "pending"
                            }}
                        )
                    
                    if correctness["correct"] < correctness["incorrect"] and correctness["correct"] != 0 and correctness["incorrect"] != 0: 
                        return False


                printf(f'Email Found[{id}] ~ {EMail}\n--------------------------')
                
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

    return Company_Bool



if __name__ == "__main__":

    idnum = 15
    tomorrow = ((datetime.now()) + timedelta(days=1)).strftime("%Y-%m-%d")
    printf(tomorrow)

    companies = collection.find({"data_dict.Verification": False}, {"Company":1, "Domain": 1})
    
    for company in companies:

        if tomorrow == datetime.now().strftime("%Y-%m-%d"):
            exit("Next Day Has Started ........")
        
        if idnum > 30:
            exit("......Credential ID above 30 don't exist......")

        printf("################################################################################")

        printf("Company Name :::: ", company["Company"])
        try:

            _pattern = get_company_pattern_list(company=company["Company"], domain=company["Domain"])

            ptrn_found = CompanyEmailPatrn(Company=company["Company"], start_id=idnum, condition=False, pattern=_pattern)
            if not ptrn_found:
                print("Company: ", company["Company"], sep=", ", file=open("Pattern_Not_Found.csv", "a"))
            
        except Exception as E:
            printf(E)
            break

        except KeyboardInterrupt as KE:
            printf("Generated KeyBoard Interrupt ::::::")
            break
        
    printf("False Phase Completed.......")
        

        
        

        
        