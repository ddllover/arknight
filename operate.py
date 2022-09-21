import logging
from os import popen

from aircv import find
from imgcv import click_icon, find_icon,click_random,find_worker
import imgcv as img
import time
import start
import configparser
config=configparser.ConfigParser()
config.read('arknight/config.ini')
logger=logging.getLogger(__name__)
home_png='arknight/picture/home.png'
home2_png='arknight/picture/home2.png'
last_png='arknight/picture/last.png'
#回到首页
def return_home():
    logger.info("返回主界面")
    
    if img.find_icon(home_png):
        img.click_icon(home_png)
        if img.find_icon(home2_png):
            img.click_icon(home2_png)
#签到和公告
def log_in():
    if(img.find_icon(config['operate_log_in']['event_x_png'])):
        logger.info("公告页面")
        img.click_icon(config['operate_log_in']['event_x_png'])
        logger.info("关闭公告页面")
        #一般公告界面会直接转签到界面，而且自动领取 等确认
        img.click_random(wait_time=5)
        while img.find_icon(config['operate_log_in']['sign_png'],sleep_time=5)==None:
            img.click_random(wait_time=3)
    if(img.find_icon(config['operate_log_in']['event_x_png'])):
        logger.info("签到页面")
        img.click_icon(config['operate_log_in']['event_x_png'])
        logger.info("关闭签到页面")


#好友信用
def friend_credit():
    #默认从主界面进入
    logger.info("访问好友基站")
    if img.find_icon(config['operate_friend']['friend_png']):
        img.click_icon(config['operate_friend']['friend_png'])
        if img.find_icon(config['operate_friend']['friends_list_png']):
            img.click_icon(config['operate_friend']['friends_list_png'])
            if img.find_icon(config['operate_friend']['base_visit_png']):
                img.click_icon(config['operate_friend']['base_visit_png'])
                logger.info(f"进入访问界面")
                for i in range(1,11):
                    if img.find_icon(config['operate_friend']['visit_next_png']):
                        img.click_icon(config['operate_friend']['visit_next_png'],3)
                    logger.info(f"访问第{i}家")
    #采购日常用资    
        return_home()

#从头开始购买 不买家具零件
def buy_():
    logger.info("消费信用")
    buy_center=config['operate_credit']['buy_center']
    credit=config['operate_credit']['credit']
    gain=config['operate_credit']['gain']
    if find_icon(buy_center):#进入 购买
        click_icon(buy_center)
        if find_icon(credit):#进入 信用商店
            click_icon(credit)
            if find_icon(gain):#领取 每日信用
                click_icon(gain)
                click_random(x=1,y=1)
                logger.info("领取每日信用")
            creditno_png=config['operate_credit']['creditno_png']
            buy_png=config['operate_credit']['buy_png']
            ini_x=200
            ini_y=400
            distance=400
            for j in range(0,2):#逐个购买
                for i in range(0,5):
                    img.click_random(ini_x+i*distance,ini_y+j*distance,wait_time=3)
                    if img.find_icon(buy_png,wait_time=3):
                        img.click_icon(buy_png)
                        if img.find_icon(creditno_png,wait_time=5):
                            logger.info("信用不足，退出")
                            img.click_random(x=1,y=1)
                            break
                        logger.info(f"购买第{j*5+i}个")
                        click_random()
            return_home()
#日常任务 周常任务
def mission_():
    #找到任务标志
    if img.find_icon(config['operate_mission']['mission_png']):
        img.click_icon(config['operate_mission']['mission_png'])
    
    if img.find_icon(config['operate_mission']['collect_day_png']):
        img.click_icon(config['operate_mission']['collect_day_png'])
        logger.info("收获日常任务")
        if img.find_icon(config['operate_mission']['collect_all_png'],wait_time=3):
            img.click_icon(config['operate_mission']['collect_all_png'])
            img.click_random(wait_time=3)
            while img.find_icon(config['operate_mission']['collect_day_png'],sleep_time=3)==None:
                img.click_random(wait_time=1)
    if img.find_icon(config['operate_mission']['collect_week_png']):
        img.click_icon(config['operate_mission']['collect_week_png'])
        logger.info("收获周常任务")
        if img.find_icon(config['operate_mission']['collect_all_png']):
            img.click_icon(config['operate_mission']['collect_all_png'])
            img.click_random(wait_time=5)

    return_home()
    #click_icon()
#进入上一次作战
def last_play():
    logger.info("进入上一次作战界面")
    if img.find_icon(config['operate_deploy']['combat_png']):
        img.click_icon(config['operate_deploy']['combat_png'])
        if img.find_icon(config['operate_deploy']['last_play_png']):
            img.click_icon(config['operate_deploy']['last_play_png'])


