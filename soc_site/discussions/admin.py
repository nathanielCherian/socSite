from django.contrib import admin
from .models import Question, Response

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date_posted')
    list_filter = ('date_posted', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_posted'
    ordering = ('date_posted',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('parent_question', 'author', 'date_posted', 'rating', 'active')
    list_filter = ('date_posted', 'author')
    search_fields = ('parent_question', 'content', 'rating')
    raw_id_fields = ('author','parent_question')
    date_hierarchy = 'date_posted'
    ordering = ('rating',)