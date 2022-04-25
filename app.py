from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import pairing_algorithm_v3

app = Flask(__name__)

# Connection to MySQL Server and Database
app.config['MYSQL_HOST'] = 'web.ecc.iwcc.edu'
app.config['MYSQL_USER'] = 'gtuser'
app.config['MYSQL_PASSWORD'] = 'XQ*JDGgk2jJ7C*sy'
app.config['MYSQL_DB'] = 'gt_db'

#global variables
table_rows = []
class_id = ""
mysql = MySQL(app)
user_id = 1
originalRoster = []
last_assignment = 0


@app.route('/')
def index():
    return render_template('index.html', partner_options=printResults(), user_info=getUser(), user_info_dash=getUserDash())


@app.route('/howToUse')
def howToUse():
    return render_template('howToUse.html', partner_options=printResults(), user_info=getUser(), user_info_dash=getUserDash())

@app.route('/aboutPairProgramming')
def aboutPairProgramming():
    return render_template('aboutPairProgramming.html', partner_options=printResults(), user_info=getUser(), user_info_dash=getUserDash())


@app.route('/form')
def form():
    return render_template('form.html', partner_options=printResults(), user_info=getUser())


@app.route('/selectClass')
def selectClass():
    cancelButton = '<button onclick="window.location.replace(\'/\');" style="background-color: rgba(220, 20, 60, 0.157); color: crimson; position: relative;  margin-top: 10px;">Cancel</button>'
    return render_template('selectClass.html', user_info=getUser(), class_options=getClasses(), cancel_button=cancelButton)
    # return render_template('selectClass.html', student_table = generateClassTable(class_id), user_info = getUser(), class_options = getClasses(), save_button = "<button>Save</button>")


@app.route('/groupHistory')
def groupHistory():
    okayButton = '<button onclick="window.location.replace(\'/\');" style="color: orangered; background-color: rgba(255, 68, 0, 0.158); position: relative; margin-top: 10px;">Back to dashboard</button>'
    return render_template('groupHistory.html', okay_button=okayButton)


@app.route('/list')
def doList():
    cursor = mysql.connection.cursor()
    #cursor.execute("SELECT student_id,first_name,last_name,gender,coding_level,preferred_partner FROM students")
    cursor.execute("SELECT s.student_id, s.first_name, s.last_name, s.gender, s.coding_level, s.preferred_partner FROM teachers t JOIN classes c  ON t.teacher_id = c.teacher_id JOIN students_classes sc ON sc.class_id = c.class_id JOIN students s ON sc.student_id = s.student_id WHERE t.teacher_id = '" + str(user_id) + "'")
    global table_rows
    table_rows = cursor.fetchall()
    cursor.close()
    student_table = "<table><tr><th colspan=1>Name</th><th>Gender</th><th>Coding Level</th><th>Preferred Partner</th><th></th></tr>"
    partner_id = []
    partner_fname = []
    partner_lname = []
    x = 0
    for y in table_rows:
        partner_id.append(y[5])
        partner_fname.append(y[1])
        partner_lname.append(y[2])
        # print(y[5])
        #print(y[1] + " " + y[2])
        x = x + 1
    for i in table_rows:
        if int(i[4]) < 2:
            coding_level = "Beginner"
        elif int(i[4]) < 5:
            coding_level = "Intermediate"
        else:
            coding_level = "Expert"
        current_partner = "none"
        if i[5] in partner_id and i[5] != 0:
            current_partner = partner_fname[i[5] -
                                            1] + " " + partner_lname[i[5] - 1]
        student_table += '<tr>' + '<td style="width:200px;"><input type="checkbox" name="add" value=' + str(i[0]) + '>' + str(i[1]) + ' ' + str(i[2]) + '</td><td>' + str(i[3]) + '</td><td>' + coding_level + '</td><td>' + str(
            current_partner) + '</td><td class="editContainer"><a href="/form?student_id=' + str(i[0]) + '&gender=' + str(i[3]) + '&coding_level=' + str(i[4]) + '&preferred_partner=' + str(i[5]) + '" class="editLink"><img src="../editIcon.png" title="Edit" alt="Edit"></a></td><tr>'
    student_table += "</table>"
    # print(student_table)
    # return "test"
    return render_template('list.html', student_table=student_table, user_info=getUser(), class_options=getClasses())


