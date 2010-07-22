import formencode

class SignUpForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username  = formencode.validators.String(not_empty=True)
    password  = formencode.validators.String(not_empty=True)

class UserForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username  = formencode.validators.String(not_empty=True)
    password  = formencode.validators.String(not_empty=False)
    is_active = formencode.validators.Bool()
    is_admin  = formencode.validators.Bool()

