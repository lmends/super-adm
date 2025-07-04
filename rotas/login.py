from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json

login_bp = Blueprint('login', __name__)

USUARIO_PADRAO = 'admin'
SENHA_HASH = generate_password_hash('superadmin123')


USUARIOS_PATH = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(USUARIOS_PATH):
        with open(USUARIOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuarios = carregar_usuarios()
        usuario = next((u for u in usuarios if u['username'] == username), None)

        
        if usuario and check_password_hash(usuario['senha_hash'], password):
            session['usuario'] = username
            return redirect(url_for('dashboard.index'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
    
    # para GET
    return render_template('login.html', error=None)

@login_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login.login'))
