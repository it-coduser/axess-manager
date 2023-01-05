from app.rest.models import AccountModel, SessionModel, RequestModel
from django_cron.models import CronJobLock, CronJobLog
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib import admin

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(CronJobLog)
admin.site.unregister(CronJobLock)
admin.site.site_title = 'Control Panel'
admin.site.site_header = 'AXESS Manager'
admin.site.index_title = 'Krasnaya Polyana'


@admin.register(AccountModel)
class AccountAdmin(admin.ModelAdmin):
    @admin.action(description='Create a new session')
    def create_session(self, request, accounts):
        for account in accounts:
            session = account.new_session()

            if session:
                self.message_user(
                    request, f'Session #{session} has been created for {account}', messages.SUCCESS)
            else:
                self.message_user(
                    request, f'Failed to create a new session for {account}', messages.ERROR)

    list_filter = ['active', 'last_request']
    readonly_fields = ['access_token']
    actions = ['create_session']
    list_display = [
        'name', 'access_token', 'session',
        'last_request', 'active'
    ]
    fieldsets = [
        [None, {
            'classes': ['wide'],
            'fields': ['active', 'name', 'access_token']
        }],
        ['REST options', {
            'classes': ['wide'],
            'fields': ['login_id', 'username', 'password', 'rest_url']
        }],
        ['SOAP options', {
            'classes': ['wide'],
            'fields': ['soap_username', 'soap_password']
        }],
    ]


@admin.register(SessionModel)
class SessionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, session=None):
        return False

    def has_delete_permission(self, request, session=None):
        return session.active if session else True

    @admin.action(description='Check selected sessions')
    def check_session(self, request, sessions):
        for session in sessions:
            if not session.active:
                continue

            if session.is_valid():
                self.message_user(
                    request, f'Session #{session} is available', messages.SUCCESS)
            else:
                self.message_user(
                    request, f'Session #{session} is unavailable', messages.WARNING)

    def delete_queryset(self, request, sessions):
        for session in sessions:
            session.active = False
            session.delete()
            session.save()

    def delete_model(self, request, session):
        session.active = False
        session.delete()
        session.save()

    list_display = ['account', 'session_id', 'created_at', 'active']
    actions = ['check_session']
    list_filter = ['active']
    fieldsets = [
        [None, {
            'classes': ['wide'],
            'fields': ['active', 'account', 'session_id', 'created_at']
        }],
    ]


@ admin.register(RequestModel)
class RequestAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ['method', 'session', 'ip_address', 'created_at']
    list_filter = ['ip_address', 'method', 'created_at']
    fieldsets = [
        [None, {
            'classes': ['wide'],
            'fields': ['ip_address', 'session', 'created_at']
        }],
        ['Request Data', {
            'classes': ['wide'],
            'fields': ['payload', 'response']
        }],
    ]
