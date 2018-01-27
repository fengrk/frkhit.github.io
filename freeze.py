import os
import shutil

from project import freezer
from project.settings import blog_path

if __name__ == '__main__':
    freezer.freeze()
    
    if os.path.exists(os.path.join(blog_path, "index.html")):
        shutil.copy(os.path.join(blog_path, "index.html"), "./index.html")
