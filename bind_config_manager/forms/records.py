import formencode

class RecordForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    type  = formencode.validators.String(not_empty=True)
    name  = formencode.validators.String(not_empty=True)
    value = formencode.validators.String(not_empty=True)
