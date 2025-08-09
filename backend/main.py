from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

# Config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://whirly:whirlypass@db:5432/whirly")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(32), default="user")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    path = Column(String(512))
    scanned = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User")

class Component(Base):
    __tablename__ = "components"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    type = Column(String(128))
    metadata = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

class TrainingModule(Base):
    __tablename__ = "training_modules"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    progress = Column(Integer, default=0)
    status = Column(String(32), default="pending")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

Base.metadata.create_all(bind=engine)

# Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DocumentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    path: str

class DocumentOut(BaseModel):
    id: int
    name: str
    path: str
    scanned: bool

class ComponentCreate(BaseModel):
    name: str
    type: str
    metadata: Optional[str] = ""

class ComponentOut(BaseModel):
    id: int
    name: str
    type: str
    metadata: Optional[str] = ""

class TrainingModuleCreate(BaseModel):
    name: str

class TrainingModuleOut(BaseModel):
    id: int
    name: str
    progress: int
    status: str

# Auth helpers
def get_password_hash(password):
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

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def require_role(role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return role_checker

# FastAPI app
app = FastAPI(title="Whirly API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth Endpoints ---
@app.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut(id=new_user.id, email=new_user.email, role=new_user.role)

@app.post("/auth/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email, "role": user.role})
    return Token(access_token=token, token_type="bearer")

# --- Document Endpoints ---
@app.post("/documents", response_model=DocumentOut)
def upload_document(doc: DocumentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_doc = Document(**doc.dict(), owner_id=user.id)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return DocumentOut(id=new_doc.id, name=new_doc.name, path=new_doc.path, scanned=new_doc.scanned)

@app.get("/documents", response_model=List[DocumentOut])
def list_documents(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    docs = db.query(Document).filter(Document.owner_id == user.id).all()
    return [DocumentOut(id=d.id, name=d.name, path=d.path, scanned=d.scanned) for d in docs]

@app.put("/documents/{doc_id}/scan", response_model=DocumentOut)
def scan_document(doc_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id, Document.owner_id == user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.scanned = True
    db.commit()
    db.refresh(doc)
    return DocumentOut(id=doc.id, name=doc.name, path=doc.path, scanned=doc.scanned)

@app.delete("/documents/{doc_id}", status_code=204)
def delete_document(doc_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id, Document.owner_id == user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return

# --- Component Endpoints ---
@app.post("/components", response_model=ComponentOut)
def add_component(comp: ComponentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_comp = Component(**comp.dict(), owner_id=user.id)
    db.add(new_comp)
    db.commit()
    db.refresh(new_comp)
    return ComponentOut(id=new_comp.id, name=new_comp.name, type=new_comp.type, metadata=new_comp.metadata)

@app.get("/components", response_model=List[ComponentOut])
def list_components(q: Optional[str] = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Component).filter(Component.owner_id == user.id)
    if q:
        query = query.filter(Component.name.ilike(f"%{q}%"))
    comps = query.all()
    return [ComponentOut(id=c.id, name=c.name, type=c.type, metadata=c.metadata) for c in comps]

@app.delete("/components/{comp_id}", status_code=204)
def delete_component(comp_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    comp = db.query(Component).filter(Component.id == comp_id, Component.owner_id == user.id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")
    db.delete(comp)
    db.commit()
    return

# --- Training Module Endpoints ---
@app.post("/training", response_model=TrainingModuleOut)
def create_training(tr: TrainingModuleCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_tr = TrainingModule(name=tr.name, owner_id=user.id)
    db.add(new_tr)
    db.commit()
    db.refresh(new_tr)
    return TrainingModuleOut(id=new_tr.id, name=new_tr.name, progress=new_tr.progress, status=new_tr.status)

@app.get("/training", response_model=List[TrainingModuleOut])
def list_training(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    trs = db.query(TrainingModule).filter(TrainingModule.owner_id == user.id).all()
    return [TrainingModuleOut(id=t.id, name=t.name, progress=t.progress, status=t.status) for t in trs]

@app.put("/training/{tr_id}/progress", response_model=TrainingModuleOut)
def update_training_progress(tr_id: int, progress: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tr = db.query(TrainingModule).filter(TrainingModule.id == tr_id, TrainingModule.owner_id == user.id).first()
    if not tr:
        raise HTTPException(status_code=404, detail="Training module not found")
    tr.progress = progress
    tr.status = "completed" if progress >= 100 else "in_progress"
    db.commit()
    db.refresh(tr)
    return TrainingModuleOut(id=tr.id, name=tr.name, progress=tr.progress, status=tr.status)

@app.delete("/training/{tr_id}", status_code=204)
def delete_training(tr_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tr = db.query(TrainingModule).filter(TrainingModule.id == tr_id, TrainingModule.owner_id == user.id).first()
    if not tr:
        raise HTTPException(status_code=404, detail="Training module not found")
    db.delete(tr)
    db.commit()
    return

# --- Admin/User Endpoints ---
@app.get("/users/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return UserOut(id=user.id, email=user.email, role=user.role)

@app.get("/users", response_model=List[UserOut], dependencies=[Depends(require_role("admin"))])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [UserOut(id=u.id, email=u.email, role=u.role) for u in users]