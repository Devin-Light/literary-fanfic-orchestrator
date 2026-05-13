#!/usr/bin/env python3
"""递归拼接正文文件，生成完整手稿。

两种模式：
1. 指定 .md 文件：解析 <!-- #include "路径" --> 指令，递归展开
2. 指定目录：遍历 卷*/ 子目录，按文件名排序拼接

智能检测：若子目录内同时存在导航文件（纯 include 指令）和章文件，
        只解析导航文件；否则按文件名顺序读取所有 .md。
"""

import re, sys, os

_CHINESE_NUMS = str.maketrans('一二三四五六七八九十', '1234567890')

def _sort_key(name):
    """提取文件名中的中文数字并转换为阿拉伯数字，用于正确排序。"""
    return name.translate(_CHINESE_NUMS)

INCLUDE_RE = re.compile(r'<!--\s*#include\s*"([^"]+)"\s*-->')

def parse_includes(filepath, visited=None):
    """递归解析 include 指令展开文件。"""
    if visited is None:
        visited = set()
    abspath = os.path.abspath(filepath)
    if not os.path.isfile(abspath):
        raise FileNotFoundError(f"文件不存在: {abspath}")
    if abspath in visited:
        raise RecursionError(f"循环引用: {abspath}")
    visited.add(abspath)
    base = os.path.dirname(abspath)
    with open(abspath, 'r', encoding='utf-8') as f:
        for line in f:
            m = INCLUDE_RE.match(line.strip())
            if m:
                path = m.group(1).strip()
                if not path:
                    raise ValueError(f"{abspath}: include 路径不能为空")
                target = os.path.join(base, path)
                yield from parse_includes(target, visited.copy())
            else:
                yield line

def _md_files_sorted(dirpath):
    """返回目录下按文件名排序的所有 .md 文件路径。"""
    return sorted(
        [os.path.join(dirpath, f) for f in os.listdir(dirpath) if f.endswith('.md')],
        key=_sort_key
    )

def _find_nav(md_files):
    """在 .md 文件中找到首个导航文件（非章节正文），没有则返回 None。

    导航文件特征：每行要么为空，要么是 include 指令，要么是 HTML 注释。
    章节正文文件特征：包含非注释、非 include 的实际内容。
    """
    for f in md_files:
        with open(f, 'r', encoding='utf-8') as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped:
                    continue
                if INCLUDE_RE.match(stripped):
                    continue
                if stripped.startswith('<!--') and stripped.endswith('-->'):
                    continue
                break  # 有实际内容，不是导航文件
            else:
                return f  # 全部行都是 include、注释或空行
    return None

def walk_and_read(root_dir):
    """遍历根目录下的子目录，按序拼接正文。"""
    for name in sorted(os.listdir(root_dir), key=_sort_key):
        full = os.path.join(root_dir, name)
        if not os.path.isdir(full):
            continue
        md_files = _md_files_sorted(full)
        if not md_files:
            continue
        nav = _find_nav(md_files)
        if nav:
            yield from parse_includes(nav)
        else:
            for f in md_files:
                with open(f, 'r', encoding='utf-8') as fh:
                    yield from fh
                yield '\n'

def build(root):
    root_abs = os.path.abspath(root)
    if not os.path.exists(root_abs):
        raise FileNotFoundError(f"路径不存在: {root_abs}")
    if os.path.isdir(root_abs):
        yield from walk_and_read(root_abs)
    else:
        yield from parse_includes(root_abs)

if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    for line in build(root):
        sys.stdout.write(line)
