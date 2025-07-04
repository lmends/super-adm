from datetime import datetime, timezone
import requests

PLANILHA_URL = "https://script.google.com/macros/s/AKfycbxipN263e3-o9PT5QZZNUzts5rRV66pSYQpfdlGD1h2VXjlVtxErlZbkkcFTXdVHPsT6Q/exec"

def carregar_dados():
    try:
        response = requests.get(PLANILHA_URL)
        if response.status_code == 200:
            dados = response.json()
            # Pega a data e hora atuais em UTC para uma comparação precisa
            hoje_utc = datetime.now(timezone.utc)

            for c in dados:
                vencimento_str = c.get("vencimento")

                if vencimento_str:
                    try:
                        # 1. Converte a string para um objeto datetime ciente do fuso horário (UTC)
                        vencimento_dt = datetime.fromisoformat(vencimento_str.replace('Z', '+00:00'))
                        
                        # 2. Lógica de status correta e simplificada
                        if vencimento_dt < hoje_utc:
                            c["status"] = "vencido"
                        else:
                            c["status"] = "ativo"

                        # 3. Formata a data para dd/mm/aaaa (no lugar certo)
                        c["vencimento"] = vencimento_dt.strftime('%d/%m/%Y')
                            
                    except Exception as e:
                        print(f"Erro ao converter data: {vencimento_str} -> {e}")
                        c["status"] = "indefinido"
                        c["vencimento"] = "Data inválida"
                else:
                    c["status"] = "indefinido"
                    c["vencimento"] = "--"

            return dados
        else:
            # Retorna a lista vazia em caso de erro HTTP
            return []
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return []