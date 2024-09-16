from django.contrib import admin

from user.forms import CustomUserCreationForm
from user.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
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
    
