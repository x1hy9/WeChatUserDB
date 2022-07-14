import getpass
import re
import os

def check_os():
    os_name = os.name
    if os_name == "nt":
        # windows
        os_name = "windows"
    if os_name == "posix":
        # mac
        os_name = "linux"
    return os_name


def get_wxid_list(os_name):
    #mac下wxid的路径，一台机器可能存在多个微信用户登录过
    if os_name == "linux":
        wxid_list = []
        user_name = getpass.getuser()
        file_path = "/Users/" + user_name + "/library/containers/com.tencent.xinWECHAT/data/library/application " \
                                            "support/com.tencent.xinWeChat/2.0b4.0.9/"
        files_list = os.listdir(file_path)
        for file_name in files_list:
            if len(file_name) == 32:
                wxid_list.append(file_name)
        return file_path,wxid_list

    #windows下wxid路径
    if os_name == "windows":
        import win32api
        import win32con

        reg_root = win32con.HKEY_USERS
        reg_path = ""

        key = win32api.RegOpenKey(reg_root, reg_path, 0)
        for item in win32api.RegEnumKeyEx(key):
            if len(item[0]) > 20 and "Classes" not in item[0]:
               # print(item[0])
                sub_reg_path = item[0] + "\\SOFTWARE\\Tencent\\WeChat"
                #print(sub_reg_path)
                try:
                    key = win32api.RegOpenKeyEx(reg_root, sub_reg_path, 0)
                    #print(key)
                except Exception as e:
                    continue
        try:
            value, key_type = win32api.RegQueryValueEx(key, 'FileSavePath')
        except Exception as e:
            value, key_type = win32api.RegQueryValueEx(key, 'InstallPath')
            value = value + "\\locales\\WeChat Files\\"
        #print(value)
        # 文件保存路径
        if value == "MyDocument:":
            # print("The default location of the file has not been changed")
            username = getpass.getuser()
            file_path = "C:\\Users\\" + username + "\\Documents\\WeChat Files\\"
            #print(file_path)
        else:
            file_path = value

        # 获取用户文件
        try:
            wxid_list = os.listdir(file_path)
            #去除干扰文件夹
            wxid_list.remove("All Users")
            wxid_list.remove("Applet")
        except:
            print("\nfailed to find the path by the script")
            print("Please enter the path of your [WeChat Files]")
            print("You can find the path in your WeChat's setting")
            print("It looks like [x:\\\\xxx\\xxx\\WeChat Files]")
            file_path = input("The path : ") + "\\"
            wxid_list = os.listdir(file_path)
            wxid_list.remove("All Users")
            wxid_list.remove("Applet")
        return file_path,wxid_list


def check_wxid_version(raw_info):
    global wxid_version
    if "wxid_" in raw_info:
        wxid_version = "new_wxid"
    else:
        wxid_version = "old_wxid"

