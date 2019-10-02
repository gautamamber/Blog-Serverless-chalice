from chalice import Chalice
import boto3
from constant import Constants

app = Chalice(app_name='blog')
cognito = boto3.client("cognito-idp")


# Hello world
@app.route('/')
def index():
    return {'hello': 'world'}

# Cognito authentication
# Signup

@app.route('/auth/signup', methods = ['POST'])
def signup():
    request = app.current_request
    body = request.json_body
    if request.method == "POST":
        cognito.sign_up(
            ClientId = Constants.COGNITO_CLIENT,
            Username = body['Username'],
            Password = body['Password'],
            UserAttributes = [
                {
                "Name": "name",
                "Value": body['name']
                }
            ]
        )
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

