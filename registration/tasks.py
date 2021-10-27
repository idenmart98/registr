from main.celery import app


@app.task()
def send_verified_link(email, code):
    return send_mail(
        'Email verification',
        f'Confirm your registartion 127.0.0.1:8000/register/confirm/{code}/',
        settings.EMAIL_FROM,
        [email, ]
    )

@app.task()
def add(x, y):
    print(x+y)
    return x+y