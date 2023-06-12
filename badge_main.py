import bluetooth
import random
import struct
import time
from ble_advertising import advertising_payload

import sensor, image, math
from pyb import LED

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_TEMP_CHAR = (
    bluetooth.UUID(0x2A6E),
    _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,
)
_ENV_SENSE_SERVICE = (
    _ENV_SENSE_UUID,
    (_TEMP_CHAR,),
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

### Set up April Tag detection ###
red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
#sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.set_vflip(True)
sensor.skip_frames(time = 2000)
#sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
#sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

tag_families = 0
#tag_families |= image.TAG16H5 # comment out to disable this family
#tag_families |= image.TAG25H7 # comment out to disable this family
#tag_families |= image.TAG25H9 # comment out to disable this family
#tag_families |= image.TAG36H10 # comment out to disable this family
tag_families |= image.TAG36H11 # comment out to disable this family (default family)
#tag_families |= image.ARTOOLKIT # comment out to disable this family

def family_name(tag):
    #if(tag.family() == image.TAG16H5):
    #    return "TAG16H5"
    #if(tag.family() == image.TAG25H7):
    #    return "TAG25H7"
    #if(tag.family() == image.TAG25H9):
    #    return "TAG25H9"
    #if(tag.family() == image.TAG36H10):
    #    return "TAG36H10"
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"
    #if(tag.family() == image.ARTOOLKIT):
    #    return "ARTOOLKIT"


class BLE:
    #Maually set each badge number
    def __init__(self, ble, name="NICLA_BADGE_#0"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID], appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER
        )
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def set_data(self, x):
        self._ble.gatts_write(self._handle, struct.pack("<h", int(x)))

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

def to_binary(lst):
    num = 0
    for b in lst:
        num = 2 * num + b
    return num

def demo():
    ble = bluetooth.BLE()
    temp = BLE(ble)

    result = 0

    while True:
        clock.tick()
        img = sensor.snapshot()
        tags = img.find_apriltags(families=tag_families) # defaults to TAG36H11 without "families".

        red_led.off()
        green_led.off()
        blue_led.off()
        if len(tags) == 0:
            red_led.on()
        elif len(tags) == 1:
            green_led.on()
        elif len(tags) > 1:
            blue_led.on()

        write_list = [0,0,0]

        i = 0
        for tag in tags:
            tag_id = tag.id()
            if tag_id < 4:
                write_list[tag_id-1] = 1
            i += 1

            img.draw_rectangle(tag.rect(), color = (255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color = (255, 0, 0))
            #print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi, tag.z_translation())
            #print("Tag Family %s, Tag ID %d, rotation %f (degrees), Tag z-translation %f" % print_args)
        #print(clock.fps())
        print(write_list)


        result = to_binary(write_list)
        print(result)
        print()
        temp.set_data(result)

        time.sleep_ms(50)


if __name__ == "__main__":
    demo()
