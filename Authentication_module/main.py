from fastapi import FastAPI
from routes.register import route1 as register_router
from routes.login import route2 as login_router
from routes.forget_password import route3 as forget_password_router
from routes.verify_otp import route4 as verify_otp_router
from routes.reset_password import route5 as reset_password_router
        
authentication = FastAPI()

authentication.include_router(register_router)
authentication.include_router(login_router)
authentication.include_router(forget_password_router)
authentication.include_router(verify_otp_router)
authentication.include_router(reset_password_router)