from celery import Celery

app = Celery('tasks',
             broker='pyamqp://',
             backend='rpc://',
             include=['tasks'])

@app.task
def add(x, y):
    return x + y
