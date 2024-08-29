import pytest
from unittest.mock import patch, MagicMock
from app import login_funcionario
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase


@pytest.mark.parametrize("cpf, senha, mock_funcionarios, expected", [
    ("12345678909", "12345", [MagicMock(to_dict=lambda: {'cpf': '12345678909', 'senha': '12345', 'permissao': 'ATENDENTE'}, id='func_id')], {'message': 'Login realizado com sucesso!', 'funcionario_id': 'func_id', 'permissao': 'ATENDENTE'}),
    ("000000000000", "12345", None, {'error': 'CPF inválido!'}),
    ("12345678909", "senhaerrada", [MagicMock(to_dict=lambda: {'cpf': '12345678909', 'senha': '12345', 'permissao': 'ATENDENTE'}, id='func_id')], {'error': 'Senha incorreta!'}),
    ("12345678909", "", None, {'error': 'Senha em branco!'}),
    ("11111111111", "12345", [], {'error': 'Admin não encontrado!'}),
])
@patch('app.db.collection')
def test_login_funcionario(mock_db_collection, cpf, senha, mock_funcionarios, expected):
    
    if mock_funcionarios is not None:
        mock_collection = mock_db_collection.return_value
        mock_collection.where.return_value.stream.return_value = mock_funcionarios
    resultado = login_funcionario(cpf, senha)
    assert resultado == expected

    if len(cpf) == 11 and senha:
        mock_db_collection.assert_called_once_with('funcionario')
        mock_db_collection.return_value.where.assert_called_once_with('cpf', '==', cpf)

if __name__ == "__main__":
    pytest.main()
