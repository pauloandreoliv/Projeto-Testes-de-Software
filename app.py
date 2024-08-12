import re
from datetime import datetime, timedelta, timezone
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Usuário
def create_usuario(cpf, nome, email, endereco, telefone, senha):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'} # 99999999999
    
    usuario_query = db.collection('usuario').where('cpf', '==', cpf).stream()
    if list(usuario_query):
        return {'error': 'CPF já cadastrado!'}
    
    if not nome or not email or not endereco or not telefone or not senha:
        return {'error': 'Todos os campos devem ser preenchidos!'}
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email):
        return {'error': 'E-mail inválido!'}
    if not re.match(r'^\d{10,11}$', telefone):  # 81999999999
        return {'error': 'Telefone inválido!'}

    doc_ref = db.collection('usuario').add({
        'cpf': cpf,
        'nome': nome,
        'email': email,
        'endereco': endereco,
        'telefone': telefone,
        'senha': senha
    })
    return {'message': 'Cadastro realizado com sucesso!', 'id': doc_ref[1].id}

def update_usuario(cpf, update_data):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'}
    
    usuario_docs = list(db.collection('usuario').where('cpf', '==', cpf).stream())
    if not usuario_docs:
        return {'error': 'Usuário não encontrado!'}

    usuario_ref = db.collection('usuario').document(usuario_docs[0].id)
    usuario_ref.update(update_data)
    return {'message': 'Usuário atualizado com sucesso!'}

def get_usuario(cpf):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'}

    usuario_docs = list(db.collection('usuario').where('cpf', '==', cpf).stream())
    if not usuario_docs:
        return {'error': 'Usuário não encontrado!'}
    return usuario_docs[0].to_dict()

def login_usuario(cpf, senha):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'} # 99999999999

    usuario_docs = list(db.collection('usuario').where('cpf', '==', cpf).stream())
    if not usuario_docs:
        return {'error': 'Usuário não encontrado!'}

    usuario_data = usuario_docs[0].to_dict()
    if usuario_data['senha'] != senha:
        return {'error': 'Senha incorreta!'}
    else:
        return {'message': 'Login realizado com sucesso!', 'usuario_id': usuario_docs[0].id}

#Pedido
def create_pedido(cpf, endereco, formadepgmto, pratos, telefone_cliente, total):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'}
    if not endereco or not formadepgmto or not pratos or not telefone_cliente or not total:
        return {'error': 'Todos os campos devem ser preenchidos!'}
    if not re.match(r'^\d{10,11}$', telefone_cliente):
        return {'error': 'Telefone do cliente inválido!'}

    now = datetime.now(timezone.utc)
    offset = timedelta(hours=-3)
    formatted_date = (now + offset).strftime("%d de %B de %Y às %H:%M:%S") + " UTC-3"

    doc_ref = db.collection('pedido').add({
        'cpf': cpf,
        'data': formatted_date,
        'endereco': endereco,
        'formadepgmto': formadepgmto,
        'pratos': pratos,
        'telefone_cliente': telefone_cliente,
        'total': total
    })
    return {'message': 'Pedido criado com sucesso!', 'id': doc_ref[1].id}

def get_pedido(cpf):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'}

    pedido_docs = list(db.collection('pedido').where('cpf', '==', cpf).stream())
    if not pedido_docs:
        return {'error': 'Pedido não encontrado!'}
    return pedido_docs[0].to_dict()

# Admin
def cadastrar_admin(cpf, senha):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'}
    
    admin_query = db.collection('admin').where('cpf', '==', cpf).stream()
    if list(admin_query):
        return {'error': 'CPF já cadastrado como administrador!'}

    doc_ref = db.collection('admin').add({
        'cpf': cpf,
        'senha': senha
    })
    return {'message': 'Cadastro realizado com sucesso!', 'id': doc_ref[1].id}

def get_admin(cpf):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'}

    admin_docs = list(db.collection('admin').where('cpf', '==', cpf).stream())
    if not admin_docs:
        return {'error': 'Administrador não encontrado!'}
    return admin_docs[0].to_dict()


def login_admin(cpf, senha):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'} # 99999999999

    admin_docs = list(db.collection('admin').where('cpf', '==', cpf).stream())
    if not admin_docs:
        return {'error': 'Usuário não encontrado!'}

    admin_data = admin_docs[0].to_dict()
    if admin_data['senha'] != senha:
        return {'error': 'Senha incorreta!'}
    else:
        return {'message': 'Login realizado com sucesso!', 'admin_id': admin_docs[0].id}
