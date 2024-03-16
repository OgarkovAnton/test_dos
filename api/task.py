from celery import Celery
import requests

app = Celery("celery_app", broker='redis://localhost:6379/1')


@app.task(name='send_request', bind=True, rate_limit='8/s')
def send_request_task(self):
    resp = requests.post('https://chatbot.com/webhook', headers={'X-Celery-ID': self.request.id})
    print(resp.text)
