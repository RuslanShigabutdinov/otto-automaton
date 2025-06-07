from libs._path import currentPath
import os

files = [
    'chageFields.py',
    'createSession.py'
]
envFolder = f'{currentPath()}\\env'

if not os.path.isdir(f'{currentPath()}/bat'):
    os.makedirs(f'{currentPath()}/bat')

for file in files:
     with open(f'{currentPath()}/bat/{file.replace('.py', '.bat')}', "w") as f:
        f.write('@echo off\n')
        f.write(f'call {envFolder}\\Scripts\\activate\n')
        f.write(f'python {currentPath()}\\createSession.py %*\n')
        f.write(f'pause')