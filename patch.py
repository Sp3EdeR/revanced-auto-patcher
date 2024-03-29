#!/usr/bin/python3

"""
A python script to easily patch APKs with ReVanced or ReVanced Extended.
To configure the script's behaviour, edit the default settings below, or run
"python patch.py --help" to see the command-line argument interface help.
"""

import os
import sys

scriptDir = os.path.dirname(os.path.abspath(sys.argv[0]))
# The following are the default settings. Edit to change the defaults.
settings = {
    'srcDir': scriptDir,                                    # Source APKs in the script's directory
    'outDir': os.path.join(scriptDir, '..'),                # Patched APKs written one directory up
    'toolsDir': os.path.join(scriptDir, 'tools'),           # The patch tools are downloaded to the 'tools' subdirectory
    'optionsDir': scriptDir,                                # The patch  configuration options are in the 'options' subdirectory
    'keystore': os.path.join(scriptDir, 'patch.keystore'),  # The keystore to sign the patched APKs is next to the script
    'defaultPatchSource': 'rv',                            # Select whether the default provider should be ReVanced or ReVancedExtended
    'patchSources': {
        'rv': {
            'patches': {
                'proj': 'revanced/revanced-patches',
                'ver': 'latest',                            # Use 'latest' or specify the desired release version
                'type': 'application/java-archive',         # The content type of the file (for download identification)
            },
            'integrations': {
                'proj': 'revanced/revanced-integrations',
                'ver': 'latest',                            # Use 'latest' or specify the desired release version
                'type': 'application/vnd.android.package-archive', # The content type of the file (for download identification)
            },
            'cli': {
                'proj': 'revanced/revanced-cli',
                'ver': 'latest',                            # Use 'latest' or specify the desired release version
                'type': 'application/java-archive',         # The content type of the file (for download identification)
            },
            'prepend': 'RV '                                # Prepend this to the patched output file names
        },
        'rvx': {
            'patches': {
                'proj': 'inotia00/revanced-patches',
                'ver': 'latest',                            # Use 'latest' or specify the desired release version
                'type': 'application/jar',                  # The content type of the file (for download identification)
            },
            'integrations': {
                'proj': 'inotia00/revanced-integrations',
                'ver': 'latest',                            # Use 'latest' or specify the desired release version
                'type': 'application/vnd.android.package-archive', # The content type of the file (for download identification)
            },
            'cli': {
                'proj': 'inotia00/revanced-cli',
                'ver': 'latest',                            # Use 'latest' or specify the desired release version
                'type': 'application/jar',                  # The content type of the file (for download identification)
            },
            'prepend': 'RVX '                               # Prepend this to the patched output file names
        }
    }
}

import argparse
import glob
import json
import re
import shutil
import subprocess
import tempfile
import urllib.request

