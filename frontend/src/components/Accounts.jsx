import React, { useState } from 'react';
import { accountAPI } from '../services/api';
import { toast } from 'react-toastify';
import { useCurrency } from '../context/CurrencyContext';
import { CreditCard, Wallet, CheckCircle, XCircle } from 'lucide-react';
import './Accounts.css';

const Accounts = ({ accounts, onAccountSelect, selectedAccount, onRefresh }) => {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newAccount, setNewAccount] = useState({
    account_type: 'checking',
    overdraft_limit: 0,
    interest_rate: 0
  });

  const { formatCurrency } = useCurrency();

  const handleCreateAccount = async (e) => {
    e.preventDefault();
    try {
      await accountAPI.createAccount({
        ...newAccount,
        user_id: JSON.parse(localStorage.getItem('user'))?.id
      });
      toast.success('Compte créé avec succès !');
      setShowCreateModal(false);
      onRefresh();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors de la création');
    }
  };

  return (
    <div className="accounts-container">
      <div className="accounts-header">
        <h2>Mes Comptes</h2>
        <button
          className="create-btn"
          onClick={() => setShowCreateModal(true)}
        >
          + Nouveau compte
        </button>
      </div>

      <div className="accounts-list">
        {accounts.map((account) => (
          <div
            key={account.id}
            className={`account-card ${selectedAccount?.id === account.id ? 'selected' : ''}`}
            onClick={() => onAccountSelect(account)}
          >
            <div className="account-type">
              {account.account_type === 'checking' ? (
                <><CreditCard size={18} className="account-icon" /> Compte Courant</>
              ) : (
                <><Wallet size={18} className="account-icon" /> Compte Épargne</>
              )}
            </div>
            <div className="account-number">N° {account.account_number}</div>
            <div className="account-balance">{formatCurrency(account.balance)}</div>
          </div>
        ))}
      </div>

      {accounts.length === 0 && (
        <div className="no-accounts">
          <p>Aucun compte. Créez votre premier compte !</p>
        </div>
      )}

      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Créer un nouveau compte</h3>
            <form onSubmit={handleCreateAccount}>
              <div className="form-group">
                <label>Type de compte</label>
                <select
                  value={newAccount.account_type}
                  onChange={(e) => setNewAccount({ ...newAccount, account_type: e.target.value })}
                >
                  <option value="checking">Compte Courant</option>
                  <option value="savings">Compte Épargne</option>
                </select>
              </div>

              <div className="form-group">
                <label>Découvert autorisé (€)</label>
                <input
                  type="number"
                  value={newAccount.overdraft_limit}
                  onChange={(e) => setNewAccount({ ...newAccount, overdraft_limit: parseFloat(e.target.value) })}
                  min="0"
                />
              </div>

              <div className="form-group">
                <label>Taux d'intérêt (%)</label>
                <input
                  type="number"
                  value={newAccount.interest_rate}
                  onChange={(e) => setNewAccount({ ...newAccount, interest_rate: parseFloat(e.target.value) })}
                  min="0"
                  step="0.01"
                />
              </div>

              <div className="modal-buttons">
                <button type="button" className="cancel-btn" onClick={() => setShowCreateModal(false)}>
                  Annuler
                </button>
                <button type="submit" className="confirm-btn">
                  Créer
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Accounts;
