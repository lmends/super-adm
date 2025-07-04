import json
import os
from flask import Blueprint, jsonify, request
from utils.planilha import carregar_dados
from datetime import datetime, timezone, timedelta

api_bp = Blueprint('api', __name__)
HISTORICO_PATH = "historico.json"

def registrar_historico(registro):
    """
    Registra um evento no arquivo de histórico JSON.
    """
    historico = []
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
            historico = json.load(f)

    historico.insert(0, registro)  # Adiciona o registro mais recente no início
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        # Salva os últimos 100 registros para não deixar o arquivo gigante
        json.dump(historico[:100], f, indent=2, ensure_ascii=False)

@api_bp.route('/api/check')
def check():
    clinic_id = request.args.get('id')
    
    if not clinic_id:
        return jsonify({"status": "erro", "mensagem": "ID da clínica não fornecido"}), 400

    
    clinicas = carregar_dados()

    # Define o fuso horário do Brasil (UTC-3)
    fuso_horario_brasil = timezone(timedelta(hours=-3))
    
    # Procura a clínica na lista de dados já processados
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

            registro = {
                "data_hora": datetime.now(fuso_horario_brasil).strftime('%d/%m/%Y %H:%M:%S'),
                "id_clinica": c['id'],
                "nome_clinica": c.get('nome', 'Nome não encontrado'),
                "resultado": "Permitido" if pode_executar else "Bloqueado",
                "motivo": f"Status: {c['status']}"
            }
            registrar_historico(registro)


            return jsonify({
                "status": "ativo" if pode_executar else "vencido",
                "vencimento": c["vencimento"],
                "pode_executar": pode_executar
            })

    return jsonify({"status": "invalido", "pode_executar": False})
