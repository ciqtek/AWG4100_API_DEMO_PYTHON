import sys
from awg4100 import AwgDevice

local_ip = "192.168.1.5"  # 本机 IP

out_ch = 1

# 定义波形代码
wave_code = """
GAmp = 400;
f = 10;
w2 = Sin(f, L=100000);
s1 = SEQ([w2(4, T), w2(2, C)]);
OUT1 = s1;
OUT2 = s1;
OUT3 = s1;
OUT4 = s1;
"""

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

rtn, msg = dev.system_init()
check_ret(rtn, "System Reset failed.")

# 2. 参数配置
rtn, msg = dev.channel_mode(0)      # 选择独立模式
check_ret(rtn, "set mode failed: {}".format(msg))

rtn, msg = dev.awg_cast_mode(0)     # 播放模式，连续
check_ret(rtn, "set awg cast mode failed: {}".format(msg))

rtn, msg = dev.awg_offset(out_ch, "10")  # 通道1，AWG 空闲偏置
check_ret(rtn, "set offset failed: {}".format(msg))

rtn, msg = dev.marker_switch(out_ch, 1)  # 通道1，Marker 打开
check_ret(rtn, "set marker failed: {}".format(msg))

rtn, msg = dev.clock_mode(0)        # 内部时钟
check_ret(rtn, "set clock failed: {}".format(msg))

# 3. 下载波形
result = dev.load_wave_data(out_ch, wave_code) # 通道1
if result == 0:
    print("wave download failed: {}".format(result))
    sys.exit()

# 4. 设置播放次数
rtn, info = dev.awg_cast_number(0)   
check_ret(rtn, "set awg cast number failed: {}".format(info))

# 4. 播放控制
rtn, info = dev.awg_broadcast(out_ch, 1)   # 播放通道1
check_ret(rtn, "start failed: {}".format(info))

input("enter any to stop")

# 5. 停止播放
rtn, info = dev.awg_broadcast(out_ch, 0)
check_ret(rtn, "stop failed: {}".format(info))

# 6. 关闭设备
result = dev.close_device()
if not result:
    sys.exit()
