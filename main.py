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
    if "isTeacher" in session:
        if session["isTeacher"]:
            courses = mongoAPI.getAllCoursesOfTeacher(session["id"])
            return render_template("mainPage.html", 
                                    courses = courses)
        else:
            courses = mongoAPI.getAllCourseOfStudent(session["id"])
            recomendedCourse = mongoAPI.getRecomendedCourse(session["id"])
            return render_template("mainPage.html", 
                                    courses = courses, 
                                    recomendedCourses = recomendedCourse)
    else:
        recomendedCourse = mongoAPI.getAllCourseSmallInfo()
        return render_template("mainPage.html", 
                                recomendedCourses = recomendedCourse)
    return "true"

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["pass"]
        who = request.form["who"]
        if(who == "teacher" ):
            res = mongoAPI.authenticateTeacher(emailId=email,
                                            password=password)
            if(res["status"]):
                session["isTeacher"] = True
                session["id"] = str(res["id"])
                return redirect(url_for('home'))
            else:
                return render_template("login.html", 
                                        error="Wrong email or password")
        else:
            res = mongoAPI.authenticateStudent(emailId=email,
                                        password=password)
            if(res["status"]):
                session["isTeacher"] = False
                session["id"] = str(res["id"])
                return redirect(url_for("home"))
            else:
                return render_template("login.html", 
                                        error="Wrong email or password")
    else:
        return render_template("login.html")

@app.route('/registerStudent', methods = ['POST', 'GET'])
def registerStudent():
    if request.method == 'POST':
        email = request.form["email"]
        name = request.form["name"]
        dob = request.form["dob"]
        gender = request.form["gender"] == "male"
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if( password1 == password2):
            res = mongoAPI.addStudent(name, datetime.strptime(dob, '%Y-%m-%d'), gender,email, password1)
            if(res[0]["status"]):
                session["isTeacher"] = False
                # print(res)
                session["id"] = str(res[0]["id"])
                return redirect(url_for('home'))
            else:
                stu = {"name":name,"dob": dob,"gender":gender,"password": password1, "email":""}
                return render_template("registerStudent.html", 
                                        error="Email already registered", 
                                        student = stu)
        else:
            stu = {"name":name,"dob": dob,"gender":gender,"password": "", "email":email}
            return render_template("registerStudent.html", 
                                    error="password didnt match", 
                                    student = stu)
    else:
        return render_template("registerStudent.html", student = {})

@app.route('/registerTeacher', methods = ['POST', 'GET'])
def registerTeacher():
    if request.method == 'POST':
        email = request.form["email"]
        name = request.form["name"]
        dob = request.form["dob"]
        gender = request.form["gender"] == "male"
        graduation = request.form["graduation"] 
        discription = request.form["discription"] 
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if( password1 == password2):
            res = mongoAPI.addTeacher(name,
                                    datetime.strptime(dob, '%Y-%m-%d'),
                                    gender, 
                                    graduation, 
                                    discription,
                                    email, 
                                    password1)

            if(res[0]["status"]):
                session["isTeacher"] = True
                session["id"] = str(res[0]["id"])
                return redirect(url_for('home'))
            else:
                teacher = {"name":name,
                            "dob": dob,
                            "gender":gender,
                            "password": password1,
                            "email":"", 
                            "graduation": graduation,
                            "discription": discription}
                return render_template("registerTeacher.html", 
                                        error="Email already registered",
                                        teacher = teacher)
        else:
            teacher = {"name":name,
                        "dob": dob,
                        "gender":gender,
                        "password": "",
                        "email":email, 
                        "graduation": graduation,
                        "discription": discription}
            return render_template("registerTeacher.html", 
                                    error="password didnt match",
                                    teacher = teacher)
    else:
        return render_template("registerTeacher.html", teacher={})

@app.route('/addCommentToAns', methods = ['POST', 'GET'])
def addCommentToAns():
    if request.method == 'POST':
        if "isTeacher" in session and session["isTeacher"]:
            assId = request.form["assId"]
            ansId = request.form["ansId"]
            comment = request.form["comment"]
            courseId = mongoAPI.getCourseIdOfAssignment(assignmentId=assId)
            if mongoAPI.checkIfTeacherTeachesCourse(session["id"], courseId):
                mongoAPI.gradeAssignment(assId,ansId, comment)
                return redirect(url_for('assignmentDetails', assignmentId=assId))
    return "Forbidden"

@app.route('/addCourse', methods = ['POST', 'GET'])
def addCourse():
    if request.method == 'POST':
        if "isTeacher" in session and session["isTeacher"]:
            cname = request.form["name"]
            discription = request.form["discription"]
            duration = request.form["duration"]
            tags = []
            tags.append(request.form["tag1"])
            tags.append(request.form["tag2"])
            tags.append(request.form["tag3"])
            res = mongoAPI.addCourse(session["id"], cname,discription, duration, tags)
            print(res)
            return redirect(url_for('courseDetails', courseId = res[0]["ObjectId"]))
        else:
            return redirect(url_for('login'))
    else:
        if "isTeacher" in session and session["isTeacher"]:
            lines = []
            with open('./templates/tags.txt') as f:
                lines = f.read().splitlines()
            return render_template("createCourse.html", tags=lines)
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop("isTeacher")
    session.pop("id")
    return redirect(url_for('home'))

@app.route('/addNotes', methods = ['POST'])
def addNotes():
    if request.method == 'POST':
        if "isTeacher" in session:
            courseId = request.form['courseId']
            if mongoAPI.checkIfTeacherTeachesCourse(session["id"], courseId):
                mongoAPI.addNotes(request.form['ass-titl'], request.form['ass-body'], courseId)
            return redirect(url_for('courseDetails', courseId = courseId))
        return redirect(url_for('login'))

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
        return redirect(url_for('login'))

@app.route('/enrollToCourse', methods = ['POST'])
def enrollToCourse():
    if request.method == 'POST':
        if "isTeacher" in session:
            courseId = request.form['courseId']
            if(mongoAPI.checkIfStudentExists(session["id"])):
                mongoAPI.addStudentToCourse(courseId, session["id"])
            return redirect(url_for('courseDetails', courseId = courseId))
        return redirect(url_for('login', ))

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
                                    students= students,
                                    assignmentId = assignmentId)
        elif mongoAPI.checkIfStudentInCourse(courseId=courseId, studentId=session["id"]):
            res = mongoAPI.getAnswer(session["id"], assignmentId)
            details = mongoAPI.getAssignmentInfoForStudent(assignmentId)
            if(res):
                return render_template("assignmentStudent.html",
                                        details = details[0],
                                        answers = res[0])
            else:
                return render_template("assignmentStudent.html",
                                        details = details[0],
                                        )
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