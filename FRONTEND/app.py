from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Datos de ejemplo: usuarios y contraseñas (en un escenario real, esto estaría en una base de datos)
users = {
    'user1': 'password1',
    'user2': 'password2',
}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            print(f'Inicio de sesión exitoso para {username}')  # Imprime para depurar
            
        return redirect(url_for('index'))
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
