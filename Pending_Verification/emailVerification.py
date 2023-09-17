# # If i have 1000 Emails then i have to check first 10 each with 16 pattern until i get the True Point else pass
# #

from validate_email_own import PatternCheck
from pymongo import MongoClient
from urllib.parse import quote_plus
import ast
from sys import exit
from os.path import exists
from os import system
from datetime import datetime, timedelta


class PendingVerification:

    def __init__(self, start_id, last_id) -> None:
        
        self.DAILY_LIMIT = 1000

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
        self.collection = db['my_collection']

        self.idnum = start_id
        self.ID_MAX = last_id

    def printf(self, *args):
        print(*args, file=open("All_Pending_Logs.txt", "a"))

    def update_pattern_list(self, ptrn):
    
        with open("patterns.txt", "r") as file:
            patterns = file.readlines()

        patterns = [pattern.strip() for pattern in patterns]

        if ptrn in patterns:
            patterns.remove(ptrn)
            patterns.insert(0, ptrn)

        with open("patterns.txt", "w") as file:
            for pattern in patterns:
                file.write( pattern + "\n")

    def patternCatcher(self, Company):
        if exists(f'../Companies/{Company}.csv'):
            with open(f'{Company}.csv','r',encoding='utf-8') as f:
                first_line = f.readlines()[1]

                dictionary = ast.literal_eval(first_line)
                self.printf(dictionary)
                return dictionary
        else:
            self.printf("File not found")
            return dict()
    
    def get_file_data(self, file_name):
        self.Company_list = list()

        if exists(file_name):
            with open(file_name, "r") as file:
                for line in file:
                    self.Company_list.append(line.split("\n")[0])

            return self.Company_list
        else:
            system(f"touch {file_name}")
            return self.Company_list

    def Max_ID_Checker(self,):
        if self.idnum > self.ID_MAX:
            PV_Obj.printf(f"......Credential ID above {ID_MAX} don't exist......")
            return False
        return True

    def CompanyEmailPatrn(self, Company, pattern=None):

        Company_Bool = False
        try:
            correctness = {"correct": 0, "incorrect": 0}

            data = self.collection.find_one({"Company": Company,}, {"Domain": 1, "data_dict": 1})
            
            domain = data['Domain']
            for i in data["data_dict"]:

                
                NULL_COUNTER = 0

                if i['Verification'] == "pending":
                    self.printf("Checking:",i["id"])
                    id = i['id']
                    fname = i['first']
                    lname = i['last']

                    fullName = f'{fname} {lname}'.replace(".","").replace(",","").replace("(","").replace(")","")
                    self.printf(fullName)

                    while (self.idnum <= self.ID_MAX):
                        ptrn = None
                        EMail = None
                        counter = 0
                        try:

                            self.printf(f"Email[{id}] ==", fullName,'\n-------------------------')
                            ptrn, EMail, counter = PatternCheck(fullName, domain, self.idnum, pattern_list=pattern)
                            break

                        except Exception as E:
                            if "Refresh problem"  in E:
                                NULL_COUNTER += 1
                                if NULL_COUNTER >= 4: 

                                    return False

                            else:
                                NULL_COUNTER = 0
                            self.printf("Exception: ",E)
                            self.printf(f"ID Value is :::: {self.idnum}")


                    if counter > self.DAILY_LIMIT:
                        self.printf(f"******** Daily Limit Reached for ID: {self.idnum} ********")
                        self.idnum += 1

                    if EMail:
                        correctness["correct"] += 1
                        self.collection.update_one({
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

                        self.collection.update_one(
                            {"Company": Company, "data_dict" :{"$elemMatch" : {"id": id}}}, 
                            {'$set': {
                                "data_dict.$.Verification": "pending"
                                }}
                            )

                        if correctness["correct"] < correctness["incorrect"] and correctness["correct"] != 0 and correctness["incorrect"] != 0: 
                            return False


                    self.printf(f'Email Found[{id}] ~ {EMail}\n--------------------------')

                    # This Section is used to update the pattern.txt 
                    # For pattern through which latest Email has been founded
                    try:
                        self.update_pattern_list(ptrn)
                        self.printf(f'{ptrn} Listed first on patterns.txt')
                    except Exception:
                        pass


        except Exception as e:
            self.printf(e)

        return Company_Bool


if __name__ == "__main__":

    idnum = 20
    ID_MAX = 40

    PV_Obj = PendingVerification(start_id=idnum, last_id=ID_MAX)
    # Running for Pending Email Verification
    companies = PV_Obj.collection.find({"data_dict.Verification": "pending"}, {"Company":1})
    
    for company in companies:

        PV_Obj.printf("################################################################################")

        PV_Obj.printf("Company Name :::: ", company["Company"])
        try:
            ptrn_found = PV_Obj.CompanyEmailPatrn(Company=company["Company"], start_id=idnum)
            
            
        except Exception as E:
            PV_Obj.printf(E)

        except KeyboardInterrupt as KE:
            PV_Obj.printf("Generated KeyBoard Interrupt ::::::")
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
