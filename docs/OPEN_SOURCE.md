# 维护与发布检查

[首页](../README.md) · [English](../README.en.md) · [贡献约定](../CONTRIBUTING.md) · [更新摘要](../CHANGELOG.md)

这是一份可重复使用的发布清单。运行过的检查应随版本记录命令、环境和结果；下面列出的要求本身不表示已经执行。本库用于帮助研究者构造和审查证明。

## 许可与内容边界

原创代码与原创文档使用 [MIT](../LICENSE)。论文 PDF、arXiv source、附带代码、图表和引用仍遵守各自许可，见[第三方说明](../THIRD_PARTY_NOTICES.md)。优先写自己的解释和推导，保留准确引用；不要把第三方正文或实现当作原创提交。

来源 commit 与迁入范围见 [PROVENANCE](PROVENANCE.md)。核心数学前置与证明正文在本库内；部分外围应用阅读仍链接原笔记库，其可达性取决于原仓库权限。这些只能是可选阅读，不应成为完成核心证明流程的前提，也不应为修复链接而公开原笔记库。

PDF/source 和本地开发 archive 不跟踪进 Git。发布前仍须检查拟发布文件及可达历史；`.gitignore` 不能证明历史从未包含缓存、凭据或未授权素材。普通归档不清除历史，敏感信息移出当前目录也不等于撤回。

## 每次发布应检查什么

| 检查项 | 应留下的证据 |
|---|---|
| 权利与许可 | MIT 文件、迁入来源、第三方归属；新增素材的许可范围 |
| 内容与历史 | 对本次拟发布文件及相关历史的凭据/隐私/未授权材料检查，明确范围与局限 |
| 干净安装 | 无原笔记库、个人 Skill 目录、论文缓存或本地 archive 的副本可检索、展示、检查和安装 |
| 导航 | README、主题目录、章节锚点与图片可用；核心页面不依赖维护者本地文件 |
| 数学与引用 | 原命题、假设、量词、来源版本与核验等级一致，未证引理不伪装成定理 |
| 下载与来源 | 固定版本、工件哈希、解包一致性和失败报告；“收录”与“已核验”分开 |
| 行为与测试 | 记录真实命令、环境及结果；改动 skill 约束时重测相关正例、反例和证据误用 |
| 对外配置 | 仓库可见性、tag、release 与 CI 声明符合实际，不以徽章替代真实运行 |

## 本地检查入口

使用 Python 3.11+，在仓库根目录运行：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_library.py
python3 scripts/audit_proof.py examples/biased_sgd_ledger.json --require-closed
python3 scripts/download_papers.py --dry-run
```

完整缓存的维护者另运行 `python3 scripts/check_library.py --require-cache --pdfinfo`；`--pdfinfo` 需要本机安装 Poppler。纯文本新用户无需该依赖，缺失的可选论文缓存不是丢失笔记。

安装器可用 `--target` 指向独立临时位置，避免改变个人 skill。测试重复安装、已有内容不覆盖，以及从仓库外经链接调用 helper。论文下载更新后，再在无网络条件下检查缓存复用；方法见 [DOWNLOADING](DOWNLOADING.md)。

未填写的 [PROOF_LEDGER](../templates/PROOF_LEDGER.json) 是草稿；`--require-closed` 应拒绝尚未在原给定假设下闭合的目标。检查器验证记录一致性和哈希，不裁定证明的数学正确性。评测方法与审阅范围见 [evals](../evals/README.md)。

## 维护页面与发布陈述

[check-workflow.example.yml](check-workflow.example.yml) 是可选 CI 示例，不是已启用的 workflow。只有实际配置并运行后，才展示相应状态；本地 macOS 测试不写成 Linux/Windows CI 通过。

README 面向使用者说明用途、motivation、安装与入口；[CHANGELOG](../CHANGELOG.md)记录版本功能、重要修订和兼容性变化。贡献流程见 [CONTRIBUTING](../CONTRIBUTING.md)。保留当前正文、可复用评测和必要来源证据，阶段开发记录由维护者单独保存。

发布始终保留 [DL 覆盖边界](DL_THEORY_FRAMEWORK.md)、[AI 证明合同](AI_PROOF_CONTRACT.md)和[核验状态](../证明模板核验状态.md)。卡片数、论文数和测试通过率都不能保证数学正确或 agent 永不犯错。更改仓库可见性、创建 release 或启用 CI 是单独的发布操作，不由文档打磨隐式触发。
