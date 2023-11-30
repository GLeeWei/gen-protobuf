import os, sys, shutil, platform

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "./js"))
sys.path.append(os.path.join(current_dir, "./dart"))
sys.path.append(os.path.join(current_dir, "./go"))
# sys.path.append(os.path.join(current_dir, "./get_github_resp"))

from gen_protoc_js import protos_to_js
from gen_protoc_dart import protos_to_dart
from gen_protoc_go import protos_to_go
# from get_github_resp import download_github_assets

# def check_proto_dependencies():
#     ''' Checking the dependencies proto, which will be used for building
#     '''
#     try:
#     	protoc_root_path = getProtocRootPath()
#     	if not os.path.exists(protoc_root_path):
#     		file_path = download_github_assets('https://github.com/protocolbuffers/protobuf', current_dir)
#             # unzip(file_path, dart_proto_root_dir)
#             # os.remove(file_path)
#             # os.system('cd %s && dart pub get' % (os.path.join(protoc_dart_root_path, 'protoc_plugin')))
#     except Exception as e:
#         print("dart no installed. Please install dart! %s" % e)
#         sys.exit(1)

def protos_to_lanuage(src_dir, desdir, lanuage):
    sCmd = "%s --proto_path=%s --%s_out=%s %s/*.proto" % (getProtocExecutables(), src_dir, lanuage, desdir, src_dir)
    # print(sCmd)
    os.system(sCmd)

def getProtocRootDirName():
    sysPlat = platform.system()
    return 'protoc-%s' % sysPlat   

def getProtocRootPath():
    dir_name = getProtocRootDirName()
    return os.path.join(current_dir, 'process/%s' % dir_name)    

def getProtocExecutables():
    sysPlat = platform.system()
    executables = 'Darwin' == sysPlat and os.path.join(current_dir, 'process/protoc-25.1-osx/bin/protoc') or os.path.join(current_dir, './process/protoc-25.1-win64/bin/protoc.exe')
    return executables

def main():
	import argparse
	usage = "python %prog -s/--src <source dir or single source file> -d/--dest <destination dir> -l <complie target lanuage"
	parser = argparse.ArgumentParser(usage)
	parser.add_argument('-s', '--src', type=str, help='proto source dir', default=current_dir)
	parser.add_argument('-d', '--dest', type=str, help='destination dir', default=os.path.join(current_dir, 'protos'))
	parser.add_argument('-bundle', type=str, help='bundle name, only support ts or js', default='protos')
	parser.add_argument('-l','--lanuage', help='complie target lanuage, support js, ts,  dart, cpp, objc, csharp, java, kotlin, python, ruby, php go', default='js')
	args = parser.parse_args()

	if os.path.isdir(args.dest):
		shutil.rmtree(args.dest)
	os.makedirs(args.dest)

	if 'dart' == args.lanuage:
		protos_to_dart(getProtocExecutables(), args.src, args.dest)
	elif ('js' == args.lanuage or 'ts' == args.lanuage):
		protos_to_js(args.src, args.dest, args.bundle, 'ts' == args.lanuage)
	elif ('lua' == args.lanuage):
		print('unsupoort lua')
	elif 'go' == args.lanuage:
		protos_to_go(getProtocExecutables(), args.src, args.dest)
	elif ('cpp' == args.lanuage or 'objc' == args.lanuage or 'csharp' == args.lanuage or
		 'java' == args.lanuage or 'kotlin' == args.lanuage or 'python' == args.lanuage or
		 'ruby' == args.lanuage or 'php' == args.lanuage):
		protos_to_lanuage(args.src, args.dest, args.lanuage)

if __name__=="__main__":
	# check_proto_dependencies()
    main()



