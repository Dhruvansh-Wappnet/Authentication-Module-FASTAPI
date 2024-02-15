import json
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to load the data from JSON file
def load_users_from_json():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save users to JSON file
def save_users_to_json(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# Function to generate otp
def generate_otp():
    return "".join(random.choices(string.digits, k=6))

# Function to save activation OTP data to JSON file
def save_activation_otp_to_json(data):
    try:
        with open("activationotp.json", "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # Check if user_id exists in the existing data
    for entry in existing_data:
        if entry["user_id"] == data["user_id"]:
            entry["verification_code"] = data["verification_code"]
            break
    else:
        existing_data.append(data)

    with open("activationotp.json", "w") as f:
        json.dump(existing_data, f, indent=4)
        
# Function to send mails
def send_email(receiver_email, subject, message):
    sender_email = ""  # Replace with your email address
    password = ""  # Replace with your email password

    # Create a MIMEText object to represent the email content
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject
    email_message.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        # Log in to the SMTP server
        server.login(sender_email, password)
        # Send the email
        server.send_message(email_message)
        
def generate_verification_token():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))
