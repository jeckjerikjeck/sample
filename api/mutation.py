from datetime import date
from ariadne import convert_kwargs_to_snake_case
from common.api import db
from common.api.models import User, Role

@convert_kwargs_to_snake_case
def create_role_resolver(obj, info, name):
    try:
        role = Role(
           name=name
        )
        db.session.add(role)
        db.session.commit()
        payload = {
            "success": True,
            "role": [role]
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format mm-dd-yyyy"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_role_resolver(obj, info, id):
    try:
        role = Role.query.get(id)
        db.session.delete(role)
        db.session.commit()
        payload = {
            "success": True,
            "role": [role]
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format mm-dd-yyyy"]
        }
    return payload    

def update_role_resolver(obj, info, id, end_point, method):
    try:
        role = Role.query.get(id)

        if role:
            role.end_point = end_point
            role.method = method

        db.session.add(role)
        db.session.commit()
        payload = {
            "success": True,
            "role": [role]
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def create_user_resolver(obj, info, username, role_id):
    try:

        role = [role for role in Role.query.all()]
        r = [role][0][role_id-1]    

        user = User(
           username=username,
           roles=[r],
        )

        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format mm-dd-yyyy"]
        }
    return payload