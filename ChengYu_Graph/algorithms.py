import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import networkx as nx
from models import Company, CompanyRelation, db

# K-Means聚类算法实现
def perform_kmeans_clustering(n_clusters=3):
    # 从数据库获取企业数据
    companies = Company.query.all()
    
    if not companies:
        return None
    
    # 准备特征数据
    features = []
    company_ids = []
    
    for company in companies:
        company_ids.append(company.company_id)
        # 使用注册资本、专利数、员工数作为特征
        features.append([
            company.registered_capital,
            company.patent_count,
            company.employee_count
        ])
    
    # 将特征转换为numpy数组
    X = np.array(features)
    
    # 数据标准化
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    
    # 执行K-Means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X)
    
    # 更新数据库中的聚类标签
    for i, company_id in enumerate(company_ids):
        company = Company.query.get(company_id)
        company.cluster_label = int(cluster_labels[i])
    
    db.session.commit()
    
    return {
        'cluster_count': 3,
        'companies_clustered': len(company_ids),
        'cluster_labels': cluster_labels.tolist()
    }

# PageRank算法实现
def perform_pagerank(damping_factor=0.85, iterations=100):
    # 创建有向图
    G = nx.DiGraph()
    
    # 从数据库获取所有企业
    companies = Company.query.all()
    
    if not companies:
        return None
    
    # 添加所有企业作为节点
    for company in companies:
        G.add_node(company.company_id)
    
    # 从数据库获取所有企业关系
    relations = CompanyRelation.query.all()
    
    # 添加所有关系作为边，并使用关系强度作为权重
    for relation in relations:
        G.add_edge(
            relation.source_company_id,
            relation.target_company_id,
            weight=relation.relation_strength
        )
    
    # 执行PageRank算法
    pagerank_scores = nx.pagerank(G, weight='weight', alpha=damping_factor, max_iter=iterations)
    
    # 更新数据库中的PageRank分数
    for company_id, score in pagerank_scores.items():
        company = Company.query.get(company_id)
        company.pagerank_score = float(score)
    
    db.session.commit()
    
    return {
        'nodes_count': G.number_of_nodes(),
        'edges_count': G.number_of_edges(),
        'pagerank_scores': pagerank_scores
    }

# 获取聚类分析结果
def get_cluster_analysis():
    # 从数据库获取企业数据
    companies = Company.query.all()
    
    if not companies:
        return None
    
    # 按聚类标签分组
    cluster_data = {}
    for company in companies:
        if company.cluster_label is None:
            continue
        
        cluster_id = company.cluster_label
        if cluster_id not in cluster_data:
            cluster_data[cluster_id] = {
                'companies': [],
                'avg_registered_capital': 0,
                'avg_patent_count': 0,
                'avg_employee_count': 0
            }
        
        cluster_data[cluster_id]['companies'].append({
            'company_id': company.company_id,
            'company_name': company.company_name,
            'registered_capital': company.registered_capital,
            'patent_count': company.patent_count,
            'employee_count': company.employee_count
        })
    
    # 计算每个聚类的统计信息
    for cluster_id, data in cluster_data.items():
        companies = data['companies']
        count = len(companies)
        
        total_capital = sum(c['registered_capital'] for c in companies)
        total_patents = sum(c['patent_count'] for c in companies)
        total_employees = sum(c['employee_count'] for c in companies)
        
        data['avg_registered_capital'] = total_capital / count
        data['avg_patent_count'] = total_patents / count
        data['avg_employee_count'] = total_employees / count
        data['company_count'] = count
    
    return cluster_data

# 获取PageRank分析结果
def get_pagerank_analysis():
    # 从数据库获取企业数据并按PageRank分数排序
    companies = Company.query.order_by(Company.pagerank_score.desc()).all()
    
    if not companies:
        return None
    
    return [
        {
            'company_id': company.company_id,
            'company_name': company.company_name,
            'pagerank_score': company.pagerank_score,
            'industry': company.industry.industry_name if company.industry else '',
            'city': company.region.city if company.region else '',
            'district': company.region.district if company.region else ''
        }
        for company in companies
    ]