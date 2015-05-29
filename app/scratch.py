from app.sforce import _authenticate

t = _authenticate()
r = t.query("SELECT ID FROM Case WHERE Movements_Number__c={0}".format(882))
print r