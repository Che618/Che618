package com.zhice.platform.entity;

public class SimPolicyFactor {
  private Long id;
  private String name;
  private Double elasticity;
  private Double minVal;
  private Double maxVal;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public Double getElasticity() {
    return elasticity;
  }

  public void setElasticity(Double elasticity) {
    this.elasticity = elasticity;
  }

  public Double getMinVal() {
    return minVal;
  }

  public void setMinVal(Double minVal) {
    this.minVal = minVal;
  }

  public Double getMaxVal() {
    return maxVal;
  }

  public void setMaxVal(Double maxVal) {
    this.maxVal = maxVal;
  }
}
