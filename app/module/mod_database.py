import xml.etree.ElementTree as ET
import sqlite3
import itertools
from flask import Flask, g, session

import os

import config as settings

app = Flask(__name__)

settings.USER_SCOPE

def createDataBaseSchema():
    if not os.path.exists(settings.DATABASE_FOLDER_NAME):
        os.makedirs(settings.DATABASE_FOLDER_NAME)

    filename = os.path.join(os.getcwd(), settings.CONF_FOLDER_NAME, settings.USER_ENTRY_XML)
    tree = ET.parse(filename)

    root = tree.getroot()

    filename = os.path.join(os.getcwd(), settings.DATABASE_FOLDER_NAME, settings.DATABASE_SCHEMA)

    file = open(filename, "w")

    for entry in root:



        file.write("drop table if exists " + entry.tag + ";\n")

        file.write("create table " + entry.tag + " (\n")
        file.write("  pkID integer primary key autoincrement\n")


        child = root.find(entry.tag)


        for sub in child:

        #sub = child.find("sub")

            for parent in sub:
                if parent.get('type') == "reference":
                    file.write("  ,fkID_" + parent.find('name').text.lower() + " integer\n")
                else:
                    file.write("  ," + parent.find('name').text.lower() + " text\n")


        file.write("  ,fkID_created_by integer\n")

        file.write(");\n")

    file.write("INSERT INTO user (name,first_name,userid,password,access_group)VALUES ('admin', 'admin', 'admin', 'admin', 'A' );\n")
    file.write("INSERT INTO user (name,first_name,userid,password,access_group)VALUES ('simon', 'simon', 'simon', 'simon', 'B' );\n")
    file.write("INSERT INTO user (name,first_name,userid,password,access_group)VALUES ('carron', 'carron', 'carron', 'carron', 'B' );\n")

    file.close()


def createDataBase():
    if not os.path.exists(settings.DATABASE_FOLDER_NAME):
        os.makedirs(settings.DATABASE_FOLDER_NAME)

    database = os.path.join(os.getcwd(), settings.DATABASE_FOLDER_NAME, settings.DATABASE_NAME)
    conn = sqlite3.connect(database)

    schema = os.path.join(os.getcwd(), settings.DATABASE_FOLDER_NAME, settings.DATABASE_SCHEMA)

    with app.open_resource(schema, mode='r') as f:
        conn.cursor().executescript(f.read())


def getDataBase():
    if not hasattr(g, os.path.join(os.getcwd(), settings.DATABASE_FOLDER_NAME, settings.DATABASE_NAME)):
        g.sqlite_db = connectDataBase()
    return g.sqlite_db


def connectDataBase():
    rv = sqlite3.connect(os.path.join(os.getcwd(), settings.DATABASE_FOLDER_NAME, settings.DATABASE_NAME))
    rv.row_factory = sqlite3.Row

    return rv


def generateInsertRequest(f):
    table = f.get('table')
    xmlfilename = os.path.join(os.getcwd(), settings.CONF_FOLDER_NAME, settings.USER_ENTRY_XML)
    tree = ET.parse(xmlfilename)

    root = tree.getroot()
    child = root.find(table)
    #child = child.find("sub")


    element_content = []
    table_list = []

    table_list.append("fkID_created_by")
    element_content.append(str(session['pkID']))

    for sub in child:

        for element in sub:

            if element.get('editable') == "yes":
                element_content.append(f.get(element.find('name').text.lower()))
                if element.get('type') == "reference":
                    table_list.append("fkID_" + element.find('name').text)
                else:
                    table_list.append(element.find('name').text)

    return ('insert into ' + table + ' (' + ','.join(table_list) + ') values ("' + '","'.join(element_content) + '")')


def generateUpdateRequest(f):
    table = f.get('table')
    pkID = f.get('pkID')

    xmlfilename = os.path.join(os.getcwd(), settings.CONF_FOLDER_NAME, settings.USER_ENTRY_XML)
    tree = ET.parse(xmlfilename)

    root = tree.getroot()
    child = root.find(table)

    update_request = ""
    couple = ""
    first_couple = True

    for a in f:

        if first_couple:

            first_couple = False

        else:

            update_request = update_request + couple + ', '

        if (a not in "table"):
            couple = a + " = '" + f.get(a) + "'"

    update_request = update_request + couple

    return ("update " + table + " set " + update_request + " where pkID like " + pkID)


