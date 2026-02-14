import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { accountAPI } from '../services/api';
import { toast } from 'react-toastify';
import Accounts from './Accounts';
import Transactions from './Transactions';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [accounts, setAccounts] = useState([]);
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchAccounts = useCallback(async () => {
    if (!user) return;

    try {
      const response = await accountAPI.getUserAccounts(user.id);
      setAccounts(response.data);

      setSelectedAccount(prev => {
        if (!prev && response.data.length > 0) return response.data[0];
        if (prev) {
          const updated = response.data.find(a => a.id === prev.id);
          return updated || response.data[0] || null;
        }
        return null;
      });
    } catch (error) {
      toast.error('Erreur lors du chargement des comptes');
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  if (loading) {
    return <div className="loading">Chargement...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Tableau de bord</h1>
        <p>Bienvenue, {user?.first_name || user?.email}</p>
      </div>

      <div className="dashboard-grid">
        <div className="accounts-section">
          <Accounts
            accounts={accounts}
            onAccountSelect={setSelectedAccount}
            selectedAccount={selectedAccount}
            onRefresh={fetchAccounts}
          />
        </div>

        <div className="transactions-section">
          {selectedAccount ? (
            <Transactions
              account={selectedAccount}
              onRefresh={fetchAccounts}
            />
          ) : (
            <div className="no-account">
              <p>Sélectionnez un compte pour voir les transactions</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;