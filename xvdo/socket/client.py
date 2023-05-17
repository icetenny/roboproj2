import socket
import cv2
from custom_socket import CustomSocket

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# host = socket.gethostname()
host = "0.tcp.ap.ngrok.io"
port = 15888
c = CustomSocket(host, port)
c.clientConnect()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't read frame.")
        continue

    print(frame.shape)
    frame = cv2.resize(frame, (1280, 720))

    # print("Send")
    msg = c.req(frame)
    print(msg)

    # Show client frame
    cv2.imshow("client_cam", frame)
    if cv2.waitKey(1) == ord("q"):
        cap.release()

cv2.destroyAllWindows()
