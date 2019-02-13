from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Question, Option, User, UserAnswer, UserEvent, UserTotalScore

# Register your models here.
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'score', 'count_down']}),
    ]
    list_display = ('question_text', 'score')
    inlines = [OptionInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(User, UserAdmin)
