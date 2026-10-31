# openclash-rules
OpenClash 自定义分流规则

## 文件说明
| 文件 | 用途 |
| --- | --- |
| `rules.yaml` | OpenClash 自定义规则，**只改这个** |
| `shadowrocket.conf` | 小火箭配置，改完 `rules.yaml` 后由 GitHub Actions 自动生成 |
| `quantumultx.conf` / `quantumultx-rules.list` | 圈X配置和自定义分流，同样自动生成 |
| `mihomo.yaml` | OpenClash / Clash Verge 用的分组+规则（不含节点），在 Sub-Store「文件」里选「mihomo 配置」注入节点 |
| `*.template.conf` / `mihomo.template.yaml` | 小火箭 / 圈X / mihomo 配置模板（策略组、通用规则） |
| `tools/convert.py` | 转换脚本 |

## 小火箭一键导入
在 iPhone Safari 打开：

```
shadowrocket://config/add/https://testingcf.jsdelivr.net/gh/zhangchedan000/openclash-rules@main/shadowrocket.conf
```

或在小火箭「配置」页右上角 ＋，粘贴：

```
https://testingcf.jsdelivr.net/gh/zhangchedan000/openclash-rules@main/shadowrocket.conf
```

导入后点这个配置 →「使用配置」，首页「全局路由」选「配置」。节点在首页用订阅添加，策略组按节点名字自动归类（香港/美国/英国/德国/家宽）。

## 圈X 导入
圈X 右下角风车 →「配置文件」→「下载」，粘贴：

```
https://testingcf.jsdelivr.net/gh/zhangchedan000/openclash-rules@main/quantumultx.conf
```

下载后在「节点」→「引用」里添加你的订阅，首页运行模式选「规则分流」。策略组和小火箭一样按节点名字自动归类。
