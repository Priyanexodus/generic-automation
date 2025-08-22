import pyotp
import csv

CSV_FILE = "secrets.csv"


def get_secret(app_name, username):
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["app_name"] == app_name and row["username"] == username:
                return row["secret"]
    return None


def verify_otp(app_name, username, otp_input):
    secret = get_secret(app_name, username)
    if not secret:
        print("❌ No secret found for this app/user.")
        return False

    totp = pyotp.TOTP(secret)
    if totp.verify(otp_input):
        print("✅ OTP Verified Successfully!")
        return True
    else:
        print("❌ Invalid OTP. Try again.")
        return False


if __name__ == "__main__":
    app_name = input("Enter App Name: ")
    username = input("Enter Username: ")
    otp = input("Enter OTP from Google Authenticator: ")
    verify_otp(app_name, username, otp)
