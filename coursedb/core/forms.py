from django.contrib.auth.forms import UserChangeForm

from core.models import User


class UserAdminForm(UserChangeForm):

    class Meta:
        """
        Sets the model and defines the used fields.
        """

        model = User
        fields = '__all__'