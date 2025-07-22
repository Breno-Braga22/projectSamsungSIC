import cv2

def show_info(img, text, pos):
    cv2.putText(img, str(text), pos, cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

def validate_command(source, current, previous, counter):
    frames_to_validate_keras = 20  # valor fixo para simplicidade
    frames_to_validate_media = 30
    validation_threshold = frames_to_validate_keras if source == "Keras" else frames_to_validate_media
    validated = 0

    if current == previous:
        if counter >= validation_threshold:
            validated = 1
        else:
            counter += 1
    else:
        previous = current
        counter = 0

    return validated, previous, counter
