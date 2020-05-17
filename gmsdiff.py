#coding=utf-8

import os
import zipfile
import re
import shutil
import difflib
import sys
import argparse
import filecmp

gmsold_name = 'gms-oem-Q-10-202002'

gmsnew_name = 'gms-oem-Q-10-202003'
#
# extracting_old = zipfile.ZipFile(gmsold_name{0}.format('.zip'))
# extracting_old.extractall(gmsold_name)
#
# extracting_new = zipfile.ZipFile(gmsnew_name{0}.format('.zip'))
# extracting_new.extractall(gmsnew_name)

def read_file(file_name):
    try:
        file_desc = open(file_name, 'r')
        # 读取后按行分割
        text = file_desc.read().splitlines()
        file_desc.close()
        return text
    except IOError as error:
        print ('Read input file Error: {0}'.format(error))
        sys.exit()


List_new = []
List_old = []

#遍历新文件目录
for root,dirs,files in os.walk(gmsnew_name):
    for file in files:
        List_new.append(os.path.join(root,file))

print(List_new)
print("test")

for new_name in List_new:
    old = re.sub(gmsnew_name,gmsold_name,new_name)
    List_old.append(old)

print(List_old)


for new,old in zip(List_new,List_old):
    if os.path.exists(old):
        print('在上个月的gms文件中，存在该文件')
        #对比

        #判断是否为apk 格式
        fname, fename = os.path.splitext(new)
        if fename == '.apk':
            print()

        else:

            if not filecmp.cmp(new,old):
                print(new)
                news = read_file(new)
                olds = read_file(old)

                d = difflib.HtmlDiff()
                result = d.make_file(news, olds)

                path = os.path.dirname(new) #获取new文件所在的目录
                paths = '对比结果/'+path

                if not os.path.exists(paths):
                    os.makedirs(paths)

                name = os.path.basename(new)

                with open(paths+'/{0}.html'.format(name),'w')as f:
                    f.writelines(result)

    else:
        print('在上个月的文件中，不存在该文件，此文件为新增文件')
        #保存该文件
        shutil.copytree(new,'对比结果')



