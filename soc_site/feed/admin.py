from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date_posted', 'status')
    list_filter = ('status', 'created', 'date_posted', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_posted'
    ordering = ('status', 'date_posted')

