import datetime

from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


# отправка сообщения для подписчика при создании новой статьи
@shared_task
def send_mail_subscriber(pk, preview=None):
    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    subscribers: list[str] = []
    title = post.title
    for category in categories:
        subscribers += category.subscribers.all()
    subscribers_emails = [s.email for s in subscribers]

    html_context = render_to_string(
        'email/post_created_email.html',
        {
            'text': preview,
            'Link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    # отправка письма
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


# еженедельная рассылка сообщений
@shared_task
def send_weekly_mail():
    start_date = datetime.datetime.today() - datetime.timedelta(days=6)
    this_weeks_posts = Post.objects.filter(post_time__gt=start_date)
    for cat in Category.objects.all():
        post_list = this_weeks_posts.filter(post_category=cat)
        if post_list:
            subscribers = cat.subscribers.values('username', 'email')
            recipients = []
            for sub in subscribers:
                recipients.append(sub['email'])

            html_content = render_to_string(
                'email/daily_post.html', {
                    'link': f'{settings.SITE_URL}/news',
                    'posts': post_list,
                }
            )
            # отправка письма
            msg = EmailMultiAlternatives(
                subject=f'Категория - {cat.name}',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
