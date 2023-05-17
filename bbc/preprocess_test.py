import cv2

pic = cv2.imread("pic/allb.jpg")
pic = cv2.resize(pic, (120,120))
pic = cv2.resize(pic, (500,500))
gray = cv2.cvtColor(pic, cv2.COLOR_BGR2LAB)
# gray[:,:,1] = 255
# gray = cv2.cvtColor(gray, cv2.COLOR_LAB2BGR)
print(gray)
print(pic.shape, gray.shape)
cv2.imshow("test", pic)
cv2.imshow("test1", gray)
cv2.waitKey()

cv2.destroyAllWindows()