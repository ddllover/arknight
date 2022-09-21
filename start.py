#明日方舟自动每日
from imgcv import find_icon
from imgcv import click_icon 
import subprocess as su
import time
import configparser
import logging

logger = logging.getLogger(__name__)


config=configparser.ConfigParser()
config.read('arknight/config.ini')
config=config['start']

#打开模拟器
def start_mumu():
    shell_result=su.run(config['mumu_path'],shell=True)
    if shell_result.returncode==0:
        logger.info("成功打开模拟器")
    time.sleep(30)

def over_mumu():
    logger.info("关闭模拟器")
    shell_reult=su.run("taskkill /f /im NemuPlayer.exe")

#打开明日方舟
def adb_link():
    #adb连接
    logger.info("adb连接")
    start_time=time.monotonic()
    shell_result=su.run(config['adb_path']+" connect 127.0.0.1:7555",capture_output=True,shell=True)
    while shell_result.stdout.decode('utf-8').find('unable')!=-1:
        logger.info("adb没有连接上，尝试重复连接")
        shell_result=su.run(config['adb_path']+" connect 127.0.0.1:7555",capture_output=True,shell=True)
        if time.monotonic()-start_time>60:
            raise logger.error("adb连接失败退出")
    logger.info(shell_result.stdout)

def start_arknight():
    logger.info("打开明日方舟")
    start_time=time.monotonic()
    shell_result=su.run(config['adb_path']+' shell am start -n com.hypergryph.arknights/com.u8.sdk.U8UnityContext',capture_output=True,shell=True)
    while shell_result.returncode!=0:
        logger.debug("再次尝试打开")
        shell_result=su.run(config['adb_path']+' shell am start -n com.hypergryph.arknights/com.u8.sdk.U8UnityContext',capture_output=True,shell=True)
        if time.monotonic()-start_time>60:
            raise ValueError("无法打开")
    logger.info("成功打开明日方舟")
    #进入游戏界面
    #skip页面
    if find_icon(config['skip_png'],wait_time=30):
        click_icon(config['skip_png'])
    #账户管理
        if find_icon(config['account_manage_png'],30):
            click_icon(config['account_manage_png'])
    #账号登陆
            if find_icon(config['account_login_png'],30):
                click_icon(config['account_login_png'])
    #输入密码
                if find_icon(config['password_png'],30):
                    click_icon(config['password_png'])
                    time.sleep(1)
                    shell_result=su.run(config['adb_path']+' shell input text '+config['password'],capture_output=True,shell=True)
    #登录
                    if find_icon(config['login_png'],30):
                        click_icon(config['login_png'])
                        if find_icon(config['login_png'],30):
                            click_icon(config['login_png'])
    time.sleep(10)
    

if __name__=="__main__":
    #logger.basicConfig(filename='arknight.log',filemode='w',format='%(asctime)s - %(levelname)s - %(message)s',encoding='utf-8',level=logging.DEBUG)
    
    start_mumu()
    adb_link()
    start_arknight()



