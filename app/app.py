import subprocess
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from flask_mail import Mail, Message
from querys.querys import is_admin_profile, tunnel
from routes import routes_config
from sshtunnel import HandlerSSHTunnelForwarderError
import sys
import os
import logging

app = Flask(__name__)
app.secret_key = 'e6d57962610614c813054cf3c3716f01'


mail = Mail(app)

try:
    tunnel.start()
    logging.info("Tunnel SSH established successfully on local port: %s", tunnel.local_bind_port)
except HandlerSSHTunnelForwarderError as e:
    logging.error("Failed to establish SSH tunnel: %s", e)
    exit(1)

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
    try:
        # iniciar_subprocesos()
        app.run(debug=True)
    finally:
        if tunnel.is_active:
            tunnel.stop()
    
    print("Subproceso iniciado correctamente.")
    

