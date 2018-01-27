# python删除文件或目录

```
def remove_path_or_file(path_or_file_name):
    """
        删除文件
    """
    import os
    import shutil
    
    if not os.path.exists(path_or_file_name):
        import logging
        logging.warning("{} not exists!".format(path_or_file_name))
        return
    
    if os.path.isdir(path_or_file_name):
        # dir
        shutil.rmtree(path_or_file_name)
    else:
        # file
        os.remove(path_or_file_name)


```
