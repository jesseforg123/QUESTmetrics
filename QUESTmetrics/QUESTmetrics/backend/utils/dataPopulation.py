from app import db, studentBasedDataTables

'''
def populateGroupBasedData(groupId, channel=None):
    for table in groupBasedDataTables:
        query = "INSERT INTO " + table + " (groupId) VALUES (:gid);"
        db.session.execute(query, {
            'gid':groupId,
            'channel':channel
        })
        db.session.commit()

def removeFromGroupBasedData(className):
    for tbl in groupBasedDataTables:
        query = "DELETE FROM " + tbl + " WHERE groupId=(SELECT groupId FROM groups WHERE classId=(SELECT classId FROM classes WHERE className=:cname))"
        db.session.execute(query, {'cname':className})
        db.session.commit()

def removeFromGroupBasedDataSingular(name):
    for tbl in groupBasedDataTables:
        query = "DELETE FROM " + tbl + " WHERE groupId=(SELECT groupId FROM groups WHERE name = :name);"
        db.session.execute(query, {'name':name})
        db.session.commit()
'''

def removeFromStudentBasedData(className, studentId = None):
    for tbl in studentBasedDataTables:
        if studentId is not None:
            query = "DELETE FROM " + tbl + ' WHERE classId=(SELECT classId FROM classes WHERE className=:cname) AND studentId=:sid;'
            db.session.execute(query, {'cname': className, 'sid': studentId})
        else:
            query = "DELETE FROM " + tbl + ' WHERE classId=(SELECT classId FROM classes WHERE className=:cname)'
            db.session.execute(query, {'cname': className})
        db.session.commit() 

def populateStudentBasedData(groupName, studentId=None, uid=None, directoryId=None):
    if(uid):
        resp = db.session.execute("SELECT studentId FROM students WHERE uid=:uid", {'uid':uid})
        studentId = [dict(r) for r in resp][0]['studentId']
    elif(directoryId):
        resp = db.session.execute("SELECT studentId FROM students WHERE personId=(SELECT personId from people WHERE directoryId=:directoryId)", {'directoryId':directoryId})
        studentId = [dict(r) for r in resp][0]['studentId']
    

    resp = db.session.execute("SELECT classId FROM groups WHERE name=:gname;", {'gname':groupName})
    classId = [dict(r) for r in resp][0]['classId']
    for table in studentBasedDataTables:
        query = "INSERT INTO " + table +" (studentId, classId) VALUES (:sid, :cid);"
        db.session.execute(query, {
            'sid':studentId,
            'cid':classId
        })
        db.session.commit()