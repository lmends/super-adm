import json, os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash

usuarios_bp = Blueprint('usuarios', __name__)
USUARIOS_PATH = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(USUARIOS_PATH):
        with open(USUARIOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(USUARIOS_PATH, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

@usuarios_bp.route("/usuarios")
def listar_usuarios():
    usuarios = carregar_usuarios()
    return render_template("usuarios.html", usuarios=usuarios)

@usuarios_bp.route("/usuarios/novo", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]
        usuarios = carregar_usuarios()

        if any(u["username"] == username for u in usuarios):
            flash("Usuário já existe!", "erro")
            return redirect(url_for("usuarios.novo_usuario"))

        usuarios.append({
            "username": username,
            "senha_hash": generate_password_hash(senha)
        })
        salvar_usuarios(usuarios)
        flash("Usuário criado com sucesso!", "sucesso")
        return redirect(url_for("usuarios.listar_usuarios"))

    return render_template("usuario_novo.html")

@usuarios_bp.route("/usuarios/editar/<username>", methods=["GET", "POST"])
def editar_usuario(username):
    usuarios = carregar_usuarios()
    usuario = next((u for u in usuarios if u["username"] == username), None)

    if not usuario:
        flash("Usuário não encontrado!", "erro")
        return redirect(url_for("usuarios.listar_usuarios"))

    if request.method == "POST":
        nova_senha = request.form["senha"]
        usuario["senha_hash"] = generate_password_hash(nova_senha)
        salvar_usuarios(usuarios)
        flash("Senha atualizada!", "sucesso")
        return redirect(url_for("usuarios.listar_usuarios"))

    return render_template("usuario_editar.html", usuario=usuario)

@usuarios_bp.route("/usuarios/excluir/<username>", methods=["POST"])
def excluir_usuario(username):
    usuarios = carregar_usuarios()
    usuarios = [u for u in usuarios if u["username"] != username]
    salvar_usuarios(usuarios)
    flash("Usuário removido.", "sucesso")
    return redirect(url_for("usuarios.listar_usuarios"))
