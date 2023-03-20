# import os
# import socket
# import sys
from custom_socket import CustomSocket
import requests
import json
import numpy as np
# import cv2
import nlp


def main():
    # HOST = socket.gethostname()
    HOST = "192.168.1.53"
    PORT = 10030

    server = CustomSocket(HOST, PORT)
    server.startServer()

    while True:
        conn, addr = server.sock.accept()
        print("Client connected from", addr)
        text = ""

        while True:
            try:
                data = server.recvMsg(conn)
                # print(data)
                # img = np.frombuffer(data, dtype=np.uint8)
                # print(img)
                text = data.decode('utf-8')
                print(text)

                mode, t = text[:2], text[2:]
                if mode == "&&":
                    tran_text = nlp.translate(t, mode=1)
                else:

                    tran_text = nlp.translate(t)

                print(tran_text)

                print("send")
                server.sendMsg(conn, json.dumps(tran_text))


            except Exception as e:
                print(e)
                print("Connection Closed")
                break


# def main():
#     cap = cv2.VideoCapture(0)
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             print("Error")

#         cv2.imshow("frame", frame)

#         if cv2.waitKey(1) == ord('q'):
            
#             text = describe(frame)
 
#             print(text)

#             cap.release()
    
#     cv2.waitKey()
#     cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
