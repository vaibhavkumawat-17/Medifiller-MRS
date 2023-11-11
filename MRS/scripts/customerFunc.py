from scripts.customer import CustomerHandler
from scripts.institute import InstituteHandler

def getUserData(user):
    customer = CustomerHandler()
    data = customer.retriveCustomerData(user)
    return data

def logSig(jsondata:dict):
        customer = CustomerHandler()
        if jsondata['dataHead'] == 'su':
            jsondata.pop('dataHead')
            customer._log(jsondata)
            flag = customer.toSignUp(dict(jsondata)) 
            print(flag)
            if not flag:
                return (False,)
            customer._log('success')
            return (True, 'su', jsondata['usrname']) # Change this after the backend for dashboard has been completed
        elif jsondata["dataHead"] == 'si':
            customer._log(jsondata['dataHead'])
            jsondata.pop('dataHead')
            if not customer.checkSignIn(jsondata)[0]:
                return (False,)
            customer._log('True')  
            return (True, 'si', jsondata['usrname'])
        
def sendDataToInstitute(iid, user):
    institute = InstituteHandler()
    customer = CustomerHandler()
    try:
        data = customer.getSignUpData()[user]
        try:
            if user in institute.getPatients(iid):
                return False
            institute.addPatient(iid, data)
        except:
            institute.addPatient(iid, data)
        return True
    except Exception as e:
        # customer._log(e)
        # institute._log(e)
        print(e)
        return False

def getDataFromInstitute():
    institute = InstituteHandler()
    return institute.retriveInstituteData()
