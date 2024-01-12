import subprocess
import requests
import pymysql
import pyodbc

# Vérification de la santé des conteneurs Docker
def test_sante_conteneurs():
    conteneurs = ["microservice_implement_stockmanagement-flask-frontend-1"]

    for conteneur in conteneurs:
        try:
            subprocess.check_output(["docker", "ps", "--filter", f"name={conteneur}"])
            print(f"Le conteneur {conteneur} est en cours d'exécution.")
        except subprocess.CalledProcessError:
            print(f"Le conteneur {conteneur} n'est pas en cours d'exécution.")


# Vérification du bon fonctionnement de l'application Flask
def test_bon_fonctionnement_application():
    url = "http://127.0.0.1:5000/"
    response = requests.get(url)
    if response.status_code == 200:
        print("L'application Flask fonctionne correctement.")
    else:
        print("Problème avec l'application Flask.")

# Vérification du bon fonctionnement de la base de données MySQL
# def test_bon_fonctionnement_base_de_donnees():
#     server = 'microservice_implement_stockmanagement-sql-server-backend-1,1433'
#     database = "InventoryManagement"
#     username = "SA"
#     password = "abcDEF123#"

#     try:
#         # Chaîne de connexion à la base de données SQL Server
#         # conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
#         conn_str = 'DRIVER={{ODBC Driver 18 for SQL Server}};Server='+server+';Database='+ database + ';Uid=' + username  + ';Pwd='+ password + ';Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;'

#         # Connexion à la base de données
#         connection = pyodbc.connect(conn_str)
#         cursor = connection.cursor()

#         # Exécution d'une requête pour vérifier le bon fonctionnement
#         cursor.execute("SELECT COUNT(*) FROM Location")
#         count = cursor.fetchone()[0]

#         if count > 0:
#             print("La base de données SQL Server fonctionne correctement.")
#         else:
#             print("Aucune entrée dans la table. Vérifiez la base de données.")
#     except Exception as e:
#         print(f"Problème avec la base de données SQL Server: {str(e)}")
#     finally:
#         if 'connection' in locals() and connection:
#             connection.close()

# Exécution des tests
if __name__ == "__main__":
    test_sante_conteneurs()
    test_bon_fonctionnement_application()
    # test_bon_fonctionnement_base_de_donnees()