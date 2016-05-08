from django.core.validators import RegexValidator


class Common(object):

    @staticmethod
    def contains(characters, verbose=None):
        return RegexValidator(
            r'^[' + characters + ']*$',
            'Only ' + (verbose or characters) + ' characters are allowed.'
        )

    @staticmethod
    def alphanumeric():
        return Common.contains('0-9a-zA-Z', 'alphanumeric')

    @staticmethod
    def starts_with(val):
        val = str(val)
        return RegexValidator(
            '^[' + val + ']',
            'Must start with a ' + val + '.'
        )

    @staticmethod
    def starts_with_letter():
        return RegexValidator(
            '^[a-zA-Z]',
            'Must start with a letter.'
        )

    @staticmethod
    def min_length(val):
        val = str(val)
        return RegexValidator(
            '^(.){' + val + ',}$',
            'A minimum of ' + val + ' characters are required.'
        )
