import os
from optparse import OptionParser


import compress
import decode_img
import get_info
import mac_db_decode
import search_user_info
import win_db_decode

if __name__ == '__main__':
    usage = '''
    程序参数:  -d <解密的数据库类型>  -k <密钥> -g <获取登录状态微信的私钥> -s <获取登录过机器的用户信息> -c <压缩数据库文件> -i <指定要压缩的文件夹id> -o <压缩文件输出路径> -p <解密windows加密的图片文件>
    '''
    parser = OptionParser(usage)

    parser.add_option("-d", "--decode_sql_type", dest="decode_sql_type", help="输入想解密的数据库类型windows or mac")
    parser.add_option("-k", "--key", dest="key", help="仅windows需要此参数，输入您获取的以base64编码的key")
    parser.add_option("-g", "--get_key",action='store_true', dest="get_key", help="仅windows可用,获取以base64编码的key")
    parser.add_option("-s", "--search_user_info", action='store_true',dest="search_user_info", help="获取运行脚本机器上存留的wx登录信息")
    parser.add_option("-c", "--compress", dest="compress", help="压缩相关wx数据，可选择 img down db all四种类型")
    parser.add_option("-i", "--wxid", dest="wxid", help="与压缩参数配合使用")
    parser.add_option("-o", "--out",default="info.zip", dest="out", help="与压缩参数配合使用，默认输出为info.zip存储于脚本运行目录")
    parser.add_option("-p", "--ps_img", action='store_true', dest="ps_img", help="解密windows加密的图片文件*.dat")
    (options, args) = parser.parse_args()

    os_name=search_user_info.check_os()
    if options.decode_sql_type=="windows"and options.key and os_name=="windows":
        win_db_decode.win_db(options.key)
    if options.decode_sql_type=="windows"and options.key and os_name=="linux":
        mac_db_decode.win_db(options.key)
    if options.decode_sql_type=="mac"and os_name=="windows":
        win_db_decode.mac_db()
    if options.decode_sql_type=="mac"and os_name=="linux":
        mac_db_decode.mac_db()
    if options.get_key:
        get_info.get_key()
    if options.search_user_info:
        os_name = search_user_info.check_os()
        file_path, wxid_list = search_user_info.get_wxid_list(os_name)
        print("此机器共有" + str(len(wxid_list)) + "个账号登录过")
        for wxid in wxid_list:
            search_user_info.get_info(file_path, wxid,os_name)
    if options.compress:

        file_path, wxid_list = search_user_info.get_wxid_list(os_name)
        if options.compress=="db":compress.file_zip(os_name, file_path, wxid=options.wxid, out=options.out, is_db="true")
        if options.compress == "down": compress.file_zip(os_name, file_path, wxid=options.wxid, out=options.out,is_down="true")
        if options.compress == "img": compress.file_zip(os_name, file_path, wxid=options.wxid, out=options.out,is_image="true")
        if options.compress == "all": compress.file_zip(os_name, file_path, wxid=options.wxid, out=options.out,is_all="true")
    if options.ps_img:
        decode_img.deimg()


