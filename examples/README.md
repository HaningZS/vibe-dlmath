# DL 核心公式的小例子

[框架](../docs/DL_THEORY_FRAMEWORK.md) · [模板目录](../proofs/README.md)

运行：

~~~bash
python3 examples/dl_core_checks.py
~~~

同一个纯 Python 文件演示 T32 的风险分解、T34 的 ReLU 插值、T33/T35 的线性类 Rademacher 复杂度、T36 的 logistic 轨迹、T37 的有限联合分布、T38 的编码预算和 T39 的 proximal 下降。

进一步运行 `python3 examples/dl_specialization_checks.py`：11 组小模型检查负曲率、随机特征方差、时变核、attention 等变/位置反例、GNN 图对、平滑半径、Gaussian 隐私积分、客户端漂移、因果不可识别、surrogate 桥和输出层训练。对应 [完整学习证明](../docs/END_TO_END_LEARNING_PROOF.md) 与 T40–T49。

这些例子核对公式、常数与边界情形，不构成对一般统计定理的自动验证。完整的假设和证明仍在各模板卡中。

## 经典与近期证明蒸馏

- [经典有限噪声树与编码事件](classical_distillation_checks.py)：`python3 examples/classical_distillation_checks.py`。
- [指数包络与连续流](recent_distillation_checks.py)：`python3 examples/recent_distillation_checks.py`，穷举有限样本空间及精确 Gaussian 轨迹矩。
- [有偏 SGD 的已填写账本](biased_sgd_ledger.json)：`python3 scripts/audit_proof.py examples/biased_sgd_ledger.json --require-closed`。检查账本一致性，数学推导见 [对应专题](../extensions/经典下降证明的偏差与方差接口.md)。
