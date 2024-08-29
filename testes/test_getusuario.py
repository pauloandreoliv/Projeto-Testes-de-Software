import pytest
from unittest.mock import patch, MagicMock
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase


from app import get_usuario, validar_cpf

def test_get_usuario_cpf_valido():
    cpf = "12345678909"
    usuario_dados = {
        "cpf": cpf,
        "nome": "João Silva",
        "email": "joao.silva@email.com",
        "endereco": "Rua Exemplo, 123",
        "telefone": "99999999999"
    }
    with patch('app.validar_cpf', return_value=True):
        with patch('app.db.collection') as mock_db:
            mock_doc = MagicMock()
            mock_doc.to_dict.return_value = usuario_dados
            mock_db.return_value.where.return_value.stream.return_value = [mock_doc]

            resultado = get_usuario(cpf)
            assert resultado == usuario_dados

def test_get_usuario_cpf_invalido():
    cpf = "000000000000"

    with patch('app.validar_cpf', return_value=False):
        resultado = get_usuario(cpf)
        assert resultado == {"error": "CPF inválido!"}

def test_get_usuario_cpf_inexistente():
    cpf = "98765432100"

    with patch('app.validar_cpf', return_value=True):
        with patch('app.db.collection') as mock_db:
            mock_db.return_value.where.return_value.stream.return_value = []
            
            resultado = get_usuario(cpf)
            assert resultado == {"error": "Usuário não encontrado!"}

def test_get_usuario_erro_inesperado():
    cpf = "12345678909"
    
    with patch('app.db.collection') as mock_db:
        mock_db.side_effect = Exception("Erro de conexão com o banco de dados")
        
        resultado = get_usuario(cpf)
        assert resultado == {"error": "Erro de conexão com o banco de dados"}

if __name__ == "__main__":
    pytest.main()