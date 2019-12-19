import ha_jaydebeapi
import sys

from utils.exceptions import convert_result_list, JError

username = ''
password = 'API_KEY'

conn = ha_jaydebeapi.connect("com.qubole.jdbc.jdbc41.core.QDriver",
                          "jdbc:qubole://hive/default/tier1_edw_batch?endpoint=https://us.qubole.com",
                             ["", password])

if conn:
    print('Connection established with Qubole')
else:
    print('Connection Failed')

cursor = conn.cursor()
query = "select count(*) cnt from tier1_edw_batch.application"
try:
    result = cursor.execute(query)
    data = cursor.fetchall()
    if data:
        column_names = [i[0] for i in cursor.description]
        result = [dict(zip(column_names, row)) for row in data]
        result = convert_result_list(result)
        print(result)
except Exception as e:
    exc_type, exc_value, exc_trace = sys.exc_info()
    raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)

r = result[0]['cnt']
print(type(r))
print(r)

cursor.close()
conn.close()
