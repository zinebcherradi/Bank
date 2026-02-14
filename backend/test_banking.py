from services import AccountService
from entities import User, Account
from config import LocalSession
from dal import UserDao, AccountDao

def test_banking():
    service = AccountService()
    
    with LocalSession() as session:
        # Create a test user and account if they don't exist
        user = UserDao.search_by_email(session, "test@example.com")
        if not user:
            user = User(email="test@example.com", password="password")
            UserDao.create_user(session, user)
        
        account = AccountDao.get_by_user_id(session, user.id)
        if not account:
            account = Account(user_id=user.id, account_type="current", balance=1000.0)
            AccountDao.create_account(session, account)
        else:
            account = account[0]
            
        account_id = account.id
        print(f"Testing with account_id: {account_id}, initial balance: {account.balance}")

    # Test Deposit
    print("\nTesting Deposit...")
    success = service.deposit(account_id, 500.0)
    print(f"Deposit success: {success}")
    with LocalSession() as session:
        account = AccountDao.get_by_id(session, account_id)
        print(f"Balance after deposit: {account.balance}")

    # Test Withdraw
    print("\nTesting Withdraw...")
    success = service.withdraw(account_id, 200.0)
    print(f"Withdraw success: {success}")
    with LocalSession() as session:
        account = AccountDao.get_by_id(session, account_id)
        print(f"Balance after withdraw: {account.balance}")

    # Test Transfer
    print("\nTesting Transfer...")
    with LocalSession() as session:
        to_account = Account(user_id=user.id, account_type="savings", balance=0.0)
        AccountDao.create_account(session, to_account)
        to_account_id = to_account.id
    
    success = service.transfer(account_id, to_account_id, 300.0)
    print(f"Transfer success: {success}")
    with LocalSession() as session:
        from_acc = AccountDao.get_by_id(session, account_id)
        to_acc = AccountDao.get_by_id(session, to_account_id)
        print(f"Source balance: {from_acc.balance}")
        print(f"Dest balance: {to_acc.balance}")

if __name__ == "__main__":
    try:
        test_banking()
    except Exception as e:
        print(f"ERROR: {e}")
