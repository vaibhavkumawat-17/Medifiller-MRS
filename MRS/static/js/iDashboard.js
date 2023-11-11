var USER = null

async function sendandget(usrname) {
    if (document.getElementById("rp").hidden) {
        document.getElementById("rp").hidden = false;
    }

    let jsonData = {
        dataHead: "view",
        usrname: usrname
    }

    jsonData = JSON.stringify(jsonData);

    try {
        const response = await fetch(
            '/institute/Dashboard',
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: jsonData
            }
        );

        if (response.ok) {
            const responseData = await response.json();
            console.log(responseData);

            if (responseData && responseData.usrdata) {
                let data = responseData.usrdata;
                console.log(data);
                let keys = Object.keys(data);

                for (let i of keys) {  // Use 'for...of' loop to iterate over keys
                    let element = document.getElementById(i);
                    if (element) {
                        element.innerText = data[i];
                    }
                }
            }
        }
    } catch (error) {
        console.error("error: ", error);
    }
}

async function filter(){

}