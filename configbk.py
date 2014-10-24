#!/usr/bin/env python
# encoding: utf-8

import jsonpickle
import os
import shutil
from argparse import ArgumentParser
class Item(object):
    def __init__(self, id, src, dst):
        self.id = id
        self.src = src
        self.dst = dst

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-b", "--backup", action='store_true', default=False, help="Create/update backup")
    parser.add_argument("-u", "--update", action='store_true', default=False ,help="Update configs")
    parser.add_argument("-r", "--restore", action='store_true', default=False ,help="Restore configs")
    parser.add_argument("-f", "--file", type=str, default='config.backup', help='Config file')
    parser.add_argument("-d", "--dir", type=str, default='.', help='Backup dir')
    parser.add_argument("-o", "--old", type=str, default='../old', help='Old configs dir')
    parser.add_argument("-c", "--add-config", type=str, help='Add new config')
    parser.add_argument("-C", "--clean", action='store_true', default=False, help="Clean")

args = parser.parse_args()
items = []


if(args.clean):
    with open(args.file, 'r') as file:
        json=file.read().replace('\n','')
    items = jsonpickle.decode(json)
    os.remove(args.file)
    shutil.rmtree(items[0].src)
    shutil.rmtree(items[0].dst)

if(args.update):
    with open(args.file, 'r') as file:
        json = file.read().replace('\n','')
    items = jsonpickle.decode(json)
    for item in items:
        if item.id==0:
            continue
        if os.path.isfile(item.dst):
            shutil.copy(item.dst, item.src)
        else:
            try:
                shutil.rmtree(os.path.join(item.src,os.path.basename(os.path.normpath(item.dst))))
            except:
                pass
            shutil.copytree(item.dst, os.path.join(item.src,os.path.basename(os.path.normpath(item.dst))))

if(args.restore):
    with open(args.file, 'r') as file:
        json = file.read().replace('\n','')
    items = jsonpickle.decode(json)
    for item in items:
        if item.id==0:
            old = item.dst 
            continue
        if os.path.isfile(os.path.join(item.src, os.path.basename(os.path.normpath(item.dst)))):
            shutil.copy(os.path.join(item.src, os.path.basename(os.path.normpath(item.dst))), item.dst)
            shutil.copy(item.dst, old)
        else:
            try:
                shutil.rmtree(os.path.join(item.dst))
                shutil.rmtree(os.path.join(old,os.path.basename(os.path.normpath(item.dst))))
            except:
                pass
            shutil.copytree(os.path.join(item.src,os.path.basename(os.path.normpath(item.dst))),item.dst)
            shutil.copytree(item.dst, os.path.join(old, os.path.basename(os.path.normpath(item.dst))))

if(args.backup):
    file = open(args.file, 'w')
    items.append(Item(0,args.dir, args.old))
    if(args.dir != '.'):
        os.mkdir(args.dir)
    os.mkdir(args.old)
    file.write(jsonpickle.encode(items))
    file.close()

if(args.add_config!=None):
    if os.path.exists(args.file):
        with open(args.file, 'r') as file:
            json=file.read().replace('\n','')
        items = jsonpickle.decode(json)
        dir=items[0].src
        maxid = sorted(items, key=lambda item : item.id, reverse=True)[0].id
        id = maxid+1
        if args.add_config!=None:
            items.append(Item(id,os.path.join(dir,str(id)), args.add_config))
            os.mkdir(os.path.join(dir,str(id)))
            if os.path.isfile(args.add_config):
                shutil.copy(args.add_config, os.path.join(dir,str(id)))
            else:
                shutil.copytree(args.add_config, os.path.join(dir,str(id),os.path.basename(os.path.normpath(args.add_config))))


        with open(args.file, 'w') as file:
            file.write(jsonpickle.encode(items))


