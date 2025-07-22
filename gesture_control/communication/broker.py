def connectBroker():
    # Implementar conexão com o broker MQTT aqui
    print("Broker conectado (mock)")
    return "client_mock"

def sendMessage(client, message):
    # Enviar mensagem para o broker
    print(f"Enviando mensagem: {message}")

def breakBroker(client):
    # Encerrar conexão
    print("Broker desconectado (mock)")
