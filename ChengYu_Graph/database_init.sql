-- 创建数据库
CREATE DATABASE IF NOT EXISTS chengyu_industry CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE chengyu_industry;

-- 创建区域表
CREATE TABLE IF NOT EXISTS regions (
    region_id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    gdp DECIMAL(15, 2) NOT NULL,
    industrial_parks TEXT,
    main_industries TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_city_district (city, district)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建产业表
CREATE TABLE IF NOT EXISTS industries (
    industry_id INT PRIMARY KEY AUTO_INCREMENT,
    industry_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_industry_name (industry_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建企业表
CREATE TABLE IF NOT EXISTS companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    registered_capital DECIMAL(15, 2) NOT NULL,
    establish_date DATE NOT NULL,
    registered_address VARCHAR(200) NOT NULL,
    industry_id INT NOT NULL,
    region_id INT NOT NULL,
    patent_count INT DEFAULT 0,
    employee_count INT DEFAULT 0,
    cluster_label VARCHAR(50),  -- K-Means聚类结果
    pagerank_score DECIMAL(10, 6) DEFAULT 0.0,  -- PageRank评分
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_company_name (company_name),
    FOREIGN KEY (industry_id) REFERENCES industries(industry_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建企业关系表
CREATE TABLE IF NOT EXISTS company_relations (
    relation_id INT PRIMARY KEY AUTO_INCREMENT,
    source_company_id INT NOT NULL,
    target_company_id INT NOT NULL,
    relation_type VARCHAR(50) NOT NULL,  -- INVEST(投资), SUPPLY(上下游)
    relation_strength DECIMAL(3, 2) NOT NULL,  -- 0-1之间
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (source_company_id) REFERENCES companies(company_id),
    FOREIGN KEY (target_company_id) REFERENCES companies(company_id),
    UNIQUE KEY uk_relation (source_company_id, target_company_id, relation_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入初始产业数据
INSERT INTO industries (industry_name, description) VALUES
('电子信息', '包括电子设备制造、软件开发、通信技术等'),
('汽车制造', '包括整车制造、零部件生产、汽车销售等'),
('软件服务', '包括软件开发、系统集成、信息技术服务等'),
('新材料', '包括高性能材料、复合材料、纳米材料等'),
('生物医药', '包括药品研发、医疗器械、生物制品等'),
('新能源', '包括太阳能、风能、水能等可再生能源开发利用'),
('物流运输', '包括货物运输、仓储、供应链管理等'),
('航空航天', '包括航空器制造、航空电子、航天技术等'),
('数字经济', '包括数字产业、数字贸易、数字服务等');