from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(School)
admin.site.register(Post)
admin.site.register(Authenticator)
admin.site.register(Recommendation)