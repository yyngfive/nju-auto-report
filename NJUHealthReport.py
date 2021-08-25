import requests
from bs4 import BeautifulSoup
import execjs
import json
import time
import os

auth_url = 'https://authserver.nju.edu.cn/authserver/login'
service_url = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do'
url = auth_url+'?service='+service_url
encrypt_url = 'https://authserver.nju.edu.cn/authserver/custom/js/encrypt.js'
submit_url = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do'

username = os.environ['USERNAME']
password = os.environ['PASSWORD']
location = os.environ['LOCATION']

headers = {
        'User=Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

def _etd2(encrypt_url,password,pwdDefaultEncryptSalt):
    res = requests.get(encrypt_url)
    res.encoding = 'utf-8'
    js = res.text
    ctx = execjs.compile(js)
    return ctx.call('encryptAES',password,pwdDefaultEncryptSalt)

def getTicket(url,encrypt_url,username,password):
    session = requests.Session()
    res = session.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'lxml').find('form',id='casLoginForm')
    lt = soup.find('input',{'name':'lt'})['value']
    dllt = 'userNamePasswordLogin'
    execution = soup.find('input',{'name':'execution'})['value']
    _eventId = 'submit'
    rmShown = '1'
    pwdDefaultEncryptSalt = soup.find('input',{'id':'pwdDefaultEncryptSalt'})['value']
    password = _etd2(encrypt_url,password,pwdDefaultEncryptSalt)
    payload = {'username':username,
               'password':password,
               'lt':lt,
               'dllt':dllt,
               'execution':execution,
               '_eventId':_eventId,
               'rmShown':rmShown}
    res = session.post(url,data = payload,headers = headers,allow_redirects=False)
    ticket_url = res.headers['Location']
    ticket = ticket_url[ticket_url.find('=')+1:]
    return (ticket_url,ticket)

def getModAuthCas(ticket_url):
    session = requests.Session()
    res = session.get(ticket_url,headers=headers,allow_redirects=False)
    cookies = res.cookies
    cookie = requests.utils.dict_from_cookiejar(cookies)
    return cookie['MOD_AUTH_CAS']

# 这部分思路来自原作者
def report(service_url,submit_url,mod_auth_cas,location):
    request_cookie = {'MOD_AUTH_CAS':mod_auth_cas}
    res = requests.get(service_url,cookies=request_cookie,headers=headers)
    data = json.loads(res.text)  
    today = data['data'][0]
    wid = today['WID']
    curr_location = location
    is_twzc = 1
    is_has_jkqk = 1
    jrskmys = 1
    jzrjrskmys = 1
    payload = {
        'WID':wid,
        'CURR_LOCATION':curr_location,
        'IS_TWZC':is_twzc,
        'IS_HAS_JKQK':is_has_jkqk,
        'JRSKMYS':jrskmys,
        'JZRJRSKMYS':jzrjrskmys
    }
    res = requests.get(submit_url,cookies=request_cookie,params=payload)
    info = json.loads(res.text)
    if info['msg'] != '成功':
        raise Exception('Submission FAILED')
if __name__ == '__main__':
    print(username)
    try:
        ticket = getTicket(url,encrypt_url,username,password)
    except:
        raise Exception('Login FAILED!') 
    try:
        mod_auth_cas = getModAuthCas(ticket[0])
    except:
        raise Exception('Authorization FAILED!')
    try:
        report(service_url,submit_url,mod_auth_cas,location)
    except:
        raise Exception('Report FAILED!')
    print(time.asctime(time.localtime())+':Report your health information successfully!' )