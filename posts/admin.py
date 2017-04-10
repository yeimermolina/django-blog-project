from django.contrib import admin

from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "updated", "timestamp"]
	list_display_links = ["updated"]
	list_filter = ["updated", "timestamp"]
	search_fields = ["title", "content"]
	class Meta:
		model = Post

admin.site.register(Post, PostAdmin)
