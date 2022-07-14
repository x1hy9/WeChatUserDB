# WeChatUserDB
GetWeChat DBPassword&amp;&amp;UserInfo(PC数据库密码以及相关微信用户信息)

```
mac 要安装 brew install sqlcipher 否则无法使用pysqlcipher3库
windows安装pysqlcipher3要自行编译，奈何要下VS故直接调用开源exe
```

# 原理
通过pymem进行内存数据查找，获取基址+偏移量与特征,从而达到微信版本每次更新不需要重新查找地址

![image](https://user-images.githubusercontent.com/67219887/172059989-6f205894-d3cc-4e9d-8ee7-d841433aab4e.png)

# 用例
```
Usage:
    程序参数:  -d <解密的数据库类型>  -k <密钥> -g <获取登录状态微信的私钥> -s <获取登录过机器的用户信息> -c <压缩数据库文件> -i <指定要压缩的文件夹id> -o <压缩文件输出路径> -p <解密windows加密的图片文件>


Options:
  -h, --help            show this help message and exit
  -d DECODE_SQL_TYPE, --decode_sql_type=DECODE_SQL_TYPE
                        输入想解密的数据库类型windows or mac
  -k KEY, --key=KEY     仅windows需要此参数，输入您获取的以base64编码的key
  -g, --get_key         仅windows可用,获取以base64编码的key
  -s, --search_user_info
                        获取运行脚本机器上存留的wx登录信息
  -c COMPRESS, --compress=COMPRESS
                        压缩相关wx数据，可选择 img down db all四种类型
  -i WXID, --wxid=WXID  与压缩参数配合使用
  -o OUT, --out=OUT     与压缩参数配合使用，默认输出为info.zip存储于脚本运行目录
  -p, --ps_img          解密windows加密的图片文件*.dat
```

#### 解密windows数据库
```
python main.py -d windows -k CgszBB+uQfiLA1n3HUqU0vgCFvWKMU5Ltdd9LOfvZlI=

```

![image-20220713215916713](C:\Users\x1hy9\AppData\Roaming\Typora\typora-user-images\image-20220713215916713.png)



#### 解密mac数据库

```
python main.py -d mac
请输入断点调试获取到的key 并使用ctrl+D结束输入
0x6000003624e0: 0x54 0x60 0x97 0x05 0xb5 0x09 0x43 0x9f
0x6000003624e8: 0x94 0xe8 0x38 0x09 0xdc 0x5e 0x79 0x53
0x6000003624f0: 0x4f 0xdc 0xa1 0x66 0x8e 0x96 0x4a 0x98
0x6000003624f8: 0x9a 0x72 0xa6 0x17 0xe0 0x17 0x7c 0x56
```

![image-20220713220751900](C:\Users\x1hy9\AppData\Roaming\Typora\typora-user-images\image-20220713220751900.png)



#### 获取登陆机器信息

```
python main.py -s
```

![image-20220713220718486](C:\Users\x1hy9\AppData\Roaming\Typora\typora-user-images\image-20220713220718486.png)

#### 压缩WX数据

```
 python3 main.py -c db -i wxid_*********522 -o "C:\Users\文件路径\Desktop\info.zip"
```

![image-20220713220637286](C:\Users\x1hy9\AppData\Roaming\Typora\typora-user-images\image-20220713220637286.png)



#### 测试用例

```
测试数据库以放入相应文件夹，下面为作者测试时使用的key
苹果获取key的教程大家可以自行去网上搜索，因苹果权限管控太严无法自动获取key
mac(以下列形式直接粘贴即可)：
0x6000003624e0: 0x54 0x60 0x97 0x05 0xb5 0x09 0x43 0x9f
0x6000003624e8: 0x94 0xe8 0x38 0x09 0xdc 0x5e 0x79 0x53
0x6000003624f0: 0x4f 0xdc 0xa1 0x66 0x8e 0x96 0x4a 0x98
0x6000003624f8: 0x9a 0x72 0xa6 0x17 0xe0 0x17 0x7c 0x56

微信(base64加密)：
CgszBB+uQfiLA1n3HUqU0vgCFvWKMU5Ltdd9LOfvZlI=
```



# 版本

v0.0.1 

目前经测试全版本通杀 （在一些极早版本偏移量不同导致错误，可将微信更新至最新版本）

v1.0.0

新增功能：
1.添加sqlite解密模块（支持mac数据库，windows数据库）
2.添加压缩WX数据文件功能（支持单类型压缩，img，db，down支持双系统）
3.添加win WX图片数据解密功能（将.dat解密为jpg, png, gif）
4.添加获取登录过机器的用户信息功能（支持双系统）


# 后续

~~预计添加sqlite解密模块~~ 已添加！
https://www.52pojie.cn/thread-1084703-1-1.html PC微信逆向分析の绕过加密访问SQLite数据库

预计添加WX app解密功能 (短时间内不会更新 ~~作者要准备秋招~~/(ㄒoㄒ)/~~ 可以自行fork添加功能,求star)
