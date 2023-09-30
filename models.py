from app import db, app, login_manager
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()


class Usuario(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  usuario = db.Column(db.String(50))
  senha = db.Column(db.String(200))

  def __init__(self, usuario, senha):
    self.usuario=usuario
    self.senha = generate_password_hash(senha)

  def verify_password(self, pwd):
    return check_password_hash(self.senha, pwd)

  def __repr__(self):
    return '{}'.format(self.usuario)


class Contato(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100))
  cidade = db.Column(db.String(100))
  telefone = db.Column(db.String(20))
  email = db.Column(db.String(150))
  mensagem = db.Column(db.Text)
  status = db.Column(db.Boolean, default=False, nullable=False)

  def __repr__(self):
    return '{}'.format(self.nome)


class Produto(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  codigo = db.Column(db.Integer)
  nome = db.Column(db.String(100))
  descricao = db.Column(db.String(200))
  preco = db.Column(db.String(50))
  foto = db.Column(db.String(255))

  def __repr__(self):
    return '{}'.format(self.nome)


# Descomente para gerar o banco
db.create_all()
