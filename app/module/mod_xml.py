import xml.etree.ElementTree as ET
from flask import Flask, session
import os
import mod_database as database

import config as settings

app = Flask(__name__)


def getInputForm(parent):
    xmlfilename = os.path.join(os.getcwd(), settings.CONF_FOLDER_NAME, settings.USER_ENTRY_XML)
    tree = ET.parse(xmlfilename)
    root = tree.getroot()
    root = root.find(parent)

    final = []


    for sub in root.findall('sub'):

        sub_element = {}
        return_form = []

        for element in sub.findall('element'):

            input_element = {}

            radio_values = []
            reference_values = []

            input_element['type'] = element.get('type')
            input_element['name'] = element.find('name').text.lower()
            if element.get('editable') == "yes":
                input_element['display_name'] = element.find('display_name').text
                input_element['empty'] = element.get('empty')
                input_element['message'] = element.find('message').text

            # ****FOR INPUT ELEMENT****#

            if element.get('type') == "text":
                if element.get('editable') == "yes":
                    input_element['regex'] = element.find('regex').text

            # ****FOR INPUT REFERENCE****#

            if element.get('type') == "reference":

                records = database.getEntries(element.find('refer').text)

                tree2 = ET.parse(xmlfilename)
                root2 = tree2.getroot()
                root2 = root2.find(element.find('refer').text)



                for a in records:
                    print "sssssssssssss"
                    print a
                    d = {"pkey" : a['pkID'],"value" : a['name']}
                    if root2.get('scope') in settings.USER_SCOPE:
                        if a['fkID_created_by'] == session['pkID']:
                            reference_values.append(d)

                    else:
                        reference_values.append(d)

                input_element['content'] = reference_values

            # ****FOR RADIO ELEMENT****#

            if element.get('type') == "radio":

                for value in element.findall('value'):
                    radio_values.append(value.get('name'))
                    radio_values.__iter__
                    input_element['content'] = radio_values

            if element.get('editable') == "yes":
                return_form.append(input_element)

        sub_element['name']=sub.get('name')
        sub_element['data']= return_form

        final.append(sub_element)

    return final

def getInputFormValue(element,pkID):

        record = database.getEntrie(element, pkID)

        inputform = getInputForm(element)

        db = database.getDataBase()
        test = [r for r in database.dict_gen(db.execute('select * from '+element+' where pkID like ' + pkID + ''))]
        print test
        test = dict(test[0])
        for z in inputform:
            z = dict(z)
            for y in z['data']:
                if y["type"] == "reference":
                    y["value"] = test["fkID_" + y["name"]]
                else:
                    y['value']=test[y['name']]
                y['pkID'] = pkID
        return inputform

def getMaxRecords(parent):
    xmlfilename = os.path.join(os.getcwd(), settings.CONF_FOLDER_NAME, settings.USER_ENTRY_XML)
    tree = ET.parse(xmlfilename)
    root = tree.getroot()
    root = root.find(parent)
    answer = []

    max = root.get('max')

    return max

def getMinRecords(parent):
    xmlfilename = os.path.join(os.getcwd(), settings.CONF_FOLDER_NAME, settings.USER_ENTRY_XML)
    tree = ET.parse(xmlfilename)
    root = tree.getroot()
    root = root.find(parent)
    answer = []

    min = root.get('min')

    return min

def getScope(parent):
    xmlfilename = os.path.join(os.getcwd(), settings.CONF_FOLDER_NAME, settings.USER_ENTRY_XML)
    tree = ET.parse(xmlfilename)
    root = tree.getroot()
    root = root.find(parent)
    answer = []

    scope = root.get('scope')

    return scope
