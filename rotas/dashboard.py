# dashboard.py (CORRIGIDO)

from flask import Blueprint, render_template, redirect, url_for, session
from utils.planilha import carregar_dados
# A linha 'from datetime import datetime' não é mais necessária aqui

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login.login'))

    # Simplesmente carregue os dados. Eles já vêm prontos!
    clinicas = carregar_dados()

    # O loop que estava aqui foi REMOVIDO.

    total = len(clinicas)
    ativos = len([c for c in clinicas if c["status"] == "ativo"])
    
    return render_template('index.html', clinicas=clinicas, total=total, ativos=ativos)


@dashboard_bp.route('/historico')
def historico():
    import os
    import json

    historico = []
    if os.path.exists("historico.json"):
        with open("historico.json", "r", encoding="utf-8") as f:
            historico = json.load(f)

    return render_template("historico.html", historico=historico)