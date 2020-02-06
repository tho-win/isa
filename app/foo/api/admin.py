from django.contrib import admin
from .models import Language, School, User
admin.site.register(School)
admin.site.register(User)
admin.site.register(Language)

