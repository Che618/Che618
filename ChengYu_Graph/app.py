from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config
import os
from datetime import date

# 导入模型
from models import db, Industry, Region, Company, CompanyRelation

# 创建Flask应用实例
app = Flask(__name__)

# 加载配置
app.config.from_object(config['default'])

# 启用CORS
CORS(app)

# 初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.config['DATABASE']}"
db.init_app(app)

# 导入算法模块
from algorithms import perform_kmeans_clustering, perform_pagerank, get_cluster_analysis, get_pagerank_analysis

# 导入日期处理模块
from datetime import date

# 创建数据库表
with app.app_context():
    db.create_all()
    
    # 插入初始产业数据
    initial_industries = [
        Industry(industry_name='电子信息', description='包括电子设备制造、软件开发、通信技术等'),
        Industry(industry_name='汽车制造', description='包括整车制造、零部件生产、汽车销售等'),
        Industry(industry_name='软件服务', description='包括软件开发、系统集成、信息技术服务等'),
        Industry(industry_name='新材料', description='包括高性能材料、复合材料、纳米材料等'),
        Industry(industry_name='生物医药', description='包括药品研发、医疗器械、生物制品等'),
        Industry(industry_name='新能源', description='包括太阳能、风能、水能等可再生能源开发利用'),
        Industry(industry_name='物流运输', description='包括货物运输、仓储、供应链管理等'),
        Industry(industry_name='航空航天', description='包括航空器制造、航空电子、航天技术等'),
        Industry(industry_name='数字经济', description='包括数字产业、数字贸易、数字服务等')
    ]
    
    for industry in initial_industries:
        if not Industry.query.filter_by(industry_name=industry.industry_name).first():
            db.session.add(industry)
    
    # 插入初始区域数据
    initial_regions = [
        Region(city='成都', district='高新区', gdp=3000.0, industrial_parks='成都高新区、天府软件园', main_industries='电子信息、软件服务'),
        Region(city='成都', district='天府新区', gdp=2500.0, industrial_parks='天府新区核心区', main_industries='电子信息、数字经济'),
        Region(city='重庆', district='两江新区', gdp=3500.0, industrial_parks='两江新区工业园区', main_industries='汽车制造、电子信息'),
        Region(city='重庆', district='渝北区', gdp=2000.0, industrial_parks='渝北工业园区', main_industries='航空航天、智能制造')
    ]
    
    for region in initial_regions:
        if not Region.query.filter_by(city=region.city, district=region.district).first():
            db.session.add(region)
    
    db.session.commit()
    
    # 获取产业和区域的ID
    industries = {ind.industry_name: ind.industry_id for ind in Industry.query.all()}
    regions = {(reg.city, reg.district): reg.region_id for reg in Region.query.all()}
    
    # 插入初始企业数据
    initial_companies = [
        Company(company_name='成都电子科技有限公司', registered_capital=5000.0, establish_date=date(2010, 1, 1), 
               registered_address='成都高新区天府大道', industry_id=industries['电子信息'], 
               region_id=regions[('成都', '高新区')], patent_count=150, employee_count=500),
        Company(company_name='重庆汽车制造集团', registered_capital=10000.0, establish_date=date(2005, 3, 15), 
               registered_address='重庆两江新区金山大道', industry_id=industries['汽车制造'], 
               region_id=regions[('重庆', '两江新区')], patent_count=200, employee_count=1500),
        Company(company_name='成都软件服务有限公司', registered_capital=2000.0, establish_date=date(2012, 6, 20), 
               registered_address='成都天府新区天府大道', industry_id=industries['软件服务'], 
               region_id=regions[('成都', '天府新区')], patent_count=80, employee_count=200),
        Company(company_name='重庆新材料科技有限公司', registered_capital=3000.0, establish_date=date(2015, 9, 10), 
               registered_address='重庆渝北区回兴街道', industry_id=industries['新材料'], 
               region_id=regions[('重庆', '渝北区')], patent_count=120, employee_count=300),
        Company(company_name='成都生物医药研究院', registered_capital=1500.0, establish_date=date(2018, 11, 25), 
               registered_address='成都高新区科园南路', industry_id=industries['生物医药'], 
               region_id=regions[('成都', '高新区')], patent_count=90, employee_count=150),
        Company(company_name='重庆新能源科技有限公司', registered_capital=4000.0, establish_date=date(2013, 4, 5), 
               registered_address='重庆两江新区金渝大道', industry_id=industries['新能源'], 
               region_id=regions[('重庆', '两江新区')], patent_count=180, employee_count=400),
        Company(company_name='成都物流运输有限公司', registered_capital=1000.0, establish_date=date(2008, 2, 28), 
               registered_address='成都天府新区物流园', industry_id=industries['物流运输'], 
               region_id=regions[('成都', '天府新区')], patent_count=20, employee_count=100),
        Company(company_name='重庆航空航天技术有限公司', registered_capital=6000.0, establish_date=date(2011, 8, 15), 
               registered_address='重庆渝北区空港新城', industry_id=industries['航空航天'], 
               region_id=regions[('重庆', '渝北区')], patent_count=250, employee_count=600),
        Company(company_name='成都数字经济有限公司', registered_capital=2500.0, establish_date=date(2016, 12, 10), 
               registered_address='成都高新区天府软件园', industry_id=industries['数字经济'], 
               region_id=regions[('成都', '高新区')], patent_count=100, employee_count=250)
    ]
    
    for company in initial_companies:
        if not Company.query.filter_by(company_name=company.company_name).first():
            db.session.add(company)
    
    db.session.commit()
    
    # 获取企业ID
    companies = {comp.company_name: comp.company_id for comp in Company.query.all()}
    
    # 插入初始企业关系数据
    initial_relations = [
        CompanyRelation(source_company_id=companies['成都电子科技有限公司'], target_company_id=companies['成都软件服务有限公司'], 
                       relation_type='SUPPLY', relation_strength=0.8),
        CompanyRelation(source_company_id=companies['重庆汽车制造集团'], target_company_id=companies['重庆新材料科技有限公司'], 
                       relation_type='SUPPLY', relation_strength=0.9),
        CompanyRelation(source_company_id=companies['重庆新能源科技有限公司'], target_company_id=companies['重庆汽车制造集团'], 
                       relation_type='SUPPLY', relation_strength=0.7),
        CompanyRelation(source_company_id=companies['成都电子科技有限公司'], target_company_id=companies['成都数字经济有限公司'], 
                       relation_type='INVEST', relation_strength=0.6),
        CompanyRelation(source_company_id=companies['重庆航空航天技术有限公司'], target_company_id=companies['重庆新材料科技有限公司'], 
                       relation_type='COLLABORATE', relation_strength=0.85),
        CompanyRelation(source_company_id=companies['成都生物医药研究院'], target_company_id=companies['成都软件服务有限公司'], 
                       relation_type='TECHNICAL_SUPPORT', relation_strength=0.5)
    ]
    
    for relation in initial_relations:
        if not CompanyRelation.query.filter_by(
            source_company_id=relation.source_company_id, 
            target_company_id=relation.target_company_id,
            relation_type=relation.relation_type
        ).first():
            db.session.add(relation)
    
    db.session.commit()