def get_info(file_path,wxidc,os_name):

    if os_name == "windows":
        file = file_path + wxidc + "\\config\\AccInfo.dat"
        try:
            file_size = os.path.getsize(file)
        except:
            print(wxidc+"为失效文件夹")
            print()
            return
    if os_name == "linux":

        file = file_path + wxidc + r"/account/userinfo.data"
        try:
            file_size = os.path.getsize(file)
        except:
            print(wxidc+"为失效文件夹")
            print()
            return
    if file_size == 0:
        return
    print("=================基本信息=================")
    print("用于压缩文件参数id：" + wxidc)
    with open(file, mode="r", encoding="ISO-8859-1") as f:
        # 处理raw数据
        raw_info = f.read()
        # 获取原始wxid的版本
        check_wxid_version(raw_info)
        if os_name == "windows":
            if wxid_version == "new_wxid":
                raw_info = raw_info[raw_info.find("wxid"):]
            if wxid_version == "old_wxid":
                raw_info = raw_info
        if os_name == "linux":
            c_p_c = raw_info[:raw_info.find(":")]
            raw_info = raw_info[raw_info.find("wxid"):]
        info = ""
        for char in raw_info:
            if "\\" not in ascii(char):
                info = info + str(char)
            else:
                info = info + "`"
        info_2 = list(set(info.split("`")))
        info_2.sort(key=info.index)
        info = info_2
        info_list = []
        for x in info:
            if len(x) > 1:
                info_list.append(x)
        info = info_list
        if wxid_version == "old_wxid":
            for x in info:
                an = re.search("[a-zA-Z0-9_]+", x)
                if len(x) >= 6 and len(an.group(0)) >= 6:
                    d_list = r"!@#$%^&*()+={}|:\"<>?[]\;',./`~'"
                    flag_id = 0
                    for i in x:
                        if i in d_list:
                            wxid = x.replace(i, "")
                            flag_id = 1
                    if flag_id == 0:
                        wxid = an.group(0)
                    break
            info = info[info.index(x):]
            info[0] = wxid

    if info != []:
        # 获取微信id
        try:
            wxid = info[0]
            print("The wxid : " + wxid)
        except:
            pass

        # 获取微信号
        # 微信号长度限制为6-20位, 且只能以字母开头
        try:
            for misc in info:
                if 6 <= len(misc) <= 20 and misc[0].isalpha() is True:
                    wx = misc
            print("The wechat : " + wx)
            info.remove(wx)
        except:
            print("The wechat : " + wxid)


        # 获取手机号
        for misc in info:
            p_numbers = r"[\+0-9]+"
            p = re.compile(p_numbers)
            numbers = re.search(p, misc)
            try:
                if "+" in numbers.group(0) and len(numbers.group(0) >= 6):
                    number = numbers.group(0)
                else:
                    p_numbers = r"0?(13|14|15|17|18|19)[0-9]{9}"
                    p = re.compile(p_numbers)
                    numbers = re.search(p, misc)
                    number = numbers.group(0)
            except:
                continue
            if "*" in number:
                number = number.replace("*", "")
            print("The phone : " + number)
            try:
                info.remove(number)
            except:
                info.remove(number + "*")
            break

        #获取文件传输记录
        if os_name=="windows":
                down_path = file_path + wxidc + "\\FileStorage\\File"
                down_path_list = os.listdir(down_path)[:len(os.listdir(down_path)) - 1]
                for down_doc in down_path_list:
                    print("=================" + down_doc + "=================")
                    for down_info in os.listdir(down_path + "\\" + down_doc):
                        print(down_info)
                    print("===========================================")
                    print()
                    print()

                print("以下目录为2022.06后存储位置改变的文件列表")
                print()
                new_path = file_path + wxid + "\\FileStorage\\MsgAttach\\"

                for root, dirs, files in os.walk(new_path):
                    # 遍历输出目录路径

                    for name in dirs:
                        if name in "File":
                            for time_file in os.listdir(root + "\\" + name):
                                print("================" + time_file + "====================")
                                for file_name in os.listdir(root + "\\" + name + "\\" + time_file):
                                    print(file_name)
                                print("===========================================")
                                print()
                                print()
        if os_name=="linux":
                for parent,dirnames,filenames in os.walk(file_path+wxidc+"/Message/MessageTemp/"):
                    for dirname in dirnames:

                        if dirname in "OpenData":

                            print("=================文件列表=================")
                            print( os.path.basename(parent) )
                            print("文件夹下存在的文件：")
                            for file_name in os.listdir(parent+"/OpenData"):
                                print(file_name)
                            print("=================文件列表=================")
                            print()
                            print()



if __name__ == '__main__':
    os_name=check_os()
    file_path,wxid_list=get_wxid_list(os_name)
    print("此机器共有" + str(len(wxid_list)) + "个账号登录过")
    for wxid in wxid_list:
       get_info(file_path,wxid,os_name)