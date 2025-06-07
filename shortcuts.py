from _path import currentPath
import os
import win32com.client

files = [
    'changeFields',
    'createSession'
]

imgPath = f'{currentPath()}/img'

envFolder = f'{currentPath()}\\env'

def createBat(file):
    with open(f'{currentPath()}/_bat/{file}.bat', "w") as f:
        f.write('@echo off\n')
        f.write(f'call {envFolder}\\Scripts\\activate\n')
        f.write(f'python {currentPath()}\\{file}.py %*\n')

def createShortcut(targetFolder, file, description=""):
    batPath = f'{targetFolder}/{file}'
    shortcutPath = f'{currentPath()}/shortcuts/{file}.lnk'
    
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcutPath)

    iconPath = f'{imgPath}/{file}.ico'
    shortcut.IconLocation = f'{iconPath},0'
    
    shortcut.TargetPath = batPath
    shortcut.WorkingDirectory = targetFolder
    shortcut.Description = description
    shortcut.Save()

def main():
    targetFolder = f'{currentPath()}/_bat'
    if not os.path.isdir(targetFolder):
        os.makedirs(targetFolder)
    if not os.path.isdir( f'{currentPath()}/shortcuts'):
        os.makedirs( f'{currentPath()}/shortcuts')
    for file in files:
        createBat(file)
        createShortcut(targetFolder, file)


if __name__ == '__main__':
  main()