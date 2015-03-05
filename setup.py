from distutils.core import setup
import py2exe

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>myProgram</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.30729.4918"
            processorArchitecture="X86"
            publicKeyToken="1fc8b3b9a1e18e3b"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

"""
installs manifest and icon into the .exe
but icon is still needed as we open it
for the window icon (not just the .exe)
changelog and logo are included in dist
"""

import os
# find pythoncard resources, to add ad 'data_files'
pycard_resources = []
for filename in os.listdir('.'):
    if filename.find('.rsrc.') > -1:
        pycard_resources += [filename]

includes = []
# includes for PythonCard
for comp in ['button', 'image', 'staticbox', 'statictext',
             'textarea', 'textfield', 'passwordfield']:
    includes += ['PythonCard.components.' + comp]
#includes for lyric engine
files = os.listdir(os.path.join(os.path.dirname(__file__), 'lyric_engine', 'modules'))
import re
test = re.compile('[a-z].*\.py$')
files = [x for x in files if test.search(x)]
def filenameToModuleName(f):
    return 'lyric_engine.modules.' + os.path.splitext(f)[0]
moduleNames = [filenameToModuleName(x) for x in files]

includes += moduleNames
includes += ['lyric_engine.include.common', 'lyric_engine.include.lyric_base']
print(includes)

setup(
#    console = ['py_lyric_retriever.py'],
    windows = [
        {
            "script": "py_lyric_retriever.py",
            "icon_resources": [(1, "lyric_ico.ico")],
            "other_resources": [(24,1,manifest)],
        }
    ],
    options = {
        "py2exe": {
            "optimize": 2,
            "compressed": 1,
            "includes": includes,
        }
    },
    data_files = [('', ['lyric_ico.ico', 'waiting.gif'] + pycard_resources)]
)

