from flask import  (Flask,
                    redirect,
                    render_template,
                    request,
                    session,
                    jsonify,
                    url_for,
                    json)
from datetime import datetime, timedelta
from bson.json_util import default, loads
from bson.objectid import ObjectId
import mongoAPI

app=Flask(__name__)
app.secret_key="secret key"

app.permanent_session_lifetime = timedelta(days=5)


@app.route('/')
def home():
   # todos 
   #if logged in as teacher
        #send his course
    #else if logged in as student 
        #send all his registered courses
    # else send all the course ordered by no of enrolments
    if "isTeacher" in session:
        courses = mongoAPI.getAllCourseSmallInfo()
        # print(courses[0]["teacherId"][0]["teacherName"])
        return render_template("mainPage.html", courses = courses)
        # return "logged in"+ session["id"]
    else:
        courses = mongoAPI.getAllCourseSmallInfo()
        # print(courses[0]["teacherId"][0]["teacherName"])
        return render_template("mainPage.html", courses = courses)
    return "true"


@app.route('/loginTeacher', methods = ['POST', 'GET'])
def loginTeacher():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["pass"]
        res = mongoAPI.authenticateTeacher(emailId=email,
                                        password=password)
        if(res["status"]):
            session["isTeacher"] = True
            session["id"] = str(res["id"])
            return render_template("login.html", error="logged in Successfully")
        else:
            return render_template("login.html", error="Wrong email or password")
    else:
        return render_template("login.html")
    # session["isTeacher"] = True
    # session["id"] = "60ced16a28ee6a510070bd86"
    # return "true"

@app.route('/loginStudent', methods = ['POST', 'GET'])
def loginStudent():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["pass"]
        res = mongoAPI.authenticateStudent(emailId=email,
                                        password=password)
        if(res["status"]):
            session["isTeacher"] = False
            session["id"] = str(res["id"])
            return render_template("login.html", error="logged in Successfully")
        else:
            return render_template("login.html", error="Wrong email or password")
    else:
        return render_template("login.html")
    # session["isTeacher"] = False
    # session["id"] = "60cf3ed5c8f9ccd0ab113ac7"
    # return "true"

@app.route('/logout')
def logout():
    session.pop("isTeacher")
    session.pop("id")
    return " "

@app.route('/addNotes', methods = ['POST'])
def addNotes():
    if request.method == 'POST':
        if "isTeacher" in session:
            courseId = request.form['courseId']
            if mongoAPI.checkIfTeacherTeachesCourse(session["id"], courseId):
                mongoAPI.addNotes(request.form['ass-titl'], request.form['ass-body'], courseId)
            return redirect(url_for('courseDetails', courseId = courseId))
        return redirect(url_for('loginTeacher', ))

@app.route('/addAssignment', methods = ['POST'])
def addAssignment():
    if request.method == 'POST':
        if "isTeacher" in session:
            courseId = request.form['courseId']
            date = datetime.strptime(request.form["ass-due"], '%Y-%m-%d')
            if mongoAPI.checkIfTeacherTeachesCourse(session["id"], courseId):
                mongoAPI.addAssignment(request.form['ass-titl'], 
                                        request.form['ass-body'],
                                        courseId,
                                        date)
            return redirect(url_for('courseDetails', courseId = courseId))
        return redirect(url_for('loginTeacher', ))

@app.route('/ansToAssignment', methods = ['POST'])
def ansToAssignment():
    if request.method == 'POST':
        if "isTeacher" in session:
            courseId = mongoAPI.getCourseIdOfAssignment(request.form["assignmentId"])
            if mongoAPI.checkIfStudentInCourse(courseId=courseId, studentId=session["id"]):
                mongoAPI.ansToAssignment(answeredBy=session["id"],
                                        courseId=courseId,
                                        assId=request.form["assignmentId"],
                                        answer=request.form["ans"])
    return redirect(url_for('courseDetails', courseId = courseId))

@app.route('/assignment/<string:assignmentId>')
def assignmentDetails(assignmentId):
    if "isTeacher" in session:
        courseId = mongoAPI.getCourseIdOfAssignment(assignmentId=assignmentId)
        if mongoAPI.checkIfTeacherTeachesCourse(session["id"], courseId):
            students = mongoAPI.getAllStudentsFrom(courseId=courseId)
            details = mongoAPI.getAssignmentInfoForTeacher(assignmentId)
            return render_template("assignmentTeacher.html",
                                    details = details[0], 
                                    students= students)
        elif mongoAPI.checkIfStudentInCourse(courseId=courseId, studentId=session["id"]):
            details = mongoAPI.getAssignmentInfoForStudent(assignmentId)
            return render_template("assignmentStudent.html",
                                    details = details[0])
    return "PERMISSION DENIED"



@app.route('/course/<string:courseId>')
def courseDetails(courseId):
    isEnrolled = False
    courseDetails = mongoAPI.getMoreInfoAbout(courseId)
    teacherId = courseDetails[0]["teacherId"][0]["_id"]
    otherCourses = mongoAPI.getAllCoursesOfTeacher(teacherId)
    relatedCourse = mongoAPI.getRelatedCourse(courseId)
    if "isTeacher" in session:
        if session["isTeacher"]:
            if mongoAPI.checkIfTeacherTeachesCourse(session["id"], courseId):
                assignmentDetails = mongoAPI.getAllAssignmentOfCourseShortInfo(courseId)
                notes = mongoAPI.getAllNotesOfCourse(courseId)
                notes =  json.dumps(notes)
                students = mongoAPI.getAllStudentsFrom(courseId=courseId)
                return render_template("courseViewTeacher.html",
                            students = students,
                            notes = notes,
                            assignments = assignmentDetails,
                            courseDetails = courseDetails, 
                            isEnrolled = isEnrolled,
                            otherCourses = otherCourses,
                            relatedCourses = relatedCourse)
        else:
            if(mongoAPI.checkIfStudentInCourse(courseId, session["id"])):
                assignmentDetails = mongoAPI.getAllAssignmentOfCourseShortInfo(courseId)
                notes = mongoAPI.getAllNotesOfCourse(courseId)
                notes =  json.dumps(notes)
                isEnrolled = True
                return render_template("courseView.html", 
                            notes = notes,
                            assignments = assignmentDetails,
                            courseDetails = courseDetails, 
                            isEnrolled = isEnrolled,
                            otherCourses = otherCourses,
                            relatedCourses = relatedCourse)        
    # print(otherCourses)
    return render_template("courseView.html", 
                            courseDetails = courseDetails, 
                            isEnrolled = isEnrolled,
                            otherCourses = otherCourses,
                            relatedCourses = relatedCourse)

if __name__=="__main__":
    app.run(debug=True)