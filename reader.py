import serial
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle
import os

class eegSmtReader:
    def __init__(self, port_name):
        self.port_name = port_name
        
    def read_data(self, predicat):
        self.cer = serial.Serial(self.port_name, baudrate=57600)
        
        data = b''
        first = True
        while predicat:
            if first:
                t = self.cer.read_all()
                first = False
                continue
            data += self.cer.read_all()
            
            time.sleep(0.05)
            
        data = data[2000:]
        
        
        parse_data = [[] for _ in range(17)]
        
        for ind, data_byte in enumerate(data):
            parse_data[ind % 17].append(data_byte)


        sep_parse_data = [row[:-1] for row in parse_data]
        
        self.sep_parse_data = sep_parse_data
        self.cer.close()
        
        res = np.array(sep_parse_data)
        
        for ind, row in enumerate(res):
            
            if (row[:100] == 165.0).sum() == 100:
                res = np.roll(res, -ind, axis=0)
                break
        
        self.data = res
        
        sub_data = res[[i for i in range(4, 16)]]
        
        res_arr = []
        binary_func = lambda elem: np.binary_repr(elem, width=8)
        for row_first, row_second in zip(sub_data[::2], sub_data[1::2]):
            res_row = [int(binary_func(first) + binary_func(second), 2) for first, second in zip(row_first, row_second)]

            res_arr.append(res_row)
        
        
        np_res_arr = np.array(res_arr)
        
        return np_res_arr[0] + np_res_arr[1]


