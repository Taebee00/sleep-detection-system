# sleep-detection-system
2021년 1학기 **임베디드통신시스템** 기말 프로젝트 - **라즈베리파이**를 이용한 **졸음 감지 및 방지 시스템**

> 상세 동영상 링크: <https://youtu.be/T8NQtY3ZAkc>

|![image](https://github.com/Taebee00/sleep-detection-system/assets/104549849/a7760ed5-e7ff-414f-ae7a-80ce772c7e35)|![image](https://github.com/Taebee00/sleep-detection-system/assets/104549849/19658390-3140-4611-87d5-8b3c92f5e853)|
|---|---|



## 프로젝트 개요
운전자의 졸음을 인식하고 피드백 및 경고를 통해 졸음운전 문제를 해결하고자 함

## 프로젝트 기간
2021.05.23 ~ 2021.06.10

## 개발 환경
### HW
- Jeston Nano
- Speaker
- I2C LCD
- USB Webcam
- Amp
### SW
- Python
- OpenCV
- Dlib library

## Detection
### Face Detection
- Dlib library 에서 제공하는 `get_frontal_face_detector`함수를 이용하여 이미지 속 얼굴의 위치를 detect
- `shape_predictor`함수를 이용하여 detect된 얼굴을 68개의 landmark로 변환

![image](https://github.com/Taebee00/sleep-detection-system/assets/104549849/a8d12e17-0f28-4d23-9dc4-b51d683f8103)

### Eye Blink Detection
- Eye Aspect Ratio(EAR) Algorithm

  눈의 종횡 비 변화를 이용해 눈 감김을 판단하는 알고리즘
  
  ![image](https://github.com/Taebee00/sleep-detection-system/assets/104549849/50a3af23-f12e-4373-a9cb-432633a210e4)
  
- Face Detection을 통해 얻은 68개의 landmark 중 눈에 해당하는 36~47번 landmark를 이용하여 EAR rate를 계산
- EAR rate가 감소하며 눈의 종횡 비가 감소한 것이므로 '눈 감김'으로 판단
- '눈 감김'의 빈도를 count 하여 졸음을 감지

![image](https://github.com/Taebee00/sleep-detection-system/assets/104549849/5df815f4-9d9b-41ca-ac85-fee027cfcc9b)

## Warning
- I2C LCD에 경고 메세지 출력
`lcd.writ_string('Careful\r\nAre you sleepy?)`
- espeak를 통해 경고 메시지를 TTS 방식으로 출력
`os.system("espeak -a 200 -p 20 -s 240 -v en-us+f5" + " " +text)`

## 기대 효과 및 장점
- 단순히 눈을 감았다 뜨는 것이 아닌, 일정한 시간 안에 몇 번 감았는지를 계산해 운전자의 졸음 여부를 확실하고 체계적으로 감시하고 감지할 수 있음
- 졸음을 감지하면 운전자에게 시각적으로, 청각적으로 신호를 전달하여 운전자가 즉각적인 피드백을 받을 수 있도록 함
- 운전 관련 분야가 아닌 거짓말 탐지 등, 눈을 깜빡임을 인식하는 다른 다양한 분야에도 쓰일 수 있음

