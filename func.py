from app import *

# Validando create de usuário
resultado = create_usuario("99999999999", "João Silva", "joao@exemplo.com", "Rua A, 123", "81999999999", "senha123")
print(resultado)  # {'message': 'Cadastro realizado com sucesso!', 'id': 'ID'}

# Validando update de usuário
resultado = update_usuario("99999999999", {"endereco": "Rua B, 456"})
print(resultado)  # {'message': 'Usuário atualizado com sucesso!'}

# Validando get de usuário
resultado = get_usuario("99999999999")
print(resultado)  # Dados do usuário

# Validando login de usuário
resultado = login_usuario('99999999999', 'senha123')
print(resultado)

# Validando create de pedido
resultado = create_pedido("99999999999", "Rua B, 456", "Cartão", 'Prato1, Prato2', "81999999999", 59.90)
print(resultado)  # {'message': 'Pedido criado com sucesso!', 'id': 'ID'}

# Validando get de pedido
resultado = get_pedido("99999999999")
print(resultado)  # Dados do pedido

# Validando create admin
resultado = cadastrar_admin("99999999999", "senhaadmin")
print(resultado)  # {'message': 'Cadastro realizado com sucesso!', 'id': 'ID'}

# Validando get de admin
resultado = get_admin("99999999999")
print(resultado)  # Dados do admin

# Validando login de admin
resultado = login_admin('99999999999', 'senhaadmin')
print(resultado)

# Validando create de prato
resultado = create_prato("Prato Teste", "http://exemplo.com/img.jpg", 29.90)
print(resultado)  # {'message': 'Cadastro realizado com sucesso!', 'id': 'ID'}

# Validando delete de prato
prato_id = resultado['id']  # ID do prato adicionado
resultado = delete_prato(prato_id)
print(resultado)  # {'message': 'Prato excluído com sucesso!'}

# Validando list de pratos
resultado = list_pratos()
print(resultado)  # Lista de dicionários com os pratos e seus IDs

# Validando create de promoção
resultado = create_promocao("Promoção Teste", "http://exemplo.com/promo.jpg", 19.90)
print(resultado)  # {'message': 'Promoção cadastrada com sucesso!', 'id': 'ID'}

# Validando delete de promoção
promocao_id = resultado['id']  # ID do promoção adicionado
resultado = delete_promocao(promocao_id)
print(resultado)  # {'message': 'Promoção excluída com sucesso!'}

# Validando list de promoções
resultado = list_promocaos()
print(resultado)  # Lista de dicionários com as promoções e seus IDs

# Validando create de unidade de restaurante
resultado = create_unidade("Unidade Teste", "http://exemplo.com/unidade.jpg", "Avenida Teste, 123")
print(resultado)  # {'message': 'Unidade de restaurante cadastrada com sucesso!', 'id': 'ID'}

# Validando delete de unidade de restaurante
unidade_id = resultado['id']  # ID da unidade de restaurante adicionada
resultado = delete_unidade(unidade_id)
print(resultado)  # {'message': 'Unidade de restaurante excluída com sucesso!'}

# Validando list de unidades de restaurante
resultado = list_unidades()
print(resultado)  # Lista de dicionários com as unidades
