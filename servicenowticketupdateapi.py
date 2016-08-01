#!/usr/bin/env python

from suds import *
wsdl_url='<service now wsdl URL>'
try:
  cli=client.Client(url=wsdl_url,username='<username>',password='password')
  cli.service.update(sys_id='<Service_req>',comments='Machines <ip_list> created. Hence closing the ticket', incident_state=6)
  print "Sysid <Service_req> has been closed succesfully"
except Exception as e:
  print "Failure in closing the ticket due to error" + str(e)
  exit(1)



#!/usr/bin/env python

from suds import *
wsdl_url='<service now wsdl url>'
try:
  cli=client.Client(url=wsdl_url,username='<username>',password='<password>')
  inc_h=cli.service.insert(active='True',assigned_to='charan teja',assignment_group='IT',
                           caller_id='Test',u_product_tier_1='Hardware',
                           u_product_tier_2='Desktop Devices',u_product_tier_3='Desktop',
                           u_operational_tier_1='End User Services',u_operational_tier_2='How To Support',
                           u_support_organization='IT',u_operational_tier_3='General',u_source='Email',
                           description='Service down',short_description='Service is down.Please check',
                           impact=2,incident_state=1,urgency=1)
  print "Service_req=%s" %(str(inc_h.sys_id))
  print "Incident_Number=%s" %(str(inc_h.number))
except Exception as e:
  print "Error while creating service request" + str(e)
  exit(1)
