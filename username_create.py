import hashlib 
import uuid
import extensions

algorithm = 'sha512'
db = extensions.connect_to_database()
cur = db.cursor()
cur.execute('use group120db')
cur.execute('SELECT * FROM User')
users = cur.fetchall()
for user in users:
	password = user['password']
	salt = uuid.uuid4().hex
	m = hashlib.new(algorithm)
	m.update(salt + password)
	password_hash = m.hexdigest()
	finPassword = "$".join([algorithm,salt,password_hash])
	print 'INSERT ' + 'INTO ' + 'User ' + 'VALUES(' + '\'' +user['username'] + '\''  + ', ' + '\'' +user['firstname'] + '\''  + ', ' + '\'' +user['lastname'] + '\''  + ', ' + '\'' + finPassword + '\''  + ', '  + '\'' +user['email'] + '\'' +');'
