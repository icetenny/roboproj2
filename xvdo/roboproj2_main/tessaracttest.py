import cv2
import pytesseract


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Error")
        continue

    cv2.imshow("cam", frame)

    if cv2.waitKey(1) == ord('q'):
        cap.release()

cv2.imwrite(f"data/{input('File name: ')}.jpg", frame)

# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
print(pytesseract.image_to_string(img_rgb,lang='tha'))
# print(pytesseract.image_to_boxes(img_rgb))
# print(pytesseract.image_to_data(img_rgb))

cv2.waitKey()
cv2.destroyAllWindows()
