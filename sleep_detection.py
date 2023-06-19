import cv2
import dlib
from functools import wraps
from scipy.spatial import distance
import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD
import os

def calculate_EAR(eye): # 눈 거리 계산
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear_aspect_ratio = (A+B)/(2.0*C)
	return ear_aspect_ratio

#GPIO Warning dismiss
GPIO.setwarnings(False)

# 카메라 셋팅
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# dlib 인식 모델 정의
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# gpio 셋팅
lastsave = 0
output_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(output_pin, GPIO.OUT, initial = GPIO.LOW)
buzzer = 13

#buzzer_frequency set
scale = [261, 294, 329, 349, 392, 440, 493, 523]
GPIO.setup(buzzer, GPIO.OUT)
p = GPIO.PWM(buzzer, 100)
listd = [0,4,6,4,0,4,6,0]

#LCD setting
lcd = CharLCD('PCF8574', 0x27)

def counter(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        tmp.count += 1
        time.sleep(0.05)
        global lastsave
        if time.time() - lastsave > 5:
            lastsave = time.time()
            tmp.count = 0
        return func(*args, **kwargs)
    tmp.count = 0
    return tmp

@counter
def close():
    cv2.putText(frame,"Closed",(20,100), cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4)

#def sound():
    #global curr_value
    #GPIO.output(output_pin, GPIO.HIGH)
    #time.sleep(2) 
    #GPIO.output(output_pin, GPIO.LOW)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:

        face_landmarks = dlib_facelandmark(gray, face)
        leftEye = []
        rightEye = []

        for n in range(36,42): # 오른쪽 눈 감지
        	x = face_landmarks.part(n).x
        	y = face_landmarks.part(n).y
        	leftEye.append((x,y))
        	next_point = n+1
        	if n == 41:
        		next_point = 36
        	x2 = face_landmarks.part(next_point).x
        	y2 = face_landmarks.part(next_point).y
        	cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        for n in range(42,48): # 왼쪽 눈 감지
        	x = face_landmarks.part(n).x
        	y = face_landmarks.part(n).y
        	rightEye.append((x,y))
        	next_point = n+1
        	if n == 47:
        		next_point = 42
        	x2 = face_landmarks.part(next_point).x
        	y2 = face_landmarks.part(next_point).y
        	cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        left_ear = calculate_EAR(leftEye)
        right_ear = calculate_EAR(rightEye)

        EAR = (left_ear+right_ear)/2
        EAR = round(EAR,2)

        if EAR<0.19:
            close()
            print(f'close count : {close.count}')
            #lcd.home()
            #lcd.write_string('closed')
            
            #time.sleep(0.01)
            if close.count == 15:
                print("Driver is sleeping")
                lcd.home()
                lcd.write_string('Careful!\r\nAre you sleepy?')
                text="Warning"
                for i in range(1,3):
                	os.system("espeak -a 200 -p 20 -s 240 -v en-us+f5" + " " + text)
                for i in range(1, 8):
                        p.start(100)
                        p.ChangeDutyCycle(10)                        
                        p.ChangeFrequency(scale[listd[i]])
                        time.sleep(0.2)
                        if i >= 7:
                                 p.stop()
                                 break
                lcd.clear()
        print(EAR)

    cv2.imshow("Are you Sleepy?", frame)

    key = cv2.waitKey(30)
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()
