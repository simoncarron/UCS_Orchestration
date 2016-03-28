from flask import session, send_file

from Exscript.protocols import SSH2
from Exscript import Account

import mod_database as database
import mod_xml as xml

import config as settings

import time

import flask
from flask import Blueprint
from flask import render_template, request, redirect, url_for
import threading

pod_blueprint = Blueprint('pod_blueprint', __name__, template_folder='templates')

authorization_role = "A"

POOL_TIME = 1  # Seconds

def deployPOD(pkID):
    with database.app.app_context():

        # START STEP 1

        database.updatePodStatus(pkID,"TRAN_Connection_to_POD...")
        account = Account('admin', 'd')
        conn = SSH2()
        conn.connect('10.78.80.1')
        print "Response was:", repr(conn.response)

        conn.login(account)
        print "Response was:", repr(conn.response)

        time.sleep(15)
        database.updatePodStatus(pkID,"TRAN_Connection_to_POD...Sucess")
        time.sleep(10)

        # END STEP 1

        # START STEP 2

        database.updatePodStatus(pkID,"TRAN_Push_config_to_POD...")

        conn.execute('conf t')
        print "Response was:", repr(conn.response)

        conn.execute('interface GigabitEthernet0/1.103')
        print "Response was:", repr(conn.response)
        conn.execute('encapsulation dot1Q 103')
        print "Response was:", repr(conn.response)
        conn.execute('ip address 192.168.1.1 255.255.255.0')
        print "Response was:", repr(conn.response)
        conn.execute('ip nat inside')
        print "Response was:", repr(conn.response)
        conn.execute('ip nat inside source static 192.168.1.1 10.78.80.6')
        print "Response was:", repr(conn.response)

        time.sleep(3)
        database.updatePodStatus(pkID,"TRAN_Push_config_to_POD...Sucess")
        time.sleep(3)
        # END STEP 1



        # END PROCESS
        database.updatePodStatus(pkID,"FINA_Success to push it")



###TEST######

@pod_blueprint.route('/run')
def run():
    yourThread = threading.Timer(POOL_TIME, deployPOD, str(database.getPodID(str(session['pkID']))))
    yourThread.start()

    print("RUN")

    return redirect('/showMyPod')

@pod_blueprint.route('/status', methods=['POST'])
def status():

    statusPod = {}
    if statusPod.__len__() == 0:
        statusPod['status'] = database.getPodStatus(str(database.getPodID(str(session['pkID']))))
        statusPod['description'] = database.getPodStatus(str(database.getPodID(str(session['pkID']))))

    return flask.jsonify(statusPod)


@pod_blueprint.route('/showMyPod')
def showMyPod():
    authorization_role = "B"
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            ########END OF AUTHENTICATION########
            db = database.getDataBase()

            db.row_factory = database.dict_factory
            cur = db.execute("select * from pod where pkID like '" + str(session['fkID_pod']) + "'")

            MyPod = cur.fetchone()

            return render_template('pod/showMyPod.html', title="My Pod", pod=MyPod)


@pod_blueprint.route('/showPod')
def showPod():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            ########END OF AUTHENTICATION########

            element = "pod"

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

            return render_template('pod/index.html', title="POD", entries=resultReturn, reach_max_entries=reach_max_entries,
                               reach_min_entries=reach_min_entries, min_entries=min_entries)


@pod_blueprint.route('/addPodForm')
def addPodForm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            ########END OF AUTHENTICATION########

            element = "pod"

            inputform = xml.getInputForm(element)

            return render_template('pod/addPodForm.html', title="Add a new POD", inputform=inputform, table=element)


@pod_blueprint.route("/addPod", methods=['POST'])
def addPod():
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

            return redirect(url_for('pod_blueprint.showPod'))


@pod_blueprint.route('/deletePod', methods=['POST'])
def deletePod():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            ########END OF AUTHENTICATION########

            db = database.getDataBase()
            db.execute('delete from pod where pkID = ' + request.form['pkID'])
            db.commit()

            return redirect(url_for('pod_blueprint.showPod'))


@pod_blueprint.route('/modifyPodForm', methods=['POST'])
def modifyPodForm():
    ########AUTHENTICATION########
    if not session.get('user'):
        return render_template(settings.AUTHENTIFICATION_TEMPLATE)
    else:
        if not session.get('access_group') in authorization_role:
            return render_template(settings.AUTHORIZATION_TEMPLATE)
        else:
            ########END OF AUTHENTICATION########

            element = "pod"

            inputform = xml.getInputFormValue(element,request.form['pkID'] )


            return render_template('pod/modifyPodForm.html', title="Modify POD", inputform=inputform,
                                   table="pod", pkID=request.form['pkID'])


@pod_blueprint.route("/updatePod", methods=['POST'])
def updatePod():
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

            return redirect(url_for('pod_blueprint.showPod'))

@pod_blueprint.route('/return-files/<file>')
def return_files_tut(file):
    print file
    return send_file('temp/07/'+file, attachment_filename=file)