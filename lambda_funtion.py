import boto3
import os
import smtplib

from email.message import EmailMessage
from datetime import datetime


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EC2_Instances')
ec2 = boto3.resource('ec2')



def delete_item(instance_id):
    """ Funtion to delete item from DynamoDB """
    response = table.delete_item(
        Key={
            'Instance_id': instance_id,
        },
    )
    print("removed item",instance_id)


def add_item(instance_id):
    """ Funtion to add item to DynamoDB """
    t=datetime.now().strftime("%y/%m/%d %H:%M:%S.%f")
    table.put_item(
                Item={
                    'Instance_id': instance_id,
                    'time_stamp':  t})
                    
    print("Added Item",instance_id)               

def get_item(instance_id):
    """ Funtion to get item from DynamoDB"""
    
    item = table.get_item(
    Key={
        'Instance_id': instance_id,
    },
    )

    if 'Item' in item:
        return item
    else:
        return None
     

   
    
def time_diff(t):
    """ To check if the 6 hr time limit has exceeded"""
    
    
    old_time=datetime.strptime(t["Item"]["time_stamp"], "%y/%m/%d %H:%M:%S.%f")
    cur_time=datetime.now()
    duration = cur_time-old_time                     
    duration_in_s = duration.total_seconds() 
    
    print("Duration:",duration_in_s)
    # checking if the time exceeded 6hrs
    if duration_in_s >= 21600 :
        return True
    else :
        return False

def notifer_status_check(instance_id,instance_mail,params):
    """ Check if the EC2 instances need to be notified or terminated """
    
    
    item=get_item(instance_id)
    
    
    joined_string = ",".join(params)
   
    if item == None :
        add_item(instance_id)
        msg_body=f"You don\'t seem to have the {joined_string} tags set for the instance {instance_id}. Please update them within 6 hours to continue using the EC2 instance."
        send_email(instance_id,instance_mail,msg_body)
        
    
    elif time_diff(item) :
        msg_body=f"Your AWS EC2 Instance with id {instance_id} is being terminated since the required tags {joined_string} haven\'t been updated."
        send_email(instance_id,instance_mail,msg_body)
        print("Terminating the instances")
        ec2.Instance(instance_id).terminate()
        
    
    
   


  
def send_email(instance_id,instance_mail,msg_body):
    """ Funtion to send email """
    
    
    gmail_user = os.environ["mail_username"]
    gmail_password = os.environ["mail_password"]
  
    
   
    msg = EmailMessage()
    msg.set_content(msg_body)
    msg['Subject'] = 'Update Tags in AWS EC2 Instance'
    msg['From'] = gmail_user
    msg['To'] = instance_mail

    # Send the message via our own SMTP server.
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        print("send mail to ",instance_mail," Sucesss")
    except Exception as ex:
        print ("Something went wrong….",ex)
    
   
def remove_terminated():
    """ Remove expired items from DynamoDB"""
    
    print("Removing terminated instances")
    for instance in ec2.instances.all().filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['shutting-down','terminated']}]):
        delete_item(instance.id)
    
    
    
def check_instances():
    """ Check the tags of the EC2 instances """
    
    for instance in ec2.instances.all().filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['pending','running','stopping','stopped']}]):
     
        instance_name=None
        instance_envi=None
        instance_mail=None
       
       
        for tags in instance.tags:
            if tags["Key"] == 'Name':
                instance_name = tags["Value"]
            elif tags["Key"] == 'Environment':
                instance_envi = tags["Value"]
            elif tags["Key"] == 'created by':
                instance_mail = tags["Value"]
        
        
        print("Tags Name-",instance_name,", Environment-",instance_envi,", Created by-",instance_mail, ", InstanceID ",instance.id)
        
        if instance_name == None or instance_envi == None :
            params=[]
            if instance_name == None :
                params.append("Name")
            if instance_envi == None :
                params.append("Environment")
                
            notifer_status_check(instance.id,instance_mail,params)
        
        elif get_item(instance.id)!=None :
            delete_item(instance.id)
            
    remove_terminated()
    
def lambda_handler(event, context):
    """ Main driver funtion """
    check_instances()
    
        
            
                





