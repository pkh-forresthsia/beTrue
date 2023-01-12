let tabMap=[['overview','priceTable'],['month revenue','revenueTable']]

document.getElementById("defaultOpen").click();
document.getElementById("overlay").style.display = "none";
document.getElementById("loader").style.display = "none";

createAllContent()
for(let i=0;i<tabMap.length;i++){
    console.log(tabMap[i][1])
}

function createContent(tabName="overview",table='revenueTable',url="/table/") {
    loadingPage()
    let stockId = document.getElementById('stockId').value;
    console.log("print stock id",stockId)
    fetch(url+stockId).then(function (response) {
        return response.json()
    }).then(function (data) {

        data=JSON.parse(data[table]) 
        
        createTable(tabName,data)
        showPage()
    })
}
function createAllContent(){
    createContent()
    
    // revenueContent=JSON.parse(content['revenueTable']) 
    // createTable('month revenue',revenueContent)
    // createContent('month revenue','revenueTable')
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
    document.getElementById("overlay").style.display = "none";
}
function loadingPage(){
    document.getElementById("overlay").style.display = "block";
    document.getElementById("loader").style.display = "block"
}

function createTable(tabName,data){
    let tableContent=document.getElementById(tabName+" -table")
    tableContent.innerHTML=''
    let thead=document.createElement("thead")
    let theadTr=document.createElement("tr")
    let tbody=document.createElement("tbody")
    thead.appendChild(theadTr)
    tableContent.appendChild(thead)
    tableContent.appendChild(tbody)
    const okeys = Object.keys(data)
    const ovalues = Object.values(data)
    
    for (i=0;i<okeys.length;i++){
        let trTh=document.createElement('th')
        trTh.textContent=okeys[i]
        theadTr.appendChild(trTh)
    }
    for (i=0;i<Object.keys(ovalues[0]).length;i++){
        let tbodyTr=document.createElement('tr')
        tbody.appendChild(tbodyTr)
        for (j=0;j<okeys.length;j++){
            let trTd=document.createElement('td')
            trTd.textContent=ovalues[j][i]
            tbodyTr.appendChild(trTd)
        }
    }   
}
