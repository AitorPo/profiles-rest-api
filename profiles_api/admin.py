from django.contrib import admin
# Manually imported
from profiles_api import models

# Register UserProfile model in our admin panel
admin.site.register(models.UserProfile)
