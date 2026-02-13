import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import './Profile.css';

const Profile = () => {
    const { user } = useAuth();
    const [isEditing, setIsEditing] = useState(false);

    if (!user) {
        return <div className="loading">Chargement...</div>;
    }

    return (
        <div className="profile-container">
            <div className="profile-header">
                <h1>Informations personnelles</h1>
                <p>Consultez et gérez vos informations personnelles</p>
            </div>

            <div className="profile-card">
                <div className="profile-section">
                    <h2>Informations de base</h2>
                    <div className="info-grid">
                        <div className="info-item">
                            <label>Prénom</label>
                            <div className="info-value">{user.first_name || 'Non renseigné'}</div>
                        </div>
                        <div className="info-item">
                            <label>Nom</label>
                            <div className="info-value">{user.last_name || 'Non renseigné'}</div>
                        </div>
                        <div className="info-item">
                            <label>Email</label>
                            <div className="info-value">{user.email}</div>
                        </div>
                        <div className="info-item">
                            <label>Téléphone</label>
                            <div className="info-value">{user.phone || 'Non renseigné'}</div>
                        </div>
                    </div>
                </div>

                <div className="profile-section">
                    <h2>Informations du compte</h2>
                    <div className="info-grid">
                        <div className="info-item">
                            <label>ID Utilisateur</label>
                            <div className="info-value">{user.id}</div>
                        </div>
                        <div className="info-item">
                            <label>Date de création</label>
                            <div className="info-value">
                                {user.created_at ? new Date(user.created_at).toLocaleDateString('fr-FR') : 'Non disponible'}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Profile;
