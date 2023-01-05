from django_cron import CronJobBase, Schedule
from app.rest.models import AccountModel


class UpdateSessionTask(CronJobBase):
    code = 'app.rest.cron.update_session'

    schedule = Schedule(run_every_mins=3)

    def do(self):
        accounts = AccountModel.objects.filter(active=True)

        for account in accounts:
            session = account.new_session()

            if session:
                print(f'>> Session #{session} has been created for {account}')
            else:
                print(f'>> Failed to update session for {account}')
