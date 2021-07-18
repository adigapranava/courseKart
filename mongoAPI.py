from pymongo import MongoClient
from datetime import timedelta
from bson.json_util import dumps, loads
from datetime import datetime, date
from bson.objectid import ObjectId
import uuid
import json
import os


client=MongoClient(os.environ['mongoURL'])
db = client["courseManagementsDatabase"]
collTeacher = db["teacher"]
collCourse = db["course"]
collStudent = db["student"]
collAssignment = db["assignment"]

"""
# authenticationProcess
"""

def checkIfTeacherExists(teacherId):
    results = collTeacher.find({
        "_id": ObjectId(teacherId)
    })
    return len(list(results)) > 0

def checkIfStudentExists(studentId):
    results = collStudent.find({
        "_id": ObjectId(studentId)
    })
    return len(list(results)) >0

def checkIfEmailOfStudentExists(emailId):
    results = collStudent.find({
        "emailId": emailId
    })
    return len(list(results)) > 0

def checkIfTeacherTeachesCourse(teacherId, courseID):
    results = collCourse.find({
        "_id": ObjectId(courseID),
        "teacherId" : ObjectId(teacherId)
    })
    
    return len(list(results)) > 0

def checkIfEmailOfTeacherExists(emailId):
    results = collTeacher.find({
        "emailId": emailId
    })
    return len(list(results)) > 0

def authenticateTeacher(emailId, password):
    results = collTeacher.find({
        "emailId": emailId,
        "password": password
    })
    results = list(results)
    if(len(results)>0):
        return {"status": True, "id": results[0]["_id"]}
    else:
        return {"status": False, "id": results}

def authenticateStudent(emailId, password):
    results = collStudent.find({
        "emailId": emailId,
        "password": password
    })
    results = list(results)
    if(len(results)>0):
        return {"status": True, "id": results[0]["_id"]}
    else:
        return {"status": False, "id": results}

""" 
# adding users, courses
"""

def addTeacher(teacherName, dob, gender, graduation, discription, emailId, password):
    if( not checkIfEmailOfTeacherExists(emailId)):
        results = collTeacher.insert({
                    "teacherName": teacherName,
                    "dob": dob,
                    "gender": gender,
                    "graduation": graduation,
                    "discription": discription,
                    "ratings":3,
                    "emailId": emailId,
                    "password": password
                })
        return [{"status": True, "id": results}]
    else:
        return [{"status": False, "id": "emailAlreadyExists"}]

def addStudent(name, dob, gender, emailId, password):
    if( not checkIfEmailOfStudentExists(emailId)):
        results = collStudent.insert({
            "name":name,
            "dob": dob,
            "gender": gender,
            "emailId": emailId,
            "password": password
        })
        return [{"status": True, "id": results}]
    else:
        return [{"status": False, "id": "emailAlreadyExists"}]

def addCourse(teacherId, courseName, discription, duration, tags=[]):
    if(checkIfTeacherExists(teacherId)):
        results = collCourse.insert({
            "courseName": courseName,
            "strartDate": datetime.now(),
            "discription": discription,
            "duration": duration,
            "teacherId": ObjectId(teacherId),
            "tags": tags
        })
        return [{"status":True, "ObjectId": results}]
    else:
        return [{"status":False, "reason": "Invalid teacherId"}]

# if not already present then adds student
def addStudentToCourse(courseId, studentId):
    if(not checkIfStudentExists(studentId)):
        return [{"status": False, "reason": "invalid studentId"}]
    if( not checkIfStudentInCourse(courseId, studentId) ):
        results = collCourse.update(
            {"_id": ObjectId(courseId)},
            {"$push": {"students": ObjectId(studentId)}}
        )
        return list(results)
    else:
        return [{"status": False, "reason": "already present"}]

def addAssignment(title, discription, courseId, submitDate):
    results = collAssignment.insert({
                    "title": title, 
                    "courseId": ObjectId(courseId),
                    "discription": discription, 
                    "postedDate": datetime.now(),
                    "dueDate": submitDate
                })
    assigId = results 

    results = collCourse.update(
        {"_id": ObjectId(courseId)},
        {"$push": {
                "assignments": ObjectId(assigId)
            }
        }   
    )
    return list(results)

def addNotes(title, notes, courseId):
    results = collCourse.update(
        {"_id": ObjectId(courseId)},
        {"$push": {
            "notes": {
                "title": title, 
                "discription": notes, 
                "postedDate": datetime.now()
                }
            }
        }   
    )
    return list(results)

""" 
Student course Relations
"""
# returns true if present else false
def checkIfStudentInCourse(courseId, studentId):
    results = collCourse.find(
                {"_id": ObjectId(courseId)},
                {"students": 1}
                )
    results = list(results)
    try:
        studentsId =  results[0]["students"]
    except:
        studentsId = []
    if(ObjectId(studentId) in studentsId):
        # print("present")
        return True
    else:
        # print("Not Present")
        return False

