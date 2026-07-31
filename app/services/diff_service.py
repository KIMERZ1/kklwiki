import difflib

def diff_lines(old_content, new_content):
    old_lines = (old_content or "").splitlines()
    new_lines = (new_content or "").splitlines()
    return list(
        difflib.unified_diff(old_lines, new_lines, fromfile="이전", tofile="이후", lineterm="")
    )
