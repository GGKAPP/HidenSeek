from flask import Flask, request, make_response, redirect, render_template_string

app = Flask(__name__)

# Pre-defined username and password
VALID_USERNAME = "jonjones"
VALID_PASSWORD = "lojci279@#$$mscubscksi"
FLAG = "heCTF{C00K13S_AUTH_C4NT_G3T_11f30jk7}"

# Home route (Login Page)
@app.route('/')
def home():
    return render_template_string('''
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body { background-color: #f8f9fa; }
            .login-container {
                max-width: 400px;
                margin: auto;
                padding: 30px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                margin-top: 50px;
            }
            .login-header { text-align: center; margin-bottom: 20px; }
            .btn-primary { background-color: #5CB85C; border: none; }
            .btn-primary:hover { background-color: #4CAE4C; }
        </style>
        <div class="login-container">
            <h2 class="login-header">Login</h2>
            <form action="/login" method="POST">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input class="form-control" type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input class="form-control" type="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
        </div>
    ''')

# Login route (POST method)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Create a response object
    response = make_response(redirect('/dashboard'))

    # Check for valid credentials
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        # Set cookie if valid login
        response.set_cookie('password', 'true')
        response.set_cookie('username', username)
    else:
        # Set cookie to false if login fails
        response.set_cookie('password', 'false')
        response.set_cookie('username', username)
        
    return response

# Dashboard route (protected content)
@app.route('/dashboard')
def dashboard():
    auth_status = request.cookies.get('password', 'false')

    # Check if the auth cookie is set to true
    if auth_status == 'true':
        username = request.cookies.get('username')
        return render_template_string(f'''
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {{ background-color: #f8f9fa; }}
                .content-container {{
                    max-width: 600px;
                    margin: auto;
                    padding: 30px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    margin-top: 50px;
                }}
                .logout-btn {{
                    margin-top: 20px;
                    text-align: center;
                }}
            </style>
            <div class="content-container">
                <h2>Welcome, {username}!</h2>
                <p><b>Protected Content:</b> {FLAG}</p>
                <div class="logout-btn">
                    <a href="/logout" class="btn btn-danger">Logout</a>
                </div>
            </div>
        ''')
    else:
        # If unauthorized or cookie is tampered
        return "<h3>Access Denied! Unauthorized User.</h3>"

# Logout route (Clears Cookies)
@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('password', '', expires=0)
    response.set_cookie('username', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)
