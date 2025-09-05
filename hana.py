from hdbcli import dbapi
from config import HANA_HOST, HANA_PORT, HANA_USER, HANA_PASSWORD

def query_hana(sql: str):
    try:
        conn = dbapi.connect(
            address=HANA_HOST,
            port=HANA_PORT,
            user=HANA_USER,
            password=HANA_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        return f"SAP HANA DB Error: {str(e)}"
