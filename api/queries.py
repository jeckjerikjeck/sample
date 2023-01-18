from flask import session
from sqlalchemy import null
from common.api.models import Role, User
from ariadne import convert_kwargs_to_snake_case
from common.rbac.validate_role import Validate_request

def listUsers_resolver(obj, info):
    try:
        users = User.query.all()
        
        # print(users)
        p_users = {
            "success": True,
            "user": users
        }
    except Exception as error:
        p_users = {
            "success": False,
            "errors": [str(error)]
        }
    return p_users

def listRole_resolver():
    try:
        roles = [role for role in Role.query.all()]
        # print(roles)
        p_roles = {
            "success": True,
            "role": roles
        }
    except Exception as error:
        p_roles = {
            "success": False,
            "errors": [str(error)]
        }
    return p_roles

@convert_kwargs_to_snake_case
def getUsers_resolver(obj, info, id):
    try:
       
        users = User.query.get(id)


        if users:
            role_id= users.roles

        roles = Role.query.all()
       
       
        if users:
            status = Validate_request.validate(1)
            users.stat = str(status)

        
        query = {
            "success": True,
            "user": users
        }

    except AttributeError:
        query = {
            "success": False,
            "errors": ["No data Found"]
        }
    return query

def getUser_resolver(obj, info, id):
    try:
       
        users = User.query.get(id)
        #users = User.query.join(Role, User.id==id).first()
        # print(user)
        
        if users:
            role_id= users.roles

        status = Validate_request.validate(role_id[0])

        query = {
            "success": True,
            "message": status,
            "user": users
        }

    except AttributeError:
        query = {
            "success": False,
            "errors": ["No data Found"]
        }
    return query

@convert_kwargs_to_snake_case
def getRole_resolver(obj, info, id):
    try:
        role = Role.query.get(id)
        status = Validate_request.validate(role)
    
        if role:
            if role.end_point is None and role.method is None:
                role.end_point = "Not set"
                role.method = "Not set"    
        # print(user)
        query = {
            "success": True,
            "message": status,
            "role": [role]
        }
    except AttributeError:
        query = {
            "success": False,
            "errors": ["User matching {{id}} not found"]
        }
    return query



@convert_kwargs_to_snake_case
def getRole2_resolver(obj, info, id):
    try:
        role = Role.query.get(id)
        # print(user)
        query = {
            "success": True,
            "role": [role]
        }
    except AttributeError:
        query = {
            "success": False,
            "errors": ["User matching {{id}} not found"]
        }
    return query

@convert_kwargs_to_snake_case
def authRole_resolver(obj, info, id):
    try:
       
        users = User.query.get(id)
        #users = User.query.join(Role, User.id==id).first()
        # print(user)

        roles = Role.query.all()
        #r = [role][0][0]

        for i in range(len(roles)):
            if [roles][0][i] == users.roles[0]:
                role = Role.query.get(i+1)
                role_id = role.name
                break
    
        status = Validate_request.validate
        if status:
            stat = "POST"
        else:
            stat = "GET"              
        if users:
            users.stat = stat

        query = {
            "success": True,
            "auth": users
        }

    except AttributeError:
        query = {
            "success": False,
            "errors": ["No data Found"]
        }
    return query    