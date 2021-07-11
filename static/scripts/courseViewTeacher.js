// var announcements;
var isTeacher = true;

function removeNoti(params) {
    document.getElementById("noti").remove();
}

function showDiscription() {
    var annId = parseInt(event.target.id);
    // console.log(event.target.parentNode);
    var noti = document.createElement('div');
    noti.setAttribute("id", "noti");
    noti.classList.add('fullnotification');

    var notiPart = document.createElement('div');
    notiPart.classList.add('noti-part');

    var i = document.createElement("i");
    i.onclick = removeNoti;
    i.classList.add("fas");
    i.classList.add("fa-times");
    i.classList.add("close");

    var h1 = document.createElement('h1');
    h1.innerText = announcements[annId]["title"];

    var p = document.createElement("p");
    p.innerText = announcements[annId]["discription"];
    /* if (isTeacher) {
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("name", "edit");
        form.setAttribute("action", "");

        var FN = document.createElement("input");
        FN.setAttribute("type", "hidden");
        FN.setAttribute("name", "announcementId");
        FN.setAttribute("value", announcements[annId].pk);

        var s = document.createElement("button");
        s.setAttribute("type", "submit");
        s.innerText = "Edit"
    } */

    notiPart.appendChild(i);
    notiPart.appendChild(h1);
    notiPart.appendChild(p);
    noti.appendChild(notiPart);
    document.body.appendChild(noti);
}

function showAnouncement() {
    var allAnnDiv = document.getElementById("all-announcements");
    // announcements.appendChild()
    var k = 0;
    announcements.forEach(element => {
        var ann = document.createElement("DIV");
        ann.setAttribute("id", k + "-announcement");
        ann.classList.add("announcement");

        var annHead = document.createElement("DIV");
        annHead.classList.add("announcement-head");
        annHead.setAttribute("id", k + "-innerDiv");

        var h2 = document.createElement("H2");
        h2.setAttribute("id", k + "-h2");
        h2.innerText = element["title"];


        var sp = document.createElement("span");
        sp.setAttribute("id", k + "-span");
        var date = new Date(element["postedDate"])
        sp.innerText = date.getDate() + "/" + date.getMonth() + "/" + date.getFullYear();

        annHead.appendChild(h2);
        annHead.appendChild(sp);

        var p = document.createElement("p");
        p.setAttribute("id", k + "-para");
        p.innerText = element["discription"];
        p.classList.add("annu-disc");

        ann.appendChild(annHead);
        ann.appendChild(p);
        ann.onclick = showDiscription;


        allAnnDiv.appendChild(ann);
        k++;
    });
}



// creating notes and assignments

function createNotes() {
    document.querySelector(".create-notes").style.display = "block";
}

function cancelNotes(params) {
    document.querySelector(".create-notes").style.display = "none";
}

function createAssignment() {
    document.querySelector(".create-assignment").style.display = "block";
}

function cancelAssignment(params) {
    document.querySelector(".create-assignment").style.display = "none";
}

function showStudents(params) {
    document.querySelector(".studentsInfos").style.display = "block";
}

function cancelStudents(params) {
    document.querySelector(".studentsInfos").style.display = "none";
}

showAnouncement();