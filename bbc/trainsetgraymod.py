import cv2
import numpy as np

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
    return ",".join(map(str,((pic_gray[sy+1:sy+SLOT_DIM-1, sx+1:sx+SLOT_DIM-1]+1)%256).flatten()))


RESIZE_DIM = 240
TOPLEFT = (122,26)
BOTRIGHT = (522,422)
SLOT_DIM = RESIZE_DIM // 6
pos_index = 0
n_slot = 9
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
print("s: save, c: change label, q: quit, n:next slot")

while cap.isOpened():
    ret, frame = cap.read()
    frame_re = cv2.resize(frame[TOPLEFT[1]: BOTRIGHT[1], TOPLEFT[0]:BOTRIGHT[0]], (RESIZE_DIM, RESIZE_DIM))
    frame_show = np.copy(frame_re)

    frame_gray = cv2.cvtColor(frame_re, cv2.COLOR_BGR2GRAY)


    for i in range(RESIZE_DIM):
        for j in range(RESIZE_DIM):
            b, g, r = map(int,frame_re[i,j])
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

    draw_grid(frame_show, 6, 6, (0,0,0),1)

    for n in range(n_slot):
        draw_points(frame_show, center_list[(pos_index+n)%36], 6, (0,0,0))
    

    frame_show = cv2.resize(frame_show, (480,480))

    # sx, sy = start_point_list[pos_index]

    cv2.imshow("frame", frame_show)
    # cv2.imshow("id_frame", frame_gray[sy+1:sy+SLOT_DIM-1, sx+1:sx+SLOT_DIM-1])
    cv2.imshow("gray", frame_gray)
    key = cv2.waitKey(10)

    if  key == ord('q'):
        cap.release()
    elif key == ord('s'):
        fshape = open("train_shape_m.csv", "a")

        for n in range(n_slot):

            print(f"SAVING AT POSITION {(pos_index+n)%36}, LABEL = {label}")
            fshape.write(get_shape_data(frame_gray, start_point_list[(pos_index+n)%36])+f",{label}\n")
        cv2.imshow("frame", np.ones(frame_show.shape)*255)
        cv2.waitKey(50)

        fshape.close()
    elif key == ord('c'):
        print("CHANGING LABEL")
        while True:
            newlabel = int(input("INPUT NEW INDEX: "))
            if newlabel in range(10):
                label = newlabel
                print("NEW LABEL", label)
                break
            else:
                print("try again")

    elif key == ord('n'):
        print("NEXT SLOT")
        pos_index = (pos_index+1)%36
cv2.destroyAllWindows()