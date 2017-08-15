from django.contrib import admin
from .models import Post, PostSite

class PostAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
        return super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

admin.site.register(Post, PostAdmin)
admin.site.register(PostSite)