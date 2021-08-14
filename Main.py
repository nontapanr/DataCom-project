import cv2
import sys
import time
import serial
import PROCESS
import numpy as np
from PIL import Image

readPort = "COM10"

width = 160
height = 120


def read_image(serial, name):
    print("reading image")
    data = serial.read(width * height)
    print("received image")
    image = Image.frombytes("P", (width, height), data)
    image.save(f"./Project_Camera/{name}.bmp")


def capture(port, name):
    print(f"port : {port}")
    ser = serial.Serial(
        port=port,
        baudrate=1000000,
        parity=serial.PARITY_NONE,
        bytesize=serial.EIGHTBITS,
        stopbits=serial.STOPBITS_ONE
    )
    print("waiting for Arduino")
    time.sleep(1)

    if not ser.isOpen():
        ser.open()
        print("serial is opened")
    else:
        print("serial already open")

    for i in range(8):
        print("waiting for RDY")
        ser.read_until("*RDY*".encode())
        # print("reading image")
        read_image(ser, name)
        print("finish reading")

    ser.close()


def scan():
    result = []
    ser = serial.Serial("COM10", 115200)
    time.sleep(3)

    # scan Left
    ser.write("L".encode())
    time.sleep(3)
    capture("COM4", "left")
    result_L = PROCESS.process("left.bmp")
    result.extend(result_L)
    time.sleep(0.1)

    # scan Mid
    ser.write("M".encode())
    time.sleep(3)
    capture("COM4", "mid")
    result_M = PROCESS.process("mid.bmp")
    result.extend(result_M)
    time.sleep(0.1)

    # scan Right
    ser.write("R".encode())
    time.sleep(3)
    capture("COM4", "right")
    result_R = PROCESS.process("right.bmp")
    result.extend(result_R)
    time.sleep(0.1)

    # back to Mid
    ser.write("M".encode())
    ser.close()

    return result


def scanLeft():
    ser = serial.Serial("COM10", 115200)
    time.sleep(3)
    ser.write("L".encode())
    time.sleep(2)
    capture("COM4", "left")
    result_L = PROCESS.process("left.bmp")
    time.sleep(0.1)

    # back to Mid
    ser.write("M".encode())
    ser.close()

    return result_L


def scanMid():
    ser = serial.Serial("COM10", 115200)
    time.sleep(3)
    ser.write("M".encode())
    time.sleep(2)
    capture("COM4", "mid")
    result_M = PROCESS.process("mid.bmp")
    time.sleep(0.1)

    # back to Mid
    ser.write("M".encode())
    ser.close()

    return result_M


def scanRight():
    ser = serial.Serial("COM10", 115200)
    time.sleep(3)
    ser.write("R".encode())
    time.sleep(2)
    capture("COM4", "right")
    result_R = PROCESS.process("right.bmp")
    time.sleep(0.1)

    # back to Mid
    ser.write("M".encode())
    ser.close()

    return result_R


avgColor = 55
command = ''


def decodePic(receivedData):
    output = ""
    if(len(receivedData) == 61):
        receivedData = receivedData[:-1]

        for i in range(4, len(receivedData), 5):
            if(int(receivedData[i]) >= avgColor):
                output += "1"
            else:
                output += "0"

    elif(len(receivedData) == 21):
        receivedData = receivedData[:-1]

        for i in range(4, len(receivedData), 5):
            if(int(receivedData[i]) >= avgColor):
                output += "1"
            else:
                output += "0"

    return output

def toBinary(data): # เปลี่ยนค่าที่อ่านได้ เป็น 1, 0
    output = ""
    for item in data:
        if int(item) >= avgColor:
            output += "1"
        else:
            output += "0"

    return output
            


if __name__ == "__main__":
    ser = serial.Serial(readPort, 115200)
    if not ser.isOpen():
        ser.Open()
    if ser.inWaiting():
        command = ser.readline().decode()

    if("AR" in command):
        # ถ่ายภาพ ->วิ่งforใน value ของreseult เอาค่ามาต่อกัน-> STRING 61 ค่า
        result = scan()
        sendBackData = decodePic(result)
        ser.write(sendBackData.encode())
        ser.close()

    elif("LR" in command):
        # ถ่ายภาพ -> โค้ดผ้าไหม -> STRING
        # STRING = Process(data)
        result = scanLeft()
        sendBackData = decodePic(result)
        ser.write(sendBackData.encode())
        ser.close()

    elif("MR" in command):
        # ถ่ายภาพ -> โค้ดผ้าไหม -> STRING
        # STRING = Process(data)
        result = scanMid()
        sendBackData = decodePic(result)
        ser.write(sendBackData.encode())
        ser.close()

    elif("RR" in command):
        # ถ่ายภาพ -> โค้ดผ้าไหม -> STRING
        # STRING = Process(data)
        result = scanRight()
        sendBackData = decodePic(result)
        ser.write(sendBackData.encode())
        ser.close()

    elif("A" in command):
        # ถ่ายภาพ ->วิ่ง for ใน value ของ reseult เอาค่ามาต่อกัน-> STRING 61 ค่า
        # sendBackData = STRING
        sendBackData = ""
        result = scan()
        for item in result:
            sendBackData += result[item]
        ser.write(sendBackData.encode())
        ser.close()

    elif("L" in command):
        # ถ่ายภาพ -> โค้ดผ้าไหม -> STRING
        # sendBackData = STRING
        sendBackData = scanLeft()
        ser.write(sendBackData.encode())
        ser.close()

    elif("R" in command):
        # ถ่ายภาพ -> โค้ดผ้าไหม -> STRING
        # sendBackData = STRING
        sendBackData = scanRight()
        ser.write(sendBackData.encode())
        ser.close()

    elif("M" in command):
        # ถ่ายภาพ -> โค้ดผ้าไหม -> STRING
        # sendBackData = STRING
        sendBackData = scanMid()
        ser.write(sendBackData.encode())
        ser.close()

    elif(len(command) == 4):
        # ถ่ายภาพ(scan) ->วิ่งforใน value ของreseult เอาค่ามาต่อกัน-> STRING 61 ค่า
        # sendBackData = decodePic()
        sendBackData = ""
        result = scan()
        for item in result:
            sendBackData += decodePic(result[item])

        if sendBackData[0:4] == command:
            ser.write("LEFT".encode())

        elif sendBackData[4:8] == command:
            ser.write("MIDDLE".encode())

        elif sendBackData[8:12] == command:
            ser.write("RIGHT".encode())

        else:
            ser.write("NOT FOUND".encode())

        ser.close()
