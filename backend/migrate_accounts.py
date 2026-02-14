import mysql.connector
import random
import string
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

def migrate_accounts():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        print("Connexion réussie")
        
        # 1. Ajouter la colonne account_number (autoriser temporairement NULL)
        cursor.execute("DESCRIBE t_accounts")
        cols = [col[0] for col in cursor.fetchall()]
        if 'account_number' not in cols:
            print("Ajout de la colonne account_number...")
            cursor.execute("ALTER TABLE t_accounts ADD COLUMN account_number VARCHAR(20) NULL AFTER user_id")
            conn.commit()
        
        # 2. Générer des numéros pour les comptes existants
        cursor.execute("SELECT id FROM t_accounts WHERE account_number IS NULL")
        accounts = cursor.fetchall()
        
        for (acc_id,) in accounts:
            while True:
                num = ''.join(random.choices(string.digits, k=10))
                cursor.execute("SELECT id FROM t_accounts WHERE account_number = %s", (num,))
                if not cursor.fetchone():
                    cursor.execute("UPDATE t_accounts SET account_number = %s WHERE id = %s", (num, acc_id))
                    print(f"Compte {acc_id} -> {num}")
                    break
        
        conn.commit()
        
        # 3. Rendre la colonne NOT NULL et UNIQUE
        print("Finalisation de la colonne...")
        cursor.execute("ALTER TABLE t_accounts MODIFY COLUMN account_number VARCHAR(20) NOT NULL")
        cursor.execute("ALTER TABLE t_accounts ADD UNIQUE (account_number)")
        conn.commit()
        
        print("✅ Migration des comptes terminée!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erreur migration: {e}")

if __name__ == "__main__":
    migrate_accounts()
