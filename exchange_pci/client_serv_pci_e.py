from socket import *
import struct as st
import pickle
import os, sys
import mmap


PAGE = 1024

# dict_com = {"AXI":"AXIL", "MOD":"W", "Addr":0, "Len":0}

class PCIeTool:
    """
    Classs messege.
    """

    def trace(self, message):
        # messege
        print(message)

class SilentPCIeTool:
    """
    Classs no messege.
    """

    def trace(self, message):
        pass

class drivPCIeTrace(PCIeTool):
    """
    Exchanging to pcie.
    """

    def __init__(self, deviseRD, deviseWR, deviseCTRL, BAR_AXI = 1048576):
        # max size BAR for AXI Lite
        self.BAR_AXI = BAR_AXI
        # driver path
        self.deviseRD   = deviseRD
        self.deviseWR   = deviseWR
        self.deviseCTRL = deviseCTRL
        # connect driver
        self.status_driver = self.open_driv()
        self.trace("error driver: %d" % self.status_driver)

    def open_driv(self):
        """
        Open files driver.
        """

        try:
            # Open system files on write AXI4
            self.fw = os.open(self.deviseWR, os.O_WRONLY | os.O_NONBLOCK)
            # Open system files on read AXI4
            self.fr = os.open(self.deviseRD, os.O_RDONLY | os.O_NONBLOCK)
            # Open system files on read/write AXI Lite
            self.faxi = os.open(self.deviseCTRL, os.O_RDWR | os.O_SYNC)
            # Allocate memory
            self.mm = mmap.mmap(self.faxi, self.BAR_AXI, offset=0)
        except FileNotFoundError:
            self.trace("Not found driver!")
            return 2
        else:
            self.trace("Driver OK")
            return 0

    def axi4l_w(self, addr, data):
        """
        Write 4 bytes to PCIe via mmap.
        :param addr: address in bytes
        :param data: data (4 bytes)
        :return: 4 (bytes)
        """

        self.mm[addr: addr + 4] = data
        self.trace("send to AXIL")
        return 4

    def axi4l_r(self, addr):
        """
        Read 4 bytes from PCIe via mmap.
        :param addr: address in bytes
        :return: data (4 bytes)
        """

        self.trace("resive from AXIL")
        return self.mm[addr: addr + 4]

    def axi4_w(self, addr, data):
        """
        Write array bytes to PCIe.
        :param addr: address in bytes
        :param data: array data (in bytes)
        :param len: lenght bytes
        :return: number of recorded words
        """
        # Shift address writting data
        os.lseek(self.fw, addr, os.SEEK_SET)
        self.trace("send to AXI4")
        # Writting data
        return os.write(self.fw, data)

    def axi4_r(self, addr, len):
        """
        Read array bytes from PCIe.
        :param addr: address in bytes
        :param len: lenght bytes
        :return: array data (in bytes)
        """
        # Shift address reading data
        os.lseek(self.fr, addr, os.SEEK_SET)
        self.trace("resive from AXI4")
        # Reading data
        return os.read(self.fr, len)

    def __del__(self):
        """
        Function closed driver.
        """

        # close mm
        try:
            self.mm.close()
            self.trace("clear mmap")
        except AttributeError as err:
            print(str(err))
        # close file write
        try:
            os.close(self.fw)
            self.trace("closed " + self.deviseWR)
        except NameError as err:
            print(str(err))
        except AttributeError as err:
            print(str(err))
        # close file read
        try:
            os.close(self.fr)
            self.trace("closed " + self.deviseRD)
        except NameError as err:
            print(str(err))
        except AttributeError as err:
            print(str(err))
        # close file ctrl
        try:
            os.close(self.faxi)
            self.trace("closed " + self.deviseCTRL)
        except NameError as err:
            print(str(err))
        except AttributeError as err:
            print(str(err))

class drivPCIe(SilentPCIeTool, drivPCIeTrace):
    pass

