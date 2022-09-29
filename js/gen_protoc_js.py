# -*- coding: UTF-8 -*-
import sys, os, shutil
import time
import subprocess

current_dir = os.path.dirname(os.path.realpath(__file__))

def check_environment_variables():
    ''' Checking the environment node, which will be used for building
    '''
    try:
        retCode = subprocess.call(['node', '-v'])
        if 0 == retCode:
            try :
                retCode2 = subprocess.call(['pbjs', '-v'])
                if 0 == retCode2:
                    print("protobufjs-cli installed")
            except Exception:
                print("install protobufjs-cli")
                os.system('npm install --location=global protobufjs-cli')

    except Exception:
        print("nodejs no installed. Please install nodejs!")
        sys.exit(1)

def protos_to_js(srcDir, destDir, bundle, ts):
    check_environment_variables()
    protoList = []
    for fn in os.listdir(srcDir):
        if fn.endswith(".proto"):
            protoList.append(os.path.join(srcDir, fn))

    if (0 < len(protoList)):
        bundleName = os.path.join(destDir, bundle)
        sProtoList = ' '.join(protoList)
        print('gen ' + sProtoList)
        os.system("pbjs -t static-module -w commonjs -o %s.js %s --no-beautify --no-typeurl --no-create" % (bundleName, sProtoList))
        ts and os.system("pbts -o %s.d.ts %s.js" % (bundleName, bundleName))


