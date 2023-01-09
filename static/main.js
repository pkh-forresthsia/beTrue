document.getElementById("defaultOpen").click();
document.getElementById("loader").style.display = "none";

function getSingleData() {
    document.getElementById("loader").style.display = "block"
    const stockIdElement = document.getElementById('stockId')
    const stockId = stockIdElement.value
    console.log("get form data", "/test/"+stockId)
    fetch("/test/"+stockId).then(function (response) {
        return response.json()
    }).then(function (data) {
        const okeys = Object.keys(data)
        // for (i=0;i<okeys.length;i++){

        // }
        console.log(okeys.length)
        firstOvalues = Object.values(data)[0]
        console.log(firstOvalues)
        console.log(Object.keys(firstOvalues).length)
        console.log(data)
        showPage()
    })
}

function openContent(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

function showPage() {
    document.getElementById("loader").style.display = "none";
    // document.getElementById("myDiv").style.display = "block";
}
