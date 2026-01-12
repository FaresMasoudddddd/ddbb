import cx_Oracle

def get_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XEPDB1")  # change to your PDB name
    return cx_Oracle.connect(
        user="hotel",
        password="hotel123",
        dsn=dsn
    )
