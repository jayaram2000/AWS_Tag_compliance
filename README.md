# AWS_Tag_compliance
AWS lambda function to enforce tag policy on EC2 instances hosted in a region


## Description

A python serverless lambda function which would terminate all EC2 instances which don’t follow a tagging criteria. The funtion checks EC2 instances which don’t have ‘Environment’ and ‘Name’ tags attached on it and sends reminder mail to respective emails pointed by the 'created by' tag. Terminates the instances if the tags havent been upated within 6 hrs from the notifed mail.

## Getting Started

### Dependencies

* AWS Lambda funtion 
* DynamoDB instance
* EventBridge CloudWatch Events
* python 3.8
* boto3 SDK
* smtplib

### Deployment Procedure

1) Create an AWS Lambda funtion in the same region as the EC2 instances 
    * Use python 3.9 runtime and default role with basic Lambda permissions
    * Add AmazonEC2FullAccess, AmazonDynamoDBFullAccess policies to the default role created
    * 

2) Add environment variables for Email account to notify users 
    * Enable 2-factor authentication for the mail account and generate an app password
    * Add the following envirnoment varibales under the configuration->environment variables in lambda funtion 
      ~~~
      mail_username : yourmail@example.com
      mail_password : your_password
      ~~~
      
3) Create a trigger to call the lambda funtion hourly
    * Create a new trigger using EventBridge CloudWatch Events
    * create a new rule with any suitable name and the given schedule expression <b>cron(0 * * * ? *)
   
5)  How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

Jayaram J 
[Jayaram J]("mailto:jayaramjawahar@gmail.com?subject=Mail from AWS Tag github repo")

