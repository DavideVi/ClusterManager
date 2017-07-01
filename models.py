import os,datetime
from mongoengine import *

'''
Database connection handled here
Details extracted from system environment variables
'''

if os.environ['CM_DB_URI'] is not None:
    db_uri = os.environ['CM_DB_URI']
else:
    raise ValueError('CM_DB_URI system environment variable is not set')

if os.environ['CM_DB_NAME'] is not None:
    db_name = os.environ['CM_DB_NAME']
else:
    raise ValueError('CM_DB_NAME system environment variable is not set')

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
