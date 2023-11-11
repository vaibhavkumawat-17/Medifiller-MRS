async function sendSearch() {
    let sh = document.getElementById("search").value;
    try{
        const response = await fetch(
            "/customer/Dashboard",
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body:JSON.stringify({search: sh})
            }
        );
        if (response.ok) {
            const responseData = await response.json(); // Parse the response JSON data
            const instituteList = responseData.instituteList; // Assuming the response contains an "instituteList" key
            // Now you have the updated institute list as a dictionary
            console.log(instituteList)
            // Create HTML content based on the instituteList (you can adapt this to your HTML structure)
            let htmlContent = '';
            for (const key in instituteList) {
                if (instituteList.hasOwnProperty(key)) {
                    const institute = instituteList[key];
                    // Build HTML content using the institute data, e.g., institute.instituteID, institute.instituteName
                    htmlContent += `
                        <div class="ui horizontal equal width segments">
                            <div class="ui segment">${institute.instituteID}</div>
                            <div class="ui segment">${institute.instituteName}</div>
                            <div class="ui segment"><a href="${institute.addToInstituteLink}">Add</a></div>
                        </div>
                    `;
                }
            }
        
            // Update the content within the "dashboard-content" div
            document.getElementById("dashboard-content").innerHTML = htmlContent;
        } else {
            console.error("Error:", responseData.error);
        }
    }
    catch (error) {
        console.error("Error", error)
    }
}    
