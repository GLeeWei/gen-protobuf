# -*- coding: UTF-8 -*-
import sys, os, shutil
import time
import subprocess
import platform

def check_environment_variables():
    ''' Checking the environment node, which will be used for building
    '''
    try:
        retCode = subprocess.call(['dart', '--version'])
    except Exception:
        print("dart no installed. Please install dart!")
        sys.exit(1)

def protos_to_dart(executables, srcDir, destDir):
    check_environment_variables()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    protoc_gen_dart_bin = os.path.join(current_dir, 'protobuf.dart-protobuf/protoc_plugin/bin/')
    sysPlat = platform.system()
    protoc_gen_dart = os.path.join(protoc_gen_dart_bin, 'Darwin' == sysPlat and 'protoc-gen-dart' or 'protoc-gen-dart.bat')
    sCmd = "%s --proto_path=%s --dart_out=%s %s/*.proto --plugin=%s" % (executables, srcDir, destDir, srcDir, protoc_gen_dart)
    # print(sCmd)
    os.system(sCmd)