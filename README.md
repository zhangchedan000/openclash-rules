# openclash-rules
OpenClash 自定义分流规则

## 文件说明
| 文件 | 用途 |
| --- | --- |
| `rules.yaml` | OpenClash 自定义规则，**只改这个** |
| `shadowrocket.conf` | 小火箭配置，改完 `rules.yaml` 后由 GitHub Actions 自动生成 |
| `shadowrocket.template.conf` | 小火箭配置模板（策略组、通用规则） |
| `tools/to_shadowrocket.py` | 转换脚本 |

## 小火箭一键导入
在 iPhone Safari 打开：

```
shadowrocket://config/add/https://cdn.jsdelivr.net/gh/zhangchedan000/openclash-rules@main/shadowrocket.conf
```

或在小火箭「配置」页右上角 ＋，粘贴：

```
https://cdn.jsdelivr.net/gh/zhangchedan000/openclash-rules@main/shadowrocket.conf
```

导入后点这个配置 →「使用配置」，首页「全局路由」选「配置」。节点在首页用订阅添加，策略组按节点名字自动归类（香港/美国/英国/德国/家宽）。
