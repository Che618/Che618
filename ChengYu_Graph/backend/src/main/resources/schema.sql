-- 区域表
CREATE TABLE sys_region (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(64) NOT NULL,
  current_population BIGINT NOT NULL,
  birth_rate_base DECIMAL(10, 4) NOT NULL
);

-- 政策因子表
CREATE TABLE sim_policy_factor (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(128) NOT NULL,
  elasticity DECIMAL(10, 4) NOT NULL,
  min_val DECIMAL(10, 2) NOT NULL,
  max_val DECIMAL(10, 2) NOT NULL
);

-- 推演结果日志表
CREATE TABLE sim_result_log (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  region_id BIGINT NOT NULL,
  policy_snapshot JSON NOT NULL,
  projection_year INT NOT NULL,
  projected_birth_rate DECIMAL(10, 4) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_sim_region FOREIGN KEY (region_id) REFERENCES sys_region(id)
);
