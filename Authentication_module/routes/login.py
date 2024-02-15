from fastapi import APIRouter
import sys
sys.path.append('C:\Wappnet\Tasks\Project_flaskapi\Authentication_module')
from models import UserLogin
import hashlib
from utils import load_users_from_json

route2 = APIRouter()

    
@route2.post("/login")
async def login(user_data: UserLogin):
    username = user_data.username
    password  = user_data.password
    
    # Validate input data
    if not username or not password:
        return {"message": "Missing username or password"}
    
    users = load_users_from_json()
    for user in users:
        if user["username"] == username:
            # Decode the hashed password from the JSON file
            hashed_password = user["password"]

            # Hash the provided password for comparison
            hashed_input_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # Compare the hashed passwords
            if hashed_password == hashed_input_password:
                return {"message": "Login successful"}
            else:
                return {"error": "Invalid password"}
            
    # If username not found, return error message
    return {"error": "Invalid username"}