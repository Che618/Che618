package com.zhice.platform.service;

import com.zhice.platform.model.PolicyInput;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class SimulationService {
  /**
   * 根据政策输入计算未来五年的出生率投影。
   *
   * <p>核心逻辑（简化版）：未来出生率 = 基准出生率 * (1 + Σ(政策投入 * 弹性系数))</p>
   *
   * <p>弹性系数的含义：当政策投入增加 1 单位时，出生率相对变化的比例。
   * 例如：育儿补贴的弹性系数为 0.0001，代表补贴每增加 1 元，
   * 出生率增加 0.01%（= 0.0001）。所有政策影响会叠加，形成综合的弹性效应。</p>
   */
  public List<Double> calculateProjection(List<PolicyInput> inputs, double baseBirthRate) {
    double elasticitySum = 0;
    for (PolicyInput input : inputs) {
      // 累积政策投入与弹性系数的乘积，得到总的政策放大倍率
      elasticitySum += input.getValue() * input.getElasticity();
    }

    double policyMultiplier = 1 + elasticitySum;
    List<Double> projection = new ArrayList<>();
    for (int year = 0; year < 5; year++) {
      double yearlyGrowth = baseBirthRate * policyMultiplier * (1 + year * 0.01);
      projection.add(round(yearlyGrowth));
    }
    return projection;
  }

  private double round(double value) {
    return Math.round(value * 10000.0) / 10000.0;
  }
}
