import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import logging
import re
import os

# Email configuration
SENDER_EMAIL = "priyadharshan.27csb@licet.ac.in"  # Your Google Workspace email
APP_PASSWORD = os.getenv("APP_PASSWORD")  # App-specific password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Email template (HTML for bold formatting)
EMAIL_SUBJECT = "You're Invited to LICET Alumni Meet 2025! 🎉"
EMAIL_BODY_HTML = """
<html>
<body>
<p>Dear {name},</p>

<p>Warmest greetings from your LICET Alumni Office! 🥰</p>

<p>We’re thrilled to personally invite <i>you</i> to the <b>11th LICET Alumni Meet 2025</b>, happening on <b>Friday, August 15, 2025</b>, at our beloved LICET Campus in Chennai. 🌟</p>

<p>This year’s theme, <b>“Timeless Bonds, Endless Journeys,”</b> celebrates the unbreakable connections we forged at LICET and the incredible paths you’ve traveled since graduation. It’s a chance to come home, reconnect, and make new memories with your LICET family! 💙</p>

<p>This year is extra special as we:</p>
<ul>
    <li>🎂 Celebrate the <b>10th anniversary</b> of LICET’s second graduating batch (2011–2015)</li>
    <li>🤝 Reconnect with friends, faculty, and mentors who shaped your journey</li>
    <li>🎈 Enjoy fun activities, shared stories, and celebrations of our alumni legacy</li>
</ul>

<p>Your presence will light up this reunion and make it unforgettable! 🫶 Please spread the word to your batchmates so we can make this gathering as vibrant as ever. 🚀</p>

<p><b>Save the Date</b>: August 15, 2025<br>
Stay tuned for the detailed schedule and registration info. For now, kindly confirm your presence and update your current status via this link:<br>
👉 <a href="https://forms.gle/vfTJnGyUt43aLbLU8">Register Here</a></p>

<p>We can’t wait to welcome you back to your alma mater with open hearts! 🏫✨</p>

<p>Warmest regards,<br>
<b>LICET Alumni Office</b><br>
#ForeverLICET 💖</p>
</body>
</html>
"""

# Plain text fallback for clients that don't support HTML
EMAIL_BODY_PLAIN = """
Dear {name},

Warmest greetings from your LICET Alumni Office!

We’re thrilled to personally invite you to the 11th LICET Alumni Meet 2025, happening on Friday, August 15, 2025, at our beloved LICET Campus in Chennai.

This year’s theme, “Timeless Bonds, Endless Journeys,” celebrates the unbreakable connections we forged at LICET and the incredible paths you’ve traveled since graduation. It’s a chance to come home, reconnect, and make new memories with your LICET family!

This year is extra special as we:
- Celebrate the 10th anniversary of LICET’s second graduating batch (2011–2015)
- Reconnect with friends, faculty, and mentors who shaped your journey
- Enjoy fun activities, shared stories, and celebrations of our alumni legacy

Your presence will light up this reunion and make it unforgettable! Please spread the word to your batchmates so we can make this gathering as vibrant as ever.

Save the Date: August 15, 2025
Stay tuned for the detailed schedule and registration info. For now, kindly confirm your presence and update your current status via this link:
[Register Here](https://forms.gle/vfTJnGyUt43aLbLU8)

We can’t wait to welcome you back to your alma mater with open hearts!

Warmest regards,
LICET Alumni Office
#ForeverLICET
"""

# Set up logging
logging.basicConfig(
    filename="email_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def is_valid_email(email):
    """Validate email address using a regex."""
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(email and re.match(email_pattern, email))


def send_email(recipient_email, recipient_name):
    """Send a personalized email to the recipient."""
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = EMAIL_SUBJECT

    # Personalize the email body
    personalized_body_html = EMAIL_BODY_HTML.format(name=recipient_name)
    personalized_body_plain = EMAIL_BODY_PLAIN.format(name=recipient_name)

    # Attach plain text and HTML versions
    msg.attach(MIMEText(personalized_body_plain, "plain"))
    msg.attach(MIMEText(personalized_body_html, "html"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        logging.info(f"Email sent successfully to {recipient_name} ({recipient_email})")
        print(f"Email sent successfully to {recipient_name} ({recipient_email})")
    except Exception as e:
        logging.error(
            f"Failed to send email to {recipient_name} ({recipient_email}): {str(e)}"
        )
        print(f"Failed to send email to {recipient_name} ({recipient_email}): {str(e)}")


def main():
    csv_file = "test_data.csv"  # CSV file path
    sent_emails = set()  # Track sent emails to avoid duplicates

    # Verify file exists
    if not os.path.exists(csv_file):
        logging.error(f"Error: The file {csv_file} was not found.")
        print(f"Error: The file {csv_file} was not found.")
        return

    try:
        with open(csv_file, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            # Log and print headers for debugging
            logging.info(f"CSV Headers: {reader.fieldnames}")
            print(f"CSV Headers: {reader.fieldnames}")

            # Verify required columns
            required_columns = {"Name", "Email"}
            missing_columns = required_columns - set(
                field for field in reader.fieldnames if field
            )
            if missing_columns:
                logging.error(f"Missing required columns in CSV: {missing_columns}")
                print(f"Missing required columns in CSV: {missing_columns}")
                return

            for row in reader:
                try:
                    name = row["Name"].strip()
                    email = row["Email"].strip()
                except KeyError as e:
                    logging.error(f"KeyError: {str(e)} in row {row}")
                    print(f"Error: Missing column {str(e)} in row {row}")
                    continue

                # Skip if no email or invalid email
                if not email or not is_valid_email(email):
                    logging.warning(
                        f"Skipping {name}: Invalid or missing email ({email})"
                    )
                    print(f"Skipping {name}: Invalid or missing email ({email})")
                    continue

                # Skip if email was already processed
                if email in sent_emails:
                    logging.info(f"Skipping duplicate email for {name}: {email}")
                    print(f"Skipping duplicate email for {name}: {email}")
                    continue

                # Send email
                send_email(email, name)
                sent_emails.add(email)

    except FileNotFoundError:
        logging.error(f"Error: The file {csv_file} was not found.")
        print(f"Error: The file {csv_file} was not found.")
    except Exception as e:
        logging.error(f"Error reading CSV file: {str(e)}")
        print(f"Error reading CSV file: {str(e)}")


if __name__ == "__main__":
    main()
