import time

def create_log_file(log_file):
    # 步骤3：处理日志文件
    try:
        if log_file.exists():
            log_file.unlink()  # 删除旧日志
            print(f"[{time.ctime()}] 已删除旧日志文件")
        log_file.touch()  # 创建新日志文件
        print(f"[{time.ctime()}] 已创建新日志文件")
    except PermissionError:
        print(f"[{time.ctime()}] 日志文件操作权限不足")

def append_log(log_file,log_entry):
    # 记录到日志文件
    with log_file.open("a", encoding="utf-8") as log_f:
        log_f.write(log_entry)


def extract_filename(s: str) -> str:
    """
    从路径字符串中提取最后一个/和最后一个.之间的内容

    :param s: 输入字符串（如 "路径/文件名.扩展名"）
    :return: 提取内容（如 "文件名"），若格式不符则返回空字符串
    """
    try:
        # 查找最后一个斜杠位置
        last_slash = s.rfind('/')
        if last_slash == -1:
            # 无斜杠时查找最后一个点
            last_dot = s.rfind('.')
            return s[:last_dot] if last_dot != -1 else s
        else:
            # 在斜杠右侧查找最后一个点
            substring = s[last_slash + 1:]
            last_dot = substring.rfind('.')
            return substring[:last_dot] if last_dot != -1 else substring
    except Exception as e:
        print(f"处理异常: {str(e)}")
        return ""
