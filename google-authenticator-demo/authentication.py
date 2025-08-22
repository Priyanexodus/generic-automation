import pyotp
import qrcode
import csv
import os

CSV_FILE = "secrets.csv"


# Save secret into CSV
def save_secret(appname, username, secret):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["app_name", "username", "secret"])
        writer.writerow([appname, username, secret])


# Load secret by appname
def get_secret(appname, username):
    if not os.path.isfile(CSV_FILE):
        return None
    with open(CSV_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["app_name"] == appname and row["username"] == username:
                return row["secret"]
    return None


# Function to create QR and store secret
def create_qr(username="user@example.com", appname="MyApp"):
    # Generate secret
    secret = pyotp.random_base32()
    print(f"Generated secret for {username} in {appname}")

    # Generate provisioning URI
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name=appname)

    # Save QR code
    filename = f"{appname}_{username}_qr.png".replace("@", "_")
    qrcode.make(uri).save(filename)
    print(f"✅ QR code saved as {filename}. Scan it in Google Authenticator.")

    # Save secret in CSV
    save_secret(appname, username, secret)
    print(f"✅ Secret saved in {CSV_FILE}")


# Function to verify code using stored secret
def verify_code(appname, username):
    secret = get_secret(appname, username)
    if not secret:
        print("❌ No secret found for given app and user.")
        return

    totp = pyotp.TOTP(secret)
    user_code = input("Enter the 6-digit code from Google Authenticator: ")

    if totp.verify(user_code):
        print("✅ Authentication successful!")
    else:
        print("❌ Invalid code. Try again.")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("1. Create QR code")
    print("2. Verify code")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        app = input("Enter app name: ")
        user = input("Enter username/email: ")
        create_qr(user, app)
    elif choice == "2":
        app = input("Enter app name: ")
        user = input("Enter username/email: ")
        verify_code(app, user)
    else:
        print("Invalid choice.")
