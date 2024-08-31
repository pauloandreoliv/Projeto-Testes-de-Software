import pytest
from unittest.mock import patch, MagicMock
from app import cadastrar_funcionario
import warnings 
warnings.filterwarnings('ignore')  # Ignorar warning do firebase


@pytest.mark.parametrize("cpf, senha, permissao, permissao_registrador, mock_funcionario_query, side_effect, expected", [
    ("12345678909", "12345", "ATENDENTE", "GERENTE", 
     [], 
     None,
     {'message': 'Cadastro realizado com sucesso!', 'permissao': 'ATENDENTE'}),

    ("00000000000", "12345", "ATENDENTE", "GERENTE", 
     [], 
     None,
     {'error': 'CPF inválido!'}),

    ("12345678909", "12345", "COZINHEIRO", "GERENTE", 
     [], 
     None,
     {'error': 'Novo nível de permissão é inválido!'}),

    ("12345678909", "12345", "ATENDENTE", "ATENDENTE", 
     [], 
     None,
     {'error': 'Nível de permissão inválido!'}),

    ("12345678909", "12345", "ATENDENTE", "GERENTE", 
     [MagicMock()], 
     None,
     {'error': 'CPF já cadastrado como funcionário!'}),

    ("12345678909", "12345", "ATENDENTE", "GERENTE", 
     [], 
     Exception("Erro Inesperado"), 
     {'error': 'Erro Inesperado'}),
])
@patch("app.db.collection")
@patch("app.validar_cpf")
def test_cadastrar_funcionario(mock_validar_cpf, mock_db_collection, cpf, senha, permissao, permissao_registrador, mock_funcionario_query, side_effect, expected):
    if cpf == "00000000000":
        mock_validar_cpf.return_value = False
    else:
        mock_validar_cpf.return_value = True

    mock_db_collection.return_value.where.return_value.stream.return_value = mock_funcionario_query
    
    if side_effect:
        mock_db_collection.return_value.where.side_effect = side_effect

    mock_add = MagicMock()
    mock_db_collection.return_value.add.return_value = (None, mock_add)
    mock_add.id = "doc_id"

    result = cadastrar_funcionario(cpf, senha, permissao, permissao_registrador)

    if 'id' in result:
        expected['id'] = "doc_id"

    assert result == expected

if __name__ == "__main__":
    pytest.main()
