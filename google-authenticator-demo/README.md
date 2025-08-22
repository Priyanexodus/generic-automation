🔐 Google Authenticator Integration (Python + CSV Storage)
📖 Description

This project demonstrates how to use Google Authenticator with a Python program to enable Two-Factor Authentication (2FA).

It uses TOTP (Time-based One-Time Passwords) to generate 6-digit codes that refresh every 30 seconds.

Users scan a QR code to add the account in their Google Authenticator app.

During login or verification, users provide the 6-digit code from the app, which is validated against the stored secret key.

Secret keys are stored securely in a CSV file with the app name and username for reuse.

This ensures that even if a password is leaked, attackers cannot access the system without the Authenticator code.

⚙️ Workflow
Step 1: Setup & Secret Key Generation

User registers with an app name and username.

Program generates a secret key.

Program creates a QR code that the user scans with Google Authenticator.

Secret is stored in secrets.csv.

📂 Example:

app_name,username,secret
MyApp,user@example.com,JBSWY3DPEHPK3PXP

Step 2: Authentication / Verification

User logs in and provides their username, app name, and 6-digit OTP from Google Authenticator.

Program retrieves the secret from secrets.csv.

Program uses the secret to generate the expected OTP.

If user’s OTP matches → ✅ Authentication successful. Otherwise → ❌ Invalid code.

🔄 Visual Workflow
           ┌───────────────┐
           │  User Signup   │
           └───────┬───────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Generate Secret Key │
        └───────┬────────────┘
                │
                ▼
       ┌─────────────────────┐
       │ Generate QR Code    │
       │ User scans in app   │
       └───────┬────────────┘
               │
     Save secret in secrets.csv
               │
               ▼
    ┌───────────────────────────────┐
    │         User Login            │
    └───────────┬──────────────────┘
                │
                ▼
   ┌─────────────────────────────┐
   │ Enter OTP from Authenticator│
   └───────────┬────────────────┘
               │
               ▼
      ┌──────────────────────┐
      │ Verify with Secret   │
      └───────────┬─────────┘
                  │
       ┌──────────┴─────────┐
       ▼                    ▼
  ✅ Success          ❌ Invalid Code


👉 This way, you clearly separate:

Enrollment phase (QR + secret storage)

Verification phase (OTP validation)