import re
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase

cred = credentials.Certificate('key.json') # Necessário gerar nova devido a restrições do Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

# Funcionalidades
def validar_cpf(cpf):
    if not re.match(r'^\d{11}$', cpf):
        return False
    else:
        return True

def notificar_confirmacao(email_cliente, pedido_id, permissao):
    try:
        if permissao.upper().strip() not in ['ATENDENTE', 'GERENTE']:
            return {'error': 'Nível de permissão inválido!'}
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email_cliente):
            return {'error': 'E-mail inválido!'}

        pedido_data = db.collection('pedido').document(pedido_id).get()
        if not pedido_data.exists:
            return {'error': 'Pedido não encontrado!'}
        
        pedido_dict = pedido_data.to_dict()
        data_pedido = pedido_dict.get('data')
        forma_pgmto = pedido_dict.get('formadepgmto')
        pratos = str(pedido_dict.get('pratos'))
        total = str(pedido_dict.get('total'))

        conectar = smtplib.SMTP("smtp.office365.com", 587)
        conectar.starttls()
        conectar.login("enviarcompython@outlook.com", "Python@123456")
        mensagem = MIMEMultipart()
        mensagem['From'] = "enviarcompython@outlook.com"
        mensagem['To'] = email_cliente
        mensagem['Subject'] = "Confirmação de Pedido"
        HTML = f"""
        <p>Prezado(a) cliente,</p>
        <p>Seu pedido foi <b>confirmado</b> com sucesso!</p>
        <p>Em caso de cancelamento por parte do restaurante, entraremos em contato com você pelo telefone.</p>
        <p>Se desejar desistir do pedido, ligue para nós até 10 minutos após a realização do pedido.</p>
        <ul>
        <li>Data: {data_pedido}</li>
        <li>Forma de pagamento: {forma_pgmto}</li>
        <li>Pratos: {pratos}</li>
        <li>Total: {total}</li>
        </ul>
        <p>Atenciosamente,</p>
        <p>Equipe do Restaurante</p>
        """
        mensagem.attach(MIMEText(HTML, 'html'))
        texto = mensagem.as_string()

        conectar.sendmail("enviarcompython@outlook.com", email_cliente, texto)
        conectar.close()

        return {'message': 'Notificação de pedido confirmado enviada via e-mail!'}
    except Exception as e:
        return {'error':  'Erro Inesperado'}

# Usuário
def create_usuario(cpf, nome, email, endereco, telefone, senha):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
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
    except Exception as e:
        return {'error':  'Erro Inesperado'}

def update_usuario(cpf, update_data):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
            return {'error': 'CPF inválido!'}
        if 'email' in update_data.keys() and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', update_data['email']):
            return {'error': 'E-mail inválido!'}
        if 'telefone' in update_data.keys() and not re.match(r'^\d{10,11}$', update_data['telefone']):
            return {'error': 'Telefone inválido!'}
        
        usuario_docs = list(db.collection('usuario').where('cpf', '==', cpf).stream())
        if not usuario_docs:
            return {'error': 'Usuário não encontrado!'}

        usuario_ref = db.collection('usuario').document(usuario_docs[0].id)
        usuario_ref.update(update_data)
        return {'message': 'Usuário atualizado com sucesso!'}
    except Exception as e:
        return {'error':  'Erro Inesperado'}

def get_usuario(cpf):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
            return {'error': 'CPF inválido!'}

        usuario_docs = list(db.collection('usuario').where('cpf', '==', cpf).stream())
        if not usuario_docs:
            return {'error': 'Usuário não encontrado!'}
        return usuario_docs[0].to_dict()
    except Exception as e:
        return {'error':  'Erro Inesperado'}

def login_usuario(cpf, senha):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
            return {'error': 'CPF inválido!'} 

        if senha is None or senha == '':
            return {'error': 'Senha em branco!'} 
        
        usuario_docs = list(db.collection('usuario').where('cpf', '==', cpf).stream())
        if not usuario_docs:
            return {'error': 'Usuário não encontrado!'}

        usuario_data = usuario_docs[0].to_dict()
        if usuario_data['senha'] != senha:
            return {'error': 'Senha incorreta!'}
        else:
            return {'message': 'Login realizado com sucesso!', 'usuario_id': usuario_docs[0].id, 'usuario_cpf': usuario_data['cpf']}
    except Exception as e:
        return {'error':  'Erro Inesperado'}

