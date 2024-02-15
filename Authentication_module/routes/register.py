import sys
sys.path.append('C:\Wappnet\Tasks\Project_flaskapi\Authentication_module')
from models import UserRegistration
from fastapi import APIRouter
import re
from utils import save_users_to_json, load_users_from_json
import hashlib


route1 = APIRouter()
    
users = load_users_from_json()
    
@route1.post("/register")
async def register(user_data : UserRegistration):
    username = user_data.username
    email = user_data.email
    password = user_data.password
    
    # Validate input data
    if not username or not email or not password:
        return {"error": "Please provide missing username, email, or password"}
    
    # # Validate email format
    # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    #     return {"error": "Invalid email format"}
    
    # Check if the username is already taken
    if any(user["username"] == username for user in users):
        return {"error": "User with this username already exists"}
    
    # Check if the user with the email already exists
    if any(user["email"] == email for user in users):
        return {"error": "User with this email already exists"}
    
    user_id = len(users) + 1
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    # Create a user instance using the model
    user_data = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "password": hashed_password
    }
    users.append(user_data)

    # Save new user to file
    save_users_to_json(users)
    
    return {"message" : "User registered successfully"}
    
    