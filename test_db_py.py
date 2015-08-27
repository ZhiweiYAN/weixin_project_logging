
import db
#### Test Unit ####
db_name = "test002"
db_user = "postgres"
db_pw = "1234"
db_port = "5432"
db_host = "127.0.0.1"

#connection handle for PostgreSQL
###################
print "=" * 60
db.InitDBTables(db_name, db_user, db_pw, db_host, db_port)
u = db.Work_Flow.insert(creator_id='001')
u.execute()
print "=" * 60

