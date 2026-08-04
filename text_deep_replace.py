#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从脚本所在目录开始，递归扫描全部文件和文件夹：
1. 若文件/文件夹名称中含有 "xxxx"，重命名为 "kxcymc"。
2. 若文本文件内容中含有 "xxxx"，替换为 "kxcymc"。
"""

import os
import re

OLD = "byted"
NEW = "katra"
# 不区分大小写匹配 xxxx / xxxx / xxxx 等
PATTERN = re.compile(re.escape(OLD), re.IGNORECASE)

# 脚本所在目录作为根目录
ROOT = os.path.dirname(os.path.abspath(__file__))
# 脚本自身文件名，避免处理自己
SELF = os.path.basename(os.path.abspath(__file__))


def replace_in_file_content(path):
    """替换文本文件内容中的 OLD；二进制文件自动跳过。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError, OSError):
        # 二进制文件或无法读取，跳过内容替换
        return
    if PATTERN.search(content):
        new_content = PATTERN.sub(NEW, content)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[内容] {path}")
        except (PermissionError, OSError) as e:
            print(f"[内容失败] {path}: {e}")


def rename_if_needed(parent, name):
    """若名称含 OLD 则重命名，返回最终名称。"""
    if PATTERN.search(name):
        new_name = PATTERN.sub(NEW, name)
        old_path = os.path.join(parent, name)
        new_path = os.path.join(parent, new_name)
        try:
            os.rename(old_path, new_path)
            print(f"[重命名] {old_path} -> {new_path}")
            return new_name
        except OSError as e:
            print(f"[重命名失败] {old_path}: {e}")
            return name
    return name


def main():
    # 自底向上遍历，先处理内容和文件名，再处理文件夹名，避免路径失效
    for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
        # 处理文件
        for fname in filenames:
            if dirpath == ROOT and fname == SELF:
                continue  # 跳过脚本自身
            # 先替换内容
            replace_in_file_content(os.path.join(dirpath, fname))
            # 再重命名文件
            rename_if_needed(dirpath, fname)

        # 处理子文件夹名
        for dname in dirnames:
            rename_if_needed(dirpath, dname)

    print("完成。")


if __name__ == "__main__":
    main()
