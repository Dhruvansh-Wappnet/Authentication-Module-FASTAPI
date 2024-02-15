from fastapi import APIRouter
import sys
sys.path.append('C:\Wappnet\Tasks\Project_flaskapi\Authentication_module')
from models import ResetPassword
import hashlib
import json


route5 = APIRouter()
    
@route5.post('/reset_password')
async def reset_password(user_data: ResetPassword):
    verification_token = user_data.verification_token
    new_password = user_data.new_password
    
    # Load activation token data from JSON file
    try:
        with open("activationtoken.json", "r") as f:
            activation_data = json.load(f)
    except FileNotFoundError:
        return {"error": "Activation token database not found"}

    # Check if the token matches any entry in activation data
    token_matched = False
    user_id = None
    for entry in activation_data:
        if entry["verification_token"] == verification_token:
            token_matched = True
            user_id = entry["user_id"]
            break

    if not token_matched or not user_id:
        return {"error": "Invalid or expired token"}

    # Load users from JSON file
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        return {"error": "User database not found"}

    # Find the user with the provided user_id
    user = next((user for user in users if user["user_id"] == user_id), None)
    if not user:
        return {"error": "User not found"}

    # Hash the new password
    hashed_new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

    # Update the password for the user
    user["password"] = hashed_new_password

    # Save the updated users back to the JSON file
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

    # Empty the activation token data
    with open("activationtoken.json", "w") as f:
        json.dump([], f)

    return {"message": "Password reset successfully"}