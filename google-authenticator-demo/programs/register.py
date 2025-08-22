import pyotp
import qrcode
import csv
import os

CSV_FILE = "secrets.csv"


def register_user(app_name, username):
    # Generate a secret key
    secret = pyotp.random_base32()

    # Create provisioning URI (for Google Authenticator)
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name=app_name)

    # Generate QR Code
    qr = qrcode.make(uri)
    qr_filename = f"./qrs-imgs/{app_name}_{username}_qr.png"
    qr.save(qr_filename)
    print(f"[+] QR code saved as {qr_filename}. Scan it with Google Authenticator.")

    # Save secret to CSV
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["app_name", "username", "secret"])
        writer.writerow([app_name, username, secret])

    print(f"[+] Secret stored for {username} in {CSV_FILE}")


if __name__ == "__main__":
    app_name = input("Enter App Name: ")
    username = input("Enter Username (e.g. email): ")
    register_user(app_name, username)
