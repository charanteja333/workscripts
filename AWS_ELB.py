#!/usr/bin/python

#Authenticate aws . Not required if .aws config files are present in user home

from boto3.session import Session
session = Session(aws_access_key_id='<keyid>',
                  aws_secret_access_key='<secretkey>',
                  region_name='<region>')

#create load balancer
client = session.client('elb')
response1 = client.create_load_balancer(
    LoadBalancerName='<LOADBALANCERNAME>',
    Listeners=[
        {
            'Protocol': '<LOADBALANCERPROTOCOL>',
            'LoadBalancerPort': <LOADBALANCERPORT>,
            'InstanceProtocol': '<INSTANCEPROTOCOL>',
            'InstancePort': <INSTANCEPORT>,
        },
    ],
   
     Subnets=[
        '<SUBNETS>',
    ],
     SecurityGroups=[
        '<SECURITYGROUPS>',
    ],
    Scheme='<SCHEME>',
  
)

#point to instances
response2 = client.register_instances_with_load_balancer(
    LoadBalancerName='<LOADBALANCERNAME>',
    Instances=[
        {
            'InstanceId': '<INSTANCEIDS>'  #Instance ID's should be comma seperated
        },
    ]
)

print "ELBDNSNAME=",response1['DNSName']

#Add health check parameters
response3 = client.configure_health_check(
    LoadBalancerName='<LOADBALANCERNAME>',
    HealthCheck={
        'Target': '<HEALTHCHECKTARGET>',
        'Interval': <HEATLHCHECKINTERVAL>,
        'Timeout': <HEATLHCHECKTIMEOUT>,
        'UnhealthyThreshold': <HEATLHCHECKUNHEALTHYTHRESHOLD>,
        'HealthyThreshold': <HEATLHCHECKHEALTHYTHRESHOLD>,
    }
)

#Add tags

tags="<TAGS>"
tags=tags.split(',')
for i in tags:
  i=i.split(':')
  response5 = client.add_tags(
    LoadBalancerNames=[
        '<LOADBALANCERNAME>',
    ],
    Tags=[
        {
            'Key': str(i[0]),
            'Value': str(i[1])
        },
    ]
)
