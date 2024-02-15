from fastapi import APIRouter
import sys
sys.path.append('C:\Wappnet\Tasks\Project_flaskapi\Authentication_module')
from models import VerifyOtp
import json
from utils import generate_verification_token


route4 = APIRouter()
    
@route4.post('/verify_otp')
async def verify_otp_and_generate_token(user_data: VerifyOtp):
    email = user_data.email
    verification_code = user_data.verification_code
    
    if not email:
        return {"error":"Please provide your email address."}
    
    if not verification_code:
        return {"error":"Please provide the OTP received on your email."}
    
    # Load users from JSON file
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        return {"error": "User data not found"}

    # Find the user with the provided email
    user = next((user for user in users if user['email'] == email), None)
    if not user:
        return {"error": "User not found"}

    # Get the user_id
    user_id = user['user_id']

    # Load activation OTP data from JSON file
    try:
        with open('activationotp.json', 'r') as f:
            activation_data = json.load(f)
    except FileNotFoundError:
        return {"error": "Activation data not found"}

    # Check if the user_id and verification code match any entry in activation data
    for entry in activation_data:
        if entry['user_id'] == user_id and entry['verification_code'] == verification_code:
            # If match found, generate a verification token

            # Generate a verification token
            verification_token = generate_verification_token()

            # Load activation data from JSON file
            try:
                with open("activationtoken.json", "r") as f:
                    activation_data = json.load(f)
            except FileNotFoundError:
                activation_data = []

            # Check if the user_id already exists in activation data
            user_exists = False
            for entry in activation_data:
                if entry["user_id"] == user_id:
                    entry["verification_token"] = verification_token
                    user_exists = True
                    break

            # If user_id doesn't exist in activation data, append a new entry
            if not user_exists:
                activation_data.append({"user_id": user_id, "verification_token": verification_token})

            # Save updated activation data back to JSON file
            with open("activationtoken.json", "w") as f:
                json.dump(activation_data, f, indent=4)

            # Print the token
            print(f"Verification token: {verification_token}")

            return {"message": "Token generated successfully", "verification_token": verification_token}

    # If no match found, return error message
    return {"error": "Incorrect verification code or user ID"}