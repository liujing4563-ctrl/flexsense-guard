# Simulink 模型接口约定

## 目的

本目录预留用于后续人工建立 Simulink（`.slx`）模型。文本工具无法可靠生成
`.slx` 二进制文件，因此本阶段不创建 Simulink 模型，只记录接口约定。

## 接口约定

### Plant 模型（Simulink）

| 端口 | 方向 | 信号 | 单位 |
|------|------|------|------|
| 1 | 输入 | tau_m（电机力矩指令） | Nm |
| 2 | 输入 | tau_ext（外部扰动力矩） | Nm |
| 3 | 输出 | theta_m（电机位置） | rad |
| 4 | 输出 | omega_m（电机速度） | rad/s |
| 5 | 输出 | theta_l（负载位置，真值） | rad |
| 6 | 输出 | omega_l（负载速度，真值） | rad/s |
| 7 | 输出 | tau_s（扭转力矩） | Nm |

### 采样时间

- 基础采样时间：1 ms（1000 Hz）
- 控制频率：与采样时间一致

### 文件命名

- `flex_joint_plant.slx`：主 Plant 模型
- `flex_joint_observer.slx`：Observer 子系统
- `probe_runner.slx`：探针运行框架

### 实现要求

1. 使用 MATLAB 函数块或 S-Function 封装 `flex_joint_dynamics.m`
2. 参数通过 MATLAB 工作空间传递
3. 记录仿真数据到 MATLAB 工作空间 `results` 结构体
4. 与 `simulate_flex_joint.m` 在相同输入下输出一致（差值 < 1e-6）
