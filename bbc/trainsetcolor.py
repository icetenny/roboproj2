import cv2
import numpy as np

def get_center_list(f_w, f_h, nw, nh):
    l=[]
    for h in range(nh):
        for w in range(nw):
            
            l+=[(int(w/nw*f_w + f_w/nw/2), int(h/nh*f_h+f_h/nh/2))]
    
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


RESIZE_DIM = 120
TOPLEFT = (123,16)
BOTRIGHT = (511,408)

pos_index = 0
n_slot = 4
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
# print(center_list)

print("s: save, c: change label, q: quit, n:next slot")


while cap.isOpened():
    ret, frame = cap.read()
    frame_bgr = cv2.resize(frame[TOPLEFT[1]: BOTRIGHT[1], TOPLEFT[0]:BOTRIGHT[0]], (RESIZE_DIM, RESIZE_DIM))
    frame_lab = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2LAB)
    frame_show = np.copy(frame_bgr)
    
    # print(frame.shape)

    if not ret:
        print("Error")
        continue

    draw_grid(frame_show, 6, 6, (0,0,0), 1)

    
    # for c in center_list:
    #     draw_points(frame_show, c, 3, (0,0,0))

    for n in range(n_slot):

        draw_points(frame_show, center_list[(pos_index+n)%36], 3, (0,0,0))
    

    frame_show = cv2.resize(frame_show, (480,480))

    cv2.imshow("frame", frame_show)

    key = cv2.waitKey(10)

    if  key == ord('q'):
        cap.release()
    elif key == ord('s'):
        fbgr = open("train_color_bgr.csv", "a")
        flab = open("train_color_lab.csv", "a")

        for n in range(n_slot):
            print(f"SAVING AT POSITION {pos_index + n}, LABEL = {label}")
            fbgr.write(get_color_data(frame_bgr, center_list[(pos_index+n)%36], 3)+f",{label}\n")
            flab.write(get_color_data(frame_lab, center_list[(pos_index+n)%36], 3)+f",{label}\n")

        cv2.imshow("frame", np.ones(frame_show.shape)*255)
        cv2.waitKey(50)
        fbgr.close()
        flab.close()
    elif key == ord('c'):
        print("CHANGING LABEL")
        while True:
            newlabel = int(input("INPUT NEW INDEX: "))
            if newlabel in range(9):
                label = newlabel
                print("NEW LABEL", label)
                break
            else:
                print("try again")

    elif key == ord('n'):
        print("NEXT SLOT")
        pos_index = (pos_index+1)%36
        



cv2.destroyAllWindows()
