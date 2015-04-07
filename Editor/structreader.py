'''
#-------------------------------------------------------------------------------
# Name:        structreader.py

# Author:      Vincent
#
# Date Created:     07/12/2014
# Date Modified:    07/12/2014
#-------------------------------------------------------------------------------

Purpose: Used for reading the data files

'''
import struct

def unpack(data,data_type):
    '''
    Purpose: Unpacks data of type 'data_type' from 'data' and strips data of it
    Inputs:
        data:      (bytearray) Packed binary data
        data_type: (str) String specifing type, can be u8,s8,u16,s16,u32,s32, or
                         str
    Output:
        Returns the value of the data
    '''
    if data_type == 'u8':
        return unpackInteger(data,8,False)
    elif data_type == 's8':
        return unpackInteger(data,8,True)
    elif data_type == 'u16':
        return unpackInteger(data,16,False)
    elif data_type == 's16':
        return unpackInteger(data,16,True)
    elif data_type == 'u32':
        return unpackInteger(data,32,False)
    elif data_type == 's32':
        return unpackInteger(data,32,True)
    elif data_type == 'str':
        return unpackString(data)
    elif data_type == 'chr':
        return unpackChar(data)

def pack(data,value,data_type):
    '''
    Purpose: Packs a value as binary data onto the End of a bytearray. The
             data type must match the value passed
    Inputs:
        data:  (bytearray) Bytearray that may or may not already have data
                           packed
        value: (string/int) Value to be packed
        data_type: (str) String specifing type, can be u8,s8,u16,s16,u32,s32, or
                         str
    '''
    if data_type == 'u8':
        packInteger(data,value,8,False)
    elif data_type == 's8':
        packInteger(data,value,8,True)
    elif data_type == 'u16':
        packInteger(data,value,16,False)
    elif data_type == 's16':
        packInteger(data,value,16,True)
    elif data_type == 'u32':
        packInteger(data,value,32,False)
    elif data_type == 's32':
        packInteger(data,value,32,True)
    elif data_type == 'str':
        packString(data,value)
    elif data_type == 'char':
        packChar(data,value)

def unpackInteger(data,size,signed):
    '''
    Purpose: Returns a int of size 'size' from front of packed data. Will strip
             off the int from the data
    Inputs:
        data:   (bytearray) Packed binary data with a u32 type in front
        size:   (int)    Integer size in bits
        signed: (bool)   True if signed, False if unsigned
    Output:
        (int)   The integer
        (bytes) New data with integer stripped off
    '''
    if size == 32:
        fmt = 'I'
    elif size == 16:
        fmt = 'H'
    elif size == 8:
        fmt = 'B'
    else:
        raise ValueError('Size Invalid')
    if signed:
        fmt = fmt.lower()
    b_int = data[:(size//8)]
    for x in range(size//8):
        data.pop(0)
    _int = struct.unpack(fmt,b_int)[0]
    return _int


def unpackString(data):
    '''
    Purpose: Returns a string in the front of packed data. Will strip off the
             string from the rest of the data
    Inputs:
        data:   (bytearray) Packed binary data with a string in front
    Output:
        (str) The unpacked string
    '''
    size = unpackInteger(data,32,False)
    string = ''
    for x in range(size):
        char = struct.unpack('c',bytes( (data[0],) ) )
        string += char[0].decode('ascii')
        data.pop(0)
    return string

def packInteger(data,_int,size,signed):
    '''
    Purpose: Packs an integer as binary data
    Inputs:
        data:   (bytearray) Bytearray that may or may not already have data
                            packed
        _int:   (int)       The integer to be packed
        size:   (int)       Integer size in bits
        signed: (bool)      True if signed, False if unsigned
    '''
    if size == 32:
        fmt = 'I'
    elif size == 16:
        fmt = 'H'
    elif size == 8:
        fmt = 'B'
    else:
        raise ValueError('Size Invalid')
    if signed:
        fmt = fmt.lower()
    p_int = bytearray(struct.pack(fmt,_int))
    for byte in p_int:
        data.append(byte)

def packString(data,string):
    size = len(string)
    p_size = bytearray(struct.pack('I',size))
    chars = list(string)
    for x in p_size:
        data.append(x)
    for char in chars:
        p_char = int.from_bytes(struct.pack('c',char.encode('ascii')),byteorder='big')
        data.append(p_char)

def packChar(data,char):
    char = int.from_bytes(struct.pack('c',char.encode('ascii')),byteorder='big')
    data.append(char)

def unpackChar(data):
    char = struct.unpack('c',bytes( (data[0],) ) )
    data.pop(0)
    return char[0].decode('ascii')
