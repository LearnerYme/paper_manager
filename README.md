# paper_manager

A very simple paper-manage tool. I write this for programing practice but I'll be glad if it can help you.^^

**Build up**

After downloading this tool, get into this directory and run `bash build.sh` and wait a while until it prints 'Initialization finished.' on your screen.

Some standard libraries of Python3 are needed, and you might need not to install any other packages.

Anyway, here I list imported packages:

* os

* tkinter

* datetime

* argparse

* sqlite3

**Run**

If you have already built up, run `python3 paper_manager.py` or `./PM.sh`.

**Usage**

* Type in search condition and click 'search' to search paper in the database.

* Click 'list all' to see all the papers in the database.

* Right Click listed paper to open, show information or delete selected paper.

* Browse and select new paper from local file and type in title, alias, key words, and choose tags, then click add to append new paper to the database.

* Modify the .py file, delete 'paper_info.db' and then rebuild to change tags (PHY, ML, OTHER). It's quite difficulte and complex ... If you need more tag, I'm sorry that current version cannot support this ...

**TO DO**

* Tag-changing util.

* Read/Unread mark.