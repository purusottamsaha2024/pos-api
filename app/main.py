from fastapi import FastAPI,responses, Depends,status, HTTPException
# from sqlalchemy.orm import Session
# from models import User
# from database import SessionLocal, get_db
# from passlib.context import CryptContext
# from jose import JWTError, jwt
from pydantic import BaseModel
# from datetime import timedelta, datetime
import psycopg2
from  psycopg2.extras import RealDictCursor
import datetime

SECRET_KEY = "#4521411414141414142412#"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
# Models for request and response
class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str
    rebember_token: str
    is_active: bool
    created_at:datetime
    updated_at: datetime
    

try :
    con = psycopg2.connect(host='localhost',database='pos-db', password='Gorilla.5050', user='postgres', cursor_factory=RealDictCursor)
    cursor=con.cursor()
    print('Db connection succesfull')
except Exception as error :
    print("Error :", error)

@app.get("/user/")
def get_user():
    cursor.execute("""Select* from users""")
    user =cursor.fetchall()
    print(user)
    return {"data":user}
@app.post("/createuser", status_code=status.HTTP_201_CREATED)
def post_user(createuser:UserCreate):
    cursor.execute("""INSERT INTO USERS(username,email,password_hash,rebemeber_token,is_active,created_at)values(%s,%s,%s,%s,%s,%s)RETURNING * """,
                   UserCreate.username,UserCreate.email,UserCreate.password_hash,UserCreate.rebember_token,UserCreate.is_active,UserCreate.created_at)
    new_user=cursor.fetchone()
    pass

# # Models for request and response
# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str

# class UserLogin(BaseModel):
#     username: str
#     password: str
#     remember_me: bool = False

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# # Utility Functions
# def get_password_hash(password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # API to register user
# @app.post("/register/")
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     hashed_password = get_password_hash(user.password)
#     db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return {"msg": "User created"}

# # API to login user
# @app.post("/login/", response_model=Token)
# def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == login_data.username).first()
#     if not user or not verify_password(login_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
    
#     access_token_expires = timedelta(days=7) if login_data.remember_me else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
#     return {"access_token": access_token, "token_type": "bearer"}
##Ja bal bhai k