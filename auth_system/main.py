from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import logging
import os
import secrets

# Configuration and Environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://authuser:authpass@db:5432/authdb")
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MFA_ENABLED = True

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("auth_system")

# --- SQLAlchemy Setup ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- OAuth2 ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# --- Models ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(32), default="user")
    mfa_secret = Column(String(32), nullable=True)
    mfa_enabled = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    failed_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String(64))
    severity = Column(String(16))
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String(1024))

# --- Create Tables ---
Base.metadata.create_all(bind=engine)

# --- Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    mfa_enabled: bool
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class MFAChallenge(BaseModel):
    mfa_secret: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class UserProfileUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]

# --- Utils ---
def get_password_hash(password):
    # Strong password policy enforcement
    if len(password) < 10 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
        raise HTTPException(status_code=400, detail="Password does not meet complexity requirements")
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_security_event(user_id, event_type, severity, details):
    db = SessionLocal()
    event = SecurityEvent(user_id=user_id, event_type=event_type, severity=severity, details=details)
    db.add(event)
    db.commit()
    db.close()
    logger.info(f"Security event: {event_type} (severity={severity}) for user {user_id}: {details}")

# --- RBAC Helper ---
def require_role(roles: List[str]):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            log_security_event(user.id, "PERMISSION_DENIED", "WARN", f"Role {user.role} not in allowed roles {roles}")
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return role_checker

# --- MFA Helper ---
def generate_mfa_secret():
    return secrets.token_hex(16)

def verify_mfa_code(secret, code):
    # Placeholder for TOTP/HOTP verification (use pyotp in production)
    return code == secret[::-1][:6]  # Simulate MFA for demo purposes

# --- User Authentication ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user

