from django.contrib import admin
from user.models import WinUser, WinUserGrade


class WinUserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "user_grade",
        "user_passwd",
        "user_name",
        "user_email",
        "user_tel",
        "user_reg_date",
        "user_point",
    )


class WinUserGradeAdmin(admin.ModelAdmin):
    list_display = ("user_grade", "user_grade_name")


admin.site.register(WinUser, WinUserAdmin)
admin.site.register(WinUserGrade, WinUserGradeAdmin)
