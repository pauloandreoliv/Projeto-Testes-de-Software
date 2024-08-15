from app import *

# Validando create de usuário
resultado = create_usuario("88999999999", "João Silva", "joao@exemplo.com", "Rua A, 123", "81999999999", "senha123")
print(resultado)  

# Validando update de usuário
resultado = update_usuario("88999999999", {"endereco": "Rua B, 456"})
print(resultado) 

# Validando get de usuário
resultado = get_usuario("88999999999")
print(resultado) 

# Validando login de usuário
resultado = login_usuario('88999999999', 'senha123')
print(resultado)

# Validando create de pedido
resultado = create_pedido("88999999999", "Rua B, 456", "Cartão", 'Prato1, Prato2', "81999999999", 59.90)
id_pedido = resultado['id']
print(resultado) 

# Validando notificação de confirmação do pedido
resultado = notificar_confirmacao("paos@discente.ifpe.edu.br", id_pedido, 'ATENDENTE')
print(resultado)

# Validando avaliação de pedido
resultado = avaliar_pedido(id_pedido, 8)
print(resultado)

# Validando cálculo de avaliações
resultado = calcular_media_avaliacoes('ATENDENTE')
print(resultado)

# Validando get de pedido
resultado = get_pedido("88999999999")
print(resultado)  

# Validando create funcionario
resultado = cadastrar_funcionario("12999999999", "senhafuncionario", 'ATENDENTE', 'GERENTE')
print(resultado) 

# Validando get de funcionario
resultado = get_funcionario("99999999999", 'GERENTE')
print(resultado) 

# Validando login de funcionario
resultado = login_funcionario('99999999999', 'senhafuncionario')
print(resultado)

# Validando create de prato
resultado = create_prato("Prato Teste", "http://exemplo.com/img.jpg", 29.90, 'GERENTE')
print(resultado) 

# Validando create de promocao
prato_id = resultado['id'] 
resultado = create_promocao(prato_id, True, 'GERENTE')
print(resultado)

# Validando delete de prato
resultado = delete_prato(prato_id, 'GERENTE')
print(resultado) 

# Validando list de pratos
resultado = list_pratos()
print(resultado)  

# Validando list de promocoes
resultado= list_promocoes()
print(resultado)
