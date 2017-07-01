import os,datetime
from mongoengine import *

'''
Database connection handled here
Details extracted from system environment variables
'''
if 'CM_DB_URI' in os.environ and 'CM_DB_NAME' in os.environ:
    db_uri = os.environ['CM_DB_URI']
    db_name = os.environ['CM_DB_NAME']

    # TODO: Handle invalid connection string
    connect(
        db=db_name,
        host=db_uri
    )

'''
Instance collection
'''
class InstanceRecord(EmbeddedDocument):
    instance_state = StringField(max_length = 20)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)

class Instance(Document):
    instance_id = StringField(max_length = 200, unique = True, required= True)
    instance_name = StringField(max_length = 200)
    instance_type = StringField(max_length = 200, required= True)
    instance_zone = StringField(max_length = 20, required= True)
    instance_account = StringField(max_length = 12, required= True)
    records = ListField(EmbeddedDocumentField(InstanceRecord))
