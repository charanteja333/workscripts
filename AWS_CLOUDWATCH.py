
#!/usr/bin/python

#Authenticate aws . Not required if .aws config files are present in user home


from boto3.session import Session
session = Session(aws_access_key_id='',
                  aws_secret_access_key='',
                  region_name='<region>')

client = session.client('cloudwatch')

response = client.put_metric_alarm(
    AlarmName='Alarm-<Instance ID>',
    AlarmDescription='Alarm-<Instance ID>',
    ActionsEnabled=True,
 
    AlarmActions=[
        '<SNS ID>',
    ],
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': '<Instance ID>'
        },
    ],
    Period=300,
    Unit='Percent',
    EvaluationPeriods=1,
    Threshold=30.0,
    ComparisonOperator='GreaterThanOrEqualToThreshold'
)


response=client.delete_alarms(AlarmNames=['Alarm-<Instance ID>'])


