import os, sys, datetime
from datetime import timedelta
from flask import Flask
from flask import jsonify
from models import Instance, InstanceRecord

app = Flask(__name__)

@app.route('/aggregate')
def get_aggregate():

    result = {}

    # Retrieving records for all instances in the last day
    aggregate_data = Instance.objects(records__timestamp__gte=datetime.datetime.now() - timedelta(days=1))

    for instance in aggregate_data:

        # We have zone but we want region
        instance_region = instance["instance_zone"][:-1]

        # Adding region to results if it does not exist
        if instance_region not in result:
            result[instance_region] = {}

        # Adding type into region if it does not exist
        if instance["instance_type"] not in result[instance_region]:
            result[instance_region][instance["instance_type"]] = 1
        # If it does, simply incrementing the counter
        else:
            result[instance_region][instance["instance_type"]] += 1

    return jsonify(result)

if __name__ == '__main__':

    if 'CM_DB_URI' not in os.environ or 'CM_DB_NAME' not in os.environ:
        sys.stderr.write("\033[91mCM_DB_URI and CM_DB_NAME system variables are required\033[0m\n")
        sys.stderr.write("\033[91mApplication will now exit\033[0m\n")
        exit(1)

    app.run(debug = True)
