from random import sample
from string import hexdigits, octdigits
import sqlite3 as s3
from sqlitekvstore import SQLiteKVStore as kv
# import weasyprint
import qrcode # Testing Basis
import datetime
import json

class InstituteHandler:
    _institute = None
    
    def __init__(self) -> None:
        pass

    def _log(self, queue):
        with open('log.txt', "a") as f:
            f.write(f'institute::logged-at::>{datetime.datetime.now()}:: {queue}\n')
            f.close()

    def toSignUp(self, data:dict):
        db = kv("institute.db")
        self._log(data)
        self._institute = data.get('instituteID')
        if "institute-data" not in db.keys():
            db["institute-data"] = json.dumps({})
        
        try:
            if self._institute in json.loads(db.get('institute-data')):
                return False
        except Exception as e:
            self._log(e)
        
        id = json.loads(db.get("institute-data"))
        id[self._institute] = data
        db["institute-data"] = json.dumps(id)
        db.close()
        return (True, data["instituteID"])
    
    def checkSignIn(self, data:dict):
        db = kv("institute.db")
        self._institute = data["instituteID"]
        datas = json.loads(db["institute-data"])
        if self._institute not in datas.keys():
            return (False, "Institute Id Not Found")
        
        datas = datas[self._institute]
        if datas["pass"] != data["pass"]:
            return (False, "Incorrect Password")
        
        return (True, None)
    
    def retriveInstituteData(self, iID=None):
        with kv("institute.db") as db:
            if iID is None:
                return json.loads(db["institute-data"])
            data = json.loads(db["institute-data"][iID])
            db.close()
        return data
    
    def addPatient(self, iid, data):
        try:
            db = kv("institute.db")
            dataPatients = json.loads(db.get("patients", "{}"))
            institute_data = dataPatients.get(iid, {})
            institute_data[data["usrname"]] = data
            dataPatients[iid] = institute_data
            db["patients"] = json.dumps(dataPatients)
            db.close()
            return True
        except Exception as e:
            self._log(f"Error in addPatient: {str(e)}")
            return False  # Indicate failure

    def add_subscription(self, iid, sub):
        try:
            db = kv("institute.db")
            data = json.loads(db["institute-data"][iid])
            data["sub"] = sub
            db["institute-data"][iid] = json.dumps(data)
            db.close()
            return True
        except:
            return False


    def getPatients(self, iid):
        try:
            db = kv("institute.db")
            patientData = json.loads(db["patients"])
            institute = patientData[iid]
            return institute
        except Exception as e:
            self._log(f"Error in getPatient: {str(e)}")

    def showPatients(self):
        db = kv("institute.db")
        data = list(db["patients"])
        db.close()
        return(data)
    
        


