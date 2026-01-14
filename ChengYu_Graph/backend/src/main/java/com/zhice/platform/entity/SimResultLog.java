package com.zhice.platform.entity;

import java.time.LocalDateTime;

public class SimResultLog {
  private Long id;
  private Long regionId;
  private String policySnapshot;
  private String projectionJson;
  private LocalDateTime createdAt;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public Long getRegionId() {
    return regionId;
  }

  public void setRegionId(Long regionId) {
    this.regionId = regionId;
  }

  public String getPolicySnapshot() {
    return policySnapshot;
  }

  public void setPolicySnapshot(String policySnapshot) {
    this.policySnapshot = policySnapshot;
  }

  public String getProjectionJson() {
    return projectionJson;
  }

  public void setProjectionJson(String projectionJson) {
    this.projectionJson = projectionJson;
  }

  public LocalDateTime getCreatedAt() {
    return createdAt;
  }

  public void setCreatedAt(LocalDateTime createdAt) {
    this.createdAt = createdAt;
  }
}
