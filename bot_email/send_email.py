import smtplib, ssl

def SendEmail(data):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = ""  # Enter your address
    receiver_email = ""  # Enter receiver address
    password = ''
    message = """\
    Subject: GPU Stock Alert

    This message is sent from Python: The bot find some potential available gpus -->""" + " ".join(str(elem) for elem in data)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
