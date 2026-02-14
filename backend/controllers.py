from fastapi import APIRouter, HTTPException, Response, Depends
from dto import UserResponse, UserRequest, AccountRequest, AccountResponse, TransactionResponse
from services import UserService, AccountService, TransactionService, AuthService
from auth import create_access_token, get_current_user_id
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional

router_users = APIRouter(prefix="/users")
router_accounts = APIRouter(prefix="/accounts")
router_transactions = APIRouter(prefix="/transactions")
router_auth = APIRouter(prefix="/auth")

class LoginRequest(BaseModel):
    email: str
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

@router_users.get("/", response_model=List[UserResponse])
def get_users():
    service = UserService()
    users = service.get_all()
    return [UserResponse.from_orm(user) for user in users]

@router_users.post("/", response_model=UserResponse)
def register_user(user_request: UserRequest):
    service = UserService()
    try:
        user_created = service.create_user(user_request)
        if user_created:
            return UserResponse.from_orm(user_created)
        raise HTTPException(status_code=400, detail="Erreur lors de la création du compte")
    except ValueError as e:
        if "EMAIL_ALREADY_EXISTS" in str(e):
            raise HTTPException(status_code=400, detail="Email déjà existant")
        raise HTTPException(status_code=400, detail="Erreur de validation")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la création du compte")

@router_users.delete("/{email}")
def delete_user(email: str):
    service = UserService()
    if service.delete_user(email):
        return Response(content="Utilisateur supprimé avec succès", status_code=200)
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@router_users.get("/{email}", response_model=UserResponse)
def search_by_email(email: str):
    service = UserService()
    user = service.search_by_email(email)
    if user:
        return UserResponse.from_orm(user)
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@router_auth.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest):
    auth_service = AuthService()
    user = auth_service.authenticate_user(login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=30)
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@router_auth.get("/me", response_model=UserResponse)
def get_current_user(current_user_id: int = Depends(get_current_user_id)):
    user_service = UserService()
    user = user_service.get_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return UserResponse.from_orm(user)

@router_auth.put("/change-password")
def change_password(password_request: ChangePasswordRequest, current_user_id: int = Depends(get_current_user_id)):
    auth_service = AuthService()
    if auth_service.change_password(current_user_id, password_request.current_password, password_request.new_password):
        return {"message": "Mot de passe modifié avec succès"}
    raise HTTPException(status_code=400, detail="Mot de passe actuel incorrect ou erreur lors de la modification")

@router_accounts.post("/", response_model=AccountResponse)
def create_account(account_request: AccountRequest, current_user_id: int = Depends(get_current_user_id)):
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != account_request.user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    service = AccountService()
    account = service.create_account(account_request)
    if account:
        return AccountResponse.from_orm(account)
    raise HTTPException(status_code=400, detail="Échec de la création du compte")

@router_accounts.get("/user/{user_id}", response_model=List[AccountResponse])
def get_accounts_by_user(user_id: int, current_user_id: int = Depends(get_current_user_id)):
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    service = AccountService()
    accounts = service.get_accounts_by_user(user_id)
    return [AccountResponse.from_orm(acc) for acc in accounts]

@router_accounts.get("/{account_id}", response_model=AccountResponse)
def get_account_by_id(account_id: int, current_user_id: int = Depends(get_current_user_id)):
    service = AccountService()
    account = service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != account.user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    return AccountResponse.from_orm(account)

@router_accounts.delete("/{account_id}")
def delete_account(account_id: int, current_user_id: int = Depends(get_current_user_id)):
    account_service = AccountService()
    account = account_service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != account.user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    if account_service.delete_account(account_id):
        return Response(content="Compte supprimé avec succès", status_code=200)
    raise HTTPException(status_code=400, detail="Échec de la suppression")

@router_accounts.post("/{account_id}/deposit")
def deposit(account_id: int, amount: float, current_user_id: int = Depends(get_current_user_id)):
    account_service = AccountService()
    account = account_service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != account.user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Montant invalide")
    if account_service.deposit(account_id, amount):
        return Response(content=f"Dépôt de {amount} effectué avec succès", status_code=200)
    raise HTTPException(status_code=400, detail="Échec du dépôt")

@router_accounts.post("/{account_id}/withdraw")
def withdraw(account_id: int, amount: float, current_user_id: int = Depends(get_current_user_id)):
    account_service = AccountService()
    account = account_service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != account.user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Montant invalide")
    if account_service.withdraw(account_id, amount):
        return Response(content=f"Retrait de {amount} effectué avec succès", status_code=200)
    raise HTTPException(status_code=400, detail="Fonds insuffisants ou montant invalide")

@router_accounts.post("/{account_id}/transfer")
def transfer(account_id: int, to_account_number: str, amount: float, current_user_id: int = Depends(get_current_user_id)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Montant invalide")
    account_service = AccountService()
    from_account = account_service.get_account_by_id(account_id)
    if not from_account:
        raise HTTPException(status_code=404, detail="Compte source non trouvé")
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != from_account.user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    if account_service.transfer(account_id, to_account_number, amount):
        return Response(content=f"Virement de {amount} vers le compte {to_account_number} effectué avec succès", status_code=200)
    raise HTTPException(status_code=400, detail="Échec du virement : compte destinataire introuvable ou solde insuffisant")

@router_transactions.get("/account/{account_id}", response_model=List[TransactionResponse])
def get_transactions_by_account(account_id: int, current_user_id: int = Depends(get_current_user_id)):
    account_service = AccountService()
    account = account_service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != account.user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    service = TransactionService()
    transactions = service.get_transactions_by_account(account_id)
    return [TransactionResponse.from_orm(t) for t in transactions]

@router_transactions.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction_by_id(transaction_id: int, current_user_id: int = Depends(get_current_user_id)):
    service = TransactionService()
    transaction = service.get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    account_service = AccountService()
    account = account_service.get_account_by_id(transaction.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    if not current_user or current_user.id != account.user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    return TransactionResponse.from_orm(transaction)
