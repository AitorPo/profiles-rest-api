from django.contrib import admin
# Manually imported
from profiles_api import models

# Register classes in models.py into our admin panel
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
