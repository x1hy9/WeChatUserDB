#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@ Author: x1hy9
@ Camping is fun :)
@ Time:  6/05/2022
@ FileName: main.py
"""
import struct
import sys
from time import sleep

import pymem
from pymem.pattern import scan_pattern_page
import binascii


# getCBytes 获得C语言格式的密码
def getCBytes(password) -> str:
    password=password[2:]
    result = ""
    for i in range(0, len(password)-1, 2):
        result += "0x" + password[i:i + 2] + ", "

    return """
        unsigned char pass[] = {%s};
    """ % (result)
def pattern_scan_all(handle, pattern, *, return_multiple=False):
    next_region = 0

    found = []
    user_space_limit = 0x7FFFFFFF0000 if sys.maxsize > 2**32 else 0x7fff0000
    while next_region < user_space_limit:
        next_region, page_found = scan_pattern_page(
            handle,
            next_region,
            pattern,
            return_multiple=return_multiple
        )

        if not return_multiple and page_found:
            return page_found

        if page_found:
            found += page_found

    if not return_multiple:
        return None

    return found

# getuserinfo
def getuserinfo(p) -> (int, str):
    # The address of the wechatwin.dll loaded by this process
    base_address = pymem.process.module_from_name(p.process_handle, "wechatwin.dll").lpBaseOfDll
    wechat_addr=base_address
    bytes_path = b'-----BEGIN PUBLIC KEY-----\n...'

    #Find a string and re Find addr
    base_address=pattern_scan_all(p.process_handle, bytes_path, return_multiple=True)

    #通过字符串的地址反向寻找地址
    for i in base_address :
        #base_address = base_address[len(base_address) - 1]
        bytes_path1 = (i).to_bytes(4, byteorder="little", signed=True)
        cc = pattern_scan_all(p.process_handle, bytes_path1, return_multiple=True)
        if cc[0]>wechat_addr:
            base_address=cc[0]
            break

    #Get_UserName
    int_username_len = p.read_int(base_address - 0x5c)
    username = p.read_bytes(base_address - 0x6c, int_username_len)

    #Get_Wxid
    int_wxid_len = p.read_int(base_address - 0x44)
    wxid_addr = p.read_int(base_address - 0x54)
    wxid = p.read_bytes(wxid_addr, int_wxid_len)

    #Get_MobilePhoneModels
    int_mobileModel_len=p.read_int(base_address - 0xC)
    mobileModel=p.read_bytes(base_address - 0x1c,int_mobileModel_len)





    #Get_Tel
    int_Tel_len=p.read_int(base_address - 0x47c)
    Tel = p.read_bytes(base_address - 0x48c,int_Tel_len)

    #Get_SqliteKey
    int_SqliteKey_len = p.read_int(base_address - 0x8c)
    SqliteKey = p.read_bytes(base_address - 0x90, int_SqliteKey_len)
    cc=p.read_bytes(p.read_int(base_address-0x90),int_SqliteKey_len)
    cc_str=str(cc)
    cc_str=cc_str[2:len(cc_str)-1]








    #Get_Public_Key
    int_PublicKey_len = p.read_int(base_address + 0x10)
    PublicKey = p.read_bytes(p.read_int(base_address),int_PublicKey_len)
    PublicKey =  PublicKey.decode()
    PublicKey =  PublicKey.replace("\n", "")


    # Get_Private_Key
    int_PrivateKey_len = p.read_int(base_address + 0x28)
    add=p.read_int(base_address+0x18)
    PrivateKey = p.read_bytes(add,int_PrivateKey_len)
    PrivateKey=PrivateKey.decode()
    PrivateKey=PrivateKey.replace("\n","")


    print(f"""
            WeChatWin.Dll的基地址为: {base_address}
            用户微信名称为：{username.decode()}
            用户微信ID为：{wxid.decode()}
            用户手机号为：{Tel.decode()}
            用户公钥为：{PublicKey}
            用户私钥为：{PrivateKey}
            解密ChatMsg.db的C语言格式密码: {getCBytes(str(binascii.b2a_hex(cc)))}
                Enjoy Python!  
                    By: x1hy9
            
        """)



if __name__ == '__main__':
    p = pymem.Pymem()
    p.open_process_from_name("WeChat.exe")
    getuserinfo(p)