@app.route('/selectClass1', methods=['POST', 'GET'])
def login():
    # if request.method == 'GET':
    # return "Login via the login Form"

    if request.method == 'POST':
        student_id = request.form['studentId']
        gender = request.form['gender']
        coding_level = request.form['codingLevel']
        preferred_partner = request.form['preferredPartner']
        cursor = mysql.connection.cursor()
        #cursor.execute("INSERT INTO students (first_name,last_name,gender,coding_level,preferred_partner) VALUES (%s,%s,%s,%s,%s)",(first_name,last_name,gender,coding_level,preferred_partner))
        cursor.execute("UPDATE students SET gender = '" +
                       gender + "' WHERE student_id = '" + student_id + "'")
        mysql.connection.commit()
        cursor.execute("UPDATE students_classes SET coding_level = '" + coding_level + "', preferred_partner = '" +
                       preferred_partner + "' WHERE student_id = '" + student_id + "' and class_id = '" + class_id + "'")
        mysql.connection.commit()
        cursor.close()
        #okayButton = '<button onclick="window.location.replace(\'/\');" style="position: relative; bottom: 22px; left: 100px;">Okay</button>'
        okayButton = '<button onclick="window.location.replace(\'/\');" style="color: orangered; background-color: rgba(255, 68, 0, 0.158); position: relative; margin-top: 10px;">Back to dashboard</button>'
        return render_template('selectClass.html', student_table=generateClassTable(class_id), user_info=getUser(), class_options=getClasses(), save_button="<button>Update Class</button>", okay_button=okayButton)

    return printResults()


@app.route('/selectClass', methods=['POST', 'GET'])
def doSelectClass():
    global class_id
    class_id = request.form['classId']
    #okayButton = '<button onclick="window.location.replace(\'/\');" style="position: relative; bottom: 22px; left: 100px;">Okay</button>'
    okayButton = '<button onclick="window.location.replace(\'/\');" style=" color: orangered; background-color: rgba(255, 68, 0, 0.158); position: relative; margin-top: 10px;">Back to dashboard</button>'
    return render_template('selectClass.html', student_table=generateClassTable(class_id), user_info=getUser(), class_options=getClasses(), save_button="<button>Update Class</button>", okay_button=okayButton)


