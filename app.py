from chalice import Chalice
import boto3
from constant import Constants

app = Chalice(app_name='blog')
cognito = boto3.client("cognito-idp")
dynamo = boto3.resource("dynamodb")
user_table = dynamo.Table(Constants.USER_TABLE)

def add_user(body):
    user_table.put_item(
        Item = body
    )

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

