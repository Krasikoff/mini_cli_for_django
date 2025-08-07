from django.contrib import admin
from django.shortcuts import redirect

from .models import Rule


class RuleAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        if "execute" in request.POST:
            if not obj.was_executed_before:
                try:
                    obj.execute()
                    obj.was_executed_before = True
                    obj.save()
                except (ValueError, TypeError):
                    pass
            return redirect(".")
        return super().response_change(request, obj)


admin.site.register(Rule, RuleAdmin)
