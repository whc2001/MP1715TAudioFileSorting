from math import ceil, floor
import re
import os

# ===设置===
#OUTPUT_DIR = ".\Sorted"

# 输出文件名模板
FILENAME_OUTPUT_TEMPLATE = "%title%(%artist%)"

# 输入文件名模板
FILENAME_INPUT_TEMPLATE = re.compile(r"(?P<artist>.+?) - (?P<title>.+)")

# 输出文件名最大长度字节数（一个汉字算2个）
FILENAME_LENGTH_LIMIT = 30

# 标题最大占输出文件名的百分之多少
FILENAME_TITLE_MAX_PERCENT = 0.7
# =========

def StrLen(text):
    strLen = len(text)
    strLenUtf8 = len(text.encode("utf-8"))
    return int((strLenUtf8 - strLen) / 2) + strLen

def GetAvailableLength(template):
    return FILENAME_LENGTH_LIMIT - StrLen(template.replace("%artist%", "").replace("%title%", ""))

def TruncateStr(text, length, ellipse=".."):
    if StrLen(text) <= length:
        return text
    availableLength = length - StrLen(ellipse)
    truncatedText = ""
    for char in text:
        charLen = max(len(char), len(char.encode("utf-8")))
        if StrLen(truncatedText) + charLen >= availableLength:
            break
        truncatedText += char
    return truncatedText + ellipse

def GetRenameFileName(filename):
    fileNameMatch = FILENAME_INPUT_TEMPLATE.search(filename)
    title = fileNameMatch.group("title")
    artist = fileNameMatch.group("artist")
    titleLength = min(StrLen(title), ceil(GetAvailableLength(FILENAME_OUTPUT_TEMPLATE) * FILENAME_TITLE_MAX_PERCENT))
    artistLength = FILENAME_LENGTH_LIMIT - titleLength - 1
    title = TruncateStr(title, titleLength)
    artist = TruncateStr(artist, artistLength)
    return FILENAME_OUTPUT_TEMPLATE.replace("%title%", title).replace("%artist%", artist)

dire = input()
for file in os.listdir(dire):
    oldName, ext = os.path.splitext(file)
    newName = GetRenameFileName(oldName)
    print(f"{oldName}: {StrLen(oldName)} -> {newName}: {StrLen(newName)}")
    os.rename(f"{dire}\\{oldName}{ext}", f"{dire}\\{newName}{ext}")
