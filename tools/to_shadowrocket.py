"""把 rules.yaml（OpenClash 规则）转成小火箭用的 shadowrocket.conf。

用法：python tools/to_shadowrocket.py
GitHub Actions 会在 rules.yaml 改动后自动运行。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / "rules.yaml"
TEMPLATE = ROOT / "shadowrocket.template.conf"
OUTPUT = ROOT / "shadowrocket.conf"

# Clash 和小火箭写法不同的规则类型
TYPE_MAP = {
    "DST-PORT": "DEST-PORT",
    "SRC-IP-CIDR": "SRC-IP",
    "MATCH": "FINAL",
}
# 小火箭不支持的类型，跳过
UNSUPPORTED = {"PROCESS-NAME", "PROCESS-PATH", "IN-PORT", "IN-TYPE", "NETWORK", "SUB-RULE"}
BUILTIN = {"DIRECT", "REJECT", "PROXY", "REJECT-DROP", "REJECT-NO-DROP"}


def read_rules():
    rules = []
    for raw in RULES.read_text(encoding="utf-8").splitlines():
        line = raw.split(" #", 1)[0].strip()
        if not line.startswith("- "):
            continue
        rules.append(line[2:].strip().strip("'\""))
    return rules


def main():
    template = TEMPLATE.read_text(encoding="utf-8")
    groups = set(re.findall(r"^(.+?)\s*=\s*(?:select|url-test|fallback|load-balance)", template, re.M))

    out, warnings = [], []
    for rule in read_rules():
        parts = [p.strip() for p in rule.split(",")]
        kind = parts[0].upper()
        if kind in UNSUPPORTED:
            warnings.append(f"跳过（小火箭不支持）: {rule}")
            continue
        parts[0] = TYPE_MAP.get(kind, kind)
        if parts[0] == "FINAL":
            warnings.append(f"跳过（模板里已有 FINAL）: {rule}")
            continue
        policy = parts[2] if len(parts) > 2 else ""
        if policy and policy not in groups and policy.upper() not in BUILTIN:
            warnings.append(f"策略组不存在，请在模板里补上: {policy}  ({rule})")
        out.append(",".join(parts))

    # 去掉模板开头的说明注释，换成自动生成提示
    body = re.sub(r"\A(?:#.*\n)+\s*", "", template)
    header = "# 小火箭配置：由 rules.yaml 自动生成，不要手改，改 rules.yaml 或 shadowrocket.template.conf\n\n"
    OUTPUT.write_text(header + body.replace("{{CUSTOM_RULES}}", "\n".join(out)), encoding="utf-8", newline="\n")
    print(f"已生成 {OUTPUT.name}，自定义规则 {len(out)} 条")
    for w in warnings:
        print("警告:", w)
    return 1 if any("策略组不存在" in w for w in warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
