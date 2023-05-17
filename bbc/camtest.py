import cv2

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

def draw_points(pic, center_list, d, color):
    for cx, cy in center_list:

        pic[cy,cx] = color
        pic[cy-d,cx] = color
        pic[cy+d,cx] = color
        pic[cy,cx-d] = color
        pic[cy,cx+d] = color


RESIZE_DIM = 120
TOPLEFT = (129,12)
BOTRIGHT = (522,408)


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
print(center_list)
while cap.isOpened():
    ret, frame = cap.read()
    frame_re = cv2.resize(frame[TOPLEFT[1]: BOTRIGHT[1], TOPLEFT[0]:BOTRIGHT[0]], (RESIZE_DIM, RESIZE_DIM))
    
    # print(frame.shape)

    if not ret:
        print("Error")
        continue

    draw_grid(frame_re, 6, 6, (0,0,0),1)
    # draw_circle(frame, center_list, 1, (0,0,0),1)
    draw_points(frame_re, center_list, 3, (0,0,0))

    frame_show = cv2.resize(frame_re, (480,480))

    cv2.imshow("frame", frame_show)
    cv2.imshow("ori_frame", frame)

    if cv2.waitKey(1) == ord('q'):
        cap.release()
cv2.destroyAllWindows()