import pytest
from unittest.mock import patch, MagicMock

from app import get_funcionario

def mock_validar_cpf(cpf):
    return cpf != "00000000000"

@pytest.mark.parametrize("cpf, permissao, mock_return, expected", [
    ("12345678909", "GERENTE", [{'cpf': '12345678909', 'nome': 'João'}], {'cpf': '12345678909', 'nome': 'João'}),

    ("00000000000", "GERENTE", None, {'error': 'CPF inválido!'}),

    ("12345678909", "FUNCIONARIO", None, {'error': 'Nível de permissão inválido!'}),

    ("98765432100", "GERENTE", [], {'error': 'funcionário não encontrado!'}),

    ("12345678909", "GERENTE", Exception("Erro inesperado"), {'error': 'Erro inesperado'}),
])
@patch("app.validar_cpf", side_effect=mock_validar_cpf)
@patch("app.db.collection")
def test_get_funcionario(mock_db_collection, mock_validar_cpf, cpf, permissao, mock_return, expected):
    if isinstance(mock_return, list):
        mock_docs = [MagicMock(to_dict=MagicMock(return_value=doc)) for doc in mock_return]
        mock_db_collection.return_value.where.return_value.stream.return_value = mock_docs
    elif isinstance(mock_return, Exception):
        mock_db_collection.return_value.where.return_value.stream.side_effect = mock_return

    result = get_funcionario(cpf, permissao)
    assert result == expected

if __name__ == "__main__":
    pytest.main()