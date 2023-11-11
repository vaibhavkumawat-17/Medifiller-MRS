from flask import *
from scripts.customer import CustomerHandler
from scripts.institute import InstituteHandler
from scripts import customerFunc
from scripts import instituteFunc
import os, base64
import weasyprint
import time

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['DATABASE'] = "customer.db"
sec_key = base64.b64encode(os.urandom(64)).decode('utf-8')
app.config['SECRET_KEY'] = sec_key
# app.secret_key = sec_key

global customer, institute, data, ulogin, ilogin_, uCustomer
customer = CustomerHandler()
institute = InstituteHandler()
ulogin = ilogin_ = False
uCustomer = None

customer._log(sec_key)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index-p.html")

@app.route('/service')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

# User section
@app.route('/customer/Dashboard', methods=["POST", "GET"])
def uDashboard():
    if not ulogin:
        redirect(url_for("login"))

    if request.method == 'POST':
        usrFormData = customer.retriveCustomerData(user=session["user"])
        institute_list = list(customerFunc.getDataFromInstitute().values())
        jsonData = request.get_json()
        print(jsonData)
        if "search" in jsonData:
            search_term = jsonData["search"].lower()  # Convert search term to lowercase for case-insensitive search
            il = [i for i in institute_list if any(search_term in str(d).lower() for d in i.values())]
            # print(il)
            for i in il:
                i["addToInstituteLink"] = url_for('addToInstitute', iid=i['instituteID'])
            # print(il)
            return jsonify({"instituteList":il})
    usrFormData = customer.retriveCustomerData(user=session["user"])
    institute_list = list(customerFunc.getDataFromInstitute().values())
    customer._log(institute_list)
    return render_template('uDashboard.html', dat=usrFormData, instituteList=institute_list,  listLen = range(len(institute_list)))

@app.route("/customer/add-to-institute/<iid>")
def addToInstitute(iid):
    if customerFunc.sendDataToInstitute(iid, session["user"]):
        customer._log('adding to institute=> success')
        return redirect(url_for('uDashboard'))
    return redirect(url_for('uDashboard'))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        try:
            jsondata = request.get_json()
            if jsondata is None:
                return (jsonify({"error": "Invalid JSON"}), 400)

            a = customerFunc.logSig(jsondata)
            if a[0]:
                # return render_template('index.html')
                customer._log(a[2])
                session["user"] = a[2]
                session["user_view"]=a[2]
                ulogin = True
                customer._log(a[1])
                response_data = {
                    "success": True,
                    "template_name": url_for('uDashboard') if a[1] == "si" else url_for('formRender')
                }
                response = jsonify(response_data)
                return response, 200       
            else:
                return (jsonify({"error": "Login failed"}), 401)
        except Exception as e:
            return (jsonify({"error": str(e)}), 500)
    return render_template('s.html')

@app.route('/ToC')
def ToC():
    return render_template("ToC.html")

@app.route('/customer/form', methods=["POST", "GET"])
def formRender():
    if request.method == "POST":
        data = dict(request.form)
        if customer.toCustomerData(data, session["user"]):
            return redirect(url_for("uDashboard"))
    return render_template("uforms.html")



# Institute Section 

@app.route("/ilogin", methods=["POST", "GET"])
def ilogin():
    if request.method == "POST":
        try:
            jsondata = request.get_json()
            institute._log("Ive received the json data")
            if jsondata is None:
                return (jsonify({"error": "Invalid JSON"}), 400)
            institute._log("json data successfully checked")
            institute._log('Ive reached the data processing')
            a = instituteFunc.logSig(jsondata)
            institute._log(f'Ive processed the data and the response is {a}')
            if a[0]:
                print(a)
                session["instituteID"] = a[2]
                return redirect(url_for('iDashboard'))
            else:
                return (jsonify({"error": "Login failed"}), 401)
        except Exception as e:
            return (jsonify({"error": str(e)}), 500)
    return render_template('is.html')

@app.route('/institute/subscription')
def subscription():
    return render_template('subscription.html')

@app.route('/institute/Dashboard', methods=["POST", "GET"])
def iDashboard():
    if not ilogin:
        redirect(url_for("login"))

    if request.method == 'POST':
        jsonData = request.get_json()
        if jsonData["dataHead"] == "view":
            # print(jsonData["usrname"])
            data = customerFunc.getUserData(jsonData["usrname"])
            session["user_view"]=jsonData["usrname"]
            data = {"usrdata": data}
            # print(data)
            return (jsonify(data),200)

    uList = instituteFunc.patients(session["instituteID"])
    print(uList)
    return render_template("iDashboard.html", userList = uList, userLen=range(len(uList)))
    

@app.route('/institute/ToC')
def iToC():
    return render_template("iToC.html")


@app.route('/download/pdf/')
def pdf_download():
    # Retrieve the key from the URL query parameter
    k = session["user_view"]
    
    # Retrieve data based on the key
    a = customer.retriveCustomerData(k)
    
    # Generate the PDF and provide it for download
    html = render_template('pdf.html', dat=a)
    # with open('temp/htm/temp.html', 'w') as f:
    #     f.write(html)
    # with open('temp/htm/temp.html', 'r') as f:
    #     html = f.read()
    file = weasyprint.HTML(string=html)
    file.write_pdf(f'{os.getcwd()}/temp/{k}_formData.pdf')
    # return redirect(url_for('main'))
    return send_file(f'{os.getcwd()}/temp/{k}_formData.pdf')


if __name__ == "__main__":
    app.run(debug=True, port=5005)  