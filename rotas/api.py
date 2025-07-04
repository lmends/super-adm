import json
import os
from flask import Blueprint, jsonify, request
from utils.planilha import carregar_dados
from datetime import datetime

api_bp = Blueprint('api', __name__)
HISTORICO_PATH = "historico.json"

def registrar_historico(registro):
    historico = []
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
            historico = json.load(f)

    historico.insert(0, registro)  # adiciona no topo
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico[:100], f, indent=2, ensure_ascii=False)  # salva últimos 100

@api_bp.route('/api/check')
def check():
    clinic_id = request.args.get('id')
    clinicas = carregar_dados()
    for c in clinicas:
        if c['id'] == clinic_id:
            # Verifica se está vencido
            try:
                try:
                    # tenta ISO
                    vencimento = datetime.fromisoformat(c["vencimento"])
                except ValueError:
                    # tenta BR
                    vencimento = datetime.strptime(c["vencimento"], "%d/%m/%Y")
                agora = datetime.now()
                esta_valida = vencimento >= agora
                
            except Exception as e:
                print(f"Erro ao analisar data: {e}")
                esta_valida = False

            pode_executar = c["status"] == "ativo" and esta_valida

            return jsonify({
                "status": "ativo" if pode_executar else "vencido",
                "vencimento": c["vencimento"],
                "pode_executar": pode_executar
            })

    return jsonify({"status": "invalido", "pode_executar": False})
