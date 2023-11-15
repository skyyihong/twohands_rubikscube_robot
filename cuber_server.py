# python 3.6
import json
from snap import snap_full_pic
from cube_solve import cube_step
from socket import *

# 1. 创建udp套接字

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(("0.0.0.0", 9000))
dest_addr = ('10.255.255.143', 80)


def udp_handle(buffer):
    buffer = json.dumps(buffer).encode()
    udp_socket.sendto(buffer, dest_addr)
    print("sended:", buffer)
    recv_raw = udp_socket.recvfrom(9000)
    recv_data = json.loads(recv_raw[0].decode())
    status_txt = recv_data.get("status")
    return status_txt


def run():
    # 3. 从键盘获取数据
    send_list = [
        {"init": 0},
        {"size_R": 0},
        {"size_F": 0},
        {"size_L": 0},
        {"size_B": 0},
        {"size_U": 0},
        {"size_D": 0},
        {"size_end": 0}
    ]
    size_key = ["size_R", "size_F", "size_L", "size_B", "size_U", "size_D"]

    for send_content in send_list:
        status_txt = udp_handle(send_content)
        if status_txt in size_key:
            snap_full_pic(status_txt)
            print(status_txt)
    if status_txt == "size_end":
        # return
        ret = cube_step()
        result_total = len(ret["result"])
        result_start = {"result": ret["result"][:result_total // 2], "total": result_total}
        result = udp_handle(result_start)
        result_end = {"result": ret["result"][result_total // 2:], "total": result_total}
        result = udp_handle(result_end)
        print("result:", result)


if __name__ == '__main__':
    run()
