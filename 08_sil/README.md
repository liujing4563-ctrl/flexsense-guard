# C/C++ SIL 工作包

主责：嵌入式 Linux 同学。

负责 C/C++ 接口、实现、CMake、CTest、回放、一致性测试、执行时间、内存和异常
保护。P1 和主算法冻结前不移植 Observer，不得自行改变模型或公共字段。

子目录：`include/`、`src/`、`tests/`、`benchmarks/`。构建产物统一放入已忽略的
`08_sil/build/`。

当前状态：目录结构已规划，主体实现 `BLOCKED`。
