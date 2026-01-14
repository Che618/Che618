CREATE TABLE sys_region (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(64) NOT NULL,
  current_population BIGINT NOT NULL,
  birth_rate_base DOUBLE NOT NULL
);

CREATE TABLE sim_policy_factor (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(64) NOT NULL,
  elasticity DOUBLE NOT NULL,
  min_val DOUBLE NOT NULL,
  max_val DOUBLE NOT NULL
);

CREATE TABLE sim_result_log (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  region_id BIGINT NOT NULL,
  policy_snapshot JSON NOT NULL,
  projection_json JSON NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
