import operate as op
import start
import time
import sys
import logging
import logging.handlers
import datetime
f_handler = logging.handlers.TimedRotatingFileHandler('arknight/log/arknight.log', when='midnight', interval=1, backupCount=7,encoding='utf-8', atTime=datetime.time(0, 0, 0, 0))    
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
s_handler=logging.StreamHandler(stream=sys.stdout)
s_handler.setLevel(logging.INFO)
logging.basicConfig(handlers=[f_handler,s_handler],level=logging.DEBUG)
def help(mumu=0,ark=0,log_in=0,auto_deploy=0,friend=0,mission=0,over=0,base_gain=0):
    if mumu:#打开模拟器
        start.start_mumu()
    start.adb_link()
    if ark:#打开明日方舟
        start.start_arknight()
    if log_in:
        #如果出现公告 签到
        op.log_in()
    if auto_deploy:#刷本
        op.auto_deploy(num=-1,potion=0,originite=0,last=0)
    if friend:#访问好友基站
        op.friend_credit()
        #op.buy_()
    if mission:#每日任务 每周任务
        op.mission_()
    if base_gain:#基站收菜
        op.base_gain_()
    if over:#关闭模拟器
        start.over_mumu()

if __name__=="__main__":
    #num=int(input("请自动进入关卡，并输入你要打的关卡次数（打到理智没有请输入-1）:"))
    #print(sys.argv)
    #交互 input()
    #start.start_mumu()
    #start.start_mumu()
    #start.adb_link()
    #op.buy_()
    #op.auto_deploy(num=-1,potion=0,originite=0,last=0)
    #start.over_mumu()
    help(mumu=0,ark=0,log_in=0,auto_deploy=1,friend=1,mission=1,over=0,base_gain=1)
    #help(mumu=1,ark=1,log_in=1,auto_deploy=1,friend=1,mission=0,over=1,base_gain=0)
    #op.buy_()
    #op.change1()