# 创建数据目录
os.makedirs(app.config['DATA_DIR'], exist_ok=True)

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# API路由
# 获取所有产业
@app.route('/api/industries', methods=['GET'])
def get_industries():
    industries = Industry.query.all()
    return jsonify([{
        'industry_id': ind.industry_id,
        'industry_name': ind.industry_name,
        'description': ind.description
    } for ind in industries])

# 获取所有区域
@app.route('/api/regions', methods=['GET'])
def get_regions():
    regions = Region.query.all()
    return jsonify([{
        'region_id': reg.region_id,
        'city': reg.city,
        'district': reg.district,
        'gdp': reg.gdp,
        'industrial_parks': reg.industrial_parks,
        'main_industries': reg.main_industries
    } for reg in regions])

# 获取所有企业
@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify([{
        'company_id': comp.company_id,
        'company_name': comp.company_name,
        'registered_capital': comp.registered_capital,
        'establish_date': str(comp.establish_date),
        'registered_address': comp.registered_address,
        'industry_id': comp.industry_id,
        'industry_name': comp.industry.industry_name,
        'region_id': comp.region_id,
        'city': comp.region.city,
        'district': comp.region.district,
        'patent_count': comp.patent_count,
        'employee_count': comp.employee_count,
        'cluster_label': comp.cluster_label,
        'pagerank_score': comp.pagerank_score
    } for comp in companies])

