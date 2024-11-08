import time
import roslibpy
from abb.bridge import ABBGoFa
from sensor.ForceSensor import LoacellSensor
# from kuka.bridge import KUKAVarProxy

# KUKA_REMOTE_HOST = '192.168.2.3' 

if __name__ == '__main__':

    # ros client
    client = roslibpy.Ros(host= "127.0.0.1", port=9090)
    client.run()

    # sensors
    sensor1 = LoacellSensor("ForceSensor1", client, serial_port='COM5', baudrate=57600)
    # sensor2 = LoacellSensor("ForceSensor2", client, serial_port='COM4', baudrate=57600)

    # robots
    abb = ABBGoFa("GoFa1", client, auto_home = True)
    # kr210 = KUKAVarProxy("KR210", KUKA_REMOTE_HOST, auto_home = False)
    
    try:
        while True:
            time.sleep(2)
            # print ("listening for trajectories ...")
    except KeyboardInterrupt:
        sensor1.cleanup()
        # sensor2.cleanup()
        abb.cleanup()
        # kr210.cleanup()
