from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import Contato, Produto, Usuario
from werkzeug.security import generate_password_hash


@app.route('/')
def home():
  return render_template('home.html')

@app.route('/quem_somos')
def quem_somos():
  return render_template('quem_somos.html')

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
  produtos = Produto.query.all()
  return render_template('produtos.html', produtos=produtos)


@app.route('/produtos_lista', methods=['get', 'post'])
@login_required
def produtos_lista():
  produtos = Produto.query.all()
  return render_template('produtos_lista.html', produtos=produtos)


@app.route('/usuarios_lista', methods=['get', 'post'])
def usuarios_lista():
  usuarios = Usuario.query.all()
  return render_template('usuarios_lista.html', usuarios=usuarios)


@app.route('/add_usuario', methods=['GET', 'POST'])
@login_required
def add_usuario():
  if not current_user.is_authenticated:
    return current_app.login_manager.unauthorized()

  if request.method == 'POST':
    usuario = request.form['usuario']
    senha = request.form['senha']
    user = Usuario(usuario=usuario, senha=senha)
    db.session.add(user)
    db.session.commit()
    flash("Usuário cadastrado com sucesso!")
    return redirect(url_for('add_usuario'))

  return render_template('add_usuario.html')


@app.route('/edit_usuario<usuario_id>', methods=['GET', 'POST'])
def edit_usuario(usuario_id):
    if current_user.is_authenticated:
        usuario = Usuario.query.get_or_404(usuario_id)
        if request.method == 'POST':
            usuario.usuario = request.form['usuario']
            usuario.senha = generate_password_hash(request.form['senha'])
            try:
                db.session.commit()
                flash('Usuário alterado com sucesso!')
                return render_template('edit_usuario.html', usuario=usuario)
            except:
                db.sessionl.rollback()
                flash('Erro ao alterar usuário')
                return render_template('edit_usuario.html', usuario=usuario)
            
        return render_template('edit_usuario.html', usuario=usuario)
    else:
        return redirect(url_for('login'))



@app.route('/delete_usuario/<usuario_id>', methods=['GET', 'POST'])
@login_required
def delete_usuario(usuario_id):
  if current_user.is_authenticated:
    usuario = Usuario.query.get_or_404(usuario_id)
    if request.method == 'GET':
      try: 
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído!')
        return redirect(url_for('usuarios_lista'))
      except:
        db.session.rollback()
        flash('Erro ao excluir usuário!')
        return redirect(url_for('usuario_lista'))


@app.route('/add_produto', methods=['GET', 'POST'])
@login_required
def add_produto():
  if not current_user.is_authenticated:
    return current_app.login_manager.unauthorized()

  if request.method == 'POST':
    codigo = request.form["codigo"]
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    preco = request.form["preco"]
    foto = request.form["foto"]
    produto = Produto(codigo=codigo, nome=nome, descricao=descricao, preco=preco, foto=foto)
    db.session.add(produto)
    db.session.commit()
    flash("Produto cadastrado com sucesso!")
    return redirect(url_for('add_produto'))
  return render_template('add_produto.html')


@app.route('/produto_detalhe/<produto_id>', methods=['GET', 'POST'])
def produto_detalhe(produto_id):
  produto = Produto.query.get_or_404(produto_id)
  if request.method == 'GET':
    return render_template('produto_detalhe.html', produto=produto)


@app.route('/edit_produto/<produto_id>', methods=['GET', 'POST'])
@login_required
def edit_produto(produto_id):
  if current_user.is_authenticated:
    produto = Produto.query.get_or_404(produto_id)
    if request.method == 'POST':
      produto.codigo = request.form['codigo']
      produto.nome = request.form['nome']
      produto.descricao = request.form['descricao']
      produto.preco = request.form['preco']
      produto.foto = request.form['foto']
      try:
        db.session.commit()
        flash('Produto alterado com sucesso!')
        return render_template('edit_produto.html', produto=produto)
      except:
        db.session.rollback()
        flash('Erro ao alterar produto')
        return render_template('edit_produto.html', produto=produto)
  else:
    return redirect(url_for('login'))

  return render_template('edit_produto.html', produto=produto)


@app.route('/delete_produto/<produto_id>', methods=['GET', 'POST'])
@login_required
def delete_produto(produto_id):
  if current_user.is_authenticated:
    produto = Produto.query.get_or_404(produto_id)
    if request.method == 'GET':
      try: 
        db.session.delete(produto)
        db.session.commit()
        flash('Produto excluído!')
        return redirect(url_for('produtos_lista'))
      except:
        db.session.rollback()
        flash('Erro ao excluir produto!')
        return redirect(url_for('produtos_lista'))


@app.route('/contatos_lista', methods=['get', 'post'])
@login_required
def contatos_lista():
  if current_user.is_authenticated:
    contatos = Contato.query.all()
    return render_template('contatos_lista.html', contatos=contatos)
  else:
    return redirect(url_for('login'))


@app.route('/contato_detalhe/<contato_id>', methods=['GET', 'POST'])
@login_required
def contato_detalhe(contato_id):
  if current_user.is_authenticated:
    contato = Contato.query.get_or_404(contato_id)
    if request.method == 'GET':
      return render_template('contato_detalhe.html', contato=contato)
  else:
    return redirect(url_for('login'))


@app.route('/edit_contato/<contato_id>', methods=['GET', 'POST'])
@login_required
def edit_contato(contato_id):
  if current_user.is_authenticated:
    contatos = Contato.query.all()
    contato = Contato.query.get_or_404(contato_id)
            
    if request.method == 'GET':
      if(contato.status == 0):
        contato.status = 1
      else:
        contato.status = 0
      
    contato.status = contato.status
    try:
        flash('Contato alterado com sucesso!')
        db.session.commit()
        return redirect(url_for('contatos_lista'))
    except:
        db.session.rollback()
        flash('Erro ao alterar contato!')
        return redirect(url_for('contatos_lista'))

    return redirect(url_for('contatos_lista'))
  else:
    return redirect(url_for('login'))


@app.route('/add_contato', methods=['GET', 'POST'])
def add_contato():
  if request.method == 'POST':
    nome = request.form["nome"]
    cidade = request.form["cidade"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    mensagem = request.form["mensagem"]
    contato = Contato(nome=nome, cidade=cidade, telefone=telefone, email=email, mensagem=mensagem)
    db.session.add(contato)
    db.session.commit()
    flash("Mensagem enviada com sucesso!")
    return redirect(url_for('add_contato'))
  return render_template('add_contato.html')


@app.route('/delete_contato/<contato_id>', methods=['GET', 'POST'])
@login_required
def delete_contato(contato_id):
  if current_user.is_authenticated:
    contato = Contato.query.get_or_404(contato_id)
    if request.method == 'GET':
      try: 
        db.session.delete(contato)
        db.session.commit()
        flash('Contato excluído!')
        return redirect(url_for('contatos_lista'))
      except:
        db.session.rollback()
        flash('Erro ao excluir contato!')
        return redirect(url_for('contatos_lista'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    usuario = request.form['usuario']
    pwd = request.form['senha']
    user = Usuario.query.filter_by(usuario=usuario).first()
    if not user or not user.verify_password(pwd):
      flash("Usuário ou senha inválidos!")
      return redirect(url_for('login'))
    login_user(user)
    flash("Bem-vindo! Voce está logado!")
    return redirect(url_for('home'))

  return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/info')
def info():
  return render_template('info.html')


#@app.route('/admin')
#@login_required
#def admin():
#  if current_user.is_authenticated:
#    return render_template('admin.html')
#  else:
#    return current_app.login_manager.unauthorized()

