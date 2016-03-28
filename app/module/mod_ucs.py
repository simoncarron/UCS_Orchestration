from flask import Blueprint, session
from flask import render_template, request, redirect, url_for

import mod_database as database
import mod_xml as xml

import config as settings


ucs_blueprint = Blueprint('ucs_blueprint', __name__, template_folder='templates')

authorization_role = "B"

@ucs_blueprint.route('/showUcs')
def showUcs():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            element = "ucs"

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

            return render_template('ucs/index.html', title="UCS", entries=resultReturn, reach_max_entries=reach_max_entries,
                               reach_min_entries=reach_min_entries, min_entries=min_entries)

@ucs_blueprint.route('/addUcsForm')
def addUcsForm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            element = "ucs"

            inputform = xml.getInputForm(element)

            print inputform

            return render_template('ucs/addUcsForm.html', title="Add a new UCS", inputform=inputform, table=element)



@ucs_blueprint.route("/addUcs", methods=['POST'])
def addUcs():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            print request.form
            db = database.getDataBase()
            db.execute(database.generateInsertRequest(request.form))
            db.commit()

            return redirect(url_for('ucs_blueprint.showUcs'))



@ucs_blueprint.route('/deleteUcs', methods=['POST'])
def deleteUcs():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            db = database.getDataBase()
            db.execute('delete from ucs where pkID = ' + request.form['pkID'])
            db.commit()

            return redirect(url_for('ucs_blueprint.showUcs'))


@ucs_blueprint.route('/modifyUcsForm', methods=['POST'])
def modifyUcsForm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            element = "ucs"

            inputform = xml.getInputFormValue(element,request.form['pkID'] )


            return render_template('ucs/modifyUcsForm.html', title="Modify UCS", inputform=inputform,
                               table="ucs", pkID=request.form['pkID'])

@ucs_blueprint.route("/updateUcs", methods=['POST'])
def updateUcs():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            db = database.getDataBase()
            db.execute(database.generateUpdateRequest(request.form))
            db.commit()

            return redirect(url_for('ucs_blueprint.showUcs'))