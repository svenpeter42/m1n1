# SPDX-License-Identifier: MIT
from construct import *

from ...utils import *
from ..asc import StandardASC
from ..afk.epic import *

class DCPAVControllerService(EPICStandardService):
    NAME = "dcpav-controller-epic"
    SHORT = "dcpav"

    def setPower(self, power):
        self.call(8, 0x8, struct.pack("<16xI12x", power))

    def getPower(self, power):
        return struct.unpack("<16xI12x", self.call(8, 0x9, bytes(32)))

    def wakeDisplay(self):
        self.call(8, 0xa, bytes(16))

    def sleepDisplay(self):
        self.call(8, 0xb, bytes(16))

    def forceHotPlugDetect(self):
        self.call(8, 0xc, bytes(16))

    def setVirtualDeviceMode(self, mode):
        self.call(8, 0xd, struct.pack("<16xI12x", mode))

class DCPDPControllerService(EPICStandardService):
    NAME = "dcpdp-controller-epic"
    SHORT = "dcpdp"

class DCPDPTXEndpoint(EPICEndpoint):
    SHORT = "dptx"

    SERVICES = [
        DCPAVControllerService,
        DCPDPControllerService,
    ]

class DCPDPTXRemotePortTarget(Register32):
    CORE = 3, 0
    ATC = 7, 4
    DIE = 11, 8
    CONNECTED = 15, 15

class DCPDPTXRemotePortService(EPICStandardService):
    NAME = "dcpdptx-port-epic"
    SHORT = "port"

    def displayRequest(self):
        self.call(8, 8, bytes(16))

    def displayRelease(self):
        self.call(8, 9, bytes(16))

    def hotPlugDetectChangeOccurred(self, unk=True):
        self.call(8, 10, struct.pack("<16x?15x", unk), sync=False)

    def setPower(self):
        self.call(0, 8, bytes(16))

    def connectTo(self, core, atc, die, connected, unk=0x100):
        target = DCPDPTXRemotePortTarget(CORE=core, ATC=atc, DIE=die, CONNECTED=connected)
        self.call(0, 13, struct.pack("<II24x", unk, target.value))

    def validateConnection(self, core, atc, die, connected, unk=0x100)
        target = DCPDPTXRemotePortTarget(CORE=core, ATC=atc, DIE=die, CONNECTED=connected)
        self.call(0, 14, struct.pack("<II40x", unk, target.value))


class DCPDPTXPortEndpoint(EPICEndpoint):
    SHORT = "dptxport"

    SERVICES = [
        DCPDPTXRemotePortService,
    ]

class DCPDPDevice(EPICStandardService):
    NAME = "dcpav-device-epic"
    SHORT = "dpdev"

class DCPAVDeviceEndpoint(EPICEndpoint):
    SHORT = "avdev"

    SERVICES = [
        DCPDPDevice,
    ]

class DCPDPService(EPICStandardService):
    NAME = "dcpav-service-epic"
    SHORT = "dpserv"

class DCPAVServiceEndpoint(EPICEndpoint):
    SHORT = "avserv"

    SERVICES = [
        DCPDPService,
    ]

class DCPAVSimpleVideoInterface(EPICStandardService):
    NAME = "dcpav-video-interface-epic"
    SHORT = "video"

class DCPAVVideoEndpoint(EPICEndpoint):
    SHORT = "avserv"

    SERVICES = [
        DCPAVSimpleVideoInterface,
    ]
