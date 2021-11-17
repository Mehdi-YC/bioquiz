from django.contrib import admin
from .models import Question,Image,Answer

# adding Question,Image,Answer to the administration view for crud operations
admin.site.register(Question)
admin.site.register(Image)
admin.site.register(Answer)