# if present then removes 
def removeStudentFromCourse(courseId, studentId):
    if(checkIfStudentInCourse(courseId, studentId)):
        results = collCourse.update(
            {"_id": ObjectId(courseId)},
            {"$pull": {"students": ObjectId(studentId)}}
        )
        return list(results)
    else:
        return [{"status": "not present"}]

""" 
course Notes
"""
def getAllNotesOfCourse(courseId):
    results = collCourse.aggregate([
                {"$match": {"_id": ObjectId(courseId)}},
                {"$project": {"notes": 1}},
                ])
    results = list(results)
    try:
        notes =  results[0]["notes"]
    except:
        notes = []
    # print(notes)
    return notes

""" 
course assignment
"""
def getAssignmentInfoForTeacher(assignmentId):
    results = collAssignment.aggregate([
        {"$match": {"_id": ObjectId(assignmentId)}},
        {
            "$lookup":
                {
                    "from": "student",
                    "localField": "answers.answeredBy",
                    "foreignField": "_id",
                    "as": "studentInfo"
                }
        },
    ])
    
    return list(results)

def getAssignmentInfoForStudent(assignmentId):
    results = collAssignment.aggregate([
        {"$match": {"_id": ObjectId(assignmentId)}},
        {"$project": {"answers": 0}}
    ])
    
    return list(results)

def getAllAssignmentOfCourse(courseId):
    results = collCourse.aggregate([
                {"$match": {"_id": ObjectId(courseId)}},
                {"$project": {"assignments": 1,}
                }])
    results = list(results)
    try:
        notesIds =  results[0]["assignments"]
    except:
        notesIds = []

    # print(notesIds)
    results = collAssignment.find({
                '_id': {
                    '$in': notesIds
                }
                })
    notes = list(results)
    # print(notes)

    return notes

def getAllAssignmentOfCourseShortInfo(courseId):
    results = collCourse.aggregate([
                {"$match": {"_id": ObjectId(courseId)}},
                {"$project": {"assignments": 1,}
                }])
    results = list(results)
    try:
        notesIds =  results[0]["assignments"]
    except:
        notesIds = []

    # print(notesIds)
    results = collAssignment.find(
                {'_id': {'$in': notesIds}},
                {'title': 1,'discription':1, 'dueDate': 1, 'postedDate': 1, 'courseId':1}
                )
    notes = list(results)
    # print(notes)

    return notes

def ansToAssignment(answeredBy, courseId, assId, answer):
    if(not checkIfStudentInCourse(courseId, answeredBy)):
        return [{"status":False, "reason": "student not in course"}]
    elif( not checkIfAssignmentExit(courseId, assId)):
        return [{"status":False, "reason": "Assignment Does Not Exists"}]
    elif(checkIfAnswered(answeredBy, assId)):
        return [{"status":False, "reason": "Already answered"}]
    else:
        results = collAssignment.update(
            {"_id": ObjectId(assId)},
            {"$push":{
                "answers": {
                    "answeredBy": ObjectId(answeredBy),
                    "answer": answer,
                    "submitedDate": datetime.now() 
                    }
                }
            }
        )
        return results

def checkIfAnswered(answeredBy, assId):
    results = collAssignment.find({
                "_id": ObjectId(assId),
                "answers.answeredBy": {"$in": [ObjectId(answeredBy)]}
    })
    answers = list(results)
    # print(answers)
    return len(answers)> 0

def getAnswer(answeredBy, assId):
    results = collAssignment.find({
                "_id": ObjectId(assId),
                "answers.answeredBy": {"$in": [ObjectId(answeredBy)]}
            },{
                "answers": {"$elemMatch": {"answeredBy": ObjectId(answeredBy)}}
            })
    answers = list(results)
    # print(answers)
    if len(answers)> 0:
        return answers
    else:
        return False

def gradeAssignment(assId, ansPos, comment):
    results = collAssignment.update({
        "_id": ObjectId(assId),
        },{
            "$set": {"answers."+str(ansPos)+".teachersComment": comment}
        })
    return list(results)

def checkIfAssignmentExit(courseId, assId):
    results = collCourse.find({
        "_id": ObjectId(courseId),
        "assignments":{ "$in": [ObjectId(assId)]}
    })

    course = list(results)
    return len(course) > 0



"""
  get details about courses
"""

def getCourseIdOfAssignment(assignmentId):
    results = collAssignment.find(
        {"_id":ObjectId(assignmentId)},
        {"courseId": 1}
    )
    return list(results)[0]["courseId"]

