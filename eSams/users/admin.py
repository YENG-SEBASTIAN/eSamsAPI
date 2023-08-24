from django.contrib import admin

from users.models import UserAccount, ProfileInfo

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "fullName", "level", "role")
    search_fields = ("username", "email", "level")
    list_filter = ("username", "email")
    

admin.site.register(UserAccount, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("programme", "contact", "about", "picture")
    search_fields = ("programme", "contact")
    list_filter = ("programme", "contact")
    

admin.site.register(ProfileInfo, UserProfileAdmin)

# admin.site.register(ProfileInfo)