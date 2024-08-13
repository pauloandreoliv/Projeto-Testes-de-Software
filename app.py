import re
from datetime import datetime, timedelta, timezone
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('key.json') # Necessário gerar nova devido a restrições do Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

# Usuário
def create_usuario(cpf, nome, email, endereco, telefone, senha):
    if not re.match(r'^\d{11}$', cpf):
        return {'error': 'CPF inválido!'}
    
    usuario_query = db.collection('usuario').where('cpf', '==', cpf).stream()
    if list(usuario_query):
        return {'error': 'CPF já cadastrado!'}
    
    if not nome or not email or not endereco or not telefone or not senha:
        return {'error': 'Todos os campos devem ser preenchidos!'}
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email):
        return {'error': 'E-mail inválido!'}
    if not re.match(r'^\d{10,11}$', telefone):
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
        return {'error': 'CPF inválido!'} # CPF deve conter 11 dígitos numéricos

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
        return {'error': 'CPF inválido!'} # CPF deve conter 11 dígitos numéricos

    admin_docs = list(db.collection('admin').where('cpf', '==', cpf).stream())
    if not admin_docs:
        return {'error': 'Admin não encontrado!'}

    admin_data = admin_docs[0].to_dict()
    if admin_data['senha'] != senha:
        return {'error': 'Senha incorreta!'}
    else:
        return {'message': 'Login realizado com sucesso!', 'admin_id': admin_docs[0].id}

# Produto
def create_prato(nome, url_img, valor):
    if not nome or not valor or not url_img:
        return {'error': 'Todos os campos devem ser preenchidos!'}
    if float(valor) < 0:
        return {'error': 'Valor deve ser maior que zero!'}
    
    doc_ref = db.collection('prato').add({
        'nome': nome,
        'url_img': url_img,
        'valor': valor
    })
    return {'message': 'Cadastro realizado com sucesso!', 'id': doc_ref[1].id}

def delete_prato(prato_id):
    try:
        if not prato_id:
            return {'error': 'ID do prato deve ser informado!'}
        
        prato_data = db.collection('prato').document(prato_id).get()
        if not prato_data.exists:
            return {'error': 'Prato não encontrado!'}
        else:
            db.collection('prato').document(prato_id).delete()
            return {'message': 'Prato excluído com sucesso!'}
    except Exception as e:
        return {'message': str(e)}

def get_prato(prato_id):
    try:
        if not prato_id:
            return {'error': 'ID do prato deve ser informado!'}

        prato_data = db.collection('prato').document(prato_id).get()
        if not prato_data.exists:
            return {'error': 'Prato não encontrado!'}
        return prato_data.to_dict()
    except Exception as e:
        return {'message': str(e)}

def list_pratos():
    pratos = db.collection('prato').stream()
    prato_list = []
    for prato in pratos:
        prato_list.append({'id': prato.id, **prato.to_dict()})
    if not prato_list:
        return {'error': 'Nenhum prato encontrado!'}
    return prato_list

# Promoção
def create_promocao(nome, url_img, valor):
    if not nome or not url_img or not valor:
        return {'error': 'Todos os campos devem ser preenchidos!'}
    if float(valor) < 0:
        return {'error': 'Valor deve ser maior que zero!'}
    try:
        doc_ref = db.collection('promocao').add({
            'nome': nome,
            'url_img': url_img,
            'valor': valor
        })
        return {'message': 'Promoção cadastrada com sucesso!', 'id': doc_ref[1].id}
    except Exception as e:
        return {'message': str(e)}

def delete_promocao(id):
    try:
        if not id:
            return {'error': 'ID da promoção deve ser informado!'}
        
        promocao_data = db.collection('promocao').document(id).get()
        if not promocao_data.exists:
            return {'error': 'Promoção não encontrada!'}
        else:
            db.collection('promocao').document(id).delete()
            return {'message': 'Promoção excluída com sucesso!'}
    except Exception as e:
        return {'message': str(e)}

def get_promocao(id):
    try:
        if not id:
            return {'error': 'ID da promoção deve ser informado!'}
        
        promocao_data = db.collection('promocao').document(id).get()
        if not promocao_data.exists:
            return {'error': 'Promoção não encontrada!'}
        return promocao_data.to_dict()
    except Exception as e:
        return {'message': str(e)}

def list_promocoes():
    promocoes = db.collection('promocao').stream()
    promocao_list = []
    for promocao in promocoes:
        promocao_list.append({'id': promocao.id, **promocao.to_dict()})
    if not promocao_list:
        return {'error': 'Nenhuma promoção encontrada!'}
    return promocao_list

# Unidade
def create_unidade(nome, url_img, endereco):
    if not nome or not endereco or not url_img:
        return {'error': 'Todos os campos devem ser preenchidos!'}

    try:
        doc_ref = db.collection('unidade').add({
            'nome': nome,
            'url_img': url_img,
            'endereco': endereco
        })
        return {'message': 'Unidade de unidadee cadastrada com sucesso!', 'id': doc_ref[1].id}
    except Exception as e:
        return {'message': str(e)}

def delete_unidade(nome):
    try:
        if not nome:
            return {'error': 'Nome da unidade deve ser informado!'}
    
        unidade_data = db.collection('unidade').document(nome).get()
        if not unidade_data.exists:
            return {'error': 'Unidade não encontrada!'}
        else:
            db.collection('unidade').document(nome).delete()
            return {'message': 'Unidade excluída com sucesso!'}
    except Exception as e:
        return {'message': str(e)}

def get_unidade(nome):
    if not nome:
        return {'error': 'Nome da unidade deve ser informado!'}

    try:
        unidade_data = db.collection('unidade').document(nome).get()
        if not unidade_data.exists:
            return {'error': 'Unidade não encontrada!'}
        return unidade_data.to_dict()
    except Exception as e:
        return {'message': str(e)}

def list_unidades():
    unidades = db.collection('unidade').stream()
    unidade_list = []
    for unidade in unidades:
        unidade_list.append({'id': unidade.id, **unidade.to_dict()})
    if not unidade_list:
        return {'error': 'Nenhuma unidade encontrada!'}
    return unidade_list