# 获取企业关系
@app.route('/api/company-relations', methods=['GET'])
def get_company_relations():
    relations = CompanyRelation.query.all()
    return jsonify([{
        'relation_id': rel.relation_id,
        'source_company_id': rel.source_company_id,
        'source_company_name': rel.source_company.company_name,
        'target_company_id': rel.target_company_id,
        'target_company_name': rel.target_company.company_name,
        'relation_type': rel.relation_type,
        'relation_strength': rel.relation_strength
    } for rel in relations])

# 获取图谱数据（节点和边）
@app.route('/api/graph-data', methods=['GET'])
def get_graph_data():
    # 获取所有企业作为节点
    companies = Company.query.all()
    nodes = []
    for comp in companies:
        nodes.append({
            'id': comp.company_id,
            'label': comp.company_name,
            'type': 'company',
            'industry': comp.industry.industry_name,
            'city': comp.region.city,
            'registered_capital': comp.registered_capital,
            'patent_count': comp.patent_count,
            'employee_count': comp.employee_count
        })
    
    # 获取所有企业关系作为边
    relations = CompanyRelation.query.all()
    edges = []
    for rel in relations:
        edges.append({
            'id': rel.relation_id,
            'source': rel.source_company_id,
            'target': rel.target_company_id,
            'type': rel.relation_type,
            'strength': rel.relation_strength
        })
    
    return jsonify({'nodes': nodes, 'edges': edges})

# 根据企业ID获取企业详情
@app.route('/api/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.query.get_or_404(company_id)
    return jsonify({
        'company_id': company.company_id,
        'company_name': company.company_name,
        'registered_capital': company.registered_capital,
        'establish_date': str(company.establish_date),
        'registered_address': company.registered_address,
        'industry_id': company.industry_id,
        'industry_name': company.industry.industry_name,
        'region_id': company.region_id,
        'city': company.region.city,
        'district': company.region.district,
        'patent_count': company.patent_count,
        'employee_count': company.employee_count,
        'cluster_label': company.cluster_label,
        'pagerank_score': company.pagerank_score
    })

# 获取特定企业的关系网络
@app.route('/api/companies/<int:company_id>/network', methods=['GET'])
def get_company_network(company_id):
    # 获取目标企业
    target_company = Company.query.get_or_404(company_id)
    
    # 获取所有与目标企业相关的关系
    outgoing_relations = CompanyRelation.query.filter_by(source_company_id=company_id).all()
    incoming_relations = CompanyRelation.query.filter_by(target_company_id=company_id).all()
    
    # 收集所有相关企业的ID
    related_company_ids = set()
    all_relations = outgoing_relations + incoming_relations
    
    for rel in all_relations:
        related_company_ids.add(rel.source_company_id)
        related_company_ids.add(rel.target_company_id)
    
    # 获取所有相关企业
    related_companies = Company.query.filter(Company.company_id.in_(related_company_ids)).all()
    
    # 构建节点列表
    nodes = []
    for comp in related_companies:
        nodes.append({
            'id': comp.company_id,
            'label': comp.company_name,
            'type': 'company',
            'industry': comp.industry.industry_name,
            'city': comp.region.city,
            'is_target': comp.company_id == company_id
        })
    
    # 构建边列表
    edges = []
    for rel in all_relations:
        edges.append({
            'id': rel.relation_id,
            'source': rel.source_company_id,
            'target': rel.target_company_id,
            'type': rel.relation_type,
            'strength': rel.relation_strength
        })
    
    return jsonify({'nodes': nodes, 'edges': edges})

# K-Means聚类API
@app.route('/api/clustering/kmeans', methods=['POST'])
def perform_kmeans():
    params = request.get_json()
    n_clusters = params.get('n_clusters', 3)
    result = perform_kmeans_clustering(n_clusters)
    return jsonify(result)

@app.route('/api/clustering/analysis', methods=['GET'])
def get_cluster_analysis_data():
    analysis = get_cluster_analysis()
    return jsonify(analysis)

# PageRank算法API
@app.route('/api/pagerank', methods=['POST'])
def compute_pagerank():
    params = request.get_json()
    damping_factor = params.get('damping_factor', 0.85)
    iterations = params.get('iterations', 100)
    result = perform_pagerank(damping_factor, iterations)
    return jsonify(result)

@app.route('/api/pagerank/analysis', methods=['GET'])
def get_pagerank_analysis_data():
    analysis = get_pagerank_analysis()
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])