# --- FastAPI App ---
app = FastAPI(title="Auth System", version="2.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# --- API Endpoints ---

# Registration
@app.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    log_security_event(new_user.id, "REGISTER", "INFO", "User registered")
    return UserOut(id=new_user.id, email=new_user.email, role=new_user.role, mfa_enabled=new_user.mfa_enabled, is_active=new_user.is_active)

# Login with rate limiting and lockout
@app.post("/auth/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.is_active:
        log_security_event(None, "LOGIN_FAIL", "WARN", f"User {form_data.username} not found or inactive")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(status_code=403, detail="Account locked. Try again later.")
    if not verify_password(form_data.password, user.hashed_password):
        user.failed_attempts += 1
        db.commit()
        log_security_event(user.id, "LOGIN_FAIL", "WARN", f"Failed login, attempts={user.failed_attempts}")
        if user.failed_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=10)
            db.commit()
            log_security_event(user.id, "ACCOUNT_LOCKED", "ERROR", "Too many failed login attempts")
            raise HTTPException(status_code=403, detail="Account locked due to multiple failed login attempts")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    user.failed_attempts = 0
    db.commit()
    # MFA challenge
    if MFA_ENABLED and user.mfa_enabled:
        mfa_secret = user.mfa_secret
        return {"access_token": "", "token_type": "mfa_challenge", "mfa_secret": mfa_secret}
    token = create_access_token(data={"sub": user.id, "role": user.role})
    log_security_event(user.id, "LOGIN_SUCCESS", "INFO", "User logged in")
    return Token(access_token=token, token_type="bearer")

# MFA Verification
@app.post("/auth/mfa_verify", response_model=Token)
def mfa_verify(email: EmailStr, code: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.mfa_enabled:
        raise HTTPException(status_code=401, detail="MFA not enabled or user not found")
    if not verify_mfa_code(user.mfa_secret, code):
        log_security_event(user.id, "MFA_FAIL", "WARN", f"Invalid MFA code")
        raise HTTPException(status_code=401, detail="Invalid MFA code")
    token = create_access_token(data={"sub": user.id, "role": user.role})
    log_security_event(user.id, "MFA_SUCCESS", "INFO", "MFA challenge passed")
    return Token(access_token=token, token_type="bearer")

# Enable MFA
@app.post("/auth/mfa_enable", response_model=MFAChallenge)
def enable_mfa(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.mfa_enabled:
        raise HTTPException(status_code=400, detail="MFA already enabled")
    mfa_secret = generate_mfa_secret()
    user.mfa_secret = mfa_secret
    user.mfa_enabled = True
    db.commit()
    log_security_event(user.id, "MFA_ENABLED", "INFO", "MFA enabled")
    # Send notification (email/SMS placeholder)
    return MFAChallenge(mfa_secret=mfa_secret)

# User Profile Update
@app.put("/users/me", response_model=UserOut)
def update_profile(update: UserProfileUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if update.email:
        user.email = update.email
    if update.password:
        user.hashed_password = get_password_hash(update.password)
    if update.role:
        user.role = update.role
    if update.is_active is not None:
        user.is_active = update.is_active
    db.commit()
    log_security_event(user.id, "PROFILE_UPDATE", "INFO", "Profile updated")
    return UserOut(id=user.id, email=user.email, role=user.role, mfa_enabled=user.mfa_enabled, is_active=user.is_active)

# Password Reset Request (token generation)
@app.post("/auth/password_reset", status_code=200)
def password_reset_request(req: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        # Do not reveal if user exists
        return {"message": "If your email exists, you will receive a reset link."}
    token = create_access_token(data={"sub": user.id, "action": "reset"}, expires_delta=timedelta(minutes=15))
    # Send notification (email placeholder)
    log_security_event(user.id, "PASSWORD_RESET_REQUEST", "INFO", "Password reset requested")
    return {"message": "If your email exists, you will receive a reset link.", "token": token}

# Password Reset Confirm
@app.post("/auth/password_reset/confirm", status_code=200)
def password_reset_confirm(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        action = payload.get("action")
        if action != "reset":
            raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    log_security_event(user.id, "PASSWORD_RESET", "INFO", "Password reset successful")
    return {"message": "Password reset successful"}

# Account Deactivation
@app.post("/users/deactivate", status_code=200)
def deactivate_account(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.is_active = False
    db.commit()
    log_security_event(user.id, "ACCOUNT_DEACTIVATED", "INFO", "Account deactivated")
    return {"message": "Account deactivated"}

# RBAC: List Users (admin only)
@app.get("/users", response_model=List[UserOut], dependencies=[Depends(require_role(["admin"]))])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [UserOut(id=u.id, email=u.email, role=u.role, mfa_enabled=u.mfa_enabled, is_active=u.is_active) for u in users]

# Structured Error Handling
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    logger.warn(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

# --- Third-Party Auth (Google Example) ---
@app.post("/auth/google")
def google_login(token: str, db: Session = Depends(get_db)):
    # Placeholder: Verify Google token and fetch user info (use google-auth library in production)
    google_email = "user@google.com"  # simulated
    user = db.query(User).filter(User.email == google_email).first()
    if not user:
        user = User(email=google_email, hashed_password=get_password_hash(secrets.token_urlsafe(16)), role="user")
        db.add(user)
        db.commit()
        db.refresh(user)
        log_security_event(user.id, "REGISTER_GOOGLE", "INFO", "Registered via Google")
    token = create_access_token(data={"sub": user.id, "role": user.role})
    log_security_event(user.id, "LOGIN_GOOGLE", "INFO", "Google login")
    return Token(access_token=token, token_type="bearer")

# --- Notification Placeholder ---
def send_notification(user: User, subject: str, message: str, channel: str = "email"):
    # Implement email/SMS/in-app notification logic here
    logger.info(f"Send {channel} notification to {user.email}: {subject} - {message}")

# --- Compliance/Encryption ---
# Encrypt user PII before storage (use field-level encryption in production)
def encrypt_data(data: str) -> str:
    # Placeholder for field encryption
    return data[::-1]

# --- Run Security Tests ---
def run_security_tests():
    # Placeholder for pen-test and vuln-scan logic
    logger.info("Running OWASP Top 10 tests and vulnerability scan...")

# --- High Availability/Fail-safe ---
def backup_auth_methods(user: User):
    # Placeholder for backup MFA or failover login methods
    return {"backup_codes": [secrets.token_hex(4) for _ in range(5)]}