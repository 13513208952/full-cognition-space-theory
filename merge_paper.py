#!/usr/bin/env python3
"""
合并论文各部分为完整文档
用法: python merge_paper.py
输出: full_paper.md 和 full_paper_stats.txt
"""

import os
import re
from datetime import datetime

PARTS = [
    "paper_01_abstract_intro.md",
    "paper_02_preliminaries.md",
    "paper_03_definitions.md",
    "paper_04_theorems1_2.md",
    "paper_05_theorems3_4.md",
    "paper_06_theorem5_implications.md",
    "paper_08_architecture_robustness.md",
    "paper_07_discussion_conclusion.md",
]

OUTPUT_FILE = "full_paper.md"
STATS_FILE  = "full_paper_stats.txt"

def merge():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    combined   = []
    missing    = []

    for fname in PARTS:
        fpath = os.path.join(script_dir, fname)
        if not os.path.exists(fpath):
            missing.append(fname)
            continue
        with open(fpath, encoding="utf-8") as f:
            content = f.read().strip()
        combined.append(content)
        print(f"  OK  {fname}  ({len(content):,} chars)")

    if missing:
        print(f"\n[WARNING] 缺少文件: {missing}")

    full_text = "\n\n---\n\n".join(combined)

    # 写出完整论文
    out_path = os.path.join(script_dir, OUTPUT_FILE)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    # 统计信息
    word_count  = len(full_text)
    line_count  = full_text.count("\n")
    theo_count  = len(re.findall(r"(?m)^\*\*定理\s*[\d.]+", full_text))
    proof_count = len(re.findall(r"(?m)^\*\*证明\*\*", full_text))
    ref_count   = len(re.findall(r"(?m)^\d+\.", full_text[-3000:]))  # 粗估参考文献数

    stats = f"""论文统计 — {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*45}
总字符数  : {word_count:,}
总行数    : {line_count:,}
定理数    : {theo_count}
证明数    : {proof_count}
参考文献  : 约 {ref_count} 条
合并部分  : {len(combined)}/{len(PARTS)}
输出文件  : {OUTPUT_FILE}
"""
    stats_path = os.path.join(script_dir, STATS_FILE)
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write(stats)

    print(f"\n{'='*45}")
    print(stats)
    print(f"完整论文已写入: {out_path}")

if __name__ == "__main__":
    print("开始合并论文各部分...\n")
    merge()
