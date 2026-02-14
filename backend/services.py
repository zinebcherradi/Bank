from config import LocalSession
from dal import UserDao, AccountDao, TransactionDao
from entities import User, Account, Transaction
from dto import UserRequest, AccountRequest
from auth import get_password_hash, verify_password
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class UserService:
    def create_user(self, user_request: UserRequest) -> Optional[User]:
        try:
            with LocalSession() as session:
                hashed_password = get_password_hash(user_request.password)
                user = User(
                    email=user_request.email,
                    password=hashed_password,
                    is_admin=False,
                    first_name=user_request.first_name,
                    last_name=user_request.last_name,
                    phone=user_request.phone
                )
                return UserDao.create_user(session, user)
        except ValueError as e:
            if "EMAIL_ALREADY_EXISTS" in str(e):
                print(f"[INFO] Email déjà existant: {user_request.email}")
                raise ValueError("EMAIL_ALREADY_EXISTS")
            print(f"Erreur création utilisateur: {e}")
            raise
        except SQLAlchemyError as e:
            print(f"Erreur création utilisateur: {e}")
            raise Exception(f"Erreur base de données: {str(e)}")
        except Exception as e:
            print(f"Erreur création utilisateur: {e}")
            raise
    
    def search_by_email(self, email: str) -> Optional[User]:
        with LocalSession() as session:
            return UserDao.search_by_email(session, email)

    def get_by_id(self, user_id: int) -> Optional[User]:
        with LocalSession() as session:
            return UserDao.get_by_id(session, user_id)
    
    def delete_user(self, email: str) -> bool:
        try:
            with LocalSession() as session:
                return UserDao.delete_user(session, email)
        except SQLAlchemyError as e:
            print(f"Erreur suppression utilisateur: {e}")
            return False
    
    def get_all(self) -> List[User]:
        with LocalSession() as session:
            return UserDao.get_all_users(session)


class AuthService:
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        with LocalSession() as session:
            user = UserDao.search_by_email(session, email)
            if user and verify_password(password, user.password):
                return user
            return None
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        try:
            with LocalSession() as session:
                user = UserDao.get_by_id(session, user_id)
                if not user:
                    return False
                if not verify_password(current_password, user.password):
                    return False
                user.password = get_password_hash(new_password)
                session.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Erreur changement de mot de passe: {e}")
            return False


class AccountService:
    def _generate_account_number(self, session: Session) -> str:
        import random
        import string
        while True:
            # Generate a 10-digit random number
            acc_num = ''.join(random.choices(string.digits, k=10))
            if not AccountDao.get_by_account_number(session, acc_num):
                return acc_num

    def create_account(self, account_request: AccountRequest) -> Optional[Account]:
        try:
            with LocalSession() as session:
                acc_num = account_request.account_number or self._generate_account_number(session)
                account = Account(
                    user_id=account_request.user_id,
                    account_number=acc_num,
                    account_type=account_request.account_type,
                    balance=0.0,
                    overdraft_limit=account_request.overdraft_limit,
                    interest_rate=account_request.interest_rate
                )
                return AccountDao.create_account(session, account)
        except SQLAlchemyError as e:
            print(f"Erreur création compte: {e}")
            return None
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        with LocalSession() as session:
            return AccountDao.get_by_id(session, account_id)
    
    def get_accounts_by_user(self, user_id: int) -> List[Account]:
        with LocalSession() as session:
            return AccountDao.get_by_user_id(session, user_id)
    
    def delete_account(self, account_id: int) -> bool:
        try:
            with LocalSession() as session:
                return AccountDao.delete_account(session, account_id)
        except SQLAlchemyError as e:
            print(f"Erreur suppression compte: {e}")
            return False
    
    def deposit(self, account_id: int, amount: float) -> bool:
        if amount <= 0:
            return False
        try:
            with LocalSession() as session:
                account = AccountDao.get_by_id(session, account_id)
                if not account:
                    return False
                new_balance = account.balance + amount
                if AccountDao.update_balance(session, account_id, new_balance):
                    transaction = Transaction(
                        account_id=account_id,
                        transaction_type='deposit',
                        amount=amount,
                        description=f'Deposit of {amount}'
                    )
                    TransactionDao.create_transaction(session, transaction)
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            print(f"Erreur dépôt: {e}")
            return False
    
    def withdraw(self, account_id: int, amount: float) -> bool:
        if amount <= 0:
            return False
        try:
            with LocalSession() as session:
                account = AccountDao.get_by_id(session, account_id)
                if not account:
                    return False
                max_withdrawal = account.balance + account.overdraft_limit
                if amount > max_withdrawal:
                    return False
                new_balance = account.balance - amount
                if AccountDao.update_balance(session, account_id, new_balance):
                    transaction = Transaction(
                        account_id=account_id,
                        transaction_type='withdraw',
                        amount=-amount,
                        description=f'Withdrawal of {amount}'
                    )
                    TransactionDao.create_transaction(session, transaction)
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            print(f"Erreur retrait: {e}")
            return False
    
    def transfer(self, from_account_id: int, to_account_number: str, amount: float) -> bool:
        if amount <= 0:
            return False
        try:
            with LocalSession() as session:
                from_account = AccountDao.get_by_id(session, from_account_id)
                to_account = AccountDao.get_by_account_number(session, to_account_number)
                if not from_account or not to_account:
                    return False
                if from_account.id == to_account.id:
                    return False
                max_withdrawal = from_account.balance + from_account.overdraft_limit
                if amount > max_withdrawal:
                    return False
                from_account.balance -= amount
                to_account.balance += amount
                trans_from = Transaction(
                    account_id=from_account_id,
                    transaction_type='transfer',
                    amount=-amount,
                    description=f'Transfer to account {to_account.account_number}'
                )
                trans_to = Transaction(
                    account_id=to_account.id,
                    transaction_type='transfer',
                    amount=amount,
                    description=f'Transfer from account {from_account.account_number}'
                )
                session.add(trans_from)
                session.add(trans_to)
                session.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Erreur transfert: {e}")
            return False


class TransactionService:
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        with LocalSession() as session:
            return TransactionDao.get_by_id(session, transaction_id)
    
    def get_transactions_by_account(self, account_id: int) -> List[Transaction]:
        with LocalSession() as session:
            return TransactionDao.get_by_account_id(session, account_id)
    
    def get_transactions_by_account_and_date_range(self, account_id: int, start_date: datetime, end_date: datetime) -> List[Transaction]:
        with LocalSession() as session:
            return TransactionDao.get_by_account_id_and_date_range(session, account_id, start_date, end_date)
