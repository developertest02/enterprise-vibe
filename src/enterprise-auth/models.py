from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, ForeignKey, Text, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy import TypeDecorator, CHAR
import uuid

Base = declarative_base()


class UUID(TypeDecorator):
    """Platform-independent UUID type that works with SQLite and PostgreSQL."""
    impl = CHAR
    cache_ok = True

    def __init__(self):
        super().__init__(36)

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    provider = Column(String(50), default='local')
    provider_id = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with users table
    user = relationship("User", back_populates="account", uselist=False, cascade="all, delete-orphan")

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(), ForeignKey('accounts.id', ondelete='CASCADE'))
    first_name = Column(String(255))
    last_name = Column(String(255))
    display_name = Column(String(255))
    avatar_url = Column(Text)
    bio = Column(Text)
    phone = Column(String(20))
    birth_date = Column(Date)
    gender = Column(String(20))
    address = Column(JSON)
    timezone = Column(String(50), default='UTC')
    locale = Column(String(10), default='en-US')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with accounts table
    account = relationship("Account", back_populates="user")


def get_db_session(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal