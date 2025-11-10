
import sqlite3
import os

# --- CONFIGURACION ---
DB_FILE = "../monitor_ping.db"
ADMIN_USERNAME = "admin"
# Hash pre-calculado para la contrasena "admin"
# Este hash fue generado con un entorno de bcrypt que funciona correctamente.
ADMIN_PASSWORD_HASH = "$5$rounds=535000$4x6cT92.uGgblWa7$brEv.a/5RBcxut/zk1OqaTpHgruCARaPwqb.QMGvPc9"
ADMIN_ROLE = "ADMIN"
ADMIN_FULLNAME = "Administrador del Sistema"

# --- LOGICA ---
db_path = os.path.join(os.path.dirname(__file__), DB_FILE)

print(f"Conectando a la base de datos en: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print(f"Intentando insertar o reemplazar al usuario '{ADMIN_USERNAME}'...")
    # Usamos REPLACE para sobrescribir al usuario si ya existe, o crearlo si no.
    # Esto limpia cualquier entrada rota anterior.
    cursor.execute(
        """
        REPLACE INTO TB_USUARIOS_DEL_SISTEMA (nom_usuario, password_hash, rol)
        VALUES (?, ?, ?)
        """,
        (ADMIN_USERNAME, ADMIN_PASSWORD_HASH, ADMIN_ROLE),
    )
    conn.commit()
    print("---------------------------------------------------------")
    print(f"==> Usuario '{ADMIN_USERNAME}' creado/actualizado exitosamente.")
    print("==> La contrasena es: admin")
    print("---------------------------------------------------------")

except sqlite3.Error as e:
    print(f"ERROR: Ocurrio un error con la base de datos: {e}")

finally:
    print("Cerrando conexion con la base de datos.")
    conn.close()

