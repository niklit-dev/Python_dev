from socket import *
import struct
import numpy as np
from subprocess import Popen, PIPE, call
import json
import time

import datetime

# Size one transaction
PAGE = 256
OKEY = "OK"
START_RES = "resive"


class DebugTool:
    """
    Classs messege.
    """

    def trace(self, *message):
        # messege
        print(*message)


class SilentDebugTool:
    """
    Classs no messege.
    """

    def trace(self, *message):
        pass


class GpuServer_Debug(DebugTool):
    """
    Class for run servers TCP/IP.
    """

    def __init__(self, port, data_exchange):
        self.port = port
        self.data_exchange = data_exchange
        self.ans_data = {}
        self.run_host()

    def __del__(self):
        try:
            self.sockobj.close()
        except BrokenPipeError:
            pass

    def run_host(self):
        """
        Waiting for connection.
        """

        # Run exchange
        self.exchange()

    def exchange(self):
        """
        Exchanging with client.
        :param connect: number client.
        :param data_exchange: instance with data recive and transive.
        """

        # create host
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.bind(('', self.port))
        self.sockobj.listen(5)

        self.connection, address = self.sockobj.accept()

        self.trace('Server connected by: ' + str(address))

        # Send data to program
        self.trancive_data()

        time.sleep(1)
        # close exchange
        self.connection.close()

        while 1:
            try:
                self.connection, address = self.sockobj.accept()
                self.trace('Server connected by: ' + str(address))

                # Recive deta from program
                self.recive_data()
            except Exception as ex:
                print(ex)
                # raise ex
            else:
                break
            pass

        time.sleep(1)
        # close exchange
        self.connection.close()

    def check_send(self):
        """
        Check sending bytes.
        """

        ok = self.connection.recv(3).decode()
        if ok != OKEY:
            raise Exception("socket error")
        self.trace(ok)

    def check_recv(self):
        """
        Check reciving bytes.
        """
        self.trace(OKEY.encode())
        self.connection.send(OKEY.encode())

    def trancive_data_one(self, key, val):
        """
        Sending one packege to program.
        :param key: name packege.
        :param val: data packege.
        :return:
        """

        # Sending key to program
        self.trace("from server", key.encode())
        self.connection.send(str.encode(key))
        self.check_send()
        # Send length data
        try:
            self.trace("len(val) ", len(val))
            length_mas = len(val)
        except TypeError:
            length_mas = 1
        length = struct.pack("i", length_mas * 4)
        self.trace("struct.pack ", length)
        self.connection.send(length)
        self.check_send()
        # Send type
        if isinstance(val, np.ndarray):
            if val.dtype == "int32":
                data = struct.pack("%di" % length_mas, *val)
                self.connection.send('i'.encode())
            elif val.dtype == "float64":
                data = struct.pack("%df" % length_mas, *val)
                self.connection.send('f'.encode())
        else:
            data = struct.pack("i", val)
            self.connection.send('i'.encode())
        self.check_send()
        self.trace("val ", key, " ", data)
        # Send data
        startp = 0
        lpack = length_mas * 4
        while startp < length_mas * 4:
            if lpack > PAGE:
                endp = startp + PAGE
            else:
                endp = startp + lpack
            self.connection.send(data[startp:endp])
            startp += PAGE
            lpack -= PAGE
        self.check_send()

    def recive_data_one(self):
        """
        Reciving one packege from program.
        """

        # Recive name
        name_res = self.connection.recv(PAGE).decode()
        self.check_recv()
        self.trace("name resiv: ", name_res)
        # Recive length
        len_res_b = self.connection.recv(PAGE)
        self.check_recv()
        self.trace("len_res_byte: ", len_res_b)
        len_res = struct.unpack("i", len_res_b)[0]
        self.trace("len_res_byte: ", len_res)
        # Recive type
        type_data = self.connection.recv(PAGE).decode()
        self.trace("type_data: ", type_data)
        self.check_recv()
        # Recive data
        byte_res = b""
        count = 0
        while count < len_res:
            self.connection.settimeout(1.0)
            try:
                byte_res += self.connection.recv(PAGE)
            except timeout:
                self.trace("Time Error")
                pass
            count += PAGE
            self.trace("recive ", count)
        self.check_recv()
        self.trace(struct.unpack("%d%s" % (len_res // 4, type_data), byte_res))
        self.ans_data[name_res] = struct.unpack("%d%s" % (len_res // 4, type_data), byte_res)

    def trancive_data(self):
        """
        Sending dictionary to program.
        """

        # Length dictionary
        len_dict = struct.pack("i", len(self.data_exchange))
        self.connection.send(len_dict)
        self.check_send()
        # Crawling the dictionary
        for key, val in self.data_exchange.items():
            self.trancive_data_one(key, val)

    def recive_data(self):
        """
        Recive dictionari from program.
        """

        # Recive length dictionary
        count_pack_b = self.connection.recv(PAGE)
        self.check_recv()
        self.trace("count_pack_b: ", count_pack_b)
        count_pack = struct.unpack("i", count_pack_b)[0]
        self.trace("count_pack: ", count_pack)
        # Crawling the dictionary
        for _ in range(count_pack):
            self.recive_data_one()


class GpuServer(SilentDebugTool, GpuServer_Debug):
    pass


class GpuServerJson_Debug(GpuServer_Debug):

    def __init__(self, port, data_exchange):

        _data_exchange = GpuServerJson_Debug.converter(data_exchange)
        super(GpuServerJson_Debug, self).__init__(port, _data_exchange)

    @staticmethod
    def converter(diction):
        """
        Function for converting arrays numpy to lists.
        :param diction: dictionary with arrays numpy.
        :return: dictionary with lists.
        """

        for key, val in diction.items():
            if isinstance(val, np.ndarray):
                diction[key] = val.tolist()

        return diction

    def trancive_data(self):
        """
        Sending json to program.
        """

        # Dictionary to Json
        j = json.dumps(self.data_exchange)
        data = j.encode("utf-8")
        # Length Json
        len_str = len(data)
        len_str_b = struct.pack("i", len_str)
        self.connection.send(len_str_b)
        self.check_send()
        # Send data
        startp = 0
        lpack = len_str
        while startp < len_str:
            if lpack > PAGE:
                endp = startp + PAGE
            else:
                endp = startp + lpack
            self.connection.send(data[startp:endp])
            startp += PAGE
            lpack -= PAGE
        self.check_send()

    def recive_data(self):
        """
        Recive dictionari from program.
        """

        # Recive length dictionary
        count_str_b = self.connection.recv(PAGE)
        self.check_recv()
        self.trace("count_pack_b: ", count_str_b)
        count_str = struct.unpack("i", count_str_b)[0]
        self.trace("count_pack: ", count_str)

        # Recive data
        byte_res = b""
        count = 0
        t_err = 0
        while count < count_str:
            self.connection.settimeout(1.0)
            try:
                byte_res += self.connection.recv(PAGE)
            except timeout:
                self.trace("Time Error")
                t_err += 1
                if t_err>10:
                    raise timeout
                # pass
            count += PAGE
            self.trace("recive ", count)
        self.check_recv()
        data_res = byte_res.decode("utf-8")
        self.ans_data = json.loads(data_res)


class GpuServerJson(SilentDebugTool, GpuServerJson_Debug):
    pass

