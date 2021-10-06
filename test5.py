import sqlite3

import sqlite3
con = sqlite3.connect(r'C:\Users\DE1119189\Desktop\Github\Fileserve_Observer\db\ftpdb.db')
cur = con.cursor()
#cur.execute('delete from destinations;')

for row in cur.execute('select * from destinations;'):
    print(row)

#con.commit()