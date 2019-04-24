
from socketCode import LANconnect

conn = LANconnect('client', 'localhost')

print(conn.receive(100))