from flask import render_template, Flask, session

import config
import module.mod_database as database
import module.mod_xml as xml

from module.mod_ucs import ucs_blueprint
from module.mod_vm import vm_blueprint
from module.mod_user import user_blueprint
from module.mod_pod import pod_blueprint

app = Flask(__name__)

@app.route('/')
def index():


    database.createDataBaseSchema()
    database.createDataBase()
    if session.get('user'):
        return render_template('index.html', title="Home", user=session)
    else:
        return render_template(config.AUTHENTIFICATION_TEMPLATE)


app.register_blueprint(pod_blueprint)

app.register_blueprint(ucs_blueprint)

app.register_blueprint(vm_blueprint)

app.register_blueprint(user_blueprint)

