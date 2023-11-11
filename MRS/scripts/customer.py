from random import sample
from string import hexdigits, octdigits
import sqlite3 as s3
from sqlitekvstore import SQLiteKVStore as kv
import json
import datetime
import qrcode # Testing Basis

class CustomerHandler:
    _user = None
    _regNo = None
    _data = {"regNo":"","fName":"","dob":"","gender":"","phoneN":"","eContact":"","bg":"","email":"","address":"","Allergies":"","cMedications":"","pmc":"","fmc":"","pcp":"","ip":"","pn":"","gn":"","pne":"","rtp":"",}

    def __init__(self):
        pass

    # data logging
    def _log(self, queue):
        with open("log.txt", "a") as f:
            f.write(f"customer::logged-at::>{datetime.datetime.now()}:: {queue}\n")
            f.close()

    # add data to database
    def toCustomerData(self, data: dict, user):
        try:
            db = kv("customer.db")
            self._key = "".join(sample(hexdigits, 10))
            data = dict(data)
            
            # Check if "customer-data" key exists in the database
            if "customer-data" not in db:
                db["customer-data"] = json.dumps({})
            
            # Parse existing customer data
            customer_data = json.loads(db["customer-data"])
            
            for key, value in data.items():
                if key in self._data:
                    self._data[key] = value
                else:
                    continue
            
            self._data["regNo"] = self._key

            # Update the user's data
            customer_data[user] = self._data
            
            # Store the updated customer data in the database
            db["customer-data"] = json.dumps(customer_data)
            db.close()
            
            return True
        except Exception as e:
            # Print or log the error message for debugging
            self._log(f"Error in toCustomerData: {e}")
            return False


    # retrive data from userdata
    def retriveCustomerData(self, user, key=None):
        try:
            db = kv("customer.db")
            if key is None:
                data = json.loads(db["customer-data"])[user]
                return data    
        except:
            return False
    
    def toSignUp(self, data:dict):
        db = kv("customer.db")
        # data = dict(data)
        self._user = data.get("usrname")
        # key = "".join(sample(hexdigits, 10))
        if "user-data" not in db.keys():
            db["user-data"] = json.dumps({})
        try:
            if self._user in json.loads(db.get("user-data")):
                return False
        except Exception as e:
            self._log(e)
        
        ud = json.loads(db.get("user-data"))
        # data["regNo"] = key
        ud[self._user] = data
        db["user-data"] = json.dumps(ud)
        db.close()
        return True
    
    def getSignUpData(self):
        db = kv("customer.db")
        data = json.loads(db["user-data"])
        # print(data)
        db.close()
        return data
    
    def checkSignIn(self, data:dict):
        db = kv("customer.db")
        self._user = data["usrname"]
        datas = json.loads(db["user-data"])
        if self._user not in datas.keys():
            return (False, "UserName Not found")
        
        datas = datas[self._user]
        if datas["pass"] != data["pass"]:
            return (False, "Incorrect Password")
        return (True, None)
    
    def clear(self):
            _user = None
            _regNo = None
            _data = {"regNo":"","fName":"","dob":"","gender":"","phoneN":"","eContact":"","bg":"","email":"","address":"","Allergies":"","cMedications":"","pmc":"","fmc":"","pcp":"","ip":"","pn":"","gn":"","pne":"","rtp":"",}
