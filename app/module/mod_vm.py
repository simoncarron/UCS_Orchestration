from flask import Blueprint, session
from flask import render_template, request, redirect, url_for

import mod_database as database
import mod_xml as xml

import config as settings

vm_blueprint = Blueprint('vm_blueprint', __name__, template_folder='templates')

authorization_role = "B"

@vm_blueprint.route('/showVm')
def showVm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            element = "vm"

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

            return render_template('vm/index.html', title="VM", entries=resultReturn, reach_max_entries=reach_max_entries,
                               reach_min_entries=reach_min_entries, min_entries=min_entries)


@vm_blueprint.route('/addVmForm')
def addVmForm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            inputform = xml.getInputForm("vm")
            return render_template('vm/addVmForm.html', title="Add a new VM", inputform=inputform, table="vm")


@vm_blueprint.route("/addVm", methods=['POST'])
def addVm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            db = database.getDataBase()
            db.execute(database.generateInsertRequest(request.form))
            db.commit()

            return redirect(url_for('vm_blueprint.showVm'))


@vm_blueprint.route("/updateVm", methods=['POST'])
def updateVm():
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

            return redirect(url_for('vm_blueprint.showVm'))


@vm_blueprint.route('/deleteVm', methods=['POST'])
def deleteVm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            db = database.getDataBase()
            db.execute('delete from vm where pkID = ' + request.form['pkID'])
            db.commit()

            return redirect(url_for('vm_blueprint.showVm'))


@vm_blueprint.route('/modifyVmForm', methods=['POST'])
def modifyVmForm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
    ########END OF AUTHENTICATION########

            element = "vm"

            inputform = xml.getInputFormValue(element,request.form['pkID'] )


            return render_template('vm/modifyVmForm.html', title="Modify VM", inputform=inputform, table="vm",
                                   pkID=request.form['pkID'])
