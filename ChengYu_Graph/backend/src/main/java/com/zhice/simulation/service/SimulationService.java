package com.zhice.simulation.service;

import com.zhice.simulation.model.PolicyInput;

import java.util.ArrayList;
import java.util.List;

/**
 * 核心仿真服务：根据政策输入推演未来出生率趋势。
 */
public class SimulationService {

    /**
     * 根据政策参数计算未来 5 年出生率趋势。
     *
     * @param baseBirthRate 基准出生率
     * @param inputs        政策输入列表
     * @return 未来 5 年预测结果
     */
    public List<Double> calculateProjection(double baseBirthRate, List<PolicyInput> inputs) {
        // 这里使用简化逻辑：未来出生率 = 基准出生率 * (1 + Σ(政策投入 * 弹性系数))
        // 说明：
        // 1. "政策投入"代表政策力度，例如补贴金额、产假天数的标准化值。
        // 2. "弹性系数"代表政策对出生率的敏感度，数值越大说明政策影响越明显。
        // 3. 将所有政策的影响累加后，再叠加到基准出生率上形成整体增幅。
        double elasticitySum = 0.0;
        if (inputs != null) {
            for (PolicyInput input : inputs) {
                // 重点：弹性系数计算逻辑
                // 将每个政策的“力度”与“弹性系数”相乘，得到该政策的边际影响。
                // 例如：补贴 6000 元、弹性系数 0.002，则贡献 = 6000 * 0.002。
                elasticitySum += input.getValue() * input.getElasticity();
            }
        }

        double adjustedRate = baseBirthRate * (1 + elasticitySum);

        List<Double> projection = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            // 简化假设：逐年小幅衰减，以体现人口结构的惯性。
            double yearlyRate = adjustedRate * (1 - 0.01 * i);
            projection.add(yearlyRate);
        }
        return projection;
    }
}
