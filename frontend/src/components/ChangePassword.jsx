import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { authAPI } from '../services/api';
import { toast } from 'react-toastify';
import './ChangePassword.css';

const ChangePassword = () => {
    const { user } = useAuth();
    const [formData, setFormData] = useState({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
    });
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (formData.newPassword !== formData.confirmPassword) {
            toast.error('Les mots de passe ne correspondent pas');
            return;
        }

        if (formData.newPassword.length < 6) {
            toast.error('Le mot de passe doit contenir au moins 6 caractères');
            return;
        }

        setLoading(true);

        try {
            // Appel à l'API pour changer le mot de passe
            await authAPI.changePassword({
                current_password: formData.currentPassword,
                new_password: formData.newPassword
            });

            toast.success('Mot de passe modifié avec succès !');
            setFormData({
                currentPassword: '',
                newPassword: '',
                confirmPassword: ''
            });
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Erreur lors du changement de mot de passe');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="change-password-container">
            <div className="change-password-header">
                <h1>Changer le mot de passe</h1>
                <p>Assurez-vous d'utiliser un mot de passe fort et unique</p>
            </div>

            <div className="change-password-card">
                <form onSubmit={handleSubmit} className="password-form">
                    <div className="form-group">
                        <label>Mot de passe actuel</label>
                        <input
                            type="password"
                            name="currentPassword"
                            value={formData.currentPassword}
                            onChange={handleChange}
                            placeholder="Entrez votre mot de passe actuel"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Nouveau mot de passe</label>
                        <input
                            type="password"
                            name="newPassword"
                            value={formData.newPassword}
                            onChange={handleChange}
                            placeholder="Entrez votre nouveau mot de passe"
                            minLength={6}
                            required
                        />
                        <span className="hint">Au moins 6 caractères</span>
                    </div>

                    <div className="form-group">
                        <label>Confirmer le nouveau mot de passe</label>
                        <input
                            type="password"
                            name="confirmPassword"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            placeholder="Confirmez votre nouveau mot de passe"
                            minLength={6}
                            required
                        />
                    </div>

                    <div className="password-tips">
                        <h3>Conseils pour un mot de passe sécurisé :</h3>
                        <ul>
                            <li>Utilisez au moins 8 caractères</li>
                            <li>Combinez lettres majuscules et minuscules</li>
                            <li>Incluez des chiffres et des caractères spéciaux</li>
                            <li>Évitez les informations personnelles</li>
                        </ul>
                    </div>

                    <button
                        type="submit"
                        className="submit-btn"
                        disabled={loading}
                    >
                        {loading ? 'Modification...' : 'Modifier le mot de passe'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChangePassword;
