# 历史系统架构

> 本文件仅用于历史追溯。当前架构以 [`docs/02_architecture/system_architecture.md`](../docs/02_architecture/system_architecture.md) 为准。

## 系统架构图

```mermaid
flowchart TB
    subgraph Input["输入层"]
        A1["轨迹/场景配置"]
        A2["故障注入配置"]
    end

    subgraph Plant["柔性关节数字样机"]
        B1["双惯量动力学模型"]
        B2["摩擦 · 饱和 · 时延"]
        B3["外部接触/冲击注入"]
    end

    subgraph Measurement["电机侧测量"]
        C1["电机位置 θm"]
        C2["电机速度 ωm"]
        C3["电机电流 → 力矩 τm"]
    end

    subgraph Health["信号健康检测"]
        D1["丢包检测"]
        D2["卡死检测"]
        D3["参数失配估计"]
    end

    subgraph Observer["增广状态观测器"]
        E1["EKF 预测步"]
        E2["EKF 更新步"]
        E3["名义参数模型"]
    end

    subgraph Confidence["可信评分"]
        F1["创新残差分析"]
        F2["信号健康融合"]
        F3["置信度评分"]
    end

    subgraph Classification["振动-接触辨识"]
        G1["特征提取"]
        G2["规则分类器"]
        G3["三分类输出"]
    end

    subgraph ModeManager["模式管理"]
        H1["正常跟踪"]
        H2["振动抑制"]
        H3["安全减速"]
        H4["降级模式"]
    end

    subgraph Calibration["事件触发校准"]
        I1["触发条件评估"]
        I2["低幅校准信号注入"]
        I3["更新门控"]
    end

    subgraph Validation["验证与输出"]
        J1["指标计算"]
        J2["状态记录"]
        J3["报告生成"]
    end

    A1 --> B1
    A2 --> B3
    B1 --> B2 --> B3
    B3 --> C1 & C2 & C3
    
    C1 & C2 & C3 --> D1 & D2 & D3
    D1 & D2 & D3 --> E2
    
    C1 & C2 & C3 --> E1
    E1 --> E2 --> F1
    D1 & D2 & D3 --> F2
    F1 & F2 --> F3
    
    F3 --> G1 --> G2 --> G3
    
    F3 & G3 --> H1 & H2 & H3 & H4
    
    F3 --> I1 --> I2 --> I3
    I3 --> E2
    
    H1 & H2 & H3 & H4 --> J1
    G3 --> J1
    J1 --> J2 --> J3
    
    B3 -.->|"真值（仅评价）"| J1
```

## 数据流说明

| 连线 | 数据内容 | 备注 |
|------|----------|------|
| A1 → B1 | 场景参数（载荷、轨迹、持续时间） | JSON Schema 定义格式 |
| B3 → C1~C3 | 传感器模拟输出 | 可叠加故障注入 |
| C1~C3 → E1 | 测量值 θm, ωm, τm | Observer 唯一输入 |
| E2 → F1 | 创新残差向量 | 3 维：位置、速度、力矩 |
| F3 → H1~H4 | 可信评分 + 分类结果 | 驱动模式切换 |
| F3 → I1 | 可信评分 | 触发校准的条件 |
| B3 → J1 | 真值 θl, ωl, τext | 仅用于评价，不进入 Observer |

## 模块依赖关系

```
01_plant/  (独立)
     ↓
02_observer/  (依赖 01_plant 的仿真输出)
     ↓
03_confidence_trigger/  (依赖 02_observer 的估计结果)
     ↓
04_classification/  (依赖 02_observer 和 03_confidence 的输出)
     ↓
05_control/  (依赖 02_observer, 03_confidence, 04_classification)
     ↓
06_validation/  (依赖所有上游模块的输出)
     
07_app/  (依赖 01-06 的上层应用)
08_sil/  (01-05 的 C 实现)
09_test_agent/  (测试编排工具)
```

## 关键接口

详细接口定义见 `interface_spec.md`。核心数据交换格式为 JSON（通过公共 Schema 定义），模块间通过标准化结构体传递：

- `ScenarioConfig` → 场景配置
- `SystemState` → 系统状态（估计 + 评分）
- `ValidationReport` → 验证报告
