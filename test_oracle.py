
import os
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"/opt/oracle/instantclient_21_8")

con = cx_Oracle.connect(user="tipmontt", password='p#montt_',
                               dsn="10.1.124.4:1521/edelfosp.ulagos.cl",
                               encoding="UTF-8")


print("Connected!")
cur = con.cursor()
for row in cur.execute("SELECT * FROM DELFOS.BIE_MATRICULA_ANTECEDENTES where rownum <= 10"):
    print(row)
con.close()
