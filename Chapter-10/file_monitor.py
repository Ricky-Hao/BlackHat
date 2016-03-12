#coding=utf-8
#这个被修改的示例出自
#http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html

import tempfile
import threading
import win32file
import win32con
import os

#这些是典型的临时文件所在的路径
dirs_to_monitor = ["C:\\WINDOWS\\Temp",tempfile.gettempdir()]

#文件修改行为对应的常量
FILE_CREATED        = 1
FILE_DELETED        = 2
FILE_MODIFIED       = 3
FILE_RENAMED_FROM   = 4
FILE_RENAMED_TO     = 5

def start_monitor(path_to_watch):
    #为每个监控器起一个线程
    FILE_LIST_DIRECTORY = 0x0001

    h_directory = win32file.CreateFile(
         path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    while True:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURIY,
                None,
                None
            )

            for action,file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)

                if action == FILE_CREATED:
                    print("[ + ] Created %s" % full_filename)
                elif action == FILE_DELETED:
                    print("[ - ] Deleted %s" % full_filename)
                elif action == FILE_MODIFIED:
                    print("[ * ] Modified %s" % full_filename)

                    #输出文件内容
                    print("[vvv] Dumping contents...")

                    try:
                        wait open(full_filename,"rb") as fd:
                            contents = fd.read()

                        print(contents)
                        print("[^^^] Dump conplete.")
                    except Exception as e:
                        print("[!!!] Failed.")
                        print(e)

                elif action == FILE_RENAME_FRON:
                    print("[ > ] Renamed from: %s" % full_filename)
                elif action == FILE_RENAMED_TO:
                    print("[ < ] Renamed to: %s" % full_filename)
                else:
                    print("[???] Unknown: %s" % full_filename)

        except Exception as e:
            print(e)
for path in dirs_to_monitor:
    monitor_thread = threading.Thread(target=start_monitor,args=(path,))
    print("Spawning monitoring thread for path: %s" % path)
    monitt.start()
