from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from user_account.models import SimpleUsers


class SimpleUsersInLine(admin.StackedInline):
    model = SimpleUsers
    can_delete = False


class SimpleUsersAdmin(UserAdmin):
    inlines = (SimpleUsersInLine, )

    list_display = ('username', 'email', 'first_name', 'last_name', )
    search_fields = ('username', 'email', 'first_name', 'last_name', )
    list_filter = ('first_name', 'last_name', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(SimpleUsersAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, SimpleUsersAdmin)
