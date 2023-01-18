from common.api.models import Role, User

class Validate_request:
    def __init__(self, request):
        self.request = request

    def validate(self):
        role = Role.query.all()

        if role:
            if role.end_point is None and role.method is None:
                role.end_point = "Not set"
                role.method = "Not set"

        return str(self)

    def validate_get():
        return True