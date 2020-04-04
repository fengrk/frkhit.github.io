---
layout: post
title:  rsync 实现 move 功能
category: 技术
tags:  
    - rsync
    - docker
keywords: 
description: 
---

# rsync 实现 move 功能

在实际使用 docker 时， 需要将本地目录挂载到容器上。 

但如果挂载的目录的 inode 变化（如宿主目录先被删除，后重新创建），容器读取到的目录将变为空目录。

所以， 希望实现一种特殊的 `move` 功能：

- 将源目录内容完整复制到目标目录上
- 目标目录已经存在的子目录，不能更改其文件 `inode`
- 原来的目标目录上存在、但源目录不存在的文件，需要在目标目录上删除
- 原来目标目录上存在且内容与源目录一致的文件， 尽量不要修改其文件 `inode`
  
最终使用 `rsync` 实现该功能：

```
src='~/test/abc'
dst='~/test/efg'

# move src to dst
cp -r ~/test/abc /tmp/efg
rsync -avu --progress --delete /tmp/efg ~/test/
rm -r /tmp/efg

```

## 验证代码

```
import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest


def get_md5_for_file(file_or_filename) -> str:
    if isinstance(file_or_filename, str):
        hash_md5 = hashlib.md5()
        with open(file_or_filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file_or_filename.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


class TestRsyncCopy(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def do_log(self, info: str):
        print(info)

    def get_dir_info(self, path: str) -> dict:
        """ """
        path_info: dict = {os.path.abspath(path): {"is_dir": True, "stat": os.stat(path)}}
        for _dir in os.listdir(path):
            _full_name = os.path.abspath(os.path.join(path, _dir))
            if os.path.isdir(_full_name):
                path_info.update(self.get_dir_info(path=_full_name))
                continue

            path_info[_full_name] = {"is_dir": False, "stat": os.stat(_full_name)}
            if os.path.isfile(_full_name):
                path_info[_full_name]["file_md5"] = get_md5_for_file(_full_name)

        return path_info

    def copy(self, src_dir: str, dst_dir: str):
        """ """
        tmp_dir = tempfile.mkdtemp()
        try:
            cmd_1 = "cp -r {} {}/{}".format(os.path.abspath(src_dir), tmp_dir, os.path.basename(dst_dir))
            self.do_log("run: {}".format(cmd_1))
            subprocess.check_output(cmd_1, shell=True)
            cmd = "rsync -avu --progress --delete {}/{} {}".format(tmp_dir, os.path.basename(dst_dir), os.path.abspath(os.path.dirname(dst_dir)))
            self.do_log("run: {}".format(cmd))
            result = subprocess.check_output(cmd, shell=True)
            self.do_log("{}".format(result.decode("utf-8")))
        finally:
            shutil.rmtree(tmp_dir)

    def _create_dir(self, target_dir: str, file_info: dict):
        """ """
        for file_path, file_content in file_info.items():
            # make dir
            _full_file_name = os.path.join(target_dir, file_path)
            _full_dir = os.path.dirname(_full_file_name)
            os.makedirs(_full_dir, exist_ok=True)

            if file_content is None:
                self.do_log("{} is dir".format(_full_file_name))
                os.makedirs(_full_file_name)
            else:
                with open(_full_file_name, "w") as f:
                    f.write(file_content)

    def testCopy(self):
        """ """

        # prepare dir data
        src_dir, dst_dir = "./abc", "./efg"

        # remove dir
        for _dir in [src_dir, dst_dir]:
            if os.path.exists(_dir):
                if os.path.isdir(_dir):
                    shutil.rmtree(_dir)
                else:
                    os.remove(_dir)

            # make dir
            os.mkdir(_dir)

        # prepare data
        self._create_dir(target_dir=src_dir, file_info={
            "a.txt": "abcdefg",
            "b/b.txt": "xxxxxx",
            "c.txt": "ccccccc",
        })
        self._create_dir(target_dir=dst_dir, file_info={
            "a.txt": "zzzz",
            "b/c.txt": "xxxxxx",
            "c/x.abc": "fdsfaffasf",
            "c.txt": "ccccccc",
        })
        src_file_info = self.get_dir_info(path=src_dir)
        raw_dst_file_info = self.get_dir_info(path=dst_dir)

        # copy
        self.copy(src_dir=src_dir, dst_dir=dst_dir)
        target_dst_file_info = self.get_dir_info(path=dst_dir)

        # confirm
        # 文件内容
        self.do_log("\n\ncheck file move from src to dst...")
        _src_full_dir = os.path.abspath(src_dir)
        _src_file_info = {
            _file_name[len(_src_full_dir):]: _file_info["file_md5"] for _file_name, _file_info in src_file_info.items() \
            if "file_md5" in _file_info
        }
        _dst_full_dir = os.path.abspath(dst_dir)
        _dst_file_info = {
            _file_name[len(_dst_full_dir):]: _file_info["file_md5"] for _file_name, _file_info in target_dst_file_info.items() \
            if "file_md5" in _file_info
        }
        self.assertEqual(_src_file_info, _dst_file_info)
        self.do_log("files equal between src and dst!")

        # 目录 inode
        self.do_log("\n\ncheck dir inode with same name...")
        _raw_dst_dir_info = {
            _file_name[len(_dst_full_dir):]: _file_info["stat"].st_ino for _file_name, _file_info in raw_dst_file_info.items() \
            if _file_info["is_dir"]
        }
        _target_dst_dir_info = {
            _file_name[len(_dst_full_dir):]: _file_info["stat"].st_ino for _file_name, _file_info in target_dst_file_info.items() \
            if _file_info["is_dir"]
        }
        for _dir_name, _dir_ino in _raw_dst_dir_info.items():
            if _dir_name not in _target_dst_dir_info:
                continue
            self.do_log("dir {}, raw ino {}, target ino {}".format(_dir_name, _dir_ino, _target_dst_dir_info[_dir_name]))
            self.assertEqual(_dir_ino, _target_dst_dir_info[_dir_name])

        # 相同文件 inode
        self.do_log("\n\ncheck file inode with same content...")
        _raw_dst_file_info = {
            _file_name[len(_dst_full_dir):]: _file_info for _file_name, _file_info in raw_dst_file_info.items() \
            if not _file_info["is_dir"] and "file_md5" in _file_info
        }
        _target_dst_file_info = {
            _file_name[len(_dst_full_dir):]: _file_info for _file_name, _file_info in target_dst_file_info.items() \
            if not _file_info["is_dir"] and "file_md5" in _file_info
        }
        for _dir_name, _file_info in _raw_dst_file_info.items():
            if _dir_name not in _target_dst_file_info:
                continue

            _target_file_info = _target_dst_file_info[_dir_name]
            if _file_info["file_md5"] != _target_file_info["file_md5"]:
                continue

            self.do_log("file {}, raw ino {}, target ino {}".format(_dir_name, _file_info["stat"].st_ino, _target_file_info["stat"].st_ino))
            self.assertEqual(_file_info["stat"].st_ino, _target_file_info["stat"].st_ino)

```

执行结果：

```
run: cp -r /xxx/test/abc /var/folders/qz/1gh56g497f366630wxtk4z8m0000gn/T/tmpe55ue00w/efg
run: rsync -avu --progress --delete /var/folders/qz/1gh56g497f366630wxtk4z8m0000gn/T/tmpe55ue00w/efg /xxyy/test
building file list ... 
5 files to consider
deleting efg/c/x.abc
deleting efg/c/
deleting efg/b/c.txt
efg/a.txt
           7 100%    0.00kB/s    0:00:00 (xfer#1, to-check=3/5)
efg/b/b.txt
           6 100%    5.86kB/s    0:00:00 (xfer#2, to-check=0/5)

sent 238 bytes  received 64 bytes  604.00 bytes/sec
total size is 20  speedup is 0.07



check file move from src to dst...
files equal between src and dst!


check dir inode with same name...
dir , raw ino 35323238, target ino 35323238
dir /b, raw ino 35323244, target ino 35323244


check file inode with same content...
file /c.txt, raw ino 35323248, target ino 35323248

```