def getMoreInfoAbout(courseId):
    results = collCourse.aggregate([
        {"$match": {"_id": ObjectId(courseId)}},
        # joining teacher and course
        { "$lookup": {  
            "from": "teacher", 
            "localField": "teacherId", 
            "foreignField": "_id", 
            "as": "teacherId" }}, 
    ])
    return list(results)

def getRecomendedCourse(studentId):
    # get all courses with tags of student
    results = collCourse.find(
        {"students": {"$in": [ObjectId(studentId)]}},
        {"tags":1}
    )
    coursesWithTags = list(results)

    allCourses = list()
    allCoursesTags = list()

    for course in coursesWithTags:
        allCourses.append(course["_id"])
        allCoursesTags += course["tags"]
    
    # ordering the most common tags
    tags = dict()
    for tag in allCoursesTags:
        tags[tag] = tags.get(tag, 0) + 1
    tags = dict(sorted(tags.items(), key=lambda x: x[1], reverse=True))
    tags = list(tags.keys())

    results = getAllCoursesHavingTags(tags, allCourses)
    if not results:
        results = getAllCourseSmallInfo()[:10]
    return results

def getRelatedCourse(courseId):
    results = collCourse.find(
        {"_id": ObjectId(courseId)},
        {"tags":1}
    )
    coursesWithTags = list(results)
    tags = coursesWithTags[0]["tags"]
    return getAllCoursesHavingTags(tags, [ObjectId(courseId)])

def getAllCoursesHavingTags(tags, exceptCourses = []):
    # print(tags, exceptCourses)
    recomendedCourse = list()
    for tag in tags: 
        results = collCourse.aggregate([
            {"$match": {
                "$and": [
                {"tags": {"$in": [tag]}},
                {"_id": {"$nin": exceptCourses}}]
            }},
             # joining teacher and course
            { "$lookup": {  
                "from": "teacher", 
                "localField": "teacherId", 
                "foreignField": "_id", 
                "as": "teacherId" }}, 
            # adding new field total number of Students
            { "$addFields":{
                "numberOfStudents": {
                    "$cond": { "if": { "$isArray": "$students"}, "then": { "$size": "$students"},"else": 0 
                } }}}, 
            # sorting in desanding order of number of students
            {"$sort": {
                "numberOfStudents": -1}} , 
            # selecting only the nessaryinfo
            {"$project": { "courseName": 1, "teacherId.teacherName": 1, "numberOfStudents": 1}}
        ])
        recomendedCourse += list(results)
    res = []
    for i in recomendedCourse:
        if i not in res:
            res.append(i)
    return res

# returns all students from Course
def getAllStudentsFrom(courseId):
    results = collCourse.find(
                {"_id": ObjectId(courseId)},
                {"students": 1}
                )
    results = list(results)
    try:
        studentsId =  results[0]["students"]
    except:
        studentsId = []
    
    results = collStudent.aggregate([
        {"$match": {"_id": {"$in": studentsId}}},
        {"$project":{"name":1, "gender": 1}}
    ])

    return list(results)

# all courses of Student
def getAllCourseOfStudent(studentId, onlyCourseId=False):
    if(not onlyCourseId):
        results = collCourse.aggregate([
                {"$match": {"students": {"$in": [ObjectId(studentId)]}}},
                { "$lookup": { 
                    "from": "teacher", 
                    "localField": "teacherId", 
                    "foreignField": "_id", 
                    "as": "teacherId" }},
                {"$sort": {
                    "startDate": 1}},
                {"$project": { "courseName": 1, "teacherId.teacherName": 1}}
        ])
        return list(results)
    else:
        results = collCourse.aggregate([
                {"$match": {"students": {"$in": [ObjectId(studentId)]}}},
                {"$sort": {
                    "startDate": 1}},
                {"$project": { "_id":1}}
        ])
        results = list(results)
        courseIds = list()
        for item in results:
            courseIds.append(item["_id"])
        return courseIds

# all courses of teacher
def getAllCoursesOfTeacher(teacherId, onlyCourseId=False):
    if(not onlyCourseId):
        results = collCourse.aggregate([
                {"$match": {"teacherId": ObjectId(teacherId)}},
                { "$lookup": { 
                    "from": "teacher", 
                    "localField": "teacherId", 
                    "foreignField": "_id", 
                    "as": "teacherId" }},
                {"$sort": {
                    "startDate": 1}},
                {"$project": { "courseName": 1, "teacherId.teacherName": 1}}
        ])
        return list(results)
    else:
        results = collCourse.aggregate([
                {"$match": {"teacherId": ObjectId(teacherId)}},
                {"$sort": {
                    "startDate": 1}},
                {"$project": { "_id":1}}
        ])
        results = list(results)
        courseIds = list()
        for item in results:
            courseIds.append(item["_id"])
        return courseIds

