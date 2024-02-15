from pydantic import BaseModel, EmailStr

# Pydantic model to represent user registration data
class UserRegistration(BaseModel):
    username : str
    email    : EmailStr  # EmailStr enforces email format validation
    password : str
    
# Pydantic model to represent user login data
class UserLogin(BaseModel):
    username: str
    password: str
    
# Pydantic model to represent forget password details
class Forget_Password(BaseModel):
    email : EmailStr
    
# Pydantic model to represent otp verification    
class VerifyOtp(BaseModel):
    email : EmailStr
    verification_code : str
    
# Pydantic model to represent Reset Password data   
class ResetPassword(BaseModel):
    verification_token : str
    new_password : str
    
    