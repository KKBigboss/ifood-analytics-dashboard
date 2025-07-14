import sqlite3
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')

class DataGenerator:
    def __init__(self, db_path='ifood_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        
    def create_tables(self):
        """Cria as tabelas do banco de dados"""
        
        # Limpar tabelas existentes
        self.conn.execute('DROP TABLE IF EXISTS pedidos')
        self.conn.execute('DROP TABLE IF EXISTS restaurantes')
        self.conn.execute('DROP TABLE IF EXISTS usuarios')
        self.conn.execute('DROP TABLE IF EXISTS entregadores')
        
        # Tabela de Restaurantes
        self.conn.execute('''
        CREATE TABLE restaurantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cidade TEXT NOT NULL,
            rating REAL,
            tempo_medio_preparo INTEGER,
            taxa_comissao REAL,
            data_cadastro DATE
        )
        ''')
        
        # Tabela de Usuários
        self.conn.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL,
            data_cadastro DATE,
            idade INTEGER,
            genero TEXT,
            segmento TEXT
        )
        ''')
        
        # Tabela de Pedidos
        self.conn.execute('''
        CREATE TABLE pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurante_id INTEGER,
            usuario_id INTEGER,
            valor_pedido REAL,
            taxa_entrega REAL,
            tempo_entrega INTEGER,
            status TEXT,
            data_pedido DATETIME,
            avaliacao INTEGER,
            FOREIGN KEY (restaurante_id) REFERENCES restaurantes (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de Entregadores
        self.conn.execute('''
        CREATE TABLE entregadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL,
            veiculo TEXT,
            rating REAL,
            entregas_realizadas INTEGER,
            data_cadastro DATE
        )
        ''')
        
        self.conn.commit()
        
    def generate_restaurants(self, n=200):
        """Gera dados fictícios de restaurantes"""
        categorias = ['Brasileira', 'Italiana', 'Japonesa', 'Mexicana', 'Árabe', 
                     'Fast Food', 'Pizza', 'Hambúrguer', 'Saudável', 'Doces']
        cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 
                  'Brasília', 'Fortaleza', 'Recife', 'Porto Alegre']
        
        restaurants = []
        for i in range(n):
            restaurant = (
                f"Restaurante {fake.company()}",
                random.choice(categorias),
                random.choice(cidades),
                round(random.uniform(3.0, 5.0), 1),
                random.randint(15, 60),
                round(random.uniform(0.15, 0.25), 2),
                fake.date_between(start_date='-2y', end_date='today').isoformat()
            )
            restaurants.append(restaurant)
            
        self.conn.executemany('''
            INSERT INTO restaurantes (nome, categoria, cidade, rating, tempo_medio_preparo, taxa_comissao, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', restaurants)
        
        self.conn.commit()
        print(f"✅ {n} restaurantes gerados")
    
    def generate_users(self, n=5000):
        """Gera dados fictícios de usuários"""
        cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 
                  'Brasília', 'Fortaleza', 'Recife', 'Porto Alegre']
        segmentos = ['Premium', 'Regular', 'Ocasional', 'Novo']
        
        users = []
        for i in range(n):
            user = (
                fake.name(),
                random.choice(cidades),
                fake.date_between(start_date='-2y', end_date='today').isoformat(),
                random.randint(18, 65),
                random.choice(['M', 'F']),
                random.choice(segmentos)
            )
            users.append(user)
            
        self.conn.executemany('''
            INSERT INTO usuarios (nome, cidade, data_cadastro, idade, genero, segmento)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users)
        
        self.conn.commit()
        print(f"✅ {n} usuários gerados")
    
    def generate_orders(self, n=20000):
        """Gera dados fictícios de pedidos"""
        # Obter IDs de restaurantes e usuários
        restaurant_ids = [row[0] for row in self.conn.execute('SELECT id FROM restaurantes').fetchall()]
        user_ids = [row[0] for row in self.conn.execute('SELECT id FROM usuarios').fetchall()]
        
        status_options = ['Entregue', 'Cancelado', 'Em andamento']
        
        orders = []
        for i in range(n):
            # Gera data aleatória nos últimos 365 dias
            base_date = datetime.now() - timedelta(days=random.randint(0, 365))
            status = random.choice(status_options)
            
            order = (
                random.choice(restaurant_ids),
                random.choice(user_ids),
                round(random.uniform(20, 150), 2),
                round(random.uniform(3, 12), 2),
                random.randint(20, 90),
                status,
                base_date.isoformat(),
                random.randint(1, 5) if status == 'Entregue' and random.random() > 0.1 else None
            )
            orders.append(order)
            
        self.conn.executemany('''
            INSERT INTO pedidos (restaurante_id, usuario_id, valor_pedido, taxa_entrega, tempo_entrega, status, data_pedido, avaliacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', orders)
        
        self.conn.commit()
        print(f"✅ {n} pedidos gerados")
    
    def generate_all_data(self):
        """Gera todos os dados fictícios"""
        print("🚀 Iniciando geração de dados do iFood...")
        print("Criando tabelas...")
        self.create_tables()
        
        print("Gerando restaurantes...")
        self.generate_restaurants()
        
        print("Gerando usuários...")
        self.generate_users()
        
        print("Gerando pedidos...")
        self.generate_orders()
        
        print("✅ Dados gerados com sucesso!")
        
        # Verificar dados criados
        restaurantes_count = self.conn.execute('SELECT COUNT(*) FROM restaurantes').fetchone()[0]
        usuarios_count = self.conn.execute('SELECT COUNT(*) FROM usuarios').fetchone()[0]
        pedidos_count = self.conn.execute('SELECT COUNT(*) FROM pedidos').fetchone()[0]
        
        print(f"\n📊 Resumo dos dados gerados:")
        print(f"- Restaurantes: {restaurantes_count:,}")
        print(f"- Usuários: {usuarios_count:,}")
        print(f"- Pedidos: {pedidos_count:,}")
        
    def close(self):
        """Fecha a conexão com o banco"""
        self.conn.close()

if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate_all_data()
    generator.close()
    print("\n🎉 Base de dados criada: ifood_data.db")
