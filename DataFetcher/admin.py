from django.contrib import admin

from news.models import *

# Register your models here.
admin.site.register(Provider)
admin.site.register(Category)
# admin.site.register(Author)
admin.site.register(News)
# admin.site.register(NewsSource)
admin.site.register(History)
admin.site.register(ReadLater)
admin.site.register(CMS)
