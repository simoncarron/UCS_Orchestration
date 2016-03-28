from flask import Blueprint, session
from flask import render_template, request, redirect, url_for

import config as settings
import mod_database as database
import mod_xml as xml

user_blueprint = Blueprint('user_blueprint', __name__, template_folder='templates')

authorization_role = "A"

###User###

@user_blueprint.route('/showUser')
def showUser():
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:

            element = "user"

            if xml.getScope(element) in settings.USER_SCOPE:
                entries = database.getEntries(element,session['pkID'])
                nbr_entries = database.getNbrEntries(element,session['pkID'])

            else:
                entries = database.getEntries(element)
                nbr_entries = database.getNbrEntries(element)

            resultReturn = []
            for x in entries:
                print x['pkID']
                xml.getInputFormValue(element,str(x['pkID']))
                resultReturn.append(xml.getInputFormValue(element,str(x['pkID'])))

            print resultReturn
            max_entries = int(xml.getMaxRecords(element))
            min_entries = int(xml.getMinRecords(element))

            reach_max_entries = False;
            reach_min_entries = False;

            if (nbr_entries >= max_entries):
                reach_max_entries = True;

            if (nbr_entries >= min_entries):
                reach_min_entries = True;

            print resultReturn

            return render_template('user/index.html', title="User", entries=resultReturn, reach_max_entries=reach_max_entries,
                               reach_min_entries=reach_min_entries, min_entries=min_entries)


@user_blueprint.route('/addUserForm')
def addUserForm():
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            element = "user"

            inputform = xml.getInputForm(element)

            return render_template('user/addUserForm.html', title="Add new User", inputform=inputform, table=element)


@user_blueprint.route("/addUser", methods=['POST'])
def addUser():
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            db = database.getDataBase()
            db.execute(database.generateInsertRequest(request.form))
            db.commit()

            return redirect(url_for('user_blueprint.showUser'))


@user_blueprint.route('/deleteUser', methods=['POST'])
def deleteUser():
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:

            db = database.getDataBase()
            db.execute('delete from user where pkID = ' + request.form['pkID'])
            db.commit()

            return redirect(url_for('user_blueprint.showUser'))


@user_blueprint.route('/modifyUserForm', methods=['POST'])
def modifyUserForm():
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            element = "user"

            inputform = xml.getInputFormValue(element,request.form['pkID'] )

            return render_template('user/modifyUserForm.html', title="Modify User", inputform=inputform,
                                   table="user", pkID=request.form['pkID'])


@user_blueprint.route("/updateUser", methods=['POST'])
def updateUser():
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            db = database.getDataBase()
            db.execute(database.generateUpdateRequest(request.form))
            db.commit()

            return redirect(url_for('user_blueprint.showUser'))


@user_blueprint.route('/signIn')
def signIn():
    return render_template('user/signIn.html', title="User")


@user_blueprint.route('/signOut')
def signOut():
    session.clear()
    return render_template('index2.html', title="User")


@user_blueprint.route('/validateLogin', methods=['POST'])
def validateLogin():

    session.clear()

    _username = request.form['inputUserID']
    _password = request.form['inputPassword']

    db = database.getDataBase()

    db.row_factory = database.dict_factory
    cur = db.execute("select * from user where userid like '"+_username+"'")

    userDB = cur.fetchone()

    if userDB!= None:

        if _password == str(userDB['password']):
            session['fkID_pod'] = userDB['fkID_pod']

            session['pkID'] = userDB['pkID']
            session['user'] = userDB['userid']
            session['access_group'] = userDB['access_group']
            return redirect('/')
        else:
            return render_template('/index2.html', title="Sign In", authentication="False")
    else:
        return render_template('/index2.html', title="Sign In", authentication="False")
