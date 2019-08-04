from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe

from crypto.crypto_message import decrypt
from forum.models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('created', 'modified', '_bold_subject', 'user', '_decrypted')
    readonly_fields = ('created', 'modified', '_bold_subject', 'user', '_decrypted')

    def _bold_subject(self, obj):
        return mark_safe('<b>' + obj.subject + '</b>')

    def _decrypted(self, obj):
        """
        Decrypt message from body field.
        """
        return decrypt(obj.body, settings.TEXT_SECRET_CODE)

    _decrypted.short_description = 'Decrypted'


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('created', 'modified', 'user', 'question', '_decrypted')
    readonly_fields = ('created', 'modified', 'user', 'question', '_decrypted')

    def _decrypted(self, obj):
        """
        Decrypt message from body field.
        """
        return decrypt(obj.body, settings.TEXT_SECRET_CODE)

    _decrypted.short_description = 'Decrypted'


admin.site.register(Answer, AnswerAdmin)