def generateClassTable(class_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT class_name FROM classes WHERE class_id ='" + class_id + "'")
    class_name = cursor.fetchone()
    cursor.execute("SELECT s.student_id, s.first_name, s.last_name, s.gender, s.coding_level, s.preferred_partner FROM students s JOIN students_teachers st ON s.student_id = st.student_id JOIN teachers t ON st.teacher_id = t.teacher_id WHERE st.teacher_id = '" + str(user_id) + "' ORDER BY s.last_name ASC")
    global table_rows
    table_rows = cursor.fetchall()
    cursor.execute("SELECT s.student_id, s.first_name, s.last_name, s.gender, sc.coding_level, sc.preferred_partner FROM teachers t JOIN classes c ON t.teacher_id = c.teacher_id JOIN students_classes sc ON sc.class_id = c.class_id JOIN students s ON sc.student_id = s.student_id WHERE c.class_id = '" + class_id + "' ORDER BY s.last_name ASC")
    current_students = cursor.fetchall()
    cursor.close()
    student_table = '<table> <tr> <td colspan=2>' + \
        class_name[0] + \
        ' class roster:<br><span class="font70">(Uncheck to remove students)</span></td> <th></th></tr>'
    roster = []
    for z in current_students:
        roster.append(z[0])
    currentStudentCount = 0
    for i in current_students:
        student_table += '<tr> <td style="text-align: center; width: 30px;"><input checked type="checkbox" name="addStudent" value=' + str(i[0]) + '></td><td>' + str(i[1]) + ' ' + str(i[2]) + '</td><td class="editContainer"><a href="/form?student_id=' + str(i[0]) + '&gender=' + str(
            i[3]) + '&coding_level=' + str(i[4]) + '&preferred_partner=' + str(i[5]) + '&class_name=' + class_name[0] + '&class_id=' + class_id + '&student_entry=false" class="editLink"><img width="13" src="static/editIcon.png" title="Edit" alt="Edit"></a></td></tr>'
        currentStudentCount = currentStudentCount + 1
    if currentStudentCount == 0:
        student_table += '<tr><td colspan="2"><span class="font70">None</span></td><td></td></tr>'
    student_table += "</table>"
    student_table += '<table><tr><td colspan=2>Your students currently not in this class:<br><span class="font70">(check to add students)</span></td></tr>'
    otherStudentCount = 0
    for i in table_rows:
        if i[0] not in roster:
            student_table += '<tr><td style="text-align: center; width: 30px;"><input type="checkbox" name="addStudent" value=' + \
                str(i[0]) + '></td><td>' + str(i[1]) + \
                ' ' + str(i[2]) + '</td></tr>'
            otherStudentCount = otherStudentCount + 1
    if otherStudentCount == 0:
        student_table += '<tr><td colspan="2"><span class="font70">None</span></td><td></td></tr>'
    student_table += "</table>"
    return student_table


@app.route('/updateClass', methods=['POST', 'GET'])
def updateClass():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT student_id from students_classes WHERE class_id='" + class_id + "'")
    global originalRoster
    originalRoster = []
    fromDb = cursor.fetchall()
    print(fromDb)
    for vv in fromDb:
        originalRoster.append(vv[0])
    print(originalRoster)
    delete_students = []
    fromForm = request.form.getlist('addStudent')
    print(fromForm)
    add_student = []
    for ww in fromForm:
        add_student.append(int(ww))
    originalRosterList = []
    insertList = []
    for xx in originalRoster:
        originalRosterList.append(int(xx))
    for yy in add_student:
        print(yy)
        print(originalRosterList)
        if int(yy) not in originalRosterList:
            insertList.append(int(yy))

    # print(originalRosterList)
    # print(add_student)
    # print(insertList)

    for x in originalRosterList:
        if int(x) not in add_student:
            print("Delete:")
            print(x)
            cursor.execute("DELETE FROM students_classes WHERE class_id='" +
                           str(class_id) + "' AND student_id='" + str(x) + "'")
            mysql.connection.commit()
    for y in insertList:
        print("Insert:")
        print(y)
        cursor.execute("INSERT INTO students_classes VALUES ('" +
                       str(class_id) + "', '" + str(y) + "', 0, 0)")
        mysql.connection.commit()
    cursor.close()
    okayButton = '<button onclick="window.location.replace(\'/\');" style="color: orangered; background-color: rgba(255, 68, 0, 0.158); position: relative;  margin-top: 10px;"">Back to dashboard</button>'
    return render_template('selectClass.html', student_table=generateClassTable(class_id), user_info=getUser(), class_options=getClasses(), save_button="<button>Update Class</button>", okay_button=okayButton)


def getStudents(class_id):
    return class_id


def printResults():
    cursor = mysql.connection.cursor()
    #cursor.execute("SELECT student_id,first_name,last_name FROM students")
    cursor.execute("SELECT s.student_id,s.first_name,s.last_name FROM students s JOIN students_classes sc ON s.student_id = sc.student_id WHERE class_id = '" + class_id + "'")
    global table_rows
    table_rows = cursor.fetchall()
    cursor.close()
    aString = ""
    for i in table_rows:
        aString += "<option value=" + \
            str(i[0]) + ">" + str(i[1]) + " " + str(i[2]) + "</option>"
    return f"{aString}"


def getUser():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT prefix, first_name, last_name FROM teachers WHERE teacher_id = " + str(user_id))
    record = cursor.fetchone()
    cursor.close()
    return record[1] + " " + record[2]


def getUserDash():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT prefix, first_name, last_name FROM teachers WHERE teacher_id = " + str(user_id))
    record = cursor.fetchone()
    cursor.close()
    return record[0] + " " + record[2]


def getClasses():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT class_id, class_name FROM teachers t JOIN classes c ON t.teacher_id = c.teacher_id WHERE t.teacher_id = " + str(user_id))
    option_rows = cursor.fetchall()
    cursor.close()
    global class_id
    aString = '<select required name="classId" id="classSelect">'
    for i in option_rows:
        if str(class_id) == str(i[0]):
            aString += "<option selected value=" + \
                str(i[0]) + ">" + str(i[1]) + "</option>"
        else:
            aString += "<option value=" + \
                str(i[0]) + ">" + str(i[1]) + "</option>"
    aString += '</select>'
    #aString += ' <button>Select Class</button>'
    return f"{aString}"


@app.route('/createAssignment')
def createAssignment():
    cancelButton = '<button onclick="window.location.replace(\'/\');" style=" background-color: rgba(220, 20, 60, 0.157); color: crimson; position: relative;  margin-top: 10px;">Cancel</button>'
    return render_template('createAssignment.html', user_info=getUser(), class_options=getClasses(), cancel_button=cancelButton)


@app.route('/createGroups', methods=['POST', 'GET'])
def createGroups():
    class_id = request.form['classId']
    assignment_title = request.form['assignmentTitle']
    assignment_description = request.form['assignmentDescription']
    hiddenFields = '<div id="breadCrumb" style="font-size: 12px;"><a href="#" onclick="window.history.back()">Step 1</a> > Step 2</div>'
    hiddenFields += '<input type="hidden" name="classId" value="' + class_id + '">'
    hiddenFields += '<input type="hidden" name="assignmentTitle" value="' + \
        assignment_title + '">'
    hiddenFields += '<input type="hidden" name="assignmentDescription" value="' + \
        assignment_description + '">'
    showAssignmentTitle = "Activity: " + assignment_title
    cancelButton = '<button onclick="window.location.replace(\'/\');" style=" background-color: rgba(220, 20, 60, 0.157); color: crimson; position: relative;  margin-top: 10px;">Cancel</button>'

    return render_template('createGroups.html', user_info=getUser(), class_options=getClasses(), hidden_fields=hiddenFields, show_assignment_title=showAssignmentTitle, cancel_button=cancelButton)


@app.route('/showGroups', methods=['POST', 'GET'])
def showGroups():
    classId = request.form['classId']
    assignmentTitle = request.form['assignmentTitle']
    assignmentDescription = request.form['assignmentDescription']
    groupCriteria = request.form.getlist('criteria')

    hiddenAssignmentFields = '<input type="hidden" name="assignmentTitle" value="' + \
        assignmentTitle + '">'
    hiddenAssignmentFields += '<input type="hidden" name="assignmentDescription" value="' + \
        assignmentDescription + '">'
    hiddenAssignmentFields += '<input type="hidden" name="teacher_id" value="' + \
        str(user_id) + '">'
    hiddenAssignmentFields += '<input type="hidden" name="classId" value="' + \
        str(classId) + '">'

    hiddenCriteriaFields = ''
    for gc in groupCriteria:
        hiddenCriteriaFields += '<input type="hidden" value="' + gc + '" name="criteria">'

    print(hiddenAssignmentFields)
    print(hiddenCriteriaFields)

    print("Criteria below")
    print(groupCriteria)

    if '1' in groupCriteria:
        isGenderImportant = True
    else:
        isGenderImportant = False

    if '2' in groupCriteria:
        isAbilityImportant = True
    else:
        isAbilityImportant = False

    if '3' in groupCriteria:
        isPreferenceImportant = True
    else:
        isPreferenceImportant = False

    print(isGenderImportant)
    print(isAbilityImportant)
    print(isPreferenceImportant)

    finalList = pairing_algorithm_v3.group(getStudentList(
        classId), isGenderImportant, isAbilityImportant, isPreferenceImportant)
    #tableGroupsDisplay = '<table id="groupsTable"><tr class="topRow"><th colspan=3 style="text-align: left;">Generated Groups</th>'
    tableGroupsDisplay = '<table id="groupsTable">'

    groupDisplayNum = 1

    hiddenStudentFields = ''

    for x in finalList:
        tableGroupsDisplay += "<tr><td>Group " + str(groupDisplayNum) + "</td>"
        # last_assignment
        for y in x:
            hiddenStudentFields += '<input type="hidden" name="gs" value="' + \
                str(groupDisplayNum) + '|' + str(y[1]) + '">'
            tableGroupsDisplay += "<td>" + str(y[0]) + "</td>"
        tableGroupsDisplay += "</tr>"
        groupDisplayNum = groupDisplayNum + 1
    tableGroupsDisplay += "</table>"
    tableGroupsDisplay += '<table class="criteriaKey">'
    tableGroupsDisplay += "<tr><th>Grouped based on:</th></tr>"
    if isGenderImportant:
        tableGroupsDisplay += "<tr><td>Gender</td></tr>"
    if isAbilityImportant:
        tableGroupsDisplay += "<tr><td>Skill Level</td></tr>"
    if isPreferenceImportant:
        tableGroupsDisplay += "<tr><td>Preferred Partner</td></tr>"
    tableGroupsDisplay += "</table>"

    print(hiddenStudentFields)
    return render_template('showGroups.html', assignmentTitle=assignmentTitle, assignmentDescription=assignmentDescription, tableGroupsDisplay=tableGroupsDisplay, hiddenAssignmentFields=hiddenAssignmentFields, hiddenCriteriaFields=hiddenCriteriaFields, hiddenStudentFields=hiddenStudentFields)


def getStudentList(classId):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT CONCAT_WS(' ',s.first_name,s.last_name), s.student_id, s.gender, sc.coding_level FROM students s JOIN students_classes sc ON s.student_id = sc.student_id where class_id = '" + classId + "'")
    records = cursor.fetchall()
    cursor.execute(
        "SELECT assignment_id FROM assignments ORDER BY assignment_id DESC LIMIT 1;")
    global last_assignment
    last_assignment = cursor.fetchone()
    last_assignment = last_assignment[0]

    # print(records)
    student_list = []
    for x in records:
        student_list.append(list(x))

    for i in range(len(student_list)):
        # get current student id
        id = student_list[i][1]
        sqlStatement = "SELECT group_id from student_groups WHERE student_id='" + \
            str(id) + "'  and assignment_id >= '" + \
            str(int(last_assignment) - 2) + "'"
        # print(sqlStatement)
        cursor.execute(sqlStatement)
        previousGroups = cursor.fetchall()
        # print(previousGroups[0][0])
        # print(previousGroups[1][0])
        if len(previousGroups) < 2:
            student_list[i].append(0)
            student_list[i].append(0)
        else:
            student_list[i].append(previousGroups[0][0])
            student_list[i].append(previousGroups[1][0])
        print(student_list)
    return student_list


# @app.route('/showAssignments', methods = ['POST', 'GET'])
# def saveAssignment():
    #print("show assignments")
    # return render_template('showAssignments.html')

@app.route('/showAssignments')
def showAssignments():
    #print("show assignments")
    # select * from assignments where teacher_id = 1
    cursor = mysql.connection.cursor()
    #sqlStatement = "select assignment_name, DATE_FORMAT(assignment_date,'%m/%d/%Y'), assignment_id, assignment_description, class_id from assignments where teacher_id = '" + str(user_id) + "'"
    sqlStatement = "select assignment_name, DATE_FORMAT(assignment_date,'%m/%d/%Y'), assignment_id, assignment_description, class_id from assignments where teacher_id = '" + str(
        user_id) + "' ORDER BY assignment_id DESC"
    cursor.execute(sqlStatement)
    assignments = cursor.fetchall()
    # print(sqlStatement)
    # print(assignments)
    assignmentTable = '<table id="groupsTable">'
    assignmentTable += '<tr class="topRow"><th>Name</th><th>Date</th><th>Course</th><th></th></tr>'
    for x in assignments:
        assignmentTable += '<tr><td>' + str(x[0]) + '</td><td>' + str(x[1]) + '</td><td>' + str(getClassName(x[4])) + '</td><td><form action="/assignmentSheet" method="post"><input type="hidden" value="' + str(x[2]) + '" name="assignmentId"><input type="hidden" value="' + str(x[0]) + '" name="assignmentName"><input type="hidden" value="' + str(
            x[3]) + '" name="assignmentDescription"><input type="hidden" value="' + str(x[1]) + '" name="assignmentDate"><input type="hidden" value="' + str(x[4]) + '" name="classId"><button style="background-color: rgba(0, 119, 255, 0.14); color: #0077ff;">View</button></form> <form action="/deleteAssignment" method="post"><input type="hidden" value="' + str(x[2]) + '" name="assignmentId"><button style="background-color: rgba(220, 20, 60, 0.157); color: crimson;">Delete</button></form></td></tr>'
    assignmentTable += "</table>"
    okayButton = '<button onclick="window.location.replace(\'/\');" style=" color: orangered; background-color: rgba(255, 68, 0, 0.158); position: relative; margin-top: 10px;">Back to dashboard</button>'
    return render_template('showAssignments.html', assignmentTable=assignmentTable, okay_button=okayButton, user_info=getUser())


@app.route('/insertAssignment', methods=['POST', 'GET'])
def insertAssignment():
    classId = request.form['classId']
    assignment_name = request.form['assignmentTitle']
    assignment_description = request.form['assignmentDescription']
    group_criteria = request.form.getlist('criteria')
    group_student = request.form.getlist('gs')
    assignmentNum = getNewAssignmentNum()
    #assignmentInsert = "INSERT INTO assignments (assignment_id, assignment_date, assignment_name, assignment_description, teacher_id) VALUES (%s,%s,%s,%s)",(assignmentNum, "CURDATE()", assignment_name, assignment_description, user_id)
    assignmentInsert = "INSERT INTO assignments (assignment_id, assignment_date, assignment_name, assignment_description, teacher_id, class_id) VALUES ('" + str(
        assignmentNum) + "', CURDATE(), '" + str(assignment_name) + "','" + str(assignment_description) + "','" + str(user_id) + "','" + str(classId) + "')"
    print(assignmentInsert)
    cursor = mysql.connection.cursor()
    cursor.execute(assignmentInsert)
    mysql.connection.commit()
    currentGroupNum = int(getCurrentGroupNum())
    for x in group_criteria:
        criteriaInsert = "INSERT INTO assignments_criteria (assignment_id, criteria_id) VALUES ('" + str(
            assignmentNum) + "', '" + str(x) + "')"
        print(criteriaInsert)
        cursor.execute(criteriaInsert)
        mysql.connection.commit()
    for y in group_student:
        gs = y.split("|")
        groupId = int(gs[0]) + currentGroupNum
        studentId = gs[1]
        studentInsert = "INSERT INTO student_groups (group_id, student_id, assignment_id) VALUES ('" + str(
            groupId) + "', '" + str(studentId) + "', '" + str(assignmentNum) + "')"
        print(studentInsert)
        cursor.execute(studentInsert)
        mysql.connection.commit()
    cursor.close()
    return showAssignments()


@app.route('/deleteAssignment', methods=['POST', 'GET'])
def deleteAssignment():
    assignment_id = request.form['assignmentId']
    print(assignment_id)
    deleteGroups = "DELETE FROM gt_db.student_groups WHERE assignment_id = '" + \
        assignment_id + "'"
    deleteCriteria = "DELETE FROM gt_db.assignments_criteria WHERE assignment_id = '" + \
        assignment_id + "'"
    deleteAssignment = "DELETE FROM gt_db.assignments WHERE assignment_id = '" + \
        assignment_id + "'"
    cursor = mysql.connection.cursor()
    cursor.execute(deleteGroups)
    mysql.connection.commit()
    cursor.execute(deleteCriteria)
    mysql.connection.commit()
    cursor.execute(deleteAssignment)
    mysql.connection.commit()
    cursor.close()
    return showAssignments()


@app.route('/assignmentSheet', methods=['POST', 'GET'])
def assignmentSheet():
    assignment_id = request.form['assignmentId']
    assignment_name = request.form['assignmentName']
    assignment_description = request.form['assignmentDescription']
    assignment_date = request.form['assignmentDate']
    class_id = request.form['classId']
    cursor = mysql.connection.cursor()
    groupNumsQuery = "SELECT distinct(group_id) FROM student_groups sg JOIN assignments a ON sg.assignment_id = a.assignment_id WHERE sg.assignment_id = '" + str(
        assignment_id) + "' and a.teacher_id = '" + str(user_id) + "' ORDER BY sg.assignment_id ASC"
    cursor.execute(groupNumsQuery)
    groupNums = cursor.fetchall()

    groupDisplayNum = 1

    tableGroupsDisplay = '<table id="groupsTable">'
    for x in groupNums:
        #studentNamesQuery = "SELECT CONCAT_WS(' ',s.first_name,s.last_name) FROM student_groups sg JOIN students s ON sg.student_id = s.student_id JOIN assignments a ON a.assignment_id = sg.assignment_id WHERE sg.assignment_id = '" + str(assignment_id) + "' and a.teacher_id = '" + str(user_id) + "' and sg.group_id = '" + str(x[0]) + "'"
        studentNamesQuery = "SELECT CONCAT_WS(' ',s.first_name,s.last_name) FROM student_groups sg JOIN students s ON sg.student_id = s.student_id JOIN assignments a ON a.assignment_id = sg.assignment_id WHERE sg.assignment_id = '" + str(
            assignment_id) + "' and a.teacher_id = '" + str(user_id) + "' and sg.group_id = '" + str(x[0]) + "' ORDER BY sg.group_id ASC"
        print(studentNamesQuery)
        cursor.execute(studentNamesQuery)
        studentNames = cursor.fetchall()
        tableGroupsDisplay += groupsHistoryRow(
            studentNames[0][0], studentNames[1][0], groupDisplayNum)
        groupDisplayNum = groupDisplayNum + 1
    tableGroupsDisplay += "</table>"
    tableGroupsDisplay += '<table class="criteriaKey">'
    tableGroupsDisplay += "<tr><th>Grouped based on:</th></tr>"
    for y in getCriteria(assignment_id):
        tableGroupsDisplay += "<tr><td>" + y[0] + "</td></tr>"
    tableGroupsDisplay += "</table>"
    okay_button = '<button onclick="window.history.back()">Okay</button>'
    return render_template('assignmentSheet.html', assignment_name=assignment_name, assignment_description=assignment_description, assignment_date=assignment_date, user_info=getUser(), tableGroupsDisplay=tableGroupsDisplay, okay_button=okay_button, class_name=getClassName(class_id))


def groupsHistoryRow(x, y, z):
    row = "<tr>"
    row += "<td>Group " + str(z) + "</td>"
    row += "<td>" + str(x) + "</td>"
    row += "<td>" + str(y) + "</td>"
    row += "</tr>"
    return row


def getNewAssignmentNum():
    cursor = mysql.connection.cursor()
    sqlQuery = "SELECT assignment_id + 1 FROM assignments ORDER BY assignment_id DESC LIMIT 1"
    cursor.execute(sqlQuery)
    newNum = cursor.fetchone()
    # print(newNum[0])
    return newNum[0]


def getCurrentGroupNum():
    cursor = mysql.connection.cursor()
    sqlQuery = "SELECT distinct(group_id) FROM student_groups ORDER BY group_id DESC LIMIT 1"
    cursor.execute(sqlQuery)
    curNum = cursor.fetchone()
    # print(curNum[0])
    return curNum[0]


def getCriteria(assignment_id):
    cursor = mysql.connection.cursor()
    sqlQuery = "SELECT distinct(criteria_name) FROM criteria c JOIN assignments_criteria ac ON c.criteria_id = ac.criteria_id WHERE ac.assignment_id = '" + assignment_id + "'"
    cursor.execute(sqlQuery)
    allCriteria = cursor.fetchall()
    return allCriteria


def getClassName(id):
    cursor = mysql.connection.cursor()
    sqlQuery = "SELECT class_name FROM classes WHERE class_id = '" + \
        str(id) + "'"
    cursor.execute(sqlQuery)
    className = cursor.fetchone()
    return className[0]


app.run(host='0.0.0.0', port=8080)
