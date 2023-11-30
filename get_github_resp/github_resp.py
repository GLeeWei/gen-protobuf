import os
import urllib.request
import json
import zipfile
import shutil
import platform
import re

github_api_url_prefix = 'https://api.github.com/repos/'

ZIP_URL_KEY = 'zipball_url'
TAR_URL_KEY = 'tarball_url'
ASSETS_KEY = 'assets'

def get_github_latest_release_source(github_url):
    github_prefix = 'https://github.com/'
    fix_path = github_url.replace(github_prefix, '')
    dirs = fix_path.split('/')
    project_path = '%s/%s' % (dirs[0], dirs[1])
    proj_api_url = '%s%s/releases/latest' % (github_api_url_prefix, project_path)
    # print(proj_api_url)
    json_dict = http_get_request(proj_api_url)
    return json_dict

def http_get_request(url):
    req = urllib.request.urlopen(url)
    resp = req.read()
    return json.loads(resp.decode())


def download_github_source(github_url, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    json_dict = get_github_latest_release_source(github_url)
    if ZIP_URL_KEY in json_dict:
        zip_url = json_dict[ZIP_URL_KEY]
        file_name = '%s.zip' % os.path.basename(zip_url)
        print('zip_url %s' % zip_url)
    # elif TAR_URL_KEY in json_dict:
    #     zip_url = json_dict[TAR_URL_KEY]
    #     file_name = '%s.tar' % os.path.basename(zip_url)
    #     print('zip_url %s' % zip_url)
    req = urllib.request.urlopen(zip_url)
    data = req.read()
    zip_file_path = os.path.join(dest, file_name)
    with open(zip_file_path, 'wb') as f:
        f.write(data)
        f.close()
    return zip_file_path

# def download_github_assets(github_url, dest):
#     if not os.path.exists(dest):
#         os.makedirs(dest)
#     json_dict = get_github_latest_release_source(github_url)
#     # print(json_dict)
#     os_name = platform.system()
#     os_machine = platform.machine()
#     print(os_name, os_machine)
#     if ASSETS_KEY in json_dict:
#         assets = json_dict[ASSETS_KEY]
#         for v in assets:
#             name = v['name']
#             download_url = v['browser_download_url']
#             if 'Darwin' == os_name:
#                 if re.search(r'Darwin|osx', name) and re.search(os_machine, name):
#                     print(download_url)

#     # req = urllib.request.urlopen(zip_url)
#     # data = req.read()
#     # zip_file_path = os.path.join(dest, file_name)
#     # with open(zip_file_path, 'wb') as f:
#     #     f.write(data)
#     #     f.close()
#     return zip_file_path

def unzip(file_path, dest_file_name):
    base_dir = os.path.dirname(file_path)
    tmpDir = os.path.join(base_dir, 'tmp')
    if not os.path.exists(tmpDir):
        os.makedirs(tmpDir)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(tmpDir)

    dirs = os.listdir(tmpDir)
    unzip_dir = dirs[0]
    shutil.move(os.path.join(tmpDir, unzip_dir), os.path.join(base_dir, dest_file_name))
    shutil.rmtree(tmpDir)


if __name__ == '__main__':
    url = 'https://github.com/protocolbuffers/protobuf/'
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = download_github_assets(url, current_dir)
    print(file_name)