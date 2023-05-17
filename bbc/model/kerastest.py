import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import numpy as np
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2


wtf_color_model = keras.models.load_model("model/wtf_color_det")
wtf_shape_model = keras.models.load_model("model/wtf_shape_det")
COLOR_LIST = ("blue", "red", "yellow", "purple", "green", "orange", "pink", "wine", "mint", "none")
SHAPE_LIST = ("circle", "hex", "pill", "pie", "none")

# a = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# for i in range(10):p = reconstructed_model.predict(a)
# print(p)
# np.argmax(p, axis=1)

def get_center_list(f_w, f_h, nw, nh):

    l=[]
    for h in range(nh):
        for w in range(nw):
            
            l+=[(int(w/nw*f_w + f_w/nw/2), int(h/nh*f_h+f_h/nh/2))]
    
    return l

def get_start_point_list(f_w, f_h, nw, nh):
    l = []
    for h in range(nh):
        for w in range(nw):
            
            l+=[(int(w/nw*f_w), int(h/nh*f_h))]
    
    return l
def draw_grid(pic, w, h, color, thickness):
    ph, pw,_ = pic.shape
    for i in range(1,h):
        cv2.line(pic, (0,int(ph*i/h)),(pw, int(ph*i/h)), color, thickness)
    for i in range(1,w):
        cv2.line(pic, (int(pw*i/w),0),(int(pw*i/w),ph), color, thickness)

def draw_circle(pic, center_list, radius, color, thickness):
    for center in center_list:
        cv2.circle(pic, center, radius, color, thickness)

def draw_points(pic, center, d, color):
    cx, cy = center

    pic[cy,cx] = color
    pic[cy-d,cx] = color
    pic[cy+d,cx] = color
    pic[cy,cx-d] = color
    pic[cy,cx+d] = color

def get_color_data(pic, center, d):
    # dl = []
    cx, cy = center
    return ",".join(map(str,(*pic[cy,cx], *pic[cy-d,cx], *pic[cy+d,cx], *pic[cy,cx-d], *pic[cy,cx+d])))

def get_shape_data(pic_gray, start_point):
    sx, sy = start_point
    return ",".join(map(str,pic_gray[sy+1:sy+SLOT_DIM-1, sx+1:sx+SLOT_DIM-1].flatten()))

def get_color_data_list(pic, center, d):
    cx, cy = center
    return np.array([[*pic[cy,cx], *pic[cy-d,cx], *pic[cy+d,cx], *pic[cy,cx-d], *pic[cy,cx+d]]]).astype("uint8")
    # return [*pic[cy,cx], *pic[cy-d,cx], *pic[cy+d,cx], *pic[cy,cx-d], *pic[cy,cx+d]]

def get_shape_data_list(pic_gray, start_point):
    sx, sy = start_point
    return np.array([((pic_gray[sy+1:sy+SLOT_DIM-1, sx+1:sx+SLOT_DIM-1]+1)%256).flatten()]).astype("uint8")
    # return ",".join(map(str,((pic_gray[sy+1:sy+SLOT_DIM-1, sx+1:sx+SLOT_DIM-1]+1)%256).flatten()))
RESIZE_DIM = 240
TOPLEFT = (122,26)
BOTRIGHT = (522,422)
SLOT_DIM = RESIZE_DIM // 6
pos_index = 0
n_slot = 1
label = 0

l = []
for i in range(10):
    try:
        ret, frame = cv2.VideoCapture(i).read()
        if not ret:
            continue
        l+=[i]
    except:
        continue

print(l)

cap = cv2.VideoCapture(int(input("Cam index: ")))
f_w, f_h = cap.get(3), cap.get(4)

center_list = get_center_list(RESIZE_DIM, RESIZE_DIM, 6, 6)
start_point_list = get_start_point_list(RESIZE_DIM, RESIZE_DIM, 6, 6)

# print(center_list)


while cap.isOpened():
    ret, frame = cap.read()
    frame_bgr = cv2.resize(frame[TOPLEFT[1]: BOTRIGHT[1], TOPLEFT[0]:BOTRIGHT[0]], (RESIZE_DIM, RESIZE_DIM))
    # frame_lab = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2LAB)
    frame_show = np.copy(frame_bgr)

    frame_gray = cv2.cvtColor(frame_show, cv2.COLOR_BGR2GRAY)


    for i in range(RESIZE_DIM):
        for j in range(RESIZE_DIM):
            b, g, r = map(int,frame_show[i,j])
            # print((b+g+r/3))
            m = (b+g+r)/3

            if m > 100 and ((b-m)**2 + (g-m)**2 + (r-m)**2) < 400 :
                frame_gray[i,j] = 255
                # print("yes")
            else:
                frame_gray[i, j] = 0
    
    # print(frame.shape)

    if not ret:
        print("Error")
        continue

    draw_grid(frame_show, 6, 6, (0,0,0), 1)

    
    # for c in center_list:
    #     draw_points(frame_show, c, 3, (0,0,0))

    for n in range(n_slot):

        draw_points(frame_show, center_list[(pos_index+n)%36], 6, (0,0,0))
    

    frame_show = cv2.resize(frame_show, (480,480))

    sx, sy = center_list[pos_index]

    cv2.imshow("frame", frame_show)
    cv2.imshow("frameg", frame_gray)
    cv2.imshow("id_frame", frame_gray[sy+1:sy+SLOT_DIM-1, sx+1:sx+SLOT_DIM-1])

    key = cv2.waitKey(10)

    color_l = get_color_data_list(frame_bgr, center_list[pos_index],3)
    shape_l = get_shape_data_list(frame_gray, start_point_list[pos_index])
    # print(color_l, type(color_l))

    # color_res = int(np.argmax(wtf_color_model.predict(color_l, verbose=0), axis=1))
    # if color_res != 9:
    #     print(COLOR_LIST[color_res])

    shape_res = int(np.argmax(wtf_shape_model.predict(shape_l, verbose=0), axis=1))
    if shape_res != 4:
        print(SHAPE_LIST[shape_res])


    if  key == ord('q'):
        cap.release()
    elif key == ord('n'):
        pos_index = (pos_index+1)%36


cv2.destroyAllWindows()
