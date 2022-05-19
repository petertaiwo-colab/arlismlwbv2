from django.core.mail import send_mail


def sendcode(email, passcode):
    message_name = 'Registration Passcode for MSU Machine Learning Workbench'
    message = 'Passcode:  '+passcode
    message_email = 'peter.pstaiwo@gmail.com'
    send_mail(
        message_name,
        message,
        message_email,
        [email],
    )