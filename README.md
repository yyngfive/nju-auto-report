# 每日自动打卡

原作者的`nju-auto-report.py`只是实现了打卡部分，我尝试摸索着实现了登陆的部分。后来在Github上偶然看到[OrangeX4](https://github.com/OrangeX4/daily_health_report)的南大自动打卡代码，流程是类似的，加密部分同样是直接套用原有的JS代码，不过它的功能更加完善，并且具有邮件提醒和使用Github Actions完成的每日自动打卡功能。
虽然轮子已经造好了，但是自己实现以下也是挺有趣的。于是打算把我写的代码拓展一下，添加提醒与自动打卡功能，用来学习Github Actions的使用

---
**原README内容**

---

# nju-auto-report
NJU每日健康打命令

Usage: 
```
python3 nju-auto-report.py [-l location] [-a auth-string] [-s] [-f] [-h]
  -l  --location  Specify the location of report.
  -a  --auth  --auth-string  Set the authentication string for login.
  -s  --scan-only  Scan for reports without submitting automatically.
  -f  --force-rewrite  Submit reports without skipping filled ones.
  -h  --help  Show this help.
```

用法：
```
python3 nju-auto-report-cn.py [-l location] [-a auth-string] [-s] [-f] [-h]
  -l  --location  设定打卡位置
  -a  --auth  --auth-string  设定登录认证串
  -s  --scan-only  只读模式，不会自动打卡
  -f  --force-rewrite  强制打卡，不会略过已经打卡的项目
  -h  --help  显示帮助
```

需要获取“登录认证串”，可通过访问 http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do 获取MOD_AUTH_CAS对应的Cookie值（按 F12 或 Option-Command-I 进入开发者工具，点击Application一栏，查看对应的值）。