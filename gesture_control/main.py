import cv2
import mediapipe as mp
import numpy as np
from hand_recognition import HandRecognizer
from utils import show_info, validate_command
from gpio_map import GPIO_MAP
import communication.broker as com

def main():
    client = com.connectBroker()
    cap = cv2.VideoCapture(0)
    hands_module = mp.solutions.hands
    hands_detector = hands_module.Hands(max_num_hands=1)
    drawing_utils = mp.solutions.drawing_utils
    cv2.namedWindow('Img', cv2.WINDOW_NORMAL)

    hand_recognizer = HandRecognizer()
    modo_reconhecimento = True
    modo_confirmacao = False
    modo_contagem = False
    modo_on_off = False
    modo_navegacao = False

    i = j = k = l = 0
    comando_atual = ""
    comando_anterior = ""
    index_class_element = ""
    info_display = ""

    while True:
        success, frame = cap.read()
        if not success:
            print("Erro ao capturar o vídeo!")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands_detector.process(rgb_frame)
        landmarks = results.multi_hand_landmarks
        h, w, _ = frame.shape

        if landmarks:
            if modo_reconhecimento:
                for hand in landmarks:
                    x_max, y_max, x_min, y_min = 0, 0, w, h
                    for lm in hand.landmark:
                        x, y = int(lm.x * w), int(lm.y * h)
                        x_max, x_min = max(x_max, x), min(x_min, x)
                        y_max, y_min = max(y_max, y), min(y_min, y)
                    try:
                        comando_atual, i = hand_recognizer.predict_gesture(frame, y_min, y_max, x_min, x_max, i)
                        show_info(frame, comando_atual, (w - 640, 100))

                        validado, comando_anterior, i = validate_command("Keras", comando_atual, comando_anterior, i)
                        if validado:
                            modo_reconhecimento = False
                            modo_confirmacao = True
                            info_display = f"Confirma a função {comando_atual}?"
                        show_info(frame, str(i), (w - 640, 200))
                    except Exception as e:
                        print(f"Erro ao processar imagem: {e}")
                        continue
            else:
                pontos = []
                for hand in landmarks:
                    drawing_utils.draw_landmarks(frame, hand, hands_module.HAND_CONNECTIONS)
                    pontos += [(int(pt.x * w), int(pt.y * h)) for pt in hand.landmark]

                dedos = [8, 12, 16, 20]
                contador = 0
                if pontos:
                    if pontos[4][0] < pontos[3][0]:
                        contador += 1
                    for d in dedos:
                        if pontos[d][1] < pontos[d - 2][1]:
                            contador += 1

                if modo_confirmacao:
                    validado, comando_anterior, j = validate_command("MediaPipe", contador, comando_anterior, j)
                    show_info(frame, str(j), (w - 640, 200))
                    if validado:
                        j = 0
                        if contador == 0:
                            modo_confirmacao = False
                            modo_reconhecimento = True
                            info_display = ""
                        elif contador == 1:
                            info_display = f"Função {comando_atual} confirmada!"
                            modo_confirmacao = False
                            if comando_atual != "Clima":
                                modo_contagem = True
                elif modo_contagem:
                    info_display = f"Escolha a {comando_atual}"
                    if contador == 0:
                        modo_contagem = False
                        modo_reconhecimento = True
                        info_display = ""
                    else:
                        validado, comando_anterior, k = validate_command("MediaPipe", contador, comando_anterior, k)
                        show_info(frame, str(k), (w - 640, 200))
                        if validado:
                            k = 0
                            modo_contagem = False
                            modo_on_off = True
                            index_class_element = contador
                            info_display = "On ou Off?"
                elif modo_on_off:
                    validado, comando_anterior, l = validate_command("MediaPipe", contador, comando_anterior, l)
                    show_info(frame, str(l), (w - 640, 200))
                    if validado:
                        l = 0
                        elemento = "LUZ" if comando_atual == "Luzes" else "PORTA"
                        chave = f"{elemento}{index_class_element}"
                        if elemento == "LUZ":
                            estado = "ON" if contador else "OFF"
                            com.sendMessage(client, f"{GPIO_MAP[chave]}:{estado}")
                        else:
                            angulo = "SERVO_90" if contador else "SERVO_0"
                            com.sendMessage(client, f"{GPIO_MAP[chave]}:{angulo}")
                        modo_on_off = False
                        modo_reconhecimento = True
                        index_class_element = ""
                        info_display = ""

                show_info(frame, str(contador), (w - 640, 300))

        show_info(frame, info_display, (w - 640, 40))
        cv2.imshow('Img', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    com.breakBroker(client)

if __name__ == "__main__":
    main()
