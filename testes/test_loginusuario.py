import pytest
from unittest.mock import patch, MagicMock
from app import login_usuario
import warnings 
warnings.filterwarnings('ignore')  # Ignorar warning do firebase

@pytest.mark.parametrize("cpf, senha, mock_usuarios, expected", [
    ("12345678909", "12345", [MagicMock(to_dict=lambda: {'cpf': '12345678909', 'senha': '12345'}, id='user_id')], {'message': 'Login realizado com sucesso!', 'usuario_id': 'user_id', 'usuario_cpf': '12345678909'}),
    ("000000000000", "12345", None, {'error': 'CPF inválido!'}),
    ("12345678909", "senhaerrada", [MagicMock(to_dict=lambda: {'cpf': '12345678909', 'senha': '12345'}, id='user_id')], {'error': 'Senha incorreta!'}),
    ("12345678909", "", None, {'error': 'Senha em branco!'}),
    ("11111111111", "12345", [], {'error': 'Usuário não encontrado!'}),
    ("abcdefghijk", "12345", None, {'error': 'CPF inválido!'}),
])
@patch('app.db.collection')
def test_login_usuario(mock_db_collection, cpf, senha, mock_usuarios, expected):
    
    if mock_usuarios is not None:
        mock_collection = mock_db_collection.return_value
        mock_collection.where.return_value.stream.return_value = mock_usuarios

    resultado = login_usuario(cpf, senha)
    assert resultado == expected

    if len(cpf) == 11 and cpf.isdigit() and senha:
        mock_db_collection.assert_called_once_with('usuario')
        mock_db_collection.return_value.where.assert_called_once_with('cpf', '==', cpf)

if __name__ == "__main__":
    pytest.main()