from django.contrib import admin
from .models import Post

# zakladní registrace
# admin.site.register(Post)

# pokrocila registrace
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","status","created_at","published_at")
    list_filter = ("status", "created_at")
    search_fields = ("title","content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

