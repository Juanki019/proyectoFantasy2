import subprocess
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from flask_mail import Mail, Message
from querys.querys import is_admin_profile
from routes import routes_config
import sys
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'


mail = Mail(app)

app.secret_key = 'tu_clave_secreta'

app.register_blueprint(routes_config, url_prefix='/')

def iniciar_subprocesos():
    script_path = os.path.join(os.path.dirname(__file__), 'app', 'scrappers', 'scraperJornadas.py')
    subprocess.Popen([sys.executable, script_path])
    print("Subproceso iniciado correctamente.")
    

@app.route('/')
def index():
    if 'username' in session:
        if is_admin_profile(session['username']) != 777:
            return redirect(url_for('routes.index'))
        else:
            return redirect(url_for('routes.adminDashboard'))
    else:
        return redirect(url_for('routes.login'))


if __name__ == '__main__':
    iniciar_subprocesos()
    print("Subproceso iniciado correctamente.")
    app.run(debug=True)

