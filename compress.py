import getpass
import re
import os
import zipfile



def file_zip(os_name,path,wxid,out,is_image=None,is_down=None,is_db=None,is_all=None):
    if os_name=='windows':
        dir_list=[]
        if is_all is not None:
            is_db="true"
            is_down="true"
            is_image="true"
        if is_down is not None:
            dir_list.append(path+wxid+"\\FileStorage\File")
            dir_list.append(path + wxid + "\\FileStorage\MsgAttach")

        if is_image is not None:
            dir_list.append(path+wxid+"\\FileStorage\Image")
        if is_db is not None:
            dir_list.append(path+wxid+"\\Msg\Multi")


        startdir = path + wxid + "\\FileStorage\File"  # 要压缩的文件夹路径
        file_news = out  # 压缩后文件夹的名字
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名




        for startdir in dir_list:
            # 打包路径优化
            ck_zip="下载存储\\"
            if "Image" in startdir:
                ck_zip="图片存储\\"
            if "Multil" in startdir:
                ck_zip="数据存储\\"


            if "Multil" in startdir:
                z.write(startdir + "\\MSG0.db",'MSG0.db')
                print("wx数据库压缩成功")
                continue
            for dirpath, dirnames, filenames in os.walk(startdir):
                fpath = dirpath.replace(startdir, '')
                fpath = fpath and fpath + os.sep or ''

                for filename in filenames:

                    z.write(os.path.join(dirpath, filename), ck_zip+os.path.join(fpath, filename))
                    print(filename+'压缩成功')
        z.close()
    if os_name=='linux':
        dir_list = []

        if is_all is not None:
            #dir_list.append(path+wxid+"/Message/MessageTemp")
            dir_list.append(path + wxid + "/Session")
            dir_list.append(path + wxid + "/RevokeMsg")
            dir_list.append(path + wxid + "/MMLive")
            dir_list.append(path + wxid + "/Group")
            dir_list.append(path + wxid + "/FileStateSync")
            dir_list.append(path + wxid + "/Contact")
            dir_list.append(path + wxid + "/Message")

        if is_down is not None:
           dir_list.append(path+wxid+"/Message/MessageTemp")
        if is_image is not None:
            dir_list.append(path+wxid+"/Message/MessageTemp")
        if is_db is not None:
            dir_list.append(path + wxid + "/Session")
            dir_list.append(path + wxid + "/RevokeMsg")
            dir_list.append(path + wxid + "/MMLive")
            dir_list.append(path + wxid + "/Group")
            dir_list.append(path + wxid + "/FileStateSync")
            dir_list.append(path + wxid + "/Contact")
            dir_list.append(path + wxid + "/Message")

        #print(dir_list)

        file_news = out  # 压缩后文件夹的名字
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名

        for startdir in dir_list:

            # 打包路径优化
            ck_zip="下载存储/"
            if "Image" in startdir:
                ck_zip="图片存储/"
            if "Multil" in startdir:
                ck_zip="数据存储/"


            for dirpath, dirnames, filenames in os.walk(startdir):

                fpath = dirpath.replace(startdir, '')
                fpath = fpath and fpath + os.sep or ''



                for filename in filenames:

                    if is_all is not None:
                        for dirname in dirnames:

                            if dirname in "OpenData":

                                for file_name in os.listdir(dirpath + "/OpenData"):
                                    #print(dirpath+"/"+dirname+"/"+file_name)
                                    if os.path.isfile(dirpath+"/"+dirname+"/"+file_name):
                                        #print(dirpath+"/"+dirname+"/"+file_name)
                                        z.write((dirpath+"/"+dirname+"/"+file_name),
                                                ck_zip + os.path.join(fpath, file_name))
                                        print(file_name + '压缩成功')
                        if os.path.splitext(filename)[-1] == ".db" or os.path.splitext(filename)[-1] == ".jpg" :
                            z.write(os.path.join(dirpath, filename), ck_zip + os.path.join(fpath, filename))
                            print(filename + '压缩成功')

                    if is_db is not None:
                        if os.path.splitext(filename)[-1] == ".db":
                            z.write(os.path.join(dirpath, filename), ck_zip + os.path.join(fpath, filename))
                            print(filename + '压缩成功')
                        else:
                            continue

                    if is_image is not None:
                        if os.path.splitext(filename)[-1] == ".jpg":
                            z.write(os.path.join(dirpath, filename), ck_zip + os.path.join(fpath, filename))
                            print(filename + '压缩成功')
                        else:
                            continue


                    if is_down is not None:
                        for dirname in dirnames:

                            if dirname in "OpenData":

                                for file_name in os.listdir(dirpath + "/OpenData"):
                                    # print(dirpath+"/"+dirname+"/"+file_name)
                                    if os.path.isfile(dirpath + "/" + dirname + "/" + file_name):
                                        z.write((dirpath + "/" + dirname + "/" + file_name),
                                                ck_zip + os.path.join(fpath, file_name))
                                        print(file_name + '压缩成功')

        z.close()






