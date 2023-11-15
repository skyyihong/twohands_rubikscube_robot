import network, time


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('wifi', 'xxxxxx')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    ifconfig = wlan.ifconfig()
    print('network config:', ifconfig)
    return ifconfig[0]