class fpga_server(drivPCIeTrace):
    def __init__(self, port, deviseRD, deviseWR, deviseCTRL):
        super().__init__(deviseRD, deviseWR, deviseCTRL)
        self.port = port
        # run host
        self.run_host()

    def __del__(self):
        try:
            self.sockobj.close()
        except BrokenPipeError:
            pass


    def run_host(self):
        """
        Waiting for connection
        :return:
        """
        # create host
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.bind(('', self.port))
        self.sockobj.listen(5)


        # Run server
        while True:
            # wait connection
            self.connection, address = self.sockobj.accept()

            self.trace('Server connected by: '+ str(address))
            # Run exchange
            self.exchange(self.connection)
            # close exchange
            self.connection.close()

    def exchange(self, connect):
        """
        Exchanging with client
        :param connect: number client
        :return:
        """
        sst = False
        while True:
            # Recive data
            recive = connect.recv(PAGE)
            # load dict from socket
            if recive.decode() == "MOD":
                connect.send(b"MOD resiv")
                rec = connect.recv(PAGE)
                option = pickle.loads(rec)
                self.AXI  = option["AXI"]
                self.Mod  = option["MOD"]
                self.Addr = option["Addr"]
                self.Len  = option["Len"]
                # ansver MOD
                connect.send(b"MOD OK")
            elif recive.decode() == "CLOSE":
                self.trace("Connect close")
                connect.close()
                break
            elif recive.decode() == "DRV":
                connect.send(st.pack("<i", self.status_driver))
                # State driver
                sst = True
            else:
                connect.send(b"MOD False")
                self.trace("MOD False!")
                break
            if not sst:
                # load data from socket
                # Load data if MOD: "W" and AXI: "AXIL"
                if self.Mod == "W" and self.AXI == "AXIL":
                    self.Data = connect.recv(4)
                    # ansver data
                    connect.send(b"Data OK")
                # Load data if MOD: "W" and AXI: "AXI4"
                elif self.Mod == "W" and self.AXI == "AXI4":
                    count = 0
                    self.Data = b""
                    while count < self.Len:
                        connect.settimeout(1.0)
                        try:
                            self.Data += connect.recv(PAGE)
                        except timeout:
                            pass
                        count += PAGE
                    connect.settimeout(None)
                    # ansver data
                    self.trace("Data OK!")
                    connect.send(b"Data OK")
                # if not sst:
                # run action exchange
                ans = self.action()
                # sending ansver
                connect.send(ans)
            # State driver
            sst = False


    def action(self):
        """
        Perfome action
        :return:
        """
        # write to AXI Lite
        if self.AXI == "AXIL" and self.Mod == "W":
            return st.pack("<i", self.axi4l_w(self.Addr, self.Data))
        # read from AXI Lite
        elif self.AXI == "AXIL" and self.Mod == "R":
            return self.axi4l_r(self.Addr)
        # write to AXI4
        elif self.AXI == "AXI4" and self.Mod == "W":
            # self.trace(self.Addr)
            # self.trace(self.Data)
            return st.pack("<i", self.axi4_w(self.Addr, self.Data))
        # read from AXI4
        elif self.AXI == "AXI4" and self.Mod == "R":
            return self.axi4_r(self.Addr, self.Len)

