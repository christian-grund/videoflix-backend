from django.contrib import admin

from user.forms import CustomUserCreationForm
from user.models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin interface for managing CustomUser instances, 
    allowing the addition and editing of custom fields.
    """
    add_form = CustomUserCreationForm
    fieldsets = (    
                (            
                    'Individuelle Daten',            
                    {                
                        'fields': 
                        (                    
                            'custom',                    
                            'phone',                    
                            'address'                
                        )            
                    }        
                ),  
            *UserAdmin.fieldsets  
        )
