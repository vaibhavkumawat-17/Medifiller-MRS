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

async function sendData(name) {
    let jsonData = {
        dataHead: name,
        usrname: "",
        email: "",
        pass: ""
    };

    if (name === "su") {
        jsonData.usrname = document.getElementById("uuname").value;
        jsonData.email = document.getElementById("email").value;
        jsonData.pass = document.getElementById("upass").value;
    } else if (name === "si") {
        jsonData.usrname = document.getElementById("iuname").value;
        jsonData.pass = document.getElementById("ipass").value;
    }

    jsonData = JSON.stringify(jsonData);

    try {
        const response = await fetch(
            "/login",
            {
                method: "POST",
                headers: { "Content-Type": 'application/json' },
                body: jsonData
            }
        );

        if (response.ok) {
            const responseData = await response.json(); // Parse the JSON response
        
            if (responseData.success) {
                if (responseData.template_name) {
                    // Redirect to a URL that triggers rendering the specified template
                    window.location.href = responseData.template_name;
                } else {
                    console.log("No template name provided in response.");
                }
            } else {
                console.error("Error:", responseData.error);
            }
        } else {
            console.error("Error:", response.statusText);
        }
        
    } catch (error) {
        console.error('Error:', error);
    }
}
