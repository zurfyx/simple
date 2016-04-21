from django.db import models


class LowerCaseCharField(models.CharField):

    def to_python(self, value):
        return value.lower()
