from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError

class CustomAccountAdapter(DefaultAccountAdapter):

    # validate username
    def clean_username(self, username, shallow=False):
        if len(username) >= 23:
            raise ValidationError('Please enter a username less than 23 characters')
        return DefaultAccountAdapter.clean_username(self,username) # For other default validations.

    # disable account signup
    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        return False
