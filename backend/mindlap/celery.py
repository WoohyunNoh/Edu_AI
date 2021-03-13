from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindlap.settings')  # 주의
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('mindlap')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# if __name__ == '__main__':
#     app.start()
