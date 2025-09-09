from django.contrib import admin
from django.shortcuts import redirect
from time import sleep

from django.contrib import messages
from .models import Rule


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    actions = ['do_it']


    @admin.action(description='Migrate')
    def do_it(self, request, queryset):
        self.message_user(request, "books successfully marked as published.", messages.SUCCESS)


    def response_change(self, request, obj):
        if "execute" in request.POST:
            if not obj.was_executed_before:
                try:
                    obj.execute()
                    obj.was_executed_before = True
                    sleep(3)
                    obj.save()
                except (ValueError, TypeError):
                    pass
            else:
                    obj.execute()
                    sleep(3)
                    obj.save()
            self.message_user(request, 'Выполнено',messages.SUCCESS)
            return redirect(".")
        return super().response_change(request, obj)