# Pedido
def create_pedido(cpf, endereco, formadepgmto, pratos, telefone_cliente, total, now):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
            return {'error': 'CPF inválido!'}
        
        cpf_docs = list(db.collection('usuario').where('cpf', '==', cpf).stream())
        if not cpf_docs:
            return {'error': 'Nenhum usuário encontrado com este CPF!'}
        
        if not endereco or not formadepgmto or not pratos or not telefone_cliente or not total:
            return {'error': 'Todos os campos devem ser preenchidos!'}
        if not re.match(r'^\d{10,11}$', telefone_cliente):
            return {'error': 'Telefone do cliente inválido!'}

        offset = timedelta(hours=-3)
        current_time = now + offset
        formatted_date = (current_time).strftime("%d de %B de %Y às %H:%M:%S")

        if current_time.hour < 8 or current_time.hour >= 22:
            return {'error': 'Fora do horário de funcionamento (Todos os dias das 8h às 22h)!'}
        
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
    except Exception as e:
        return {'error':  'Erro Inesperado'}

def get_pedido(cpf):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
            return {'error': 'CPF inválido!'}
        
        pedido_docs = list(db.collection('pedido').where('cpf', '==', cpf).stream())
        if not pedido_docs:
            return {'error': 'Nenhum pedido encontrado para este CPF!'}
        
        pedidos = [doc.to_dict() for doc in pedido_docs]
        return pedidos
    except Exception as e:
        return {'error':  'Erro Inesperado'}

def list_pedidos(permissao):
    try:
        if permissao.upper().strip() not in ['ATENDENTE', 'GERENTE']:
            return {'error': 'Nível de permissão inválido!'}
        
        pedidos = db.collection('pedido').stream()
        pedido_list = []
        for pedido in pedidos:
            pedido_list.append({'id': pedido.id, **pedido.to_dict()})
        if not pedido_list:
            return {'error': 'Nenhum pedido encontrado!'}
        return pedido_list
    except Exception as e:
        return {'error':  'Erro Inesperado'}

# Avaliação
def avaliar_pedido(cpf, pedido_id, nota):
    cpf_valido = validar_cpf(cpf)
    if cpf_valido == False:
            return {'error': 'CPF inválido!'}
    
    if not pedido_id:
        return {'error': 'ID do pedido deve ser informado!'}
    
    try:
        pedido_data = db.collection('pedido').document(pedido_id).get()
        if not pedido_data.exists:
            return {'error': 'Pedido não encontrado!'}
        
        pedido = pedido_data.to_dict()
        if pedido.get('cpf') != cpf:
            return {'error': 'CPF não corresponde ao CPF do pedido!'}
    
        try:
            nota = float(nota)
            if nota < 0 or nota > 10:
                raise ValueError('A nota deve ser um valor entre 0 e 10!')
        except ValueError:
            return {'error': 'Nota inválida! Deve ser um número entre 0 e 10.'}

        doc_ref = db.collection('avaliacao').add({
            'pedido_id': pedido_id,
            'nota': nota
        })
        return {'message': 'Avaliação registrada com sucesso!', 'id': doc_ref[1].id}
    except Exception as e:
        return {'error': 'Erro Inesperado'}

def calcular_media_avaliacoes(permissao):
    try:
        if permissao.upper().strip() not in ['ATENDENTE', 'GERENTE']:
            return {'error': 'Nível de permissão inválido!'}
        
        avaliacoes = list(db.collection('avaliacao').stream())

        total_avaliacoes = 0
        num_avaliacoes = 0
        for avaliacao in avaliacoes:
            avaliacao_data = avaliacao.to_dict()
            total_avaliacoes += avaliacao_data.get('nota', 0)
            num_avaliacoes += 1

        if num_avaliacoes > 0:
            media_avaliacoes = total_avaliacoes / num_avaliacoes
        else:
            return {'error': 'Nenhuma avaliação encontrada!'}

        return {'message': media_avaliacoes}
    except Exception as e:
        return {'error':  'Erro Inesperado'}

# Admin
def cadastrar_funcionario(cpf, senha, permissao, permissao_registrador):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
            return {'error': 'CPF inválido!'}
        
        if permissao.upper().strip() not in ['ATENDENTE', 'GERENTE']:
            return {'error': 'Novo nível de permissão é inválido!'}
        
        if senha is None or senha == '':
            return {'error': 'Senha inválida!'}
        
        if permissao_registrador.upper().strip() not in ['GERENTE']:
            return {'error': 'Nível de permissão inválido!'}
        
        funcionario_query = db.collection('funcionario').where('cpf', '==', cpf).stream()
        if list(funcionario_query):
            return {'error': 'CPF já cadastrado como funcionário!'}

        doc_ref = db.collection('funcionario').add({
            'cpf': cpf,
            'senha': senha,
            'permissao': permissao
        })
        return {'message': 'Cadastro realizado com sucesso!', 'id': doc_ref[1].id, 'permissao': permissao}
    except Exception as e:
        return {'error':  'Erro Inesperado'}

