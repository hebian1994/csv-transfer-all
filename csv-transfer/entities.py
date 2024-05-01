from typing import List, Dict, Any


class Template:
    def __init__(self, templateName, headerLineNum,
                 rowDelFromHead, rowDelFromTail, colDeleted, colTransfer, colRename):
        self.templateName = templateName
        self.headerLineNum = headerLineNum
        self.rowDelFromHead = rowDelFromHead
        self.rowDelFromTail = rowDelFromTail
        self.colDeleted = colDeleted
        self.colTransfer = colTransfer
        self.colRename = colRename

    def __str__(self):
        return f"Data(colRename={self.colRename[0].nowColName}')"


class ColTransfer:
    def __init__(self, colName, tranType, reg):
        self.colName = colName
        self.tranType = tranType
        self.reg = reg

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(d['colName'], d['tranType'], d['reg'])


class ColRename:
    def __init__(self, nowColName, newColName):
        self.nowColName = nowColName
        self.newColName = newColName

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(d['nowColName'], d['newColName'])


# 定义一个类来表示你期望的JSON数据的结构
class UploadReq:
    def __init__(self, data: []):
        self.data = data

    # 如果需要，可以定义一个方法来将对象转换为字典
    def to_dict(self):
        return {
            'data': self.data
        }

    # 定义一个方法来返回对象的字符串表示
    def __str__(self):
        return f"UploadReq(data={self.data}')"
