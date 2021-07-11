// var announcements;
var isTeacher = true;

/* announcements = [{
    'pk': '10',
    'fields': {
        'title': 'Notes of lesson 10',
        'datePosted': '19-01-2021',
        'discription': "As you guys copied in cie2 ill conduct quiz for individual Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, tenetur! Modi itaque nostrum, totam neque aliquam repellendus ipsam voluptas ad ducimus, odit ut, praesentium laborum esse qui iusto quae expedita."
    }
}, {
    'pk': '11',
    'fields': {
        'title': 'lets meet tomorrow',
        'datePosted': '29-01-2022',
        'discription': "As you guys copied in cie2 ill conduct quiz for individual Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, tenetur! Modi itaque nostrum, totam neque aliquam repellendus ipsam voluptas ad ducimus, odit ut, praesentium laborum esse qui iusto quae expedita."
    }
}, {
    'pk': '110',
    'fields': {
        'title': 'notes of lesson 10',
        'datePosted': '19-01-2022',
        'discription': "As you guys copied in cie2 ill conduct quiz for individual Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, tenetur! Modi itaque nostrum, totam neque aliquam repellendus ipsam voluptas ad ducimus, odit ut, praesentium laborum esse qui iusto quae expedita."
    }
}, {
    'pk': '110',
    'fields': {
        'title': 'notes of lesson 10',
        'datePosted': '19-01-2022',
        'discription': "As you guys copied in cie2 ill conduct quiz for individual Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, tenetur! Modi itaque nostrum, totam neque aliquam repellendus ipsam voluptas ad ducimus, odit ut, praesentium laborum esse qui iusto quae expedita."
    }
}, {
    'pk': '110',
    'fields': {
        'title': 'notes of lesson 10',
        'datePosted': '19-01-2022',
        'discription': "As you guys copied in cie2 ill conduct quiz for individual Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, tenetur! Modi itaque nostrum, totam neque aliquam repellendus ipsam voluptas ad ducimus, odit ut, praesentium laborum esse qui iusto quae expedita."
    }
}, ] */

function removeNoti(params) {
    document.getElementById("noti").remove();
}

function showAnnouncementDiscription() {
    var annId = parseInt(event.target.id);
    // console.log(annId, event.target.parentNode);
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

// function showAssignmentDiscription() {
//     var annId = parseInt(event.target.id);
//     // console.log(annId, event.target.parentNode);
//     var noti = document.createElement('div');
//     noti.setAttribute("id", "noti");
//     noti.classList.add('fullnotification');

//     var notiPart = document.createElement('div');
//     notiPart.classList.add('noti-part');

//     var i = document.createElement("i");
//     i.onclick = removeNoti;
//     i.classList.add("fas");
//     i.classList.add("fa-times");
//     i.classList.add("close");

//     var assignmentObj = assignment[annId];

//     var h1 = document.createElement('h1');
//     h1.innerText = assignmentObj.fields["title"];

//     var p = document.createElement("p");
//     p.innerText = assignmentObj.fields["discription"];

//     notiPart.appendChild(i);
//     notiPart.appendChild(h1);
//     notiPart.appendChild(p);
//     noti.appendChild(notiPart);

//     if (!assignmentObj.fields["submited"].submited) {
//         var form = document.createElement("form");
//         form.setAttribute("method", "post");
//         form.setAttribute("name", "edit");
//         form.setAttribute("action", "");

//         var FN = document.createElement("input");
//         FN.setAttribute("type", "hidden");
//         FN.setAttribute("name", "assId");
//         FN.setAttribute("value", assignment[annId].pk);

//         var txtarea = document.createElement("textarea");
//         txtarea.setAttribute("name", "ans");

//         var s = document.createElement("button");
//         s.setAttribute("type", "submit");
//         s.innerText = "submit"

//         form.appendChild(FN);
//         form.appendChild(txtarea);
//         form.appendChild(s);

//         noti.appendChild(form);
//     } else {
//         console.log("submited");
//     }

//     document.body.appendChild(noti);
// }

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
        ann.onclick = showAnnouncementDiscription;


        allAnnDiv.appendChild(ann);
        k++;
    });
}

/* 
function showAssignment() {
    var allAnnDiv = document.getElementById("all-assignment");
    // announcements.appendChild()
    var k = 0;
    assignment.forEach(element => {
        var ann = document.createElement("DIV");
        ann.setAttribute("id", k + "-announcement");
        ann.classList.add("announcement");

        var annHead = document.createElement("DIV");
        annHead.classList.add("announcement-head");
        annHead.setAttribute("id", k + "-innerDiv");

        var h2 = document.createElement("H2");
        h2.setAttribute("id", k + "-h2");
        h2.innerText = element.fields["title"];


        var sp = document.createElement("span");
        sp.setAttribute("id", k + "-span");
        sp.innerText = element.fields["datePosted"];

        annHead.appendChild(h2);
        annHead.appendChild(sp);

        var p = document.createElement("p");
        p.setAttribute("id", k + "-para");
        p.innerText = element.fields["discription"];
        p.classList.add("annu-disc");

        ann.appendChild(annHead);
        ann.appendChild(p);
        ann.onclick = showAssignmentDiscription;


        allAnnDiv.appendChild(ann);
        k++;
    });
} 
*/

showAnouncement();
// showAssignment();