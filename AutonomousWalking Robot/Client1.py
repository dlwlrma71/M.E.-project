from sys import argv
from Time import Time
import numpy as np
from time import sleep
import json
from http.client import HTTPConnection
import time
import RPi.GPIO as GPIO
PORT = 8000

# * 모터 GPIO정의
motor1A = 16
motor1B = 18
motor2A = 15
motor2B = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)

p1A = GPIO.PWM(motor1A, 1000)
p1B = GPIO.PWM(motor1B, 1000)
p2A = GPIO.PWM(motor2A, 1000)
p2B = GPIO.PWM(motor2B, 1000)
p1A.start(0)
p1B.start(0)
p2A.start(0)
p2B.start(0)
# * 모터 스피드를 인풋으로 받고, 모터 제어 함수 (2초 유지)


def ControlMethod(leftvalue, rightvalue):
    #! leftvalue에 90, right value에 70 이 균형이 맞았음
    # * 1 : A0 B+ 가 정방향  2: A+ B0 가 정방향
    if (leftvalue > 0):
        p1A.ChangeDutyCycle(0)
        p1B.ChangeDutyCycle(leftvalue)
    else:
        p1A.ChangeDutyCycle(-leftvalue)
    if rightvalue > 0:
        p2A.ChangeDutyCycle(rightvalue)
        p2B.ChangeDutyCycle(0)
    else:
        p2A.ChangeDutyCycle(0)
        p2B.ChangeDutyCycle(-rightvalue)
    Time.sleep(2)

# * 방향키 명령값에 따른 모터 출력값 조정 (하드웨어 점검 후 조정 )


MOTOR_SPEEDS = {
    "q": (90, 50), "w": (90, 70), "e": (70, 70),
    "a": (-80, 60), "s": (0, 0), "d": (80, -60),
    "x": (-90, -70),
}


# * json 형식 데이터 input
def main():
    while True:
        conn = HTTPConnection(
            f"{argv[1] if len(argv) > 1 else  'localhost'}:{PORT}")

        try:
            conn.request("GET", "/")
        except ConnectionRefusedError as error:
            print(error)
            sleep(1)
            continue

        print('Connected')
        res = conn.getresponse()
        while True:
            chunk = res.readline()
            if (chunk == b'\n'):
                continue
            if (not chunk):
                break

            chunk = chunk[:-1].decode()
            data = json.loads(chunk)
            print(Time(), data)
            action = data['action']
            print('action', action)
            # * 수동 주행 코드 실행
            ControlMethod(MOTOR_SPEEDS[action][0], MOTOR_SPEEDS[action][1])


main()
