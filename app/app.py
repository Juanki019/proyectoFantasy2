import subprocess
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from flask_mail import Mail, Message
from routes import routes_config
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = 'dreamxiuem@gmail.com'  
app.config['MAIL_PASSWORD'] = 'dreamxiuem24$'  

mail = Mail(app)

app.secret_key = 'tu_clave_secreta'

app.register_blueprint(routes_config, url_prefix='/')

def iniciar_subprocesos():
    subprocess.Popen([sys.executable, './scrappers/lesionadosScrap.py'])
    print("Subproceso iniciado correctamente.")
    
iniciar_subprocesos()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('routes.index'))
    else:
        return redirect(url_for('routes.login'))

if __name__ == '__main__':
    subprocess.Popen([sys.executable, './scrappers/lesionadosScrap.py'])
    print("Subproceso iniciado correctamente.")
    app.run(debug=True)

