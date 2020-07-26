from __future__ import absolute_import, unicode_literals
from celery import task

from polls.models import Question
from django.utils import timezone
from datetime import datetime

@task()
def task_number_one():
	print('gygomd')
	q_text = "Is the time {}{}".format(datetime.now(), '?')
	q = Question(question_text = q_text, pub_date=timezone.now())
	q.save()
	print(q_text)
	print("The question has been saved.")