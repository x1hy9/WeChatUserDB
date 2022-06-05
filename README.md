# WeChatUserDB
GetWeChat DBPassword&amp;&amp;UserInfo(PC数据库密码以及相关微信用户信息)

# 原理
通过pymem进行内存数据查找，获取基址+偏移量与特征,从而达到微信版本每次更新不需要重新查找地址

![image](https://user-images.githubusercontent.com/67219887/172059989-6f205894-d3cc-4e9d-8ee7-d841433aab4e.png)

# 版本

v1.0 

目前经测试全版本通杀


# 后续
预计添加sqlite解密模块
https://www.52pojie.cn/thread-1084703-1-1.html PC微信逆向分析の绕过加密访问SQLite数据库
