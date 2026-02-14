import React, { useState, useEffect, useCallback } from 'react';
import { accountAPI, transactionAPI } from '../services/api';
import { toast } from 'react-toastify';
import { useCurrency } from '../context/CurrencyContext';
import { Download, Upload, ArrowLeftRight, History } from 'lucide-react';
import './Transactions.css';

const Transactions = ({ account, onRefresh }) => {
  const [transactions, setTransactions] = useState([]);
  const [showDepositModal, setShowDepositModal] = useState(false);
  const [showWithdrawModal, setShowWithdrawModal] = useState(false);
  const [showTransferModal, setShowTransferModal] = useState(false);
  const [amount, setAmount] = useState('');
  const [toAccountNumber, setToAccountNumber] = useState('');

  const { formatCurrency } = useCurrency();


  const fetchTransactions = useCallback(async () => {
    if (!account) return;

    try {
      const response = await transactionAPI.getAccountTransactions(account.id);
      setTransactions(response.data);
    } catch (error) {
      console.error('Erreur chargement transactions:', error);
    }
  }, [account?.id]);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  const handleDeposit = async (e) => {
    e.preventDefault();
    try {
      await accountAPI.deposit(account.id, parseFloat(amount));
      toast.success('Dépôt effectué avec succès !');
      setShowDepositModal(false);
      setAmount('');
      onRefresh();
      fetchTransactions();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors du dépôt');
    }
  };

  const handleWithdraw = async (e) => {
    e.preventDefault();
    try {
      await accountAPI.withdraw(account.id, parseFloat(amount));
      toast.success('Retrait effectué avec succès !');
      setShowWithdrawModal(false);
      setAmount('');
      onRefresh();
      fetchTransactions();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors du retrait');
    }
  };

  const handleTransfer = async (e) => {
    e.preventDefault();
    try {
      await accountAPI.transfer(account.id, toAccountNumber, parseFloat(amount));
      toast.success('Virement effectué avec succès !');
      setShowTransferModal(false);
      setAmount('');
      setToAccountNumber('');
      onRefresh();
      fetchTransactions();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors du virement');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('fr-FR');
  };

  return (
    <div className="transactions-container">
      <div className="transactions-header">
        <h2>Compte N° {account.account_number}</h2>
        <div className="action-buttons">
          <button className="deposit-btn" onClick={() => setShowDepositModal(true)}>
            <Download size={20} className="btn-icon" /> Déposer
          </button>
          <button className="withdraw-btn" onClick={() => setShowWithdrawModal(true)}>
            <Upload size={20} className="btn-icon" /> Retirer
          </button>
          <button className="transfer-btn" onClick={() => setShowTransferModal(true)}>
            <ArrowLeftRight size={20} className="btn-icon" /> Virement
          </button>
        </div>
      </div>

      <div className="account-info">
        <div className="info-item">
          <span>Solde actuel</span>
          <strong>{formatCurrency(account.balance)}</strong>
        </div>
        <div className="info-item">
          <span>Découvert autorisé</span>
          <strong>{formatCurrency(account.overdraft_limit)}</strong>
        </div>
        <div className="info-item">
          <span>Type</span>
          <strong>{account.account_type === 'checking' ? 'Courant' : 'Épargne'}</strong>
        </div>
      </div>

      <h3 className="history-title">
        <History size={20} className="history-icon" /> Historique des transactions
      </h3>

      <div className="transactions-list">
        {transactions.length === 0 ? (
          <p className="no-transactions">Aucune transaction pour ce compte</p>
        ) : (
          transactions.map((t) => (
            <div key={t.id} className={`transaction-item ${t.transaction_type}`}>
              <div className="transaction-icon">
                {t.transaction_type === 'deposit' && <Download size={18} />}
                {t.transaction_type === 'withdraw' && <Upload size={18} />}
                {t.transaction_type === 'transfer' && <ArrowLeftRight size={18} />}
              </div>
              <div className="transaction-details">
                <div className="transaction-type">
                  {t.transaction_type === 'deposit' && 'Dépôt'}
                  {t.transaction_type === 'withdraw' && 'Retrait'}
                  {t.transaction_type === 'transfer' && 'Virement'}
                </div>
                <div className="transaction-date">{formatDate(t.created_at)}</div>
                <div className="transaction-desc">{t.description}</div>
              </div>
              <div className={`transaction-amount ${t.transaction_type}`}>
                {t.transaction_type === 'withdraw' || (t.transaction_type === 'transfer' && t.from_account_id === account.id)
                  ? '-'
                  : '+'}
                {formatCurrency(Math.abs(t.amount))}
              </div>
            </div>
          ))
        )}
      </div>

      {showDepositModal && (
        <div className="modal-overlay" onClick={() => setShowDepositModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3><Download size={24} /> Déposer de l'argent</h3>
            <form onSubmit={handleDeposit}>
              <div className="form-group">
                <label>Montant (€)</label>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  min="0"
                  step="0.01"
                  required
                />
              </div>
              <div className="modal-buttons">
                <button type="button" className="cancel-btn" onClick={() => setShowDepositModal(false)}>
                  Annuler
                </button>
                <button type="submit" className="confirm-btn">
                  Déposer
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showWithdrawModal && (
        <div className="modal-overlay" onClick={() => setShowWithdrawModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3><Upload size={24} /> Retirer de l'argent</h3>
            <form onSubmit={handleWithdraw}>
              <div className="form-group">
                <label>Montant (€)</label>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  min="0"
                  step="0.01"
                  required
                />
              </div>
              <div className="modal-buttons">
                <button type="button" className="cancel-btn" onClick={() => setShowWithdrawModal(false)}>
                  Annuler
                </button>
                <button type="submit" className="confirm-btn">
                  Retirer
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showTransferModal && (
        <div className="modal-overlay" onClick={() => setShowTransferModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3><ArrowLeftRight size={24} /> Effectuer un virement</h3>
            <form onSubmit={handleTransfer}>
              <div className="form-group">
                <label>Montant (€)</label>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  min="0"
                  step="0.01"
                  required
                />
              </div>
              <div className="form-group">
                <label>Numéro de compte destinataire</label>
                <input
                  type="text"
                  placeholder="Ex: 1234567890"
                  value={toAccountNumber}
                  onChange={(e) => setToAccountNumber(e.target.value)}
                  required
                />
              </div>
              <div className="modal-buttons">
                <button type="button" className="cancel-btn" onClick={() => setShowTransferModal(false)}>
                  Annuler
                </button>
                <button type="submit" className="confirm-btn">
                  Virement
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Transactions;