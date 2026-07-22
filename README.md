# SecureBank – Secure Banking Web Application

SecureBank est une application web bancaire Full Stack développée pour mettre en pratique les concepts de développement backend et frontend dans un contexte métier réaliste. L'application simule les principales fonctionnalités d'une banque en ligne, en mettant l'accent sur la sécurité, la gestion des comptes et le traitement des transactions.

Le projet a été conçu avec une architecture moderne reposant sur FastAPI pour le backend, React pour le frontend et MySQL pour la persistance des données.

## Fonctionnalités

### Authentification et sécurité

- Inscription et connexion des utilisateurs
- Authentification basée sur JWT
- Hachage sécurisé des mots de passe avec bcrypt
- Gestion des sessions
- Routes protégées
- Contrôle d'accès garantissant que chaque utilisateur accède uniquement à ses propres données

### Gestion des comptes

- Création de comptes bancaires
- Consultation du solde
- Gestion de plusieurs comptes par utilisateur
- Validation des opérations

### Transactions bancaires

- Dépôts
- Retraits
- Virements entre comptes
- Vérification des soldes disponibles
- Gestion des découverts autorisés
- Historique complet des transactions

### Tableau de bord

- Consultation des soldes en temps réel
- Historique des opérations
- Interface simple et intuitive
- Réalisation des opérations financières depuis le tableau de bord

## Architecture du projet

Le projet suit une architecture en couches favorisant la maintenabilité et la séparation des responsabilités :

- Backend REST API avec FastAPI
- Couche Services contenant la logique métier
- Couche d'accès aux données avec SQLAlchemy
- Base de données MySQL
- Frontend React utilisant Context API pour la gestion de l'état

## Technologies utilisées

### Backend

- Python
- FastAPI
- SQLAlchemy
- MySQL
- JWT
- bcrypt
- Pydantic
- Uvicorn

### Frontend

- React
- Context API
- Axios
- React Router

### Documentation

- Swagger UI

## Principales fonctionnalités techniques

- API REST sécurisée
- Authentification JWT
- Gestion des rôles et des autorisations
- Validation des données
- Gestion centralisée des erreurs
- Transactions ACID
- Architecture modulaire
- Documentation automatique de l'API

## Ce que ce projet m'a permis d'approfondir

- Sécurisation d'une application web avec JWT et bcrypt
- Gestion des variables d'environnement
- Conception d'API REST avec FastAPI
- Architecture logicielle en couches
- Utilisation de SQLAlchemy et des transactions
- Développement d'une interface React connectée à une API
- Implémentation de la logique métier bancaire
- Validation des données et gestion des exceptions

## Lancer le projet

### Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

pip install -r requirements.txt

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

## Documentation API

Une fois le backend lancé, la documentation interactive est disponible via Swagger UI à l'adresse :

```
http://localhost:8000/docs
```

## Auteur

Développé dans le cadre d'un projet d'apprentissage afin de mettre en pratique le développement Full Stack avec Python, FastAPI, React et MySQL en reproduisant les fonctionnalités essentielles d'une application bancaire sécurisée.
