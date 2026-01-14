import pandas as pd
import numpy as np
import os
import json
from config import config

class DataProcessor:
    def __init__(self):
        # 使用开发环境配置
        self.config = config['development']
        self.data_dir = self.config.DATA_DIR
        
    def load_companies_data(self):
        """加载并清洗企业数据"""
        file_path = os.path.join(self.data_dir, 'simulated_companies.csv')
        df = pd.read_csv(file_path)
        
        # 数据清洗
        df = df.dropna()  # 删除空值
        df['成立时间'] = pd.to_datetime(df['成立时间'])
        df['注册资本(万元)'] = pd.to_numeric(df['注册资本(万元)'], errors='coerce')
        df['专利数量'] = pd.to_numeric(df['专利数量'], errors='coerce')
        df['员工人数'] = pd.to_numeric(df['员工人数'], errors='coerce')
        
        # 移除异常值
        df = df[(df['注册资本(万元)'] > 0) & (df['专利数量'] >= 0) & (df['员工人数'] >= 0)]
        
        return df
    
    def load_relations_data(self):
        """加载并清洗关系数据"""
        file_path = os.path.join(self.data_dir, 'simulated_relations.csv')
        df = pd.read_csv(file_path)
        
        # 数据清洗
        df = df.dropna()
        df['关系强度'] = pd.to_numeric(df['关系强度'], errors='coerce')
        df = df[(df['关系强度'] >= 0) & (df['关系强度'] <= 1)]
        
        return df
    
    def load_regions_data(self):
        """加载并清洗区域数据"""
        file_path = os.path.join(self.data_dir, 'simulated_regions.csv')
        df = pd.read_csv(file_path)
        
        # 数据清洗
        df = df.dropna()
        df['GDP(亿元)'] = pd.to_numeric(df['GDP(亿元)'], errors='coerce')
        df = df[df['GDP(亿元)'] > 0]
        
        return df
    
    def process_data(self):
        """处理所有数据并保存为结构化格式"""
        # 加载数据
        companies_df = self.load_companies_data()
        relations_df = self.load_relations_data()
        regions_df = self.load_regions_data()
        
        # 保存为JSON格式，方便后续处理
        processed_data = {
            'companies': companies_df.to_dict('records'),
            'relations': relations_df.to_dict('records'),
            'regions': regions_df.to_dict('records')
        }
        
        output_path = os.path.join(self.data_dir, 'processed_data.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"数据处理完成，保存到 {output_path}")
        return processed_data

if __name__ == '__main__':
    processor = DataProcessor()
    processor.process_data()