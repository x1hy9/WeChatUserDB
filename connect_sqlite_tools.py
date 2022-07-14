"""
#### 加密
sqlcipher-shell64.exe client.db
ATTACH DATABASE 'encrypted.db' AS encrypted KEY 'thisiskey';
SELECT sqlcipher_export('encrypted');
.quit

#### 解密
PRAGMA key = 'thisiskey';
ATTACH DATABASE 'plaintext.db' AS plaintext;
SELECT sqlcipher_export('plaintext');
DETACH DATABASE plaintext;
"""
import binascii
import hashlib
import os
import shutil
import sys
from subprocess import Popen, PIPE




def get_exe_file():
    exe_file =  os.getcwd()+"\\windows_sqlite_tools\\sqlcipher-shell64.exe"
    return exe_file


def encryption_sqlite_file(db_file="", secret_key=""):
    """
    :param db_file: 将要加密的原始文件
    :param secret_key: 连接数据库文件的密钥
    :return:
    """
    if not db_file:
        raise ValueError("db_File is not defined！")
    if not secret_key:
        secret_key = "encrypted"
    exe_cmd = "%s %s" % (get_exe_file(), db_file)
    p1 = Popen(exe_cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    cmd_sql = "ATTACH DATABASE 'encrypted.db' AS encrypted KEY '%s'; SELECT sqlcipher_export('encrypted');" % secret_key
    code, message = p1.communicate(bytes(cmd_sql, encoding='utf-8'))
    message = message.decode("gbk")
    if int(p1.poll()) == 0:
        return "success", p1.poll(), code, message
    else:
        return "fail", p1.poll(), code, message


def decrypt_sqlite_file(db_file="", secret_key=""):
    """
    :param db_file:  将要解密的数据库文件
    :param secret_key: 连接数据库的密钥 (要与加密的密钥一致)
    :return:
    """
    if not db_file:
        raise ValueError("db_File is not defined！")

    if not secret_key:
        raise ValueError("secret_key is not defined！")
    salt = open(db_file, 'rb').read(16)
    dk = hashlib.pbkdf2_hmac('sha1', secret_key, salt, 64000, dklen=32)
    exe_cmd = "%s %s" % (get_exe_file(), db_file)
    p2 = Popen(exe_cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    cmd_sql = '''PRAGMA key = "x'%s'";PRAGMA cipher_page_size=4096; ATTACH DATABASE 'decrypt_%s' AS plaintext KEY ''; SELECT sqlcipher_export('plaintext'); DETACH DATABASE plaintext;''' % (binascii.hexlify(dk).decode(),os.path.basename(db_file))

    code, message = p2.communicate(bytes(cmd_sql, encoding='utf-8'))


    if message!=b'':
        print("数据库" + os.path.basename(db_file) + "解密失败！！！")
        os.remove("decrypt_" + os.path.basename(db_file))
        return

    print("数据库" + os.path.basename(db_file) + "解密成功")
    message = message.decode("gbk")
    shutil.copyfile("decrypt_" + os.path.basename(db_file),
                    "DECRYPT_WIN_WECHAT_DB/" + "decrypt_" + os.path.basename(db_file))
    os.remove("decrypt_" + os.path.basename(db_file))
    if int(p2.poll()) == 0:
        return "success", p2.poll(), code, message
    else:
        return "fail", p2.poll(), code, message
