
from socketCode import LANconnect

conn = LANconnect('server', 'localhost', 'localhost')

conn.send('Hello World')
