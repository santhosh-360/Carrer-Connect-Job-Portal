from django.contrib import admin

from .models import Profile
from .models import Job
from .models import Application


admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Application)