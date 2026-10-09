import os
import subprocess
from pathlib import Path

def run_cmd(cmd):
    print(f"\n> 执行命令: {' '.join(cmd)}")
    res = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    print("stdout:", res.stdout)
    if res.stderr:
        print("stderr:", res.stderr)
    return res

def has_staged_changes():
    r = run_cmd(["git", "diff", "--cached", "--quiet"])
    return r.returncode != 0

def process_all_md():
    print(f"✅ commit注释 = MD文件名（自动去掉.md后缀），启用强制推送 git push -f")

    while True:
        md_list = list(Path(".").glob("*.md"))
        if not md_list:
            print("\n🎉 全部MD处理完成！")
            break
        
        md_file = md_list[0]
        commit_msg = md_file.stem  # stem自动剔除后缀，只保留文件名
        print(f"\n===== 处理：{md_file.name}  commit注释：{commit_msg} =====")
        try:
            run_cmd(["git", "add", str(md_file)])

            if has_staged_changes():
                run_cmd(["git", "commit", "-m", commit_msg])
                # 强制推送
                run_cmd(["git", "push", "-f"])
                print(f"✅ {md_file.name} 强制推送成功")
            else:
                print(f"ℹ️ {md_file.name}远端已有相同内容，跳过提交推送")
            
            os.remove(md_file)
            print(f"🗑️ 已删除本地 {md_file.name}")

        except Exception as e:
            print(f"❌ 处理 {md_file.name} 异常：{e}")
            print("继续下一个文件\n")

if __name__ == "__main__":
    process_all_md()
