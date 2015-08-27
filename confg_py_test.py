import db
import config
import time

print "=" * 60
config.ReadConfigParameters("./parameters.xml")
config.StartRefreshThread()
time.sleep(3)
print "=" * 60
