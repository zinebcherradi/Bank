from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
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
        stmt = select(User).where(User.email == email)
        result = session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def delete_user(session: Session, email: str) -> bool:
        stmt = select(User).where(User.email == email)
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

    @staticmethod
    def get_all_users(session: Session) -> List[User]:
        stmt = select(User)
        result = session.execute(stmt)
        return list(result.scalars())


class AccountDao:
    @staticmethod
    def create_account(session: Session, account: Account) -> Account:
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

    @staticmethod
    def get_by_id(session: Session, account_id: int) -> Optional[Account]:
        stmt = select(Account).where(Account.id == account_id)
        result = session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def get_by_account_number(session: Session, account_number: str) -> Optional[Account]:
        stmt = select(Account).where(Account.account_number == account_number)
        result = session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def get_by_user_id(session: Session, user_id: int) -> List[Account]:
        stmt = select(Account).where(Account.user_id == user_id)
        result = session.execute(stmt)
        return list(result.scalars())

    @staticmethod
    def delete_account(session: Session, account_id: int) -> bool:
        stmt = select(Account).where(Account.id == account_id)
        result = session.execute(stmt)
        account = result.scalar_one_or_none()
        if account:
            session.delete(account)
            session.commit()
            return True
        return False

    @staticmethod
    def update_balance(session: Session, account_id: int, new_balance: float) -> bool:
        stmt = select(Account).where(Account.id == account_id)
        result = session.execute(stmt)
        account = result.scalar_one_or_none()
        if account:
            account.balance = new_balance
            return True
        return False


class TransactionDao:
    @staticmethod
    def create_transaction(session: Session, transaction: Transaction) -> Transaction:
        session.add(transaction)
        return transaction

    @staticmethod
    def get_by_id(session: Session, transaction_id: int) -> Optional[Transaction]:
        stmt = select(Transaction).where(Transaction.id == transaction_id)
        result = session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def get_by_account_id(session: Session, account_id: int) -> List[Transaction]:
        stmt = select(Transaction).where(Transaction.account_id == account_id)
        result = session.execute(stmt)
        return list(result.scalars())

    @staticmethod
    def get_by_account_id_and_date_range(
        session: Session, account_id: int, start_date, end_date
    ) -> List[Transaction]:
        stmt = select(Transaction).where(
            Transaction.account_id == account_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date
        )
        result = session.execute(stmt)
        return list(result.scalars())