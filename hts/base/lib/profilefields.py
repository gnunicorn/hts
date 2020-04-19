import re

from django.forms import ValidationError
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from misago.users.profilefields import basefields

class PronounField(basefields.TextProfileField):
    fieldname = "pronouns"
    label = _("Pronouns")
