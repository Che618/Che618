package com.zhice.platform.model;

import java.util.List;

public class ProjectionResponse {
  private List<Integer> years;
  private List<Double> baseTrend;
  private List<Double> policyTrend;

  public ProjectionResponse(List<Integer> years, List<Double> baseTrend, List<Double> policyTrend) {
    this.years = years;
    this.baseTrend = baseTrend;
    this.policyTrend = policyTrend;
  }

  public List<Integer> getYears() {
    return years;
  }

  public void setYears(List<Integer> years) {
    this.years = years;
  }

  public List<Double> getBaseTrend() {
    return baseTrend;
  }

  public void setBaseTrend(List<Double> baseTrend) {
    this.baseTrend = baseTrend;
  }

  public List<Double> getPolicyTrend() {
    return policyTrend;
  }

  public void setPolicyTrend(List<Double> policyTrend) {
    this.policyTrend = policyTrend;
  }
}
