import logging
import aircv  
import subprocess as su
import time
adb_path="\"C:/Program Files/MuMu/emulator/nemu/vmonitor/bin/adb.exe\""
#png_path="‪C:\\Users\\wangyan\\Desktop\\vscode\\arknight\\picture"
screen_png='arknight/picture/screen.png'
logger=logging.getLogger(__name__)
#找图标位置
def imgfind_x_y(img_soure_path,img_search_path,threshold_,rgb_,bgremove_):
    match_result=aircv.find_template(aircv.imread(img_soure_path),aircv.imread(img_search_path),threshold_,rgb_,bgremove_)
    return match_result

#找图标
def find_icon(png,wait_time=10,threshold_=0.9,rgb_=True,bgremove_=False,sleep_time=0):
    time.sleep(sleep_time)
    start_time=time.monotonic()
    while time.monotonic()-start_time<wait_time:
        logger.debug("拉取截图")
        shell_result=su.run(adb_path+" shell screencap /data/screen.png",capture_output=True)
        shell_result=su.run(adb_path+" pull /data/screen.png "+screen_png,capture_output=True)
        match_result=imgfind_x_y(screen_png,png,threshold_,rgb_,bgremove_)
        if(match_result!=None):
            logger.debug(f"找到位置:{match_result['result'][0]} {match_result['result'][1]}")
            break
    return match_result

#点击图标 默认延迟3s
def click_icon(png,wait_time=3,threshold_=0.9,rgb_=True,bgremove_=False):
    time.sleep(wait_time)
    match_result=imgfind_x_y(screen_png,png,threshold_,rgb_,bgremove_)
    if match_result==None:
        logging.error("没有找到对应的页面")
        raise ValueError("没有找到对应的页面")
        #return match_result
    shell_result=su.run(adb_path+f" shell input tap {match_result['result'][0]} {match_result['result'][1]}")
    logger.debug(f"点击:{match_result['result'][0]} {match_result['result'][1]}")
    return match_result
def swipe_(x1=1000,y1=500,x2=600,y2=500,wait_time=3):
    shell_result=su.run(adb_path+f" shell input swipe {x1} {y1} {x2} {y2}")
    time.sleep(wait_time)

#确认按钮 随意一点 默认延迟3s
def click_random(x=1000,y=1,wait_time=3):
    time.sleep(wait_time)
    logger.debug(f"随意点击{x},{y}")
    su.run(adb_path+f" shell input tap {x} {y}")

def find_worker(png,keep_time=60):
    start_time=time.monotonic()
    while time.monotonic()-start_time<keep_time:
        if find_icon(png,wait_time=5):
            click_icon(png,wait_time=1)
            break
        else:
            swipe_()
    
if __name__=="__main__":
    swipe_(1400,300,1400,200)