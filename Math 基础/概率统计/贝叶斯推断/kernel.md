---
type: note
domain: math/bayesian-inference
status: active
reviewed: 2026-09-01
---

# 贝叶斯计算中的 Kernel

在贝叶斯统计的上下文中，**Kernel（核）** 指的是一个概率密度函数（PDF）或概率质量函数（PMF）中，**随当前关心的参数（或变量）变化的部分**，而忽略与该对象无关的归一化常数。

> [!warning] “常数”取决于你把谁当变量
> 对数据 $D$ 固定、把 $\theta$ 当变量时，某项可能是常数；换成研究 $D$ 的分布时，它未必还是常数。使用 $\propto$ 时必须明确是“关于谁成比例”。

简单来说，一个概率分布的函数可以写成：

$$P(x) = C \times k(x)$$

- $P(x)$ 是完整的概率密度函数（比如 $\text{Beta}(\alpha, \beta)$ 的PDF）。

- $C$ 是**归一化常数**。它是一个不依赖于 $x$ 的常数，其唯一作用是确保整个分布的积分（或求和）等于 1。

- $k(x)$ 就是这个分布的 **Kernel（核）**。它决定了这个分布的**基本形状**。


---

### 为什么 "Kernel" 在贝叶斯统计中如此重要？

它之所以重要，完全是因为贝叶斯定理的计算方式：

$$\text{后验分布} \propto \text{似然函数} \times \text{先验分布}$$

这里的 "$\propto$" (proportional to，正比于) 符号非常关键。它意味着我们在进行计算时，**可以完全忽略掉所有不依赖于目标参数的常数项**。

我们只关心那些与参数（例如 $\theta$）相关的项。当我们把似然函数和先验分布相乘时，我们实际上**只需要把它们的 Kernel 相乘**。

$$\text{Kernel}(\text{后验}) \propto \text{Kernel}(\text{似然}) \times \text{Kernel}(\text{先验})$$

### 实例：重温 Beta-二项分布

让我们用上一个“共轭先验”的例子来精确说明 Kernel 是什么：

**1. 似然函数：二项分布**

- **完整 PDF：** $P(D|\theta) = \binom{n}{k} \theta^k (1-\theta)^{n-k}$

- **参数：** 我们关心的是 $\theta$。

- **常数：** $\binom{n}{k}$ 这一项（组合数）不依赖于 $\theta$，所以它_不是_ Kernel 的一部分。

- **Kernel：** $k(\theta) = \theta^k (1-\theta)^{n-k}$


**2. 先验分布：Beta 分布**

- **完整 PDF：** $P(\theta) = \frac{1}{B(\alpha, \beta)} \theta^{\alpha-1} (1-\theta)^{\beta-1}$

- **参数：** $\theta$

- **常数：** $\frac{1}{B(\alpha, \beta)}$ （Beta 函数的倒数）不依赖于 $\theta$。

- **Kernel：** $k(\theta) = \theta^{\alpha-1} (1-\theta)^{\beta-1}$


3. 计算后验分布的 Kernel

我们使用贝叶斯定理，只将两个 Kernel 相乘：

$$\begin{aligned} \text{Kernel}(\text{后验}) &\propto \text{Kernel}(\text{似然}) \times \text{Kernel}(\text{先验}) \\ &\propto [\theta^k (1-\theta)^{n-k}] \times [\theta^{\alpha-1} (1-\theta)^{\beta-1}] \\ &= \theta^{\alpha+k-1} (1-\theta)^{\beta+n-k-1} \end{aligned}$$

4. 识别后验分布

现在我们得到了后验分布的 Kernel。我们**“识别”**（recognize）这个 Kernel 的形式。

我们看到 $\theta^{\text{something}-1} (1-\theta)^{\text{something}-1}$ 的形式，马上就能认出：**这不就是 Beta 分布的 Kernel 吗！**

因此，我们得出结论，后验分布_必须_是一个 Beta 分布，其参数为：

- 新的 $\alpha' = \alpha + k$

- 新的 $\beta' = \beta + (n - k)$


这就是 $P(\theta|D) = \text{Beta}(\alpha+k, \beta+n-k)$。

---

### 总结

在贝叶斯统计中，**Kernel 就是一个分布的“特征签名”或“函数骨架”**。

- **作用**：它允许我们通过简单地相乘和“模式识别”，来确定后验分布的_家族_和_参数_，而完全不需要计算那些复杂的、通常涉及高维积分的归一化常数（ $P(D)$）。

- **区分**：这个 "Kernel" 不同于你在 SVM (支持向量机)中听到的 "Kernel trick"（核技巧）或 "Kernel Density Estimation"（核密度估计）中的 "Kernel"。虽然都叫 "Kernel"，但在贝叶斯计算中，它的含义特指上述的“忽略常数的分布核心”。


与点估计及完整后验的区别见 [最大似然、MAP 与贝叶斯估计](../%E6%9C%80%E5%A4%A7%E4%BC%BC%E7%84%B6%E3%80%81MAP%20%E4%B8%8E%E8%B4%9D%E5%8F%B6%E6%96%AF%E4%BC%B0%E8%AE%A1.md)；无法识别解析 kernel 时的采样路线见 [蒙特卡洛、重要性采样与 MCMC](../%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B%E3%80%81%E9%87%8D%E8%A6%81%E6%80%A7%E9%87%87%E6%A0%B7%E4%B8%8E%20MCMC.md)。