def getEntries(table,*pkID):

    db = getDataBase()
    db.row_factory = dict_factory

    if pkID.__len__() == 1:
        cur = db.execute('select * from ' + table + ' where fkID_created_by = '+str(pkID[0])+' order by pkID desc')
    else:
        cur = db.execute('select * from ' + table + ' order by pkID desc')


    entries = cur.fetchall()
    if table in "user":
        for a in entries:
            a['dependecyNbr'] = getNbrDependencyRecordsUser(table, a['pkID'])
            a['dependecyDic'] = getDicDependencyRecordsUser(table, a['pkID'])
    else:
        for a in entries:
            a['dependecyNbr'] = getNbrDependencyRecords(table, a['pkID'])
            a['dependecyDic'] = getDicDependencyRecords(table, a['pkID'])

    return entries


def getEntrie(table, pkID):
    db = getDataBase()
    cur = db.execute('select * from ' + table + ' where pkID like "' + pkID + '"')
    entries = cur.fetchall()

    return entries

def getEntrieRequest(table, colum, value):
    db = getDataBase()
    cur = db.execute('select * from ' + table + ' where '+colum+' like "' + value + '"')
    entries = cur.fetchall()

    return entries


def getNbrEntries(table,*pkID):
    db = getDataBase()
    if pkID.__len__() == 1:
        cur = db.execute('select count() from ' + table + ' where fkID_created_by = '+str(pkID[0]))
    else:
        cur = db.execute('select count() from ' + table)

    current_records = cur.fetchone()
    nbr = int(current_records[0])

    return nbr


def dict_gen(curs):
    field_names = [d[0] for d in curs.description]
    while True:
        rows = curs.fetchmany()
        if not rows: return
        for row in rows:
            yield dict(itertools.izip(field_names, row))


def getNbrDependencyRecords(table, pkID):
    db = getDataBase()

    result = ""

    cur = db.execute('select name from sqlite_master where type = "table"')
    for a in cur:
        cursor = db.execute('select * from ' + a[0])
        names = list(map(lambda x: x[0], cursor.description))

        for c in names:
            if c == "fkID_" + table:
                cur = db.execute('select count() from ' + a[0] + ' where fkID_' + table + ' like ' + pkID.__str__())

                result = cur.fetchone()[0]
    if result == "":
        result = 0

    return result

def getNbrDependencyRecordsUser(table, pkID):
    db = getDataBase()

    result = ""

    cur = db.execute('select name from sqlite_master where type = "table"')
    for a in cur:
        cursor = db.execute('select * from ' + a[0])
        names = list(map(lambda x: x[0], cursor.description))
        for c in names:
            if c == "fkID_created_by":
                cur = db.execute('select count() from ' + a[0] + ' where fkID_created_by like ' + pkID.__str__())
                result = cur.fetchone()[0]
    if result == "":
        result = 0

    return result


def getDicDependencyRecords(table, pkID):
    db = getDataBase()

    result = []

    cur = db.execute('select name from sqlite_master where type = "table"')
    for a in cur:
        cursor = db.execute('select * from ' + a[0])
        names = list(map(lambda x: x[0], cursor.description))
        for c in names:
            if c == "fkID_" + table:
                db.row_factory = dict_factory
                cur = db.execute('select * from ' + a[0] + ' where fkID_' + table + ' like ' + pkID.__str__())

                response = cur.fetchone()
                if response != None:
                    response["table"]=a[0]
                    result.append(response)

                while response is not None:
                    response = cur.fetchone()
                    if response != None:
                        response["table"]=a[0]
                        result.append(response)

    return result

def getDicDependencyRecordsUser(table, pkID):
    db = getDataBase()

    result = []

    cur = db.execute('select name from sqlite_master where type = "table"')
    for a in cur:
        cursor = db.execute('select * from ' + a[0])
        names = list(map(lambda x: x[0], cursor.description))
        for c in names:
            if c == "fkID_created_by":
                db.row_factory = dict_factory
                cur = db.execute('select * from ' + a[0] + ' where fkID_created_by like ' + pkID.__str__())
                response = cur.fetchone()
                if response != None:
                    response["table"]=a[0]
                    result.append(response)

                while response is not None:
                    response = cur.fetchone()
                    if response != None:
                        response["table"]=a[0]
                        result.append(response)

    return result

def updatePodStatus(pkID_Pod, status):
    db = getDataBase()
    db.execute("update pod set status ='"+status+"' where pkID like " + pkID_Pod)
    db.commit()

def getPodStatus(pkID_Pod):
    db = getDataBase()
    cur = db.execute('select status from pod where pkID = '+str(pkID_Pod))
    current_records = cur.fetchone()
    status = str(current_records[0])

    return status

def getPodID(pkID_User):
    db = getDataBase()
    cur = db.execute("select fkID_pod from user where pkID = "+pkID_User)
    current_records = cur.fetchone()
    ID = str(current_records[0])

    return ID



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
