import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCurrency } from '../context/CurrencyContext';
import { LayoutDashboard, User, LogOut, Shield, ChevronDown } from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
    const { user, logout } = useAuth();
    const { currency, setCurrency } = useCurrency(); // ← Ajout
    const navigate = useNavigate();
    const [showCurrencyDropdown, setShowCurrencyDropdown] = useState(false);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const currencies = [
        { code: 'EUR', name: 'Euro', symbol: '€' },
        { code: 'USD', name: 'Dollar US', symbol: '$' },
        { code: 'GBP', name: 'Livre Sterling', symbol: '£' },
        { code: 'CHF', name: 'Franc Suisse', symbol: 'CHF' },
        { code: 'MAD', name: 'Dirham Marocain', symbol: 'DH' },
        { code: 'JPY', name: 'Yen Japonais', symbol: '¥' },
        { code: 'CAD', name: 'Dollar Canadien', symbol: 'C$' },
        { code: 'AUD', name: 'Dollar Australien', symbol: 'A$' }
    ];

    const handleCurrencyChange = (code) => {
        setCurrency(code);
        setShowCurrencyDropdown(false);
    };

    if (!user) {
        return null;
    }

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Shield size={24} className="brand-icon" />
                <h1>SecureBank</h1>
            </div>

            <div className="navbar-menu">
                <button onClick={() => navigate('/dashboard')} className="nav-link">
                    <LayoutDashboard size={18} /> Dashboard
                </button>
                <button onClick={() => navigate('/profile')} className="nav-link">
                    <User size={18} /> Profile
                </button>

                {/* Sélecteur de devise */}
                <div className="currency-selector">
                    <button
                        className="currency-btn"
                        onClick={() => setShowCurrencyDropdown(!showCurrencyDropdown)}
                    >
                        <span className="currency-code">{currency}</span>
                        <ChevronDown size={14} className={`currency-arrow ${showCurrencyDropdown ? 'open' : ''}`} />
                    </button>

                    {showCurrencyDropdown && (
                        <div className="currency-dropdown">
                            {currencies.map((curr) => (
                                <button
                                    key={curr.code}
                                    className={`currency-option ${curr.code === currency ? 'active' : ''}`}
                                    onClick={() => handleCurrencyChange(curr.code)}
                                >
                                    <span className="currency-flag">{curr.symbol}</span>
                                    <span className="currency-name">{curr.name}</span>
                                    <span className="currency-code-small">{curr.code}</span>
                                    {curr.code === currency && (
                                        <span className="checkmark">✓</span>
                                    )}
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                <div className="navbar-user">
                    <span className="user-name">
                        {user.first_name && user.last_name
                            ? `${user.first_name} ${user.last_name}`
                            : user.email}
                    </span>
                    <button onClick={handleLogout} className="logout-btn">
                        <LogOut size={16} /> Déconnexion
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;