# returns all courses ordered by no of enrolles
def getAllCourse():
    results = collCourse.aggregate([ 
        { "$addFields":{ "numberOfStudents": {"$cond": {"if": { "$isArray": "$students"}, "then": { "$size": "$students"},"else": 0 } }}},
        {"$sort": {"numberOfStudents": -1}} 
    ])
    return list(results)

# returns all courses ordered by no of enrolles joined with teacher
def getAllCourseWithTeacher():
    results = collCourse.aggregate([
        { "$lookup": { 
            "from": "teacher", 
            "localField": "teacherId", 
            "foreignField": "_id", 
            "as": "teacherId" }},
        { "$addFields":{ 
            "numberOfStudents": {"$cond": {"if": { "$isArray": "$students"}, "then": { "$size": "$students"},"else": 0 } }}},
        {"$sort": {
            "numberOfStudents": -1}}
    ])

    return list(results)

# returns all courses small details with teacher
def getAllCourseSmallInfo(exceptCourses=[]):
    results  = db.course.aggregate([
        {"$match": {"_id": {"$nin": exceptCourses}}},
        # joining teacher and course
        { "$lookup": {  
            "from": "teacher", 
            "localField": "teacherId", 
            "foreignField": "_id", 
            "as": "teacherId" }}, 
        # adding new field total number of Students
        { "$addFields":{
            "numberOfStudents": {
                "$cond": { "if": { "$isArray": "$students"}, "then": { "$size": "$students"},"else": 0 
            } }}}, 
        # sorting in desanding order of number of students
        {"$sort": {
            "numberOfStudents": -1}} , 
        # selecting only the nessaryinfo
        {"$project": { "courseName": 1, "teacherId.teacherName": 1, "numberOfStudents": 1}}
        ])
    return list(results)

if __name__=="__main__":
    # print(getAllStudentsFrom("60d206dde32e15d5bceb005f"))
    # print(getAllStudentsFrom("60cedb8575025b75ea97b245"))
    a = datetime(2021, 10, 23)
    # addAssignment("test headder", "test discription", "60cedb8575025b75ea97b245", a)
    # print(getAllAssignmentOfCourseShortInfo("60cedb8575025b75ea97b245"))
    # print(checkIfAssignmentExit("60cedb8575025b75ea97b245", "60d36dbf7e4d0e6d13652e35"))
    # print(ansToAssignment("60cf3ed5c8f9ccd0ab113ac7","60cedb8575025b75ea97b245", 0, "Test answer"))
    # checkIfAnswered("60cf3ed5c8f9ccd0ab113ac7", "60cedb8575025b75ea97b245")
    # print(ansToAssignment("60cf48886cec4d85043f8a0e","60cedb8575025b75ea97b245","60d36dbf7e4d0e6d13652e35","test answers"))
    # print(getAllAssignmentOfCourse("60cedb8575025b75ea97b245"))
    # print(getAllAssignmentOfCourseShortInfo("60cedb8575025b75ea97b245"))
    # print(getAllCourseSmallInfo([ObjectId("60cedb8575025b75ea97b245")]))
    # print(getAllCourseWithTeacherOfStudent("60cf3ed5c8f9ccd0ab113ac7"))
    # print(getAllCoursesHavingTags(["business","computerScience","programming"]))
    # print()
    # print(getRecomendedCourse("60cf3ed5c8f9ccd0ab113ac7"))
    # print(getAllCourseOfStudent("60cf3ed5c8f9ccd0ab113ac7", True))
    # print(getAllCoursesOfTeacher("60ced49128ee6a510070bd88", True))
    # print(checkIfTeacherExists("60ced49128ee6a510070bd88"))
    # print(addCourse("60ced49128ee6a510070bd88", "test Course","this is tes course discription", "3", ["computerScience", "social"]))
    # print(authenticateTeacher("modi@gmail.com", "passaword"))
    # print(addStudent("testStudent",a,True,"test@gmail.com","testpassword"))
    # print(addTeacher("testStudent",a,True,"TEST", "discription","test@gmail.com","testpassword"))
    # print(getMoreInfoAbout("60ced6d475025b75ea97b244"))
    # print(getRelatedCourse("60ced6d475025b75ea97b244"))
    # getCourseIdOfAssignment("60d71042c55fe1b8a8c780d7")
    # print(ansToAssignment("60cf3ed5c8f9ccd0ab113ac7","60d01576780e9ccb770b1200","60d72ed33e42f33bbefbc112", "Test Ans"))
    # print(getAssignmentInfoForStudent("60d72ed33e42f33bbefbc112"))
    # getAnswer("60eacce25bb948228b253809", "60eacd395bb948228b25380a")
    # print(getRecomendedCourse("60f26bf1fe9fc2ad5d5bc627"))
    # print(getAllCourseOfStudent("60cf3ed5c8f9ccd0ab113ac7"))
    # print(gradeAssignment("60d36dbf7e4d0e6d13652e35", 10, "good"))
