# autoDeleteMusic
自动删除navidrome中不喜欢的歌曲

使用方法

在main.py中填写下面的变量

    # 自己音乐库的位置
    MUSIC_DIR = Path("/vol3/1000/音乐")
    #日志存放的位置
    LOG_FILE = Path("/vol2/1000/home/script/autoDeleteMusic.log")
    #下面这三个参数填自己的navidrome服务器信息
    USERNAME = ""
    PASSWORD = ""
    BASE_URL = ""

并在navidrome或者音流中建立[不喜欢]收藏夹,后续不喜欢的歌放到这个收藏夹里就会自动删除