class Patcher:
    tools = ['cli', 'patches', 'integrations']

    def __init__(self, args):
        patchSourceData = args.patchSrc
        self.outPrepend = patchSourceData['prepend']
        self.outDir = args.outDir
        Patcher.__ensureDirectory(self.outDir)
        self.toolsDir = args.toolsDir
        Patcher.__ensureDirectory(self.toolsDir)
        self.optionsDir = args.optionsDir
        Patcher.__ensureDirectory(self.optionsDir)
        self.keystorePath = args.keystore
        Patcher.__ensureDirectory(os.path.dirname(self.keystorePath))
        for tool in self.tools:
            Patcher.__ensureTool(
                patchSourceData[tool]['proj'],
                getattr(args, tool + '_version'),
                patchSourceData[tool]['type'],
                self.toolsDir)
        self.toolPaths = {
            i: glob.glob(os.path.join(self.toolsDir, '*{}*'.format(i)))[0] for i in self.tools
        }

    def Patch(self, srcPath):
        srcFile = os.path.basename(srcPath)
        outPath = os.path.join(self.outDir, self.outPrepend + srcFile)
        optionsFile = os.path.splitext(Patcher.__normalFileName(srcFile))[0] + '.json'
        tempDir = os.path.join(tempfile.gettempdir(), 'revanced-resource-cache')
        print('### Patching {}...'.format(srcFile))
        try:
            subprocess.run([
                'java', '-jar',
                self.toolPaths['cli'], 'patch',
                '--patch-bundle=' + self.toolPaths['patches'],
                '--merge=' + self.toolPaths['integrations'],
                '--options=' + os.path.join(self.optionsDir, optionsFile),
                '--keystore=' + self.keystorePath,
                '--temporary-files-path=' + tempDir,
                '--out=' + outPath,
                srcPath
            ], stdout=sys.stdout, stderr=sys.stderr, check=True)
            print('### Finished patching {} successfully!'.format(os.path.abspath(outPath)))
        except subprocess.CalledProcessError:
            print('### Failed to patch {}!'.format(srcFile))
        try:
            # Purge the temp directory after patching (the built-in purger likes to fail)
            shutil.rmtree(tempDir)
        except:
            pass

    @staticmethod
    def __ensureDirectory(directory):
        '''Ensures that the path's directory exists'''
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass

    @staticmethod
    def __normalFileName(path):
        '''Removes version strings from the file name'''
        regex = r'\b\s*v?\d+(?:\.\d+)*(?:-[^\s]*)?\b'
        return re.sub(regex, '', path)

    @staticmethod
    def __ensureTool(project, version, content_type, directory):
        '''Prepares one ReVanced tool'''

        def clearExistingTools(directory, assetName):
            '''Deletes older versions of the given tool'''
            regex = r'^([^\d]*)v?\d+(?:\.\d+(?:\.\d+)?)?[^\d]*(\.[^\.]+)$'
            assetGlob = re.sub(regex, r'\1*\2', assetName)
            for file in glob.glob(os.path.join(directory, assetGlob)):
                os.remove(file)

        if version != 'latest':
            version = 'tags/v' + version.lstrip('v')
        url = 'https://api.github.com/repos/{0}/releases/{1}'.format(project, version)
        releaseData = json.loads(urllib.request.urlopen(url).read())
        for asset in releaseData['assets']:
            if (asset['content_type'] == content_type):
                assetName = asset['name']
                assetPath = os.path.join(directory, assetName)
                if (not os.path.exists(assetPath)):
                    Patcher.__ensureDirectory(directory)
                    clearExistingTools(directory, assetName)
                    assetUrl = asset['browser_download_url']
                    urllib.request.urlretrieve(assetUrl, assetPath)

def main():
    def raise_(ex): raise ex
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'files', nargs='*',
        type=lambda x: x if os.path.exists(x) else raise_(argparse.ArgumentTypeError("file not found: " + x)),
        default=glob.glob(os.path.join(settings['srcDir'], '*.apk')),
        help='One or more APK file to patch. Patching all APKs in the default source directory if unspecified.')
    parser.add_argument('--keystore', '-k', default=os.path.abspath(settings['keystore']), help='The path of the keystore file with which to sign the APKs (default: %(default)s)')
    parser.add_argument('--optionsDir', default=os.path.abspath(settings['optionsDir']), help='The directory to store patch options files in (default: %(default)s)')
    parser.add_argument('--outDir', '-o', default=os.path.abspath(settings['outDir']), help='The directory to write patched APKs to (default: %(default)s)')
    parser.add_argument(
        '--patchSrc', choices=settings['patchSources'], default=settings['defaultPatchSource'],
        type=lambda x : settings['patchSources'][x], help='The patch source to use. Use "rv" for ReVanced and "rvx" for ReVanced Extended (default: %(default)s).')
    parser.add_argument('--toolsDir', default=os.path.abspath(settings['toolsDir']), help='The directory to store tools and patches in (default: %(default)s)')
    for tool in Patcher.tools:
        parser.add_argument(
            '--{}-version'.format(tool),
            type=lambda str : str if re.match(r'^latest|v?\d+(?:\.\d+)*(?:-[^ ]+)?$', str) else raise_(argparse.ArgumentTypeError("invalid version")),
            default=settings['patchSources'][settings['defaultPatchSource']][tool]['ver'], help='The tool version to use (default: %(default)s)')
    args = parser.parse_args()

    patcher = Patcher(args)
    for path in args.files:
        patcher.Patch(path)

if __name__ == "__main__":
    main()