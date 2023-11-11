from scripts.institute import InstituteHandler
from scripts.customer import CustomerHandler

def logSig(jsondata:dict):
        customer = InstituteHandler()
        if jsondata['dataHead'] == 'su':
            jsondata.pop('dataHead')
            # customer._log(jsondata)
            flag = customer.toSignUp(dict(jsondata)) 
            print(flag)
            if not flag:
                return (False,)
            customer._log('success')
            return (True, 'su', jsondata['instituteID']) # Change this after the backend for dashboard has been completed
        elif jsondata["dataHead"] == 'si':
            jsondata.pop('dataHead')
            if not customer.checkSignIn(jsondata)[0]:
                return (False,)
            customer._log('True')  
            return (True, 'su', jsondata['instituteID'])

def patients(iid):
    institute = InstituteHandler()
    customer = CustomerHandler()
    # print(iid)
    try:
        patient = list(institute.getPatients(iid).values())
    except:
        patient = []
    # print(patient)
    for i in range(len(patient)):
        user = patient[i]["usrname"]
        data = customer.retriveCustomerData(user=user)
        if data is False:
            patient[i]["regNo"] = ""
        else:
            patient[i]["regNo"] = data["regNo"]
    # print(patient)
    return patient

