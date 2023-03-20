# import os
# import socket
# import sys
from custom_socket import CustomSocket
import requests
import json
import numpy as np
# import cv2
import nlp
import line


def main():
    # HOST = socket.gethostname()
    HOST = "192.168.1.53"
    PORT = 10040

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

                line.notify(text)

                print("send")
                server.sendMsg(conn, json.dumps(f"Sent via Line: {text}"))


            except Exception as e:
                print(e)
                print("Connection Closed")
                break




if __name__ == '__main__':
    main()
