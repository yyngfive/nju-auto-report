# 每日自动打卡

原作者的`nju-auto-report.py`只是实现了打卡部分，我尝试摸索着实现了登陆的部分，并简化了打卡的部分。后来在Github上偶然看到[OrangeX4](https://github.com/OrangeX4/daily_health_report)的南大自动打卡代码，流程是类似的，加密部分同样是直接套用原有的JS代码，不过它的功能更加完善，并且具有邮件提醒和使用Github Actions完成的每日自动打卡功能。

虽然轮子已经造好了，但是自己实现一下也是挺有趣的。于是打算把我写的代码拓展一下，添加提醒与自动打卡功能，用来学习Github Actions的使用。

## 我新增的部分
### 公开的仓库，秘密的变量
打卡过程中会涉及到填写统一身份认证的密码，这里利用Github Secrets来设置环境变量，即使仓库是公开的，也能在很大程度上保证密码不泄露。
### 邮件服务
为了更加方便地使用邮件提醒功能，我在Vercel上部署了自己的邮件推送服务，详见[mail-bot](https://github.com/yyngfive/mail-bot)

现在只需要在Github Secrets中设置接收信息的邮箱地址环境变量即可，省去了输入密码的操作。

## 使用指南
### 用法
1. fork这个仓库
2. 设置环境变量，包括`USERNAME`，`PASSWORD`，`LOCATION`，`MAIL`
3. 等待收到邮件通知（当天可能无法打卡）

## 备注
### 如何设置Github Secrets
点击settings->secrets->new repository secret

按照表格中的对应内容，分四次添加环境变量：

|name|value|
|----|-----|
|USERNAME|你的学号|
|PASSWORD|统一身份认证密码|
|LOCATION|填报地址|
|MAIL|用来接收信息的邮箱|

### 一些小问题
1. Github Actions在实际运行过程中可能会出现超时的问题，导致打卡失败。不过如果这时邮件服务运行正常，会向你推送邮件提醒，可以手动打卡。之后可能会尝试一些解决方法，不过这并不会造成很大的影响，一般重新运行Actions就可以解决。
2. Github Actions中定时任务设置的时间是格林尼治时间，北京在东八区。我在配置文件中设定的时间是6点30分，实际打卡时间是北京时间14点30分。不过这并不影响使用。
3. 如果你一整天都没有收到邮件，请查看垃圾邮件。如果垃圾邮件中也没有，那么可能是我的邮件服务崩了或者阿里云的邮件推送服务把邮件当作垃圾邮件处理了。还有极小的可能是邮件服务免费额度用光了。

## 免责声明
本项目旨在以每日健康打卡为例学习Python爬虫的相关知识，请如实填报打卡信息，使用本项目产生的一切后果由实际使用者承担。


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
