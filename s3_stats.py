import boto.rds2
from prettytable import PrettyTable

conn = boto.rds2.connect_to_region('us-east-1', aws_access_key_id='', aws_secret_access_key='')
res = conn.describe_db_instances()
postgres = {}
mysql = {}
price_mysql = {'db.r3.xlarge': 346.750,
         'db.t2.medium': 49.640,
         'db.t2.large': 99.280,
         'db.t2.small': 24.820
         }
price_post = {'db.r3.xlarge': 365.000,
         'db.t2.medium': 53.290,
         'db.t2.large': 105.850,
         'db.t2.small': 26.280
         }

m = PrettyTable(['Name', 'Cost', 'Engine', 'MultiAZ' ])
p = PrettyTable(['Name', 'Cost', 'Engine', 'MultiAZ' ])


def cost(price, instance_type):
    for k,v in price.iteritems():
        if k == instance_type:
            return v

for k,v in res.iteritems():
    for a,b in v.iteritems():
        for j,l in b.iteritems():
            if j == 'DBInstances':
                for i in l:
                    name = i['Endpoint']['Address'].split('.')[0]
                    if i['Engine'] == 'postgres':
                        value = cost(price_mysql, i['DBInstanceClass'])
                        #we can do this because rds doesn't allow same names
                        postgres[name] = value
                        p.add_row([name, value, i['Engine'], i['MultiAZ']])
                    elif i['Engine'] == 'mysql':
                        value = cost(price_post, i['DBInstanceClass'])
                        mysql[name] =  value
                        m.add_row([name, value, i['Engine'], i['MultiAZ']])
                    else:
                        print 'UNKNOWN DBInstanceClass'

                    #print i['MasterUsername'],i['Engine'],i['PubliclyAccessible'],i['MultiAZ'],i['DBInstanceClass'], i['Endpoint']['Port'],i['Endpoint']['Address'], '\n'

m.align["Name"] = "l"
m.align["Cost"] = "l"
m.align["Engine"] = "l"
m.sortby = "Cost"
print m

p.align["Name"] = "l"
p.align["Cost"] = "l"
p.align["Engine"] = "l"
p.sortby = "Cost"
print p
