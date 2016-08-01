#!/usr/bin/env python

#Establish connection to ec2 using boto.
#AWS keys are stored in user home .aws dir which are taken by default

import boto3
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
for instance in ec2.instances.all():
  print(instance.id)

#Create VPC , subnets based on given args

vpc = ec2.create_vpc(CidrBlock='10.2.0.0/16')
client.create_tags(Resources=[vpc.id],Tags=[{'Key':'Name','Value':'New-VPC'}])
subnetpriv = vpc.create_subnet(CidrBlock='10.2.0.0/24')
subnetpub = vpc.create_subnet(CidrBlock='10.2.1.0/24')

#Gateway needs to be created first and attached to a VPC

gateway = ec2.create_internet_gateway()
response=gateway.attach_to_vpc(VpcId=vpc.id)
print "vpc=",vpc.id
print "privatesubnet=",subnetpriv.id
print "publicsubnet=",subnetpub.id
print "gateway=",gateway.id


#create route tables for private and public subnets. This will be assigned to subnet later
route_tablepriv = ec2.create_route_table(VpcId=vpc.id)
route_tablepub = ec2.create_route_table(VpcId=vpc.id)
print "publicroute=",route_tablepub.id
print "privateroute=",route_tablepriv.id

#Create security group in new VPC
security_group = ec2.create_security_group(VpcId=vpc.id,Description="test",GroupName="test")

#Modifit security group inbound rules accordingly
responsesg = security_group.authorize_ingress(
                                            CidrIp='0.0.0.0/0',
                                            IpProtocol='TCP',
                                            FromPort=0,
                                            ToPort=65535)


print "securitygroup=",security_group.id


#assign the created route tables to subnets
route_table_association_priv = route_tablepriv.associate_with_subnet(SubnetId=subnetpriv.id)
route_table_association_pub = route_tablepub.associate_with_subnet(SubnetId=subnetpub.id)

#Create route for public subnet to pass through internet gateway for internet connectivity
responsepub = route_tablepub.create_route(DestinationCidrBlock='0.0.0.0/0',GatewayId=gateway.id)



#Spawn a NAT instance in created public subnet of the new VPC
ins = ec2.create_instances(
    ImageId = '<AMI ID>',
    MinCount = 1,
    MaxCount = 1,
    KeyName = 'charan',
    InstanceType = 't2.small',

    InstanceInitiatedShutdownBehavior='stop',
    NetworkInterfaces=[{'DeviceIndex': 0,'Groups':[security_group.id],'SubnetId':subnetpub.id,'AssociatePublicIpAddress': True}],

    )
client.create_tags(Resources=[ins[0].id],Tags=[{'Key':'Name','Value':'Nat-instance-'+vpc.id}])
instance = ec2.Instance(ins[0].id)

#Disable the source dest check parameter for nat instance 
responseins = instance.modify_attribute(Attribute='sourceDestCheck',Value='False')
print "id",ins[0].id

#Wait till the instance is in running state
instance.wait_until_running()

#Create the route for route table assigned to private subnet
responsepriv=route_tablepriv.create_route(DestinationCidrBlock='0.0.0.0/0',InstanceId=ins[0].id)



#Deleting the created VPC


import boto3
ec2 = boto3.resource('ec2')

instance = ec2.Instance('<id>')
responseins = instance.terminate()
instance.wait_until_terminated()

internet_gateway = ec2.InternetGateway('<gatewayid>')
internet_gateway.detach_from_vpc(VpcId='<vpcid>')
internet_gateway.delete()

privsubnet = ec2.Subnet('<privatesubnet>')
pubsubnet = ec2.Subnet('<publicsubnet>')
privsubnet.delete()
pubsubnet.delete()

pubroute_table = ec2.RouteTable('<publicroute>')
privroute_table = ec2.RouteTable('<privateroute>')
pubroute_table.delete()
privroute_table.delete()

security_group = ec2.SecurityGroup('<securitygroup>')
security_group.delete()

vpc = ec2.Vpc('<vpcid>')
vpc.delete()


