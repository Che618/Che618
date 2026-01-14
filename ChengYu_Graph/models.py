from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

# 创建SQLAlchemy实例
db = SQLAlchemy()

# 产业模型
class Industry(db.Model):
    __tablename__ = 'industries'
    
    industry_id = Column(Integer, primary_key=True)
    industry_name = Column(String(100), nullable=False)
    description = Column(String(200))
    
    # 关系定义
    companies = relationship('Company', back_populates='industry')

# 区域模型
class Region(db.Model):
    __tablename__ = 'regions'
    
    region_id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    gdp = Column(Float, nullable=False)
    industrial_parks = Column(String(200))
    main_industries = Column(String(200))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系定义
    companies = relationship('Company', back_populates='region')

# 企业模型
class Company(db.Model):
    __tablename__ = 'companies'
    
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String(100), nullable=False)
    registered_capital = Column(Float)
    establish_date = Column(Date)
    registered_address = Column(String(200))
    industry_id = Column(Integer, ForeignKey('industries.industry_id'))
    region_id = Column(Integer, ForeignKey('regions.region_id'))
    patent_count = Column(Integer)
    employee_count = Column(Integer)
    cluster_label = Column(Integer, nullable=True)
    pagerank_score = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系定义
    industry = relationship('Industry', back_populates='companies')
    region = relationship('Region', back_populates='companies')
    outgoing_relations = relationship('CompanyRelation', foreign_keys='CompanyRelation.source_company_id', back_populates='source_company')
    incoming_relations = relationship('CompanyRelation', foreign_keys='CompanyRelation.target_company_id', back_populates='target_company')

# 企业关系模型
class CompanyRelation(db.Model):
    __tablename__ = 'company_relations'
    
    relation_id = Column(Integer, primary_key=True)
    source_company_id = Column(Integer, ForeignKey('companies.company_id'))
    target_company_id = Column(Integer, ForeignKey('companies.company_id'))
    relation_type = Column(String(50))
    relation_strength = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系定义
    source_company = relationship('Company', foreign_keys=[source_company_id], back_populates='outgoing_relations')
    target_company = relationship('Company', foreign_keys=[target_company_id], back_populates='incoming_relations')