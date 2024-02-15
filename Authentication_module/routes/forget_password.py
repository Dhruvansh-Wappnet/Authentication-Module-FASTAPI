from fastapi import APIRouter
import sys
sys.path.append('C:\Wappnet\Tasks\Project_flaskapi\Authentication_module')
from models import Forget_Password
from utils import generate_otp, load_users_from_json, save_activation_otp_to_json, send_email

route3 = APIRouter()

    
@route3.post("/forget_password")
async def forget_password(user_data: Forget_Password):
    email = user_data.email
    
    users = load_users_from_json()

    user = next((user for user in users if user["email"] == email), None)
    if user:
        # Generate a verification code
        verification_code = generate_otp()

        # Save user ID and verification code to JSON file
        activation_data = {
            "user_id": user["user_id"],
            "verification_code": verification_code,
        }
        save_activation_otp_to_json(activation_data)

        # Send verification code to the user's email
        send_email(
            email,
            "Forget Password Verification Code",
            f"Your verification code is: {verification_code}",
        )

        # Return success message
        return {"message": "Verification code sent successfully"}
    else:
        return {"error": "Email not found in the database"}
    