import os
import socket
import sys
from custom_socket import CustomSocket
import requests
import json
import numpy as np
import cv2
import nlp

# https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/REST/python-analyze.md


def describe(frame, resource_name="meen-test", Ocp_key='d579e048b37d46d683c1482b00e2696d',
             version=3.1,
             maxCandidates=1):
    describe_url = f'https://{resource_name}.cognitiveservices.azure.com/vision/v{version}/describe'
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': Ocp_key}
    params = {'language': 'en', 'maxCandidates': maxCandidates}
    im_buf_arr = cv2.imencode(".jpg", frame)[1]
    frame_bytes = im_buf_arr.tobytes()

    response = requests.post(describe_url, headers=headers, params=params, data=frame_bytes)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    # print(json.dumps(analysis))
    # print(analysis["description"])
    # image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    # cv2.imshow(part_name, part_frame)
    # cv2.waitKey()

    return analysis["description"]['captions'][0]['text']



def main():
    # HOST = socket.gethostname()
    HOST = "192.168.134.28"
    PORT = 10011

    server = CustomSocket(HOST, PORT)
    server.startServer()

    while True:
        conn, addr = server.sock.accept()
        print("Client connected from", addr)
        text = ""

        while True:
            try:
                data = server.recvMsg(conn)
                # img = np.frombuffer(data, dtype=np.uint8).reshape(720, 1280, 3)
                img = np.frombuffer(data, dtype=np.uint8).reshape(360, 640, 3)

                text = describe(img)
 
                print(text)
                th_text = nlp.translate(text)
                # print(th_text)

                print("send")
                server.sendMsg(conn, json.dumps(th_text))


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
