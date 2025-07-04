from flask import Flask
from rotas.login import login_bp
from rotas.dashboard import dashboard_bp
from rotas.api import api_bp
from rotas.usuarios import usuarios_bp


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Registrar Blueprints
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(api_bp)
app.register_blueprint(usuarios_bp)

if __name__ == '__main__':
    app.run(debug=True)

