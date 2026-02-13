import React, { createContext, useContext, useState, useEffect } from 'react';

const CurrencyContext = createContext();

export const useCurrency = () => {
  const context = useContext(CurrencyContext);
  if (!context) {
    throw new Error('useCurrency must be used within CurrencyProvider');
  }
  return context;
};

export const CurrencyProvider = ({ children }) => {
  const [currency, setCurrency] = useState(() => {
    const saved = localStorage.getItem('selectedCurrency');
    return saved || 'EUR';
  });

  useEffect(() => {
    localStorage.setItem('selectedCurrency', currency);
  }, [currency]);

  const getCurrencySymbol = (code) => {
    const symbols = {
      EUR: '€',
      USD: '$',
      GBP: '£',
      CHF: 'CHF',
      JPY: '¥',
      CAD: 'C$',
      AUD: 'A$',
      MAD: 'DH'
    };
    return symbols[code] || code;
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: currency
    }).format(amount);
  };

  const getExchangeRate = async (fromCurrency, toCurrency) => {
    if (fromCurrency === toCurrency) return 1;
    
    // Vous pouvez utiliser une API comme exchangerate-api.com
    // Pour l'instant, on utilise des taux fixes pour la démo
    const rates = {
      EUR: { USD: 1.07, GBP: 0.85, CHF: 0.96, MAD: 10.80 },
      USD: { EUR: 0.93, GBP: 0.79, CHF: 0.89, MAD: 10.10 },
      GBP: { EUR: 1.18, USD: 1.26, CHF: 1.13, MAD: 12.70 },
      MAD: { EUR: 0.093, USD: 0.099, GBP: 0.079, CHF: 0.088 }
    };
    
    return rates[fromCurrency]?.[toCurrency] || 1;
  };

  return (
    <CurrencyContext.Provider value={{
      currency,
      setCurrency,
      getCurrencySymbol,
      formatCurrency,
      getExchangeRate
    }}>
      {children}
    </CurrencyContext.Provider>
  );
};