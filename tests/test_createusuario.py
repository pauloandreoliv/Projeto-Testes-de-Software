import pytest
from unittest.mock import patch, MagicMock
from app import create_usuario
import warnings 
warnings.filterwarnings('ignore')  # Ignorar warning do firebase

def mock_validar_cpf(cpf):
    return cpf != "00000000000"

@pytest.mark.parametrize("cpf, nome, email, endereco, telefone, senha, mock_return, side_effect, expected", [
    ("12345678909", "João", "joao@email.com", "Rua A", "9999999999", "12345", 
     MagicMock(exists=False, add=MagicMock(return_value=(None, MagicMock(id='doc_id')))),
     None,
     {'message': 'Cadastro realizado com sucesso!', 'id': 'doc_id'}),

    ("00000000000", "João", "joao@email.com", "Rua A", "9999999999", "12345", 
     None, 
     None,
     {'error': 'CPF inválido!'}),

    ("12345678909", "João", "joao@email.com", "Rua A", "9999999999", "12345", 
     MagicMock(stream=MagicMock(return_value=[MagicMock()])), 
     None,
     {'error': 'CPF já cadastrado!'}),

    ("12345678909", "", "joao@email.com", "Rua A", "9999999999", "12345", 
     None, 
     None,
     {'error': 'Todos os campos devem ser preenchidos!'}),

    ("12345678909", "João", "emailinvalido", "Rua A", "9999999999", "12345", 
     None, 
     None,
     {'error': 'E-mail inválido!'}),

    ("12345678909", "João", "joao@email.com", "Rua A", "9999", "12345", 
     None, 
     None,
     {'error': 'Telefone inválido!'}),

    ("12345678909", "João", "joao@email.com", "Rua A", "9999999999", "12345", 
     None, 
     Exception("Erro Inesperado"),
     {'error': 'Erro Inesperado'}),
])
@patch("app.db.collection")
@patch("app.validar_cpf", side_effect=mock_validar_cpf)
def test_create_usuario(mock_validar_cpf, mock_db_collection, cpf, nome, email, endereco, telefone, senha, mock_return, side_effect, expected):
    if side_effect:
        mock_db_collection.return_value.where.return_value.stream.side_effect = side_effect
    else:
        if isinstance(mock_return, MagicMock):
            mock_db_collection.return_value.where.return_value.stream.return_value = mock_return.stream.return_value
            mock_db_collection.return_value.add.return_value = mock_return.add.return_value
        else:
            mock_db_collection.return_value.where.return_value.stream.return_value = []

    result = create_usuario(cpf, nome, email, endereco, telefone, senha)

    assert result == expected

if __name__ == "__main__":
    pytest.main()