def get_funcionario(cpf, permissao):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
            return {'error': 'CPF inválido!'}

        if permissao.upper().strip() not in ['GERENTE']:
            return {'error': 'Nível de permissão inválido!'}
        
        funcionario_docs = list(db.collection('funcionario').where('cpf', '==', cpf).stream())
        if not funcionario_docs:
            return {'error': 'funcionário não encontrado!'}
        return funcionario_docs[0].to_dict()
    except Exception as e:
        return {'error':  'Erro Inesperado'}

def login_funcionario(cpf, senha):
    try:
        cpf_valido = validar_cpf(cpf)
        if cpf_valido == False:
            return {'error': 'CPF inválido!'} 

        if senha is None or senha == '':
            return {'error': 'Senha em branco!'} 
        
        funcionario_docs = list(db.collection('funcionario').where('cpf', '==', cpf).stream())
        if not funcionario_docs:
            return {'error': 'Admin não encontrado!'}

        funcionario_data = funcionario_docs[0].to_dict()
        if funcionario_data['senha'] != senha:
            return {'error': 'Senha incorreta!'}
        else:
            return {'message': 'Login realizado com sucesso!', 'funcionario_id': funcionario_docs[0].id, 'permissao': funcionario_data['permissao']}
    except Exception as e:
        return {'error':  'Erro Inesperado'}

# Prato
def create_prato(nome, url_img, valor, permissao):
    try:
        if permissao.upper().strip() not in ['GERENTE']:
            return {'error': 'Nível de permissão inválido!'}
        
        if not nome or not valor or not url_img:
            return {'error': 'Todos os campos devem ser preenchidos!'}
        if float(valor) < 0:
            return {'error': 'Valor deve ser maior que zero!'}
        
        doc_ref = db.collection('prato').add({
            'nome': nome,
            'url_img': url_img,
            'valor': valor,
            'promocao': False
        })
        return {'message': 'Cadastro realizado com sucesso!', 'id': doc_ref[1].id}
    except Exception as e:
        return {'error':  'Erro Inesperado'}

def delete_prato(prato_id, permissao):
    try:
        if permissao.upper().strip() not in ['GERENTE']:
            return {'error': 'Nível de permissão inválido!'}
         
        if not prato_id:
            return {'error': 'ID do prato deve ser informado!'}
        
        prato_data = db.collection('prato').document(prato_id).get()
        if not prato_data.exists:
            return {'error': 'Prato não encontrado!'}
        else:
            db.collection('prato').document(prato_id).delete()
            return {'message': 'Prato excluído com sucesso!'}
    except Exception as e:
        return {'error': 'Erro Inesperado'}

def get_prato(prato_id):
    try:
        if not prato_id:
            return {'error': 'ID do prato deve ser informado!'}

        prato_data = db.collection('prato').document(prato_id).get()
        if not prato_data.exists:
            return {'error': 'Prato não encontrado!'}
        return prato_data.to_dict()
    except Exception as e:
        return {'error': 'Erro Inesperado'}

def list_pratos():
    try:
        pratos = db.collection('prato').stream()
        prato_list = []
        for prato in pratos:
            prato_list.append({'id': prato.id, **prato.to_dict()})
        if not prato_list:
            return {'error': 'Nenhum prato encontrado!'}
        return prato_list
    except Exception as e:
        return {'error':  'Erro Inesperado'}

# Promoção
def create_promocao(prato_id, promocao, permissao):
    if permissao.upper().strip() not in ['GERENTE']:
        return {'error': 'Nível de permissão inválido!'}
     
    if not prato_id:
        return {'error': 'ID do prato deve ser informado!'}

    if not isinstance(promocao, bool):
        return {'error': 'O valor de promoção deve ser True ou False!'}

    try:
        prato_data = db.collection('prato').document(prato_id).get()
        if not prato_data.exists:
            return {'error': 'Prato não encontrado!'}

        db.collection('prato').document(prato_id).update({'promocao': promocao})
        return {'message': 'Promoção do prato atualizada com sucesso!'}
    except Exception as e:
        return {'error': 'Erro Inesperado'}

def get_promocao(prato_id):
    try:
        if not prato_id:
            return {'error': 'ID da promoção deve ser informado!'}

        prato_data = db.collection('prato').document(prato_id).where('promocao == True').get()
        if not prato_data.exists:
            return {'error': 'Promoção não encontrada!'}
        return prato_data.to_dict()
    except Exception as e:
        return {'error': 'Erro Inesperado'}

def list_promocoes():
    try:
        pratos = db.collection('prato').where('promocao', '==', True).stream()
        prato_list = [{'id': prato.id, **prato.to_dict()} for prato in pratos]

        if not prato_list:
            return {'error': 'Nenhum prato em promoção encontrado!'}
        return prato_list
    except Exception as e:
        return {'error': 'Erro Inesperado'}