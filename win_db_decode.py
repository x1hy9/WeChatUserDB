import base64
import shutil
import os
from subprocess import Popen, PIPE

import connect_sqlite_tools

def win_db(key=""):
    if "WIN_WECHAT_DB" not in os.listdir():
        os.mkdir("WIN_WECHAT_DB")
        os.mkdir("DECRYPT_WIN_WECHAT_DB")
        print("请将数据库文件拖入WIN_WECHAT_DB文件夹下")
        print("解密数据库文件生成于DECRYPT_WIN_WECHAT_DB")
    key = base64.standard_b64decode(key)


    file_paths = []
    for root, directories, files in os.walk('WIN_WECHAT_DB'):
        for filename in files:
            if filename.endswith('.db'):
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

    for file_path in file_paths:
        connect_sqlite_tools.decrypt_sqlite_file(file_path, key)




def mac_db():

    if "MAC_WECHAT_DB" not in os.listdir():
        os.mkdir("MAC_WECHAT_DB")
        os.mkdir("DECRYPT_MAC_WECHAT_DB")
        print("请将数据库文件拖入MAC_WECHAT_DB文件夹下")
        print("解密数据库文件生成于DECRYPT_MAC_WECHAT_DB")

    lines = []
    source = ''''''
    print('''请输入断点调试获取到的key 并使用ctrl+D结束输入''')
    while True:
        try:
            lines.append(input())
        except:
            break
    lines.insert(0, "\n")
    for line in lines:
        source = source + line + "\n"

    key = ''.join(i.partition(':')[2].replace('0x', '').replace(' ', '') for i in source.split('\n')[1:8])
    file_paths = []
    for root, directories, files in os.walk('MAC_WECHAT_DB'):
        for filename in files:
            if filename.endswith('.db'):
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)


    for file_path in file_paths:
        exe_cmd = "%s %s" % (connect_sqlite_tools.get_exe_file(), file_path)
        p2 = Popen(exe_cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        cmd_sql = '''PRAGMA key = "x'%s'";PRAGMA cipher_compatibility = 3; ATTACH DATABASE 'decrypt_%s' AS plaintext KEY ''; SELECT sqlcipher_export('plaintext'); DETACH DATABASE plaintext;''' % (
        key, os.path.basename(file_path))

        code, message = p2.communicate(bytes(cmd_sql, encoding='utf-8'))

        if message != b'':
            print("数据库" + os.path.basename(file_path) + "解密失败！！！")
            os.remove("decrypt_" + os.path.basename(file_path))
            return

        print("数据库" + os.path.basename(file_path) + "解密成功")
        shutil.copyfile("decrypt_" + os.path.basename(file_path),
                        "DECRYPT_MAC_WECHAT_DB/" + "decrypt_" + os.path.basename(file_path))
        os.remove("decrypt_" + os.path.basename(file_path))
