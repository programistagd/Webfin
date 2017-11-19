from django.template.defaulttags import register


@register.filter(name='smartusername')
def smart_username(user):
    res = user.username
    if user.first_name or user.last_name:
        res += " ("
        res += user.first_name
        if user.first_name and user.last_name:
            res += " "
        res += user.last_name
        res += ")"
    return res