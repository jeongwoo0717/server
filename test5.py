from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
from pyfcm import FCMNotification
import databases
import sqlalchemy

# FastAPI 앱 생성
app = FastAPI()

# Firebase API Key
API_KEY = "AAAAtcoGVnw:APA91bEIV8dcPAa4cnAyXbCMPp_T6EVqRZ3bsiaKYtY8GKIir2a8J5f2XV9iovAtNsvAe91rjnIif-DRftrboRG99MG337Ts3HFsfg3Yu__xHzbugFZmNG3ymJzeL4zNrnDB3kurHfTI"

# Initialize FCMNotification object
push_service = FCMNotification(API_KEY)

# SQLAlchemy 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

# 모델 정의

class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    
class User1(Base):
    __tablename__ = "users1"

    id = Column(Integer, primary_key=True, index=True)
    check = Column(String, index=True)
    day = Column(String, index=True)
    date = Column(Date, unique=True)

class User2(Base):
    __tablename__ = "users2"

    id = Column(Integer, primary_key=True, index=True)
    check = Column(String, index=True)
    day = Column(String, index=True)
    date = Column(Date, unique=True)

class User3(Base):
    __tablename__ = "users3"

    id = Column(Integer, primary_key=True, index=True)
    time_range = Column(String)
    date = Column(Date, unique=True)

# 엔진 생성 및 테이블 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DTO
class TokenDto(BaseModel):
    token: str
    
# 요청/응답 모델 정의
class UserCreate(BaseModel):
    check: str
    day: str
    date: str

# 데이터베이스 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스에 사용자를 생성하는 API 엔드포인트 (첫 번째 데이터베이스 테이블)
@app.post("/users1")
def create_user1(check: str, day: str, date: str, db: Session = Depends(get_db)):
    try:
        # 문자열 형태의 날짜를 Python의 datetime 객체로 변환
        parsed_date = datetime.strptime(date, "%Y%m%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Date should be in 'YYYYMMDD' format.")
    
    # 새로운 사용자 생성
    new_user = User1(check=check, day=day, date=parsed_date)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/users2")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Convert string date to Python datetime object
        parsed_date = datetime.strptime(user_data.date, "%Y%m%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Date should be in 'YYYYMMDD' format.")

    # Create new user
    new_user = User2(check=user_data.check, day=user_data.day, date=parsed_date)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/users2.5")
def create_user2(check: str, day: str, date: str, db: Session = Depends(get_db)):
    try:
        # 문자열 형태의 날짜를 Python의 datetime 객체로 변환
        parsed_date = datetime.strptime(date, "%Y%m%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Date should be in 'YYYYMMDD' format.")
    
    # 새로운 사용자 생성
    new_user = User2(check=check, day=day, date=parsed_date)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 데이터베이스에 사용자를 생성하는 API 엔드포인트 (세 번째 데이터베이스 테이블)
@app.post("/users3")
def create_user3(time_range: str, date: str, db: Session = Depends(get_db)):
    try:
        # 문자열 형태의 날짜를 Python의 datetime 객체로 변환
        parsed_date = datetime.strptime(date, "%Y%m%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Date should be in 'YYYYMMDD' format.")
    
    new_user = User3(time_range=time_range, date=parsed_date)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 데이터베이스의 사용자를 조회하는 API 엔드포인트 (첫 번째 데이터베이스 테이블)
@app.get("/users1")
def read_users1(db: Session = Depends(get_db)):
    return db.query(User1).all()

# 데이터베이스의 사용자를 조회하는 API 엔드포인트 (두 번째 데이터베이스 테이블)
@app.get("/users2")
def read_users2(db: Session = Depends(get_db)):
    return db.query(User2).all()

# 데이터베이스의 사용자를 조회하는 API 엔드포인트 (세 번째 데이터베이스 테이블)
@app.get("/users3")
def read_users3(db: Session = Depends(get_db)):
    return db.query(User3).all()

# 데이터베이스의 특정 사용자를 상세 조회하는 API 엔드포인트 (첫 번째 데이터베이스 테이블)
@app.get("/users1/{user_id}")
def read_user1(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User1).filter(User1.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 데이터베이스의 특정 사용자를 상세 조회하는 API 엔드포인트 (두 번째 데이터베이스 테이블)
@app.get("/users2/{user_id}")
def read_user2(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User2).filter(User2.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 데이터베이스의 특정 사용자를 상세 조회하는 API 엔드포인트 (세 번째 데이터베이스 테이블)
@app.get("/users3/{user_id}")
def read_user3(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User3).filter(User3.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 데이터베이스의 특정 사용자를 삭제하는 API 엔드포인트 (첫 번째 데이터베이스 테이블)
@app.delete("/users1/{user_id}")
def delete_user1(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User1).filter(User1.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted successfully"}

# 데이터베이스의 특정 사용자를 삭제하는 API 엔드포인트 (두 번째 데이터베이스 테이블)
@app.delete("/users2/{user_id}")
def delete_user2(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User2).filter(User2.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted successfully"}

# 데이터베이스의 특정 사용자를 삭제하는 API 엔드포인트 (세 번째 데이터베이스 테이블)
@app.delete("/users3/{user_id}")
def delete_user3(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User3).filter(User3.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted successfully"}

# 클라이언트로부터 받은 토큰을 DB에 저장하는 엔드포인트
@app.post("/save_token")
async def save_token(dto: TokenDto):
    query = Token.__table__.insert().values(token=dto.token)
    await database.execute(query)
    return {"message": "Token saved successfully"}

# 클라이언트로부터 받은 토큰을 사용하여 알람을 보내는 엔드포인트
@app.post("/send_notification")
async def send_notification(body: str, title: str):
    query = Token.__table__.select()
    results = await database.fetch_all(query)
    all_tokens = [result["token"] for result in results]

    if not all_tokens:
        raise HTTPException(status_code=404, detail="No tokens found in database")

    # 모든 토큰에 대해 알림 전송 시도
    success_count = 0
    for db_token in all_tokens:
        result = push_service.notify_single_device(registration_id=db_token, message_body=body, message_title=title)
        if result.get("success", 0) == 1:
            success_count += 1

    if success_count > 0:
        return {"message": f"Notification sent to {success_count} device(s) successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send notification to any device")
