from chalice import Chalice

app = Chalice(app_name='blog')


# Hello world
@app.route('/')
def index():
    return {'hello': 'world'}

# Cognito authentication
# Signup

@app.route('/auth/signup/', method = ['POST'])
def signup():
    pass