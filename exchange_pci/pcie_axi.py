import struct as st
import client_serv_pci_e as pci


class exchPCIeTrace(pci.drivPCIeTrace):
    """
    Exchanging integer data whith PCIe.
    """

    def __init__(self, deviseRD, deviseWR, deviseCTRL, BAR_AXI = 1048576):
        super().__init__(self, deviseRD, deviseWR, deviseCTRL, BAR_AXI)

    def CMD_W(self, addr, data):
        """
        Write unsigned integer word to FPGA.
        :param addr: addres in bytes
        :param data: unsigned integer data
        :return: number write bytes
        """

        data2bit = st.pack("<i", data)
        return self.axi4l_w(addr, data2bit)

    def CMD_R(self, addr):
        """
        Read unsigned integer word from FPGA.
        :param addr: addres in bytes
        :return: data in unsigned integer format
        """

        data = self.axi4l_r(addr)
        return st.unpack("<i", data)[0]

    def DMA_W(self, addr, data, format = "q"):
        """
        Write array data in DMA mode to FPGA.
        :param addr: addres in bytes
        :param data: array data
        :param format: format data (integer, long long integer, ...)
        :return: number write bytes
        """

        data2bit = pci.num2bit(data, num = format)
        # return self.axi4_w(self, addr, data2bit)
        return self.axi4_w(addr, data2bit)

    def DMA_R(self, addr, len, format = "q"):
        """
        Read array data in DMA mode from FPGA.
        :param addr: addres in bytes
        :param len: len in bytes
        :param format: format data (integer, long long integer, ...)
        :return: array data
        """

        data = self.axi4_r(addr, len)
        return pci.bit2num(data, num = format)

class exchPCIe(pci.SilentPCIeTool, exchPCIeTrace):
    def __init__(self, deviseRD, deviseWR, deviseCTRL, BAR_AXI = 1048576):
        super().__init__(self, deviseRD, deviseWR, deviseCTRL, BAR_AXI)

class exchPCIeRemote(pci.fpga_client):
    pass


if __name__ == "__main__":

    # file read data from PCIe
    deviseRD = "/dev/xdma/card0/c2h0"
    # file write data from PCIe
    deviseWR = "/dev/xdma/card0/h2c0"
    # file exchange data for AXI4_Lite
    deviseCTRL = "/dev/xdma0_user"

    # dev = drivPCIeTrace(deviseRD, deviseWR, deviseCTRL)

    dev = exchPCIeTrace(deviseRD, deviseWR, deviseCTRL)
    dev.CMD_W(0, 10)
    a = dev.CMD_R(0)
    print(a)
    b = dev.DMA_W(0, [1,2,3,4,5,6, 2**62-1], format = "Q")
    print(b)
    c = dev.DMA_R(0, 56)
    print(c)
    b = dev.DMA_W(0, list(range(1024)), format = "Q")
    print(b)
    c = dev.DMA_R(0, 5000)
    print(c)
