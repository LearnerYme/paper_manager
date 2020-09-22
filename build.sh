#!/bin/bash

if [ ! -d "./paper_folder/" ];then
    mkdir paper_folder
fi
if [! -e "./paper_info.db" ];then
    python3 paper_manager.py -i True
fi
sysname=`uname`
if [ $sysname == "Darwin" ];then
    sed -i "s/xdg-open/open/" paper_manager.py
fi