from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class AccountRequest(BaseModel):
    user_id: int
    account_number: Optional[str] = None
    account_type: str
    overdraft_limit: float = 0.0
    interest_rate: float = 0.0

class AccountResponse(BaseModel):
    id: int
    user_id: int
    account_number: str
    account_type: str
    balance: float
    overdraft_limit: float
    interest_rate: float
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionRequest(BaseModel):
    account_id: int
    transaction_type: str
    amount: float
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    transaction_type: str
    amount: float
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True