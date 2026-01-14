package com.zhice.platform.entity;

public class SysRegion {
  private Long id;
  private String name;
  private Long currentPopulation;
  private Double birthRateBase;

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

  public Long getCurrentPopulation() {
    return currentPopulation;
  }

  public void setCurrentPopulation(Long currentPopulation) {
    this.currentPopulation = currentPopulation;
  }

  public Double getBirthRateBase() {
    return birthRateBase;
  }

  public void setBirthRateBase(Double birthRateBase) {
    this.birthRateBase = birthRateBase;
  }
}