class fpga_client(PCIeTool):
    """
    Class device data trickery
    """
    def __init__(self, serverHost, serverPort):
        self.host = serverHost
        self.port = serverPort
        self.status_driver = 1
        self.conServ()
        self.open_driv()

    def conServ(self):
        # Create socket
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.settimeout(300)
        try:
            # Connect socket to server
            self.sockobj.connect((self.host, self.port))
        except ConnectionRefusedError:
            self.trace("Connecting faild")
            self.status_driver = 1

    def __del__(self):
        try:
            self.sockobj.send(b"CLOSE")
            self.sockobj.close()
        except BrokenPipeError:
            pass

    def open_driv(self):
        """
        Request driver status.
        """
        # sending DRV
        try:
            self.sockobj.send(b"DRV")
            # if server ready, send dictionary
            self.status_driver = st.unpack("<i", self.sockobj.recv(4))[0]
            self.trace(("Driver status: ",self.status_driver))
        except BrokenPipeError:
            pass

    def axi4l_w(self, addr = 0, data = b"0"):
        """
        Function writing data to AXI Lite
        :param addr: Address write
        :param data: Data write
        :return: number bytes
        """
        # dictionari MOD
        dict_mod = {"AXI": "AXIL", "MOD": "W", "Addr": addr, "Len": 0}
        pack_mod = pickle.dumps(dict_mod)
        # sending MOD
        self.sockobj.send(b"MOD")
        # if server ready, send dictionary
        if self.sockobj.recv(PAGE).decode() == "MOD resiv":
            self.sockobj.send(pack_mod)
            self.trace(("Send: ",dict_mod))
        # control MOD
        if self.sockobj.recv(PAGE).decode() == "MOD OK":
            # sending data
            self.sockobj.send(data)
            self.trace(("Send: ", data))
        # control Data
        if self.sockobj.recv(PAGE).decode() == "Data OK":
            # resiving count bayts
            countBytes = self.sockobj.recv(4)
            if countBytes == b'':
                return  0
            else:
                return st.unpack("<i", countBytes)

    def axi4l_r(self, addr = 0):
        """
        Function reading data from AXI Lite
        :param addr: Address reading
        :return: Data reading
        """
        # dictionari MOD
        dict_mod = {"AXI": "AXIL", "MOD": "R", "Addr": addr, "Len": 0}
        pack_mod = pickle.dumps(dict_mod)
        # sending MOD
        self.sockobj.send(b"MOD")
        # if server ready, send dictionary
        if self.sockobj.recv(PAGE).decode() == "MOD resiv":
            self.sockobj.send(pack_mod)
            self.trace(("Send: ",dict_mod))
        # control MOD
        if self.sockobj.recv(PAGE).decode() == "MOD OK":
            # wait resiving data
            return self.sockobj.recv(4)

    def axi4_w(self, addr = 0, data = b'0'):
        """
        Function writing data to AXI4
        :param addr: Address write
        :param len: lenght data in bytes
        :param data: Data write
        :return: number bytes
        """
        length = len(data)
        # dictionari MOD
        dict_mod = {"AXI": "AXI4", "MOD": "W", "Addr": addr, "Len": length}
        pack_mod = pickle.dumps(dict_mod)
        # sending MOD
        self.sockobj.send(b"MOD")
        # if server ready, send dictionary
        if self.sockobj.recv(PAGE).decode() == "MOD resiv":
            self.sockobj.send(pack_mod)
            self.trace(("Send: ",dict_mod))
        # control MOD
        if self.sockobj.recv(PAGE).decode() == "MOD OK":
            # sending data
            data_pack = data
            count = 0
            Ndata = length//PAGE
            # sumCount = length-Ndata*PAGE
            while count<length:
                if length - count > PAGE:
                    sumCount = PAGE
                else:
                    sumCount = length - Ndata * PAGE
                # length = length-count
                self.sockobj.send(data_pack[count: count+sumCount])
                count += PAGE
            self.trace(("Send: ", data))
        if self.sockobj.recv(128).decode() == "Data OK":
            # resiving count bayts
            countBytes = self.sockobj.recv(4)
            return st.unpack("<i", countBytes)[0]

    def axi4_r(self, addr = 0, len = 0):
        """
        Function writing data to AXI4
        :param addr: Address write
        :param len: lenght data in bytes
        :param data: Data write
        :return: number bytes
        """
        # dictionari MOD
        dict_mod = {"AXI": "AXI4", "MOD": "R", "Addr": addr, "Len": len}
        pack_mod = pickle.dumps(dict_mod)
        # sending MOD
        self.sockobj.send(b"MOD")
        # if server ready, send dictionary
        if self.sockobj.recv(PAGE).decode() == "MOD resiv":
            self.sockobj.send(pack_mod)
            self.trace(("Send: ", dict_mod))
        # control MOD
        if self.sockobj.recv(PAGE).decode() == "MOD OK":
            data = b""
            count = 0
            # while the received data is less than the Len
            while count < len:
                data += self.sockobj.recv(PAGE)
                count += PAGE
            # wait resiving data
            return data



if __name__ == "__main__":

    # system files exchange data
    deviseRD = "/dev/xdma0_c2h_0"
    # file write data from PCIe
    deviseWR = "/dev/xdma0_h2c_0"
    # file exchange data for AXI4_Lite
    deviseCTRL = "/dev/xdma0_user"
    # Server port
    portServer = 50007
    # Server host
    portHost = "127.0.0.1"

    lenArgv = len(sys.argv)
    # sys.argv[1] == "server"

    if lenArgv > 1 and sys.argv[1] == "server":
        fpga_server(portServer, deviseRD, deviseWR, deviseCTRL)
    else:
        client = fpga_client(portHost, portServer)

        print(client.axi4l_w(addr=0, data=b'\n\x00\x00\x00'))
        print(client.axi4l_r(addr=0))

        print(client.axi4_w(addr=0, data=st.pack("<1024q", *list(range(1024)))))
        print("--------------")
        print(client.axi4_r(addr=0, len=1024*8))



