#!/usr/bin/env python
# (c) 2016 Ilja Kravchenko <fomistoklus+github@gmail.com>
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# Script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import boto.ec2
from prettytable import PrettyTable

conn = boto.ec2.connect_to_region('us-east-1',aws_access_key_id='', aws_secret_access_key='')
reservations = conn.get_all_instances()
instances = [i for r in reservations for i in r.instances]

result = {}

price = {'cc2.8xlarge' : 1460.000,
'cg1.4xlarge' : 1533.000,
't2.nano' : 4.745,
't2.micro' : 9.490,
't2.small' : 18.980,
't2.medium' : 37.960,
't2.large' : 75.920,
'm4.large' : 87.600,
'm4.xlarge' : 174.470,
'm4.2xlarge' : 349.670,
'm4.4xlarge' : 699.340,
'm4.10xlarge' : 1747.620,
'c4.large' : 76.650,
'c4.xlarge' : 152.570,
'c4.2xlarge' : 305.870,
'c4.4xlarge' : 611.740,
'c4.8xlarge' : 1222.750,
'g2.2xlarge' : 474.500,
'g2.8xlarge' : 1898.000,
'r3.large' : 121.180,
'r3.xlarge' : 243.090,
'r3.2xlarge' : 485.450,
'r3.4xlarge' : 970.900,
'r3.8xlarge' : 1941.800,
'i2.xlarge' : 622.690,
'i2.2xlarge' : 1244.650,
'i2.4xlarge' : 2489.300,
'i2.8xlarge' : 4978.600,
'd2.xlarge' : 503.700,
'd2.2xlarge' : 1007.400,
'd2.4xlarge' : 2014.800,
'd2.8xlarge' : 4029.600,
'hi1.4xlarge' : 2263.000,
'hs1.8xlarge' : 3358.000,
'm3.medium' : 48.910,
'm3.large' : 97.090,
'm3.xlarge' : 194.180,
'm3.2xlarge' : 388.360,
'c3.large' : 76.650,
'c3.xlarge' : 153.300,
'c3.2xlarge' : 306.600,
'c3.4xlarge' : 613.200,
'c3.8xlarge' : 1226.400,
'm1.small' : 32.120,
'm1.medium' : 63.510,
'm1.large' : 127.750,
'm1.xlarge' : 255.500,
'c1.medium' : 94.900,
'c1.xlarge' : 379.600,
'm2.xlarge' : 178.850,
'm2.2xlarge' : 357.700,
'm2.4xlarge' : 715.400,
't1.micro' : 14.600,
'cr1.8xlarge' : 2555.000
}

def cost(price, instance_type):
    for k,v in price.iteritems():
        if k == instance_type:
            return v

t = PrettyTable(['app name', 'cost'])

for ins in instances:
    value = cost(price, ins.instance_type)
    if ins.tags['Name'] in result:
        result[ins.tags['Name']] = result[ins.tags['Name']] + value
    else:
        result[ins.tags['Name']] = value

for k, v in result.iteritems():
    t.add_row([k,v])

t.align["app name"] = "l"
t.align["cost"] = "l"
t.sortby = "cost"
print t

