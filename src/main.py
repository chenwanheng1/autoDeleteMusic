import os
import DeleteMusic
from pathlib import Path
import time
import HttpClient
import HttpFun as httpFun
import json
import FileOperation as fileOp


if __name__ == '__main__':
    # 自己音乐库的位置
    MUSIC_DIR = Path("/vol3/1000/音乐")
    #日志存放的位置
    LOG_FILE = Path("/vol2/1000/home/script/logs/autoDeleteMusic.log")
    #下面这三个参数填自己的navidrome服务器信息
    USERNAME = ""
    PASSWORD = ""
    BASE_URL = ""
    SLEEP_TIME = 20
    TOKEN = ""
    ID = ""

    # CHECK_FILE = Path("D:\worksapce\pycharm\PythonProject\不喜欢.txt")
    # MUSIC_DIR = Path("D:\worksapce\pycharm\PythonProject\音乐")
    # LOG_FILE = Path("D:\worksapce\pycharm\\autoDeleteMusic\logs\\autoDeleteMusic.log")

    try:
        #初始化http客户端
        http_client = HttpClient.HttpClient(
            base_url=BASE_URL,
            headers={'Content-Type': 'application/json'},
            timeout=5,
            verify_ssl=False
        )
        #初始化日志
        fileOp.create_log_file(LOG_FILE)
        #登录navidrome
        TOKEN,ID = httpFun.login(http_client,"/auth/login",USERNAME,PASSWORD)

        #开始循环处理歌单
        if len(TOKEN) > 0 and len(ID) > 0:
            while True:
                #拉取歌单，并寻找【不喜欢】
                delete_list_id = httpFun.get_play_list(http_client,"/api/playlist",0,0,TOKEN,ID)
                if len(delete_list_id) <= 0:
                    log_entry = f"\n[{time.ctime()}] 没有找到【不喜欢】歌单,进入等待状态..."
                    print(log_entry)
                    fileOp.append_log(LOG_FILE, log_entry)
                    time.sleep(SLEEP_TIME)
                    continue

                #查询【不喜欢】歌单中所有的歌曲title
                delete_list = httpFun.get_delete_list(http_client,"/api/playlist/" + delete_list_id + "/tracks",delete_list_id,0,0,TOKEN,ID)
                if len(delete_list) <= 0:
                    log_entry = f"\n[{time.ctime()}] 【不喜欢】歌单为空,进入等待状态..."
                    print(log_entry)
                    fileOp.append_log(LOG_FILE, log_entry)
                    time.sleep(SLEEP_TIME)
                    continue

                #按title删除歌曲
                DeleteMusic.delete_music(delete_list, MUSIC_DIR, LOG_FILE)

                #拉取丢失文件列表
                miss_list = httpFun.get_miss_list(http_client,"/api/missing",0,0,TOKEN,ID)
                if len(miss_list) <=0:
                    log_entry = f"\n[{time.ctime()}] 没有丢失文件,进入等待状态..."
                    print(log_entry)
                    fileOp.append_log(LOG_FILE, log_entry)
                    time.sleep(SLEEP_TIME)
                    continue

                #按歌曲id从库中移除
                httpFun.delete_miss_file(http_client,"/api/missing",miss_list,TOKEN,ID)
                log_entry = f"\n[{time.ctime()}] 完成删除操作,进入等待状态..."
                print(log_entry)
                fileOp.append_log(LOG_FILE, log_entry)
                time.sleep(SLEEP_TIME)
        else:
            log_entry = f"\n[{time.ctime()}] token或者id为空! token:[{TOKEN}] || id:[{ID}]..."
            print(log_entry)
            fileOp.append_log(LOG_FILE, log_entry)
    except KeyboardInterrupt:
        http_client.close()
        log_entry = f"\n[{time.ctime()}] 程序已手动终止"
        print(log_entry)
        fileOp.append_log(LOG_FILE, log_entry)
        exit(0)