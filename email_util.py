import smtplib
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR.joinpath("TEMPLATE")


def send_email(smtp_server="", send_to_email="", fileToSend="export.csv"):
    """
    Send Email Notification
    """
    date_time = datetime.now().strftime("%m-%d-%Y_%H.%M.%S")

    from_email = "noreply@presidio.com"
    subject = "cucm-exporter job has completed"

    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = send_to_email
    msg["Subject"] = subject

    with open(TEMPLATES_DIR / "email-template.html", "r") as myfile:
        messageHTML = myfile.read().replace("\n", "").replace(r"{date_time}", date_time)

    messagePlain = f"""
        cucm-exporter has completed a job at {date_time}...

        Regards,
        The cucm admin team
        """

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)

    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    msg.attach(MIMEText(messagePlain, "plain"))
    msg.attach(MIMEText(messageHTML, "html"))

    try:
        server = smtplib.SMTP(smtp_server, 25)
    except Exception as e:
        return e.errno, e.strerror
    text = msg.as_string()
    try:
        server.sendmail(from_email, send_to_email, text)
        return "success"
    except Exception as e:
        return e.errno, e.strerror
    server.quit()


if __name__ == "__main__":
    email_send_status = send_email(
        smtp_server="mail.presidio.com",
        send_to_email="bradh@presidio.com",
        fileToSend="export.csv",
    )
    print(email_send_status)
