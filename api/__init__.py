import json
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

from common.api.models import User, Role
from common.api.models import db
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_table():
    db.create_all()

app.app_context().push()

from flask_login import LoginManager
from common.api.models import Role
login_manager = LoginManager()

login_manager.init_app(app)

from common.api.queries import getUser_resolver

@app.route('/check_role',methods = ['POST', 'GET'])
def check_role():
    try:
        return getUser_resolver(1)
        
    except Exception as error:
       return [str(error)]
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


from flask_rbac import RBAC, RoleMixin
rbac = RBAC()
rbac.init_app(app)
app.config['RBAC_USE_WHITE'] = True


class Role(RoleMixin):
    pass

anonymous = Role('anonymous')
admin = Role('admin')

rbac.set_user_model(User)
rbac.set_role_model(Role)



from flask import g, current_app  

        

    



