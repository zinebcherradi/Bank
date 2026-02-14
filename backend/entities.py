from config import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional

class User(Base):
    __tablename__ = 't_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False, unique=True, index=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    phone = Column(String(20), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    def __init__(
        self, 
        email: str, 
        password: str, 
        is_admin: bool = False,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None
    ):
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone


class Account(Base):
    __tablename__ = 't_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('t_users.id'), nullable=False)
    account_number = Column(String(20), unique=True, index=True, nullable=False)
    account_type = Column(String(20), nullable=False)
    balance = Column(Float, default=0.0)
    overdraft_limit = Column(Float, default=0.0)
    interest_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

    def __init__(
        self,
        user_id: int,
        account_number: str,
        account_type: str,
        balance: float = 0.0,
        overdraft_limit: float = 0.0,
        interest_rate: float = 0.0
    ):
        self.user_id = user_id
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.overdraft_limit = overdraft_limit
        self.interest_rate = interest_rate


class Transaction(Base):
    __tablename__ = 't_transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('t_accounts.id'), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    account = relationship("Account", back_populates="transactions")

    def __init__(
        self,
        account_id: int,
        transaction_type: str,
        amount: float,
        description: Optional[str] = None
    ):
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description