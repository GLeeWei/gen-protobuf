import sys, os
import subprocess
import platform

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "../get_github_resp"))

dart_proto_root_dir = 'protobuf.dart-protobuf'

from github_resp import download_github_source, unzip

def check_environment_variables():
    ''' Checking the environment dart, which will be used for building
    '''
    try:
        retCode = subprocess.call(['dart', '--version'])
        protoc_dart_root_path = get_protoc_dart_root_path()
        if not os.path.exists(protoc_dart_root_path):
            current_dir = os.path.dirname(os.path.realpath(__file__))
            # file_path = download_github_source('https://github.com/google/protobuf.dart/', current_dir)
            unzip(file_path, dart_proto_root_dir)
            os.remove(file_path)
            os.system('cd %s && dart pub get' % (os.path.join(protoc_dart_root_path, 'protoc_plugin')))
    except Exception as e:
        print("dart no installed. Please install dart! %s" % e)
        sys.exit(1)

def get_protoc_dart_root_path():
    return os.path.join(current_dir, 'protobuf.dart-protobuf')

def get_protoc_plugin_path():
    return os.path.join(get_protoc_dart_root_path(), 'protobuf.dart-protobuf/protoc_plugin/')

def protos_to_dart(executables, srcDir, destDir):
    check_environment_variables()
    protoc_gen_dart_bin = os.path.join(get_protoc_plugin_path(), 'bin')
    sysPlat = platform.system()
    protoc_gen_dart = os.path.join(protoc_gen_dart_bin, 'Darwin' == sysPlat and 'protoc-gen-dart' or 'protoc-gen-dart.bat')
    sCmd = "%s --proto_path=%s --dart_out=%s %s/*.proto --plugin=%s" % (executables, srcDir, destDir, srcDir, protoc_gen_dart)
    # print(sCmd)
    os.system(sCmd)


# if __name__ == '__main__':
#     check_environment_variables()