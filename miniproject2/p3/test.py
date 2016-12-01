from bsddb3 import db

# database obj for each idx file
reviews = db.DB()
pterms = db.DB()
rterms = db.DB()
scores = db.DB()

# load idx files into database objs
rterms.set_flags(db.DB_DUP)
reviews.open('rw.idx', None, db.DB_HASH, db.DB_CREATE)
pterms.open('pt.idx', None, db.DB_BTREE, db.DB_CREATE)
rterms.open('rt.idx', None, db.DB_BTREE, db.DB_CREATE)
scores.open('sc.idx', None, db.DB_BTREE, db.DB_CREATE)

cur1 = pterms.cursor()
cur2 = rterms.cursor()

nCursor = pterms.join([cur1, cur2])
print(nCursor.next())