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
    if request.method == "POST":
        response = cognito.sign_up(
            ClientId = Constants.COGNITO_CLIENT,
            Username = "ambergautam1@gmail.com",
            Password = "Test@12345",
            UserAttributes = [
                {
                "Name": "name",
                "Value": "Amber gautam"
                }
            ]
        )
        data = {
            "result": Constants.SUCCESS
        }
    return data
