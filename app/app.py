from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from flask_mail import Mail, Message
from routes import routes_config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = ''  
app.config['MAIL_PASSWORD'] = ''  

mail = Mail(app)

app.register_blueprint(routes_config, url_prefix='/')


###########################
# FUNCIONES
###########################

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('routes.index'))
    else:
        return redirect(url_for('routes.login'))

# Ruta para cargar y procesar el archivo CSV
    
if __name__ == '__main__':
    app.run(debug=True)