def auto_deploy(num=-1,potion=0,originite=0,last=False):
    if last:
        last_play()
    #理智数量 这个感觉目前没啥必要先放弃
    #先默认为要代理的关卡
    num_count=1
    while num_count<=num or num==-1:
        if img.find_icon(config['operate_deploy']['auto_png']):
            logger.debug("开始代理行动")
            #给start图标加个图库 可以识别任意模式
            if img.find_icon(config['operate_deploy']['start_png'],wait_time=3):
                img.click_icon(config['operate_deploy']['start_png'])
                if img.find_icon(config['operate_deploy']['start2_png']):
                    img.click_icon(config['operate_deploy']['start2_png'])
                    logger.info(f"第{num_count}次战斗")
                    if img.find_icon(config['operate_deploy']['finish_png']):
                        start_time=time.monotonic()

                        while img.find_icon(config['operate_deploy']['finish_png'],threshold_=0.9,sleep_time=10)!=None:
                            logger.info(f"已经{int(time.monotonic()-start_time)}s,战斗还未结束")
                        logger.info(f"第{num_count}次战斗结束")

                        img.click_random(x=1900,y=10,wait_time=5)
                        while img.find_icon(config['operate_deploy']['start_png'],sleep_time=4)==None:#没有发现再次代理图标继续点击结算
                            img.click_random(x=1900,y=10,wait_time=0)
                    else:
                        logger.error("10s内没进入战斗")
                    num_count+=1
                else:
                    #吃药
                    if img.find_icon(config['operate_deploy']['potion_png'],wait_time=3):
                        if potion!=0:
                            potion-=1
                            if img.find_icon(config['operate_deploy']['potion_ok_png']):
                                img.click_icon(config['operate_deploy']['potion_ok_png'],wait_time=3)
                                logger.info(f"吃药，剩余{potion}次")
                        else:
                            if img.find_icon(config['operate_deploy']['potion_x_png']):
                                img.click_icon(config['operate_deploy']['potion_x_png'],wait_time=3)
                            logger.error("理智不足,战斗结束")
                            break
                    if img.find_icon(config['operate_deploy']['originite_png'],wait_time=3):
                        if originite!=0:
                            originite-=1
                            if img.find_icon(config['operate_deploy']['potion_ok_png']):
                                img.click_icon(config['operate_deploy']['potion_ok_png'])
                                logger.info(f"吃源石，剩余{originite}次")
                        else:
                            if img.find_icon(config['operate_deploy']['potion_x_png']):
                                img.click_icon(config['operate_deploy']['potion_x_png'])
                            logger.error("理智不足,战斗结束")
                            break
        else:
            logger.error("可能没有勾选代理")
            img.click_icon(config['operate_deploy']['auto_png'])
    return_home()
    #识别材料并统计

def base_gain_():
    base_png=config['operate_base']['base_png']
    todo_png=config['operate_base']['todo_png']
    png=[config['operate_base']['png_1'],config['operate_base']['png_2'],config['operate_base']['png_3']]
    logger.info("基站收菜")
    if find_icon(base_png):
        click_icon(base_png)
    if find_icon(todo_png):
        click_icon(todo_png)
        for i in range(0,3):
            if find_icon(png[i]):
                click_icon(png[i])
    return_home()  
    
#进入基建  等后续实现一键换班
#利用宿舍休息 只需要两个截图来判定人物在哪并点击
def worker(work,skill=False):
    clear_png=config['operate_change']['clear_png']
    ok_png=config['operate_change']['ok_png']
    skill_png=config['operate_change']['skill_png']
    click_random(x=500,y=1000,wait_time=5)
    if skill:
        if find_icon(skill_png):
            click_icon(skill_png)
    if find_icon(clear_png):
            click_icon(clear_png)
            for i in range(0,3):
                logger.info(f"第{i+1}位干员") 
                find_worker(work[i])
            if find_icon(ok_png):
                click_icon(ok_png)  
def  base_change(make,trade):
    base_png=config['operate_base']['base_png']
    make_png=config['operate_change']['make_png']
    make0=[config['operate_change']['make02'],config['operate_change']['make03'],config['operate_change']['make04']]
    trade_png=config['operate_change']['trade_png']
    trade1=config['operate_change']['trade1']
    if find_icon(base_png):
        click_icon(base_png)
        """
        if find_icon(make_png):#制造站换班
            click_icon(make_png)
            click_random(x=500,y=900)
            logger.info("制造站第1组") 
            worker(make[0],True)   
            for i in range(0,3):
                if find_icon(make0[i]):
                    logger.info(f"制造站第{i+2}组")
                    click_icon(make0[i])
                    worker(make[i+1])   
            #退出到基站
            if find_icon(last_png):
                click_icon(last_png)
            if find_icon(last_png):
                click_icon(last_png)    
        """
        if find_icon(trade_png):#贸易站换班
            click_icon(trade_png)
            click_random(x=500,y=900)
            logger.info("贸易站第1组")
            worker(trade[0])
            if find_icon(trade1):
                click_icon(trade1)
                logger.info("贸易战第2组")
                worker(trade[1])
            #退出到基站
            if find_icon(last_png):
                click_icon(last_png)
            if find_icon(last_png):
                click_icon(last_png) 
def change1():#基站一队
    make=[[config['operate_change']['make11'],config['operate_change']['make12'],config['operate_change']['make13']],
    [config['operate_change']['make21'],config['operate_change']['make22'],config['operate_change']['make23']],
    [config['operate_change']['make31'],config['operate_change']['make32'],config['operate_change']['make33']],
    [config['operate_change']['make41'],config['operate_change']['make42'],config['operate_change']['make43']]]
    trade=[[config['operate_change']['trade11'],config['operate_change']['trade12'],config['operate_change']['trade13']],
    [config['operate_change']['trade21'],config['operate_change']['trade22'],config['operate_change']['trade23']]]
    logger.info("基站一队换班")
    base_change(make,trade)
#进入公招  公招功能

#线索
#1、先扫一遍自己看一下自己的库存量
#2、对每种线索排序，临时天数低的优先，永久的优先级最低
#3、查看接受线索，如果此种线索自己有0~1个临时的，则接取一个天数最低的
#4、置入线索，临时天数低的优先
#5、存在两个临时线索，如果自己拥有永久的线索则送人
if __name__=='__main__':
    start.adb_link()
    auto_deploy(num=-1,potion=3)