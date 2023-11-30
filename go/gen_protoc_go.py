import sys, os, shutil
import subprocess
import platform
import re

current_dir = os.path.dirname(os.path.realpath(__file__))

def get_go_path():
    ''' Checking the environment go, which will be used for building
    '''
    try:
        out = subprocess.run(['go', 'env'], capture_output=True)
        if 0 == out.returncode:
            envs = out.stdout.decode()
            envMatch = re.search(r'^GOPATH=(.*)', envs, flags=re.M)
            print('envMatch', envMatch)
            if envMatch:
                goPath = envMatch.group(1)
                # print('goPath', goPath)
            if os.path.exists(get_protoc_plugin_path(goPath)):
                return goPath 
            out = subprocess.call('export GOPROXY=https://goproxy.cn,direct && go install google.golang.org/protobuf/cmd/protoc-gen-go@latest', shell=True)
            print(out, goPath)
            if 0 == out:
                return goPath 
        return ''
    except Exception as e:
        print("go no installed. Please install go! %s " % e)
        sys.exit(1)

def get_protoc_plugin_path(goPath):
    sysPlat = platform.system()
    return os.path.join(goPath, 'bin/protoc-gen-go') if 'Darwin' == sysPlat else os.path.join(goPath, 'bin/protoc-gen-go.bat')

def protos_to_go(executables, srcDir, destDir):
    goPath = get_go_path()
    protoc_gen_go = get_protoc_plugin_path(goPath)
    sCmd = "%s --proto_path=%s --go_out=%s %s/*.proto --plugin=%s" % (executables, srcDir, destDir, srcDir, protoc_gen_go)
    print(sCmd)
    os.system(sCmd)