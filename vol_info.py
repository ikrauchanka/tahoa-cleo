# show instances volumes ids, which are `false` when instance terminating.
import json
from pprint import pprint
#aws ec2 describe-volumes --region us-west-2 --filters Name=attachment.delete-on-termination,Values=false > us-west-2
with open('us-west-2') as dfile:
  data = json.load(dfile)
print "InstanceId VolumeId     Device    DeleteOnTermination "

for i in data['Volumes']:
    for j in i['Attachments']:
        print j['InstanceId'],j['VolumeId'],j['Device'],j['DeleteOnTermination'],

    # for c in xrange(len(i['Tags'])):
    #     print i['Tags'][c]['Value']
    if i.has_key('Tags'):
        for item in i['Tags']:
            print  item['Value']
