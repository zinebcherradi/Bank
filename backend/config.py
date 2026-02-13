from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Charge .env en local uniquement
if os.getenv("RENDER") is None:
    load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "db_bank")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")

# En production (RENDER), pas de valeurs par défaut
if os.getenv("RENDER") is not None:
    if not all([DB_USER, DB_PASSWORD, DB_NAME, DB_HOST]):
        raise ValueError("Variables DB manquantes en production")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD n'est pas défini dans les variables d'environnement")

URL = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Configuration simple
engine = create_engine(URL, pool_size=10, pool_pre_ping=True)
LocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()