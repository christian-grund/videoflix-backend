from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new CustomUser instance, 
    including all fields defined in the CustomUser model.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'
