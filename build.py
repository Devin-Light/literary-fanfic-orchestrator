#!/usr/bin/env python3
"""递归解析 <!-- #include "路径" --> 指令，生成完整手稿。"""
import re, sys, os

INCLUDE_RE = re.compile(r'<!--\s*#include\s*"([^"]+)"\s*-->')

def resolve(filepath, visited=None):
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
                included = os.path.join(base, path)
                yield from resolve(included, visited.copy())
            else:
                yield line

if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '作品名.md'
    for line in resolve(root):
        sys.stdout.write(line)
