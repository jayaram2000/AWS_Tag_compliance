# AWS_Tag_compliance
AWS lambda function to enforce tag policy on EC2 instances hosted in a region


## Description

A python serverless lambda function which would terminate all EC2 instances which don’t follow a tag policy. The function checks EC2 instances which don’t have ‘Environment’ and ‘Name’ tags attached on it and sends reminder mail to respective emails pointed by the 'created by' tag. Terminates the instances if the tags havent been upated within 6 hrs from the notifed mail.

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
    * Choose author from scratch option
    * Use python 3.8 runtime and default role with basic Lambda permissions
    * Add AmazonEC2FullAccess, AmazonDynamoDBFullAccess policies to the default role created
    * Copy paste the lambda_funtion.py file contents onto the AWS lambda lambda_funtion.py file
    * Change the execution time from default 3 sec to optimal value >=2min

2) Add environment variables for Email account to notify users 
    * Enable 2-factor authentication for the mail account and generate an app password
    * Add the following envirnoment variables under the configuration->environment variables in lambda function 
      ~~~
      <b>mail_username : yourmail@example.com</b>
      <b>mail_password : your_password</b>
      ~~~
 
3) Create a AWS DynamoDB Table
   * Give the table name **'EC2_Instances'**
   * Add **'Instance_id'** as Partition key with string type
 
 
4) Create a trigger to call the lambda funtion hourly
    * Create a new trigger using EventBridge CloudWatch Events
    * create a new rule with any suitable name and the given schedule expression **cron(0 * * * ? *)**
   


### Executing program

* To test the working of the lambda function create a empty test event
* If the execution completes then all the configurations are set properly
```
code blocks for commands
```

## Help

Frequently encountered problems
* EC2 instances and the lambda funtions are set-up in different AWS regions
* Execution time is too less to complete proper execution
* 
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

Jayaram J 
[Jayaram J]("mailto:jayaramjawahar@gmail.com?subject=Mail from AWS Tag github repo")

