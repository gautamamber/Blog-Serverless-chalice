from chalice import Chalice
import boto3
from constant import Constants
from decode_verify_jwt import token_verification
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

app = Chalice(app_name='blog')
cognito = boto3.client("cognito-idp")
dynamo = boto3.resource("dynamodb")
user_table = dynamo.Table(Constants.USER_TABLE)
blog_table = dynamo.Table(Constants.BLOG_TABLE)

def add_user(body):
    user_table.put_item(
        Item = body
    )

def get_user_profile(username):
    response = user_table.get_item(
            Key = {
                "username": username
            }
        )
    return response

# Hello world
@app.route('/')
def index():
    return {'hello': 'world'}


# DynamoDB User table, put user data

# Cognito authentication
# Signup

@app.route('/auth/signup', methods = ['POST'])
def signup():
    request = app.current_request
    body = request.json_body
    if request.method == "POST":
        response = cognito.sign_up(
            ClientId = Constants.COGNITO_CLIENT,
            Username = body['username'],
            Password = body['password'],
            UserAttributes = [
                {
                "Name": "name",
                "Value": body['name']
                }
            ]
            )
        add_to_user = {
            "username" : response['UserSub'],
            "name": body['name'],
            "email": body['username'],
            "age": body['age'],
            "contact": body['contact'],
            "city": body['city']
        }

        add_user(add_to_user)
        data = {
            "result": Constants.SUCCESS
        }
    return data

# Login 
@app.route('/auth/login', methods = ['POST'])
def login():
    request = app.current_request
    body = request.json_body
    if request.method == "POST":
        response = cognito.initiate_auth(
            AuthFlow = "USER_PASSWORD_AUTH",
            AuthParameters = {
                "USERNAME": body['USERNAME'],
                "PASSWORD": body['PASSWORD']
            },
            ClientId = Constants.COGNITO_CLIENT
        )
        del response['ResponseMetadata']
        del response['ChallengeParameters']
        data = {
            "result": response
        }
        return data
    
# Change Password
@app.route('/auth/change-password', methods = ['POST'])
def change_password():
    request = app.current_request
    body = request.json_body
    if request.method == "POST":
        cognito.change_password(
            PreviousPassword = body['previous_password'],
            ProposedPassword = body['proposed_password'],
            AccessToken = body['access_token']

        )
    data = {
        "result" : Constants.SUCCESS
    }
    return data

@app.route("/profile/get-user/{username}", methods = ['GET'])
def get_user(username):
    request = app.current_request
    if request.method == "GET":
        response = get_user_profile(username)
        del response['ResponseMetadata']
        data = {
                "result": response
            }
        return data
    
# Blogs
# add new blog by user authentication

@app.route("/blog/add-new", methods = ['POST'])
def add_new():
    request = app.current_request
    body = request.json_body
    token = request.headers['authorization']
    token_data = token_verification(token)
    if token_data == False:
        data = {
            "result": Constants.NOT_AUTHORIZE
        }
    else:
        username = token_data['cognito:username']
        profile = get_user_profile(username)
        name = profile['Item']['name']
        timestamp = datetime.now().timestamp()
        created_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%S')
        blog_table.put_item(
            Item = {
                "blogId": str(uuid.uuid4()),
                "userId": username,
                "name": name,
                "title": body['title'],
                "description": body['description'],
                "created_at": created_date
            }
        )
        data = {
            "result": Constants.SUCCESS
        }
    return data

# Get complete list of all records
@app.route("/blog/list", methods = ['GET'])
def get_list():
    request = app.current_request
    token = request.headers['authorization']
    token_data = token_verification(token)
    if token_data == False:
        data = {
            "result": Constants.NOT_AUTHORIZE
        }
    else:
        response = blog_table.scan()
        data = {
                "result": response['Items']
        }
    return data

# Get only user blogs
@app.route("/blog/user-all-blog/{blog_id}", methods = ['GET'])
def get_user_blogs(blog_id):
    request = app.current_request
    token = request.headers['authorization']
    token_data = token_verification(token)
    if token_data == False:
        data = {
            "result": Constants.NOT_AUTHORIZE
        }
    else:
        username = token_data['cognito:username']
        response = blog_table.query(
            KeyConditionExpression=Key('blogId').eq(blog_id) & Key('userId').eq(username)
        )
        
        data = {
                "result": response['Items']
        }
    return data
        


