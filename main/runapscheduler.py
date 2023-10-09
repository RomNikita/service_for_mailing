from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from main.models import Mailing, LogsOfMailing

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def send_mailing(mailing_id, recipients):
    try:
        mailing = Mailing.objects.get(pk=mailing_id)
        recipients = mailing.client.values_list('email', flat=True)
        subject = mailing.message.subject_of_letter
        body = mailing.message.body_of_letter
        print("Recipients:", recipients)
        send_mail(subject, body, 'noreplyskypro9@gmail.com', recipients)

        mailing.status = f"активна"
        mailing.save()

        log = LogsOfMailing(date=timezone.now(), status=True, answer_from_service="Успешно отправлено",
                            message=mailing.message)
        log.save()
    except Exception as e:
        mailing.status = "ошибка"
        mailing.save()
        log = LogsOfMailing(date=timezone.now(), status=False, answer_from_service=str(e), message=mailing.message)
        log.save()


class DailyTrigger:
    pass


def schedule_mailing(mailing_id, send_date, frequency, recipients):
    if frequency == 'один раз в день':
        trigger = CronTrigger(hour=send_date.hour, minute=send_date.minute, day_of_week="*", day="*")
    elif frequency == 'один раз в неделю':
        trigger = CronTrigger(day_of_week=send_date.strftime('%a'), hour=send_date.hour, minute=send_date.minute)
    elif frequency == 'один раз в месяц':
        trigger = CronTrigger(day=send_date.day, hour=send_date.hour, minute=send_date.minute)

    scheduler.add_job(send_mailing, trigger=trigger, args=[mailing_id, recipients])


scheduler.start()
