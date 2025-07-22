# 🏠 MotionSync Home Systems

Sistema inteligente de automação residencial que utiliza **reconhecimento de gestos com visão computacional** para controlar dispositivos físicos, como lâmpadas, portas, ventiladores e muito mais — tudo sem encostar em nada.

---

## 🎯 Visão Geral

O MotionSync permite interações naturais com o ambiente usando **gestos das mãos capturados por webcam** e interpretados em tempo real com . Ele envia comandos via GPIO ou protocolo MQTT para controlar diversos dispositivos domésticos.

> 💡 Para uma visão geral visual e explicativa do projeto, consulte o arquivo [`motionSync.pdf`](./motionSync.pdf).

---

## 🛠️ Tecnologias Utilizadas

- 🤖 **Keras + TensorFlow 2.9.1**: Modelo de rede neural treinado para identificar gestos
- ✋ **MediaPipe Hands**: Rastreamento de mãos com alta precisão
- 📷 **OpenCV**: Captura e visualização de vídeo ao vivo
- 📡 **MQTT ()**: Comunicação com dispositivos externos ou embarcados
- 🐍 **Python 3.8+**

---
### Pré-requisitos:
- Python 3.8 ou superior
- Webcam funcional
- Placa com GPIOs (como Raspberry Pi) ou broker MQTT 
