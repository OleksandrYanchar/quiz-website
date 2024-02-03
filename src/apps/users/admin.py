from django.contrib import admin
from .models import User
from django.utils.safestring import mark_safe

class CustomUserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("username",)}
        
    list_display = ('username', 'slug', 'bio', 'display_image','email', 'is_staff')
    list_filter = ("username",'date_changed','is_activated', 'is_staff' )
    search_fields = ("username",'slug','id', 'is_activated', 'is_staff')
    readonly_fields = ('display_image', 'date_added','date_changed')
    
    fieldsets = (
        (None, {"fields": (("username", "slug"),)}),
        (None, {"fields": (('email',"is_activated", 'is_staff'),)}),
        (None, {"fields": (("date_added", "date_changed"),)}),    
        (None, {"fields": ("bio", "picture", "display_image")}),
    )
    
    def display_image(self, obj):
        if obj.picture:
            return mark_safe(f'<img src={obj.picture.url} width="100" height="110"')
            print(obj.picture.url)
        else:
            return "No Image"


    display_image.short_description = "Image"

admin.site.register(User, CustomUserAdmin)
