let container = document.getElementById('container');

function toggle() {
    container.classList.toggle('sign-in');
    container.classList.toggle('sign-up');
}

setTimeout(() => {
    container.classList.add('sign-in');
}, 200);

function checkb() {
    if (document.getElementById("ToC").checked) {
        document.getElementById("su").disabled = false;
    } else {
        document.getElementById("su").disabled = true;
    }
}

async function isendData(name) {
    let jsonData = {
        dataHead: name,
        instituteID: "",
        instituteName: "",
        institute_email: "",
        pass: ""
    };

    if (name === "su") {
        jsonData.instituteID = document.getElementById("siid").value;
        jsonData.instituteName = document.getElementById('siname').value;
        jsonData.institute_email = document.getElementById("siemail").value;
        jsonData.pass = document.getElementById("spass").value;
    } else if (name === "si") {
        jsonData.instituteID = document.getElementById("iiid").value; // Use instituteID here
        jsonData.pass = document.getElementById("ipass").value;
    }

    jsonData = JSON.stringify(jsonData);

    try {
        const response = await fetch(
            "/ilogin",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: jsonData
            }
        );
    
        if (response.ok) {
            window.location.href = '/institute/Dashboard'
        } else {
            // Handle other response status codes (e.g., errors)
            console.error("Error:", response.statusText);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}
