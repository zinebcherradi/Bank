from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from entities import User, Account, Transaction
from typing import List, Optional

class UserDao:
    @staticmethod
    def create_user(session: Session, user: User) -> User:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except IntegrityError:
            session.rollback()
            raise ValueError("EMAIL_ALREADY_EXISTS")

    @staticmethod
    def search_by_email(session: Session, email: str) -> Optional[User]:
        return session.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional[User]:
        return session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def delete_user(session: Session, email: str) -> bool:
        user = session.query(User).filter(User.email == email).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

    @staticmethod
    def get_all_users(session: Session) -> List[User]:
        return session.query(User).all()


class AccountDao:
    @staticmethod
    def create_account(session: Session, account: Account) -> Account:
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

    @staticmethod
    def get_by_id(session: Session, account_id: int) -> Optional[Account]:
        return session.query(Account).filter(Account.id == account_id).first()

    @staticmethod
    def get_by_user_id(session: Session, user_id: int) -> List[Account]:
        return session.query(Account).filter(Account.user_id == user_id).all()

    @staticmethod
    def delete_account(session: Session, account_id: int) -> bool:
        account = session.query(Account).filter(Account.id == account_id).first()
        if account:
            session.delete(account)
            session.commit()
            return True
        return False

    @staticmethod
    def update_balance(session: Session, account_id: int, new_balance: float) -> bool:
        account = session.query(Account).filter(Account.id == account_id).first()
        if account:
            account.balance = new_balance
            session.commit()
            return True
        return False


class TransactionDao:
    @staticmethod
    def create_transaction(session: Session, transaction: Transaction) -> Transaction:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

    @staticmethod
    def get_by_id(session: Session, transaction_id: int) -> Optional[Transaction]:
        return session.query(Transaction).filter(Transaction.id == transaction_id).first()

    @staticmethod
    def get_by_account_id(session: Session, account_id: int) -> List[Transaction]:
        return session.query(Transaction).filter(Transaction.account_id == account_id).all()

    @staticmethod
    def get_by_account_id_and_date_range(session: Session, account_id: int, start_date, end_date) -> List[Transaction]:
        return session.query(Transaction).filter(
            Transaction.account_id == account_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date
        ).all()