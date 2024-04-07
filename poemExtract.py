# 1、提取poem.txt文件中的诗句
# 2、序号人名不提取，只提取诗句，如3.宝刀偃月双飞电，紫马嘶云散五花。——冯恩《游侠曲》，只提取“宝刀偃月双飞电，紫马嘶云散五花”
# 3、存成如下格式 "此身原本不知愁,最怕万一见温柔", "海底月是天上月,眼前人是心上人","遇事不决,可问春风",  "一年好景君须记,最是橙黄橘绿时"分行存储

import re
import os
def cleanPoem():
    with open("poem.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if len(line) == 0 or line[0].isdigit() or "——" in line or line == "图片":
            continue
        cleaned_lines.append(line)
    
    with open("poem.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

def extractPoem():
    poems = []
    with open("poem.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            # 提取诗句
            if line.find("——") != -1:
                poem = re.search(r"\d+\.(.*?)——", line)
                if poem:
                    poems.append(poem.group(1).strip())
    return poems

def savePoem(poems):
    with open("poemExtract.txt", "a", encoding="utf-8") as f:
        for poem in poems:
            f.write(poem + "\n")

if __name__ == "__main__":
    cleanPoem()
    poems = extractPoem()
    savePoem(poems)
    print("提取诗句完成！")