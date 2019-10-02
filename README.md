# Blog-Serverless-chalice
#### A blog application in aws serverless using chalice (micro framework for building serverless application)

### AWS Services used:

* Cognito: Authentication
* DynamoDB: NoSql Database
* APIGateway: Rest API'S
* Lambda functions

### Key points:

* User able to signup, login, change password
* User Get profile
* Create new blog, only for authenticated user with (Cognito JWT token)
* Get List of all blogs
* Get List of only user's blogs

# About Chalice

#### AWS Chalice allows you to quickly create and deploy applications that use Amazon API Gateway and AWS Lambda

### Install

```
pip install chalice
```

### Start new project

```
chalice new-project helloworld && cd helloworld
```

### Deploy

```
chalice deploy
```

### Run local

```
chalice local
```

#### For more details, visit
[https://chalice.readthedocs.io/en/latest/]https://chalice.readthedocs.io/en/latest/

