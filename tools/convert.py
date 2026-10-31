"""把 rules.yaml（OpenClash 规则）转成小火箭和圈X用的配置。

输出：
  shadowrocket.conf       小火箭配置（规则直接写在 [Rule] 里）
  quantumultx.conf        圈X配置
  quantumultx-rules.list  圈X自定义分流（quantumultx.conf 里作为远程分流引用）

用法：python tools/convert.py
GitHub Actions 会在 rules.yaml 或模板改动后自动运行。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / "rules.yaml"
HEADER = "# 由 rules.yaml 自动生成，不要手改，改 rules.yaml 或对应的 *.template.conf\n\n"

# 各客户端和 Clash 写法不同的规则类型；None 表示不支持，跳过
SHADOWROCKET_TYPES = {
    "DST-PORT": "DEST-PORT",
    "SRC-IP-CIDR": "SRC-IP",
    "PROCESS-NAME": None, "PROCESS-PATH": None, "IN-PORT": None,
    "IN-TYPE": None, "NETWORK": None, "SUB-RULE": None, "MATCH": None,
}
QUANTUMULTX_TYPES = {
    "DOMAIN": "HOST",
    "DOMAIN-SUFFIX": "HOST-SUFFIX",
    "DOMAIN-KEYWORD": "HOST-KEYWORD",
    "DOMAIN-WILDCARD": "HOST-WILDCARD",
    "IP-CIDR": "IP-CIDR",
    "IP-CIDR6": "IP6-CIDR",
    "GEOIP": "GEOIP",
    "IP-ASN": "IP-ASN",
}
BUILTIN = {"DIRECT", "REJECT", "PROXY", "REJECT-DROP", "REJECT-NO-DROP"}


def read_rules():
    rules = []
    for raw in RULES.read_text(encoding="utf-8").splitlines():
        line = raw.split(" #", 1)[0].strip()
        if line.startswith("- "):
            rules.append([p.strip() for p in line[2:].strip().strip("'\"").split(",")])
    return rules


def load_template(name):
    # 去掉模板开头的说明注释
    return re.sub(r"\A(?:#.*\n)+\s*", "", (ROOT / name).read_text(encoding="utf-8"))


def write(name, text):
    (ROOT / name).write_text(HEADER + text, encoding="utf-8", newline="\n")
    print(f"已生成 {name}")


def check_policy(policy, groups, rule, client, warnings):
    if policy and policy not in groups and policy.upper() not in BUILTIN:
        warnings.append(f"[{client}] 策略组不存在，请在模板里补上: {policy}  ({','.join(rule)})")


def build_shadowrocket(rules, warnings):
    template = load_template("shadowrocket.template.conf")
    groups = set(re.findall(r"^(.+?)\s*=\s*(?:select|url-test|fallback|load-balance)", template, re.M))
    out = []
    for parts in rules:
        kind = parts[0].upper()
        mapped = SHADOWROCKET_TYPES.get(kind, kind)
        if mapped is None:
            warnings.append(f"[小火箭] 跳过不支持的规则: {','.join(parts)}")
            continue
        check_policy(parts[2] if len(parts) > 2 else "", groups, parts, "小火箭", warnings)
        out.append(",".join([mapped] + parts[1:]))
    write("shadowrocket.conf", template.replace("{{CUSTOM_RULES}}", "\n".join(out)))
    return len(out)


def build_quantumultx(rules, warnings):
    template = load_template("quantumultx.template.conf")
    groups = set(re.findall(r"^(?:static|available|round-robin|url-latency-benchmark|dest-hash|ssid)=([^,]+)", template, re.M))
    out = []
    for parts in rules:
        mapped = QUANTUMULTX_TYPES.get(parts[0].upper())
        if mapped is None or len(parts) < 3:
            warnings.append(f"[圈X] 跳过不支持的规则: {','.join(parts)}")
            continue
        policy = parts[2]
        if policy.upper() in BUILTIN:
            policy = policy.lower()
        check_policy(policy, groups, parts, "圈X", warnings)
        out.append(",".join([mapped, parts[1], policy]))
    write("quantumultx-rules.list", "\n".join(out) + "\n")
    write("quantumultx.conf", template)
    return len(out)


def main():
    rules = read_rules()
    warnings = []
    sr = build_shadowrocket(rules, warnings)
    qx = build_quantumultx(rules, warnings)
    print(f"共 {len(rules)} 条自定义规则：小火箭 {sr} 条，圈X {qx} 条")
    for w in warnings:
        print("警告:", w)
    return 1 if any("策略组不存在" in w for w in warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
