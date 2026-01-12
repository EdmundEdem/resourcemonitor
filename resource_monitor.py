import psutil
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# -------------------------
# CONFIGURATION
# -------------------------
CPU_THRESHOLD = 50
MEM_THRESHOLD = 50
DISK_THRESHOLD = 50

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "baobabsysmonitor@gmail.com"
EMAIL_PASSWORD = "ymwv inny ujew dkvp"
EMAIL_RECEIVER = "sheikhmoves@gmail.com"

LOG_FILE = "/var/log/resource_monitor.log"

# -------------------------
# LOGGING SETUP
# -------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# -------------------------
# EMAIL FUNCTION
# -------------------------
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        logging.info("Alert email sent successfully.")

    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# -------------------------
# RESOURCE CHECK FUNCTION
# -------------------------
def check_resources():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent

        logging.info(
            f"Usage - CPU: {cpu_usage}%, Memory: {mem_usage}%, Disk: {disk_usage}%"
        )

        alerts = []

        if cpu_usage > CPU_THRESHOLD:
            alerts.append(f"CPU usage is high: {cpu_usage}%")

        if mem_usage > MEM_THRESHOLD:
            alerts.append(f"Memory usage is high: {mem_usage}%")

        if disk_usage > DISK_THRESHOLD:
            alerts.append(f"Disk usage is high: {disk_usage}%")

        if alerts:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            subject = "🚨 Server Resource Alert"
            body = f"Time: {timestamp}\n\n" + "\n".join(alerts)

            logging.warning("ALERT TRIGGERED: " + " | ".join(alerts))
            send_email(subject, body)

    except Exception as e:
        logging.error(f"Monitoring error: {e}")

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    logging.info("Resource monitor started.")
    check_resources()
