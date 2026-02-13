"""
Script de migration pour ajouter les colonnes manquantes à la table t_users
"""
import mysql.connector
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

def migrate():
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        print("Connexion à la base de données réussie")
        
        # Vérifier les colonnes existantes
        cursor.execute("DESCRIBE t_users")
        existing_columns = [col[0] for col in cursor.fetchall()]
        print(f"Colonnes existantes: {existing_columns}")
        
        # Ajouter first_name si elle n'existe pas
        if 'first_name' not in existing_columns:
            print("Ajout de la colonne first_name...")
            cursor.execute("ALTER TABLE t_users ADD COLUMN first_name VARCHAR(128) NULL AFTER password")
            print("✓ Colonne first_name ajoutée")
        else:
            print("✓ Colonne first_name existe déjà")
        
        # Ajouter last_name si elle n'existe pas
        if 'last_name' not in existing_columns:
            print("Ajout de la colonne last_name...")
            cursor.execute("ALTER TABLE t_users ADD COLUMN last_name VARCHAR(128) NULL AFTER first_name")
            print("✓ Colonne last_name ajoutée")
        else:
            print("✓ Colonne last_name existe déjà")
        
        # Ajouter phone si elle n'existe pas
        if 'phone' not in existing_columns:
            print("Ajout de la colonne phone...")
            cursor.execute("ALTER TABLE t_users ADD COLUMN phone VARCHAR(20) NULL AFTER last_name")
            print("✓ Colonne phone ajoutée")
        else:
            print("✓ Colonne phone existe déjà")
        
        conn.commit()
        
        # Vérifier le résultat final
        cursor.execute("DESCRIBE t_users")
        print("\nStructure finale de la table t_users:")
        for col in cursor.fetchall():
            print(f"  - {col[0]} ({col[1]})")
        
        cursor.close()
        conn.close()
        print("\n✅ Migration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        return False
    
    return True

if __name__ == "__main__":
    migrate()
