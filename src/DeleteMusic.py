import time
import FileOperation as fileOp


def delete_music(delete_list, music_dir, log_file):
    try:
        # 步骤4：执行模糊匹配和文件删除
        if not delete_list:
            log_entry = f"\n[{time.ctime()}] 待删除列表为空，跳过操作"
            print(log_entry)
            fileOp.append_log(log_file, log_entry)
        else:
            for pattern in delete_list:
                try:
                    # 递归搜索匹配文件（包含子目录）
                    matched_files = list(music_dir.rglob(f"*{pattern}*"))
                    for file_path in matched_files:
                        if file_path.is_file():
                            try:
                                file_path.unlink()
                                log_entry = f"\n[{time.ctime()}] 成功删除 | 文件：{file_path}"
                                print(log_entry.strip())
                            except PermissionError:
                                log_entry = f"\n[{time.ctime()}] 权限错误 | 文件：{file_path}"
                                print(log_entry.strip())
                            except Exception as e:
                                log_entry = f"\n[{time.ctime()}] 删除失败 | 文件：{file_path} | 错误：{str(e)}"
                                print(log_entry.strip())
                            finally:
                                # 记录到日志文件
                                fileOp.append_log(log_file, log_entry)
                except Exception as e:
                    print(f"\n[{time.ctime()}] 模糊匹配时发生错误：{str(e)}")

    except Exception as e:
        print(f"\n[{time.ctime()}] 处理过程中发生异常：{str(e)}")