#mac 要安装 brew install sqlcipher
import base64
import shutil
import binascii
import hashlib


import os
def mac_db():
    from pysqlcipher3 import dbapi2 as sqlite
    if "MAC_WECHAT_DB" not in os.listdir():
        os.mkdir("MAC_WECHAT_DB")
        os.mkdir("DECRYPT_MAC_WECHAT_DB")
        print("请将数据库文件拖入MAC_WECHAT_DB文件夹下")
        print("解密数据库文件生成于DECRYPT_MAC_WECHAT_DB")
        return

    lines = []
    source=''''''
    print('''请输入断点调试获取到的key 并使用ctrl+D结束输入''')
    while True:
        try:
            lines.append(input())
        except:
            break
    lines.insert(0,"\n")
    for line in lines:
        source=source+line+"\n"

    key = ''.join(i.partition(':')[2].replace('0x', '').replace(' ', '') for i in source.split('\n')[1:8])
    file_paths = []
    for root, directories, files in os.walk('MAC_WECHAT_DB'):
        for filename in files:
            if filename.endswith('.db'):
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

    key = "x'" + key + "'"
    #
    count=0
    for file_path in file_paths:
       try:
           conn = sqlite.connect(file_path)
           c = conn.cursor()
           c.execute("PRAGMA key = \"" + key + "\";")
           c.execute("PRAGMA cipher_compatibility = 3")
           # c.execute("PRAGMA cipher_use_hmac = OFF;")

           c.execute(
               "ATTACH DATABASE '" + "decrypt_" + os.path.basename(file_path) + "' AS db_" + str(count) + " KEY '';")
           c.execute("SELECT sqlcipher_export('db_" + str(count) + "')")
           c.execute("DETACH DATABASE db_" + str(count) + ";")
           conn.close()
           count = count + 1


           shutil.copyfile("decrypt_" + os.path.basename(file_path),"DECRYPT_MAC_WECHAT_DB/"+"decrypt_" + os.path.basename(file_path))
           os.remove("decrypt_" + os.path.basename(file_path))
           print("数据库" + os.path.basename(file_path) + "解密成功")
       except:
           print("数据库" + os.path.basename(file_path) + "解密失败！！！")
           os.remove("decrypt_" + os.path.basename(file_path))
           continue

def win_db(key=""):
    from pysqlcipher3 import dbapi2 as sqlite
    if "WIN_WECHAT_DB" not in os.listdir():
        os.mkdir("WIN_WECHAT_DB")
        os.mkdir("DECRYPT_WIN_WECHAT_DB")
        print("请将数据库文件拖入WIN_WECHAT_DB文件夹下")
        print("解密数据库文件生成于DECRYPT_WIN_WECHAT_DB")

    file_paths = []
    for root, directories, files in os.walk('WIN_WECHAT_DB'):
        for filename in files:
            if filename.endswith('.db'):
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

    key=base64.standard_b64decode(key)


    count = 0
    for file_path in file_paths:
        try:

            salt = open(file_path, 'rb').read(16)

            dk = hashlib.pbkdf2_hmac('sha1', key, salt, 64000, dklen=32)


            conn = sqlite.connect(file_path)
            c = conn.cursor()

            c.execute('''PRAGMA key="x'%s'";''' % binascii.hexlify(dk).decode())
            c.execute("PRAGMA cipher_page_size=4096;")
            c.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1")
            c.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1")
            c.execute("ATTACH DATABASE '" + "decrypt_" + os.path.basename(file_path) + "' AS db_"+str(count)+" KEY '';")
            c.execute("SELECT sqlcipher_export('db_"+str(count)+"')")
            c.execute("DETACH DATABASE db_"+str(count)+";")
            conn.close()
            count=count+1

            shutil.copyfile("decrypt_" + os.path.basename(file_path),
                            "DECRYPT_WIN_WECHAT_DB/" + "decrypt_" + os.path.basename(file_path))
            os.remove("decrypt_" + os.path.basename(file_path))
            print("数据库" + os.path.basename(file_path) + "解密成功")
        except:
            print("数据库" + os.path.basename(file_path) + "解密失败！！！")
            os.remove("decrypt_" + os.path.basename(file_path))
            continue

