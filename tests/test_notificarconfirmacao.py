import pytest
import re
from unittest.mock import patch, MagicMock
from app import notificar_confirmacao
import smtplib
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase

@pytest.mark.parametrize("email_cliente, pedido_id, permissao, mock_pedido_exists, mock_email_success, expected", [
    ("cliente@email.com", "123", "ATENDENTE", True, True, {'message': 'Notificação de pedido confirmado enviada via e-mail!'}),
    ("cliente@email.com", "123", "COZINHEIRO", True, True, {'error': 'Nível de permissão inválido!'}),
    ("clienteemail.com", "123", "GERENTE", True, True, {'error': 'E-mail inválido!'}),
    ("cliente@email.com", "999", "GERENTE", False, True, {'error': 'Pedido não encontrado!'}),
    ("cliente@email.com", "123", "GERENTE", True, False, {'error': 'Falha ao enviar o e-mail: [detalhes da exceção]'}),
])
@patch('app.db.collection')
@patch('smtplib.SMTP')
def test_notificar_confirmacao(mock_smtp, mock_db_collection, email_cliente, pedido_id, permissao, mock_pedido_exists, mock_email_success, expected):
    mock_document = MagicMock()
    mock_db_collection.return_value.document.return_value = mock_document
    mock_document.get.return_value.exists = mock_pedido_exists
    mock_document.get.return_value.to_dict.return_value = {
        'data': '2024-08-27',
        'formadepgmto': 'Cartão de Crédito',
        'pratos': ['Prato 1', 'Prato 2'],
        'total': 50.00
    }
    mock_conectar = mock_smtp.return_value
    if mock_email_success:
        mock_conectar.sendmail.return_value = True
    else:
        mock_conectar.sendmail.side_effect = smtplib.SMTPException('Falha ao enviar o e-mail: [detalhes da exceção]')

    resultado = notificar_confirmacao(email_cliente, pedido_id, permissao)
    assert resultado == expected

    if permissao.upper().strip() in ['ATENDENTE', 'GERENTE'] and re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email_cliente) and mock_pedido_exists:
        mock_db_collection.assert_called_once_with('pedido')
        mock_db_collection.return_value.document.assert_called_once_with(pedido_id)
        mock_db_collection.return_value.document.return_value.get.assert_called_once()

        if mock_email_success:
            mock_conectar.sendmail.assert_called_once()
        else:
            mock_conectar.sendmail.assert_called_once()

if __name__ == "__main__":
    pytest.main()
