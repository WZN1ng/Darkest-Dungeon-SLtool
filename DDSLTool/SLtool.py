import os
import shutil
import json
from sys import stdin
import time
import psutil

class SLtool:
    def __init__(self):
        self.fileRoot = ""
        self.fileList = list()
        self.targetRoot = os.path.join(os.getcwd(), "template_files")
        self.gameRoot = ""
        self.roots = "./root.json"
        self.currIdx = -1

        if not os.path.exists(self.targetRoot):
            os.makedirs(self.targetRoot)
        
        self._loadRoot()
        self._updateFileList()
        print(self.fileRoot, self.fileList, self.currIdx, self.gameRoot)

    def _loadRoot(self):
        if os.path.exists(self.roots):
            dtmp = dict()
            with open(self.roots, 'r') as f:
                dtmp = json.load(f)
                f.close()
            f1 = f2 = False
            if 'fileRoot' in dtmp and os.path.exists(dtmp['fileRoot']):
                self.fileRoot = dtmp['fileRoot']
                print('存档位置读取完成!')
                f1 = True
            if 'gameRoot' in dtmp and os.path.exists(dtmp['gameRoot']):
                self.gameRoot = dtmp['gameRoot']
                print('游戏位置读取完成!')
                f2 = True
            return f1 & f2
        else:
            print('缺少文件 ' + self.roots)
            return False

    def SaveRoot(self):
        with open(self.roots, 'w') as f:
            dtmp = { "fileRoot": self.fileRoot,
                    "gameRoot": self.gameRoot}
            json.dump(dtmp, f)
            f.close()        
        print('默认存档位置已保存!')

    def _updateFileList(self):
        self.fileList = [x for x in os.listdir(self.targetRoot)]
        self.currIdx = len(self.fileList) - 1

    def changeIdx(self, idx):
        if idx < len(self.fileList):
            self.currIdx = idx
            print('默认存档已改为 ' + self.fileList[self.currIdx])
            return True
        else:
            return False

    def changeFileRoot(self, fileRoot):
        self.fileRoot = fileRoot
        self.SaveRoot()
    
    def copyFile(self, idx = -1):
        if idx == -1:
            idx = self.currIdx
        if idx < len(self.fileList):
            t = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
            source = self.fileRoot
            target = os.path.join(self.targetRoot, t)
            if os.path.exists(target):
                shutil.rmtree(target)
            
            shutil.copytree(source, target)
            self.fileList.append(t)
            self.currIdx = len(self.fileList) - 1
            print("备份成功 " + self.fileList[self.currIdx])
            return True
        else:
            return False

    def loadFile(self, idx = -1):
        if idx == -1:
            idx = self.currIdx
        if idx < len(self.fileList):
            t = self.fileList[idx]
            source = os.path.join(self.targetRoot, t)
            target = self.fileRoot
            # if not os.path.exists(source):
            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.copytree(source, target)
            print("读档成功 " + self.fileList[self.currIdx])
            self._killGameAndSteam()
            print("已关闭游戏和Steam")
            # if os.path.exists(self.gameRoot):
            #     currPath = os.getcwd()
            #     print(currPath)
            #     os.chdir(self.gameRoot)
            #     os.startfile('Darkest.exe')
            #     print("已重启游戏")
            #     os.chdir(currPath)
            return True
        else:
            return False

    def _killGameAndSteam(self):
        tgt = ["Darkest.exe", "steam.exe"]
        for proc in psutil.process_iter():
            if proc.name() in tgt and proc.is_running():
                proc.terminate()


# if __name__ == '__main__':


