import time,utime
import socket
import network
import wifi
from machine import Timer,Pin,PWM
import json

hand_status={
            "hand1":1,
            "hand2":1,
            }

servo_status={
              "servo1":180,
              "servo2":180
              }
current_result=[]
hand_change_waittime=0.2
servno_change_waittime=0.2


hand_1=Pin(12,Pin.OUT)
hand_1_dir=Pin(14,Pin.OUT)
hand_2=Pin(2,Pin.OUT)
hand_2_dir=Pin(4,Pin.OUT)

servno1_rotate=Pin(27,Pin.OUT)
servno1_dir=Pin(26,Pin.OUT)
servno2_rotate=Pin(25,Pin.OUT)
servno2_dir=Pin(33,Pin.OUT)

servno_period=500
hand_period=50

def hand_rotate(hand,degree):
#     print("*****",hand,degree)
    for i in range(50*8*degree):
        for j in (1,0):
            hand.value(j)
            utime.sleep_us(hand_period)
    time.sleep(0.2)

def hand(device,status):
    global hand_status,servno_period
    # 0为关，1为开
    status_map={
        "0":6,
        "1":6,
        "2":0.65,
        }                
    hand_num,hand_dir=(hand_1,hand_1_dir) if device=="hand1" else (hand_2,hand_2_dir)
    if status=="2":
        hand(device,0)
        hand_dir.value(0)
        hand_rotate(status_map[status])
        hand_status[device]=1
        return None
        
    if hand_status[device]!=status:
        if status==0:
            hand_dir.value(1)
        else:
            hand_dir.value(0)
#         print("----",status,type(status))
        hand_rotate(hand_num,status_map[str(status)])
        hand_status[device]=status

def servo_rotate(device,degree):
    servno_rotate= servno1_rotate if device=="servo1" else servno2_rotate
    for i in range(400/90*degree):
        for j in (1,0):
            servno_rotate.value(j)
            utime.sleep_us(servno_period)
    time.sleep(0.1)

def servo(device,degree):
    servno_dir= servno1_dir if device=="servo1" else servno2_dir    
    if degree > 0:
        servno_dir.value(1) #value为1是顺时针
        servo_rotate(device,degree)
    elif degree < 0:
        servno_dir.value(0)
        servo_rotate(device,abs(degree))
    time.sleep(servno_change_waittime)
    servo_status[device]=servo_status[device]+degree
    
def handle_cube(device,num):
    if device in ["hand1","hand2"]:
        hand(device,num)
    else:
        servo(device,num)
        
size_list={
            "size_R":[["hand1", 1]],
            "size_F":[["servo2", 90]],
            "size_L":[["servo2", 90]],
            "size_B":[["servo2", 90]],
            "size_U":[["servo2", -180],["hand1", 0],["hand2", 1],["servo2", -90],["servo1", 90]],
            "size_D":[["servo1", -180]],
            "size_end":[["servo1", 90],["hand2", 0]]
            }

# size_list={
#             "size_R":[],
#             "size_F":[],
#             "size_L":[],
#             "size_B":[],
#             "size_U":[],
#             "size_D":[],
#             "size_end":[]
#             }

def send_msg(msg):
    publish_centent=json.dumps(msg).encode()
    c.publish(b"robot_server",publish_centent)
    
def servo_origi_position():
#     sync_hands_controll(hand_close)
    handle_cube("hand1",0)
    handle_cube("hand2",0)
    tmp_servo=''
    for i in servo_status:
        if servo_status[i]%90==0:
            tmp_servo=i
            break
    hand_open="hand1" if tmp_servo=="servo1" else "hand2"
    handle_cube(hand_open,1)
    handle_cube(tmp_servo,180-servo_status[tmp_servo])
    tmp_servo="servo2" if tmp_servo=="servo1" else "servo1"
    handle_cube(tmp_servo,180-servo_status[tmp_servo])


def robot_exec(msg): # 回调函数，收到服务器消息后会调用这个函数
    global current_result
    keys=list(msg.keys())
    items=list(msg.values())       
    key=keys[0]
    size_keys=size_list.keys()
    if "result" in keys:
        result=msg["result"]
        total=msg["total"]
        current_result=current_result+result
        if total!=len(current_result):
            return({"status":"result_continue"})
        for step in current_result:
            device,num=step
            print(device,num)
            handle_cube(device,num)
            print("servo_status:",servo_status)
        servo_origi_position()
        handle_cube("hand1",0)
        handle_cube("hand2",0)
        handle_cube("hand1",2)
        handle_cube("hand2",2)
        current_result=[]
        print(hand_status)
        return({"status":"finish"})
    elif "init" in keys:
#         sync_hands_controll(hand_close)
        handle_cube("hand1",0)
        handle_cube("hand2",0)
        print(hand_status)
        return({"status":"init"})
    elif key in size_keys:
        for step in size_list[key]:
            device,num=step
            print(device,num)
            handle_cube(device,num)
        print("key:",key)
        return({"status":key})
        
def main():
    ip=wifi.connect()
    reciever_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_addr = (ip, 80)
    reciever_udp.bind(local_addr)
    print("开始运行中...")
    try:
        while True:
            recv_data = reciever_udp.recvfrom(9000)
            msg= json.loads(recv_data[0].decode())
            print("服务器接收数据:",msg)
            buffer=json.dumps(robot_exec(msg)).encode()
            reciever_udp.sendto(buffer, ("10.255.255.105", 9000))
    except Exception as e:
        print(e)
    finally:
        reciever_udp.close()
#         handle_cube("hand1",0)
#         handle_cube("hand2",0)
#         handle_cube("hand1",2)
#         handle_cube("hand2",2)

if __name__=="__main__":
    main()
