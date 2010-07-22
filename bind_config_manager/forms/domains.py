import formencode

class DomainForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    type            = formencode.validators.String(not_empty=True)
    name            = formencode.validators.String(not_empty=True)
    soa_nameserver  = formencode.validators.String(not_empty=True)
    admin_mailbox   = formencode.validators.String(not_empty=True)
    serial          = formencode.validators.Int(not_empty=False)
    refresh_ttl     = formencode.validators.Int(not_empty=False)
    retry_ttl       = formencode.validators.Int(not_empty=False)
    expire_ttl      = formencode.validators.Int(not_empty=False)
    minimum_ttl     = formencode.validators.Int(not_empty=False)
    default_ttl     = formencode.validators.Int(not_empty=False)
