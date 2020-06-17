import sys
from awg4100 import AwgDevice

local_ip = "192.168.1.5"  # 本机 IP

group_mode = True
channel_enable = [True, False, True, False]

DDS_params = {
    1: {'rate':'150', 'phase':'0', 'range':'200', 'offset':'0'}, # 通道1 [频率, 相位, 振幅, 偏置]
    2: {'rate':'100', 'phase':'0', 'range':'150', 'offset':'0'},
    3: {'rate':'200', 'phase':'0', 'range':'200', 'offset':'0'},
    4: {'rate':'300', 'phase':'0', 'range':'150', 'offset':'50'},
}

dev = AwgDevice()

result = dev.init_network(local_ip)
if result == 0:
    print("Init network failed.")
    sys.exit()

dev_info = dev.find_device()
dev_num = len(dev_info)
if dev_num == 0:
    print("Cannot found device")
    sys.exit()

for idx in range(dev_num):
    print("[{}] IP={}, MAC={}, Name={}".format(idx, \
        dev_info[idx][0], dev_info[idx][1], dev_info[idx][2]))

trgt = int(input("choice: "))

ip = dev_info[trgt][0]
mac = dev_info[trgt][1]

# 1. 连接设备
result = dev.connect(ip, mac)
if result != 1:
    print("Connect failed.")
    sys.exit()

def check_ret(rtn, msg=None):
    if rtn == 0:
        print(msg)
        sys.exit()

# 2. 参数配置
if group_mode:
    rtn, msg = dev.channel_mode(1)      # 组合模式
    for ch in range(4):
        if channel_enable[ch]:
            dev.channel_switch(ch+5, 1)
        else:
            dev.channel_switch(ch+5, 0)
else:
    rtn, msg = dev.channel_mode(0)      # 独立模式
check_ret(rtn, "set channel mode failed: {}".format(msg))

for ch in range(1, 5):
    if channel_enable[ch-1]:
        try:
            rtn, msg = dev.rate_control(ch, DDS_params[ch]['rate'])
            check_ret(rtn, "channel {} set DDS rate failed: {}".format(ch, msg))

            rtn, msg = dev.range_control(ch, DDS_params[ch]['range'])
            check_ret(rtn, "channel {} set DDS range failed: {}".format(ch, msg))

            rtn, msg = dev.phase_control(ch, DDS_params[ch]['phase'])
            check_ret(rtn, "channel {} set DDS phase failed: {}".format(ch, msg))

            rtn, msg = dev.offset_control(ch, DDS_params[ch]['offset'])
            check_ret(rtn, "channel {} set DDS offset failed: {}".format(ch, msg))
        except KeyError as e:
            print(e)
                                                               
# 4. 播放控制
if group_mode:
    rtn, msg = dev.awg_broadcast(5, 1)
    check_ret(rtn, "start failed: {}".format(msg))
else:
    for ch in range(1, 5):
        if channel_enable[ch-1]:
            rtn, msg = dev.DDS_cast(ch, 1)
            check_ret(rtn, "start channel {} failed: {}".format(ch, msg))

input("enter any to stop")

# 5. 停止播放
if group_mode:
    rtn, msg = dev.awg_broadcast(5, 0)
    check_ret(rtn, "stop failed: {}".format(msg))
else:
    for ch in range(1, 5):
        if channel_enable[ch-1]:
            rtn, msg = dev.DDS_cast(ch, 0)
            check_ret(rtn, "stop channel {} failed: {}".format(ch, msg))

# 6. 保存参数
filename = "D:\\awg_params-1.txt"
rtn, msg = dev.save_params(filename)
check_ret(rtn, "save param: {}".format(msg))
rtn, msg = dev.load_params(filename)
check_ret(rtn, "load param: {}".format(msg))
rtn, msg = dev.save_params("D:\\awg_params-2.txt")
check_ret(rtn, "save param: {}".format(msg))

# 7. 关闭设备
result = dev.close_device()
if not result:
    sys.exit()