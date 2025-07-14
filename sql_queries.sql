-- Análises SQL para Dashboard Executivo iFood
-- Demonstra habilidades avançadas em SQL e análise de dados

-- 1. ANÁLISE DE PERFORMANCE DE RESTAURANTES
-- Top 10 restaurantes por volume de vendas
SELECT 
    r.nome,
    r.categoria,
    r.cidade,
    COUNT(p.id) as total_pedidos,
    SUM(p.valor_pedido) as receita_total,
    AVG(p.valor_pedido) as ticket_medio,
    AVG(p.avaliacao) as rating_medio,
    AVG(p.tempo_entrega) as tempo_medio_entrega
FROM restaurantes r
LEFT JOIN pedidos p ON r.id = p.restaurante_id
WHERE p.status = 'Entregue'
GROUP BY r.id, r.nome, r.categoria, r.cidade
ORDER BY receita_total DESC
LIMIT 10;

-- 2. ANÁLISE TEMPORAL DE PEDIDOS
-- Volume de pedidos por mês e taxa de crescimento
WITH monthly_orders AS (
    SELECT 
        strftime('%Y-%m', data_pedido) as mes,
        COUNT(*) as total_pedidos,
        SUM(valor_pedido) as receita_mensal,
        AVG(valor_pedido) as ticket_medio_mensal
    FROM pedidos 
    WHERE status = 'Entregue'
    GROUP BY strftime('%Y-%m', data_pedido)
),
growth_calc AS (
    SELECT 
        mes,
        total_pedidos,
        receita_mensal,
        ticket_medio_mensal,
        LAG(total_pedidos) OVER (ORDER BY mes) as pedidos_mes_anterior,
        LAG(receita_mensal) OVER (ORDER BY mes) as receita_mes_anterior
    FROM monthly_orders
)
SELECT 
    mes,
    total_pedidos,
    receita_mensal,
    ticket_medio_mensal,
    CASE 
        WHEN pedidos_mes_anterior IS NOT NULL 
        THEN ROUND(((total_pedidos - pedidos_mes_anterior) * 100.0 / pedidos_mes_anterior), 2)
        ELSE NULL 
    END as crescimento_pedidos_pct,
    CASE 
        WHEN receita_mes_anterior IS NOT NULL 
        THEN ROUND(((receita_mensal - receita_mes_anterior) * 100.0 / receita_mes_anterior), 2)
        ELSE NULL 
    END as crescimento_receita_pct
FROM growth_calc
ORDER BY mes;

-- 3. ANÁLISE DE SEGMENTAÇÃO DE CLIENTES
-- RFM Analysis (Recency, Frequency, Monetary)
WITH customer_metrics AS (
    SELECT 
        u.id as usuario_id,
        u.nome,
        u.segmento,
        u.cidade,
        COUNT(p.id) as frequencia,
        SUM(p.valor_pedido) as valor_monetario,
        AVG(p.valor_pedido) as ticket_medio,
        MAX(p.data_pedido) as ultimo_pedido,
        julianday('now') - julianday(MAX(p.data_pedido)) as dias_desde_ultimo_pedido
    FROM usuarios u
    LEFT JOIN pedidos p ON u.id = p.usuario_id AND p.status = 'Entregue'
    GROUP BY u.id, u.nome, u.segmento, u.cidade
),
rfm_scores AS (
    SELECT 
        *,
        CASE 
            WHEN dias_desde_ultimo_pedido <= 30 THEN 5
            WHEN dias_desde_ultimo_pedido <= 60 THEN 4
            WHEN dias_desde_ultimo_pedido <= 90 THEN 3
            WHEN dias_desde_ultimo_pedido <= 180 THEN 2
            ELSE 1
        END as score_recencia,
        CASE 
            WHEN frequencia >= 20 THEN 5
            WHEN frequencia >= 10 THEN 4
            WHEN frequencia >= 5 THEN 3
            WHEN frequencia >= 2 THEN 2
            ELSE 1
        END as score_frequencia,
        CASE 
            WHEN valor_monetario >= 1000 THEN 5
            WHEN valor_monetario >= 500 THEN 4
            WHEN valor_monetario >= 200 THEN 3
            WHEN valor_monetario >= 100 THEN 2
            ELSE 1
        END as score_monetario
    FROM customer_metrics
    WHERE frequencia > 0
)
SELECT 
    segmento,
    COUNT(*) as total_clientes,
    AVG(score_recencia) as recencia_media,
    AVG(score_frequencia) as frequencia_media,
    AVG(score_monetario) as monetario_medio,
    AVG(valor_monetario) as lifetime_value_medio,
    AVG(frequencia) as pedidos_medio_por_cliente
FROM rfm_scores
GROUP BY segmento
ORDER BY lifetime_value_medio DESC;

-- 4. ANÁLISE DE EFICIÊNCIA OPERACIONAL
-- Tempo médio de entrega por cidade e categoria
SELECT 
    r.cidade,
    r.categoria,
    COUNT(p.id) as total_entregas,
    AVG(p.tempo_entrega) as tempo_medio_entrega,
    AVG(r.tempo_medio_preparo) as tempo_medio_preparo,
    AVG(p.tempo_entrega - r.tempo_medio_preparo) as tempo_medio_logistica,
    AVG(p.avaliacao) as satisfacao_media,
    SUM(CASE WHEN p.tempo_entrega <= 45 THEN 1 ELSE 0 END) * 100.0 / COUNT(p.id) as pct_entregas_no_prazo
FROM restaurantes r
JOIN pedidos p ON r.id = p.restaurante_id
WHERE p.status = 'Entregue'
GROUP BY r.cidade, r.categoria
HAVING COUNT(p.id) >= 10
ORDER BY tempo_medio_entrega ASC;

-- 5. ANÁLISE DE CHURN E RETENÇÃO
-- Taxa de retenção mensal
WITH monthly_active_users AS (
    SELECT 
        strftime('%Y-%m', data_pedido) as mes,
        usuario_id
    FROM pedidos 
    WHERE status = 'Entregue'
    GROUP BY strftime('%Y-%m', data_pedido), usuario_id
),
retention_analysis AS (
    SELECT 
        m1.mes as mes_atual,
        COUNT(DISTINCT m1.usuario_id) as usuarios_ativos,
        COUNT(DISTINCT m2.usuario_id) as usuarios_retidos,
        CASE 
            WHEN COUNT(DISTINCT m1.usuario_id) > 0 
            THEN ROUND(COUNT(DISTINCT m2.usuario_id) * 100.0 / COUNT(DISTINCT m1.usuario_id), 2)
            ELSE 0 
        END as taxa_retencao
    FROM monthly_active_users m1
    LEFT JOIN monthly_active_users m2 ON 
        m1.usuario_id = m2.usuario_id 
        AND date(m1.mes || '-01', '+1 month') = date(m2.mes || '-01')
    GROUP BY m1.mes
)
SELECT * FROM retention_analysis
ORDER BY mes_atual;

-- 6. ANÁLISE DE CANCELAMENTOS
-- Taxa de cancelamento por categoria e fatores relacionados
SELECT 
    r.categoria,
    r.cidade,
    COUNT(p.id) as total_pedidos,
    SUM(CASE WHEN p.status = 'Cancelado' THEN 1 ELSE 0 END) as pedidos_cancelados,
    ROUND(SUM(CASE WHEN p.status = 'Cancelado' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.id), 2) as taxa_cancelamento,
    AVG(CASE WHEN p.status = 'Entregue' THEN r.tempo_medio_preparo END) as tempo_preparo_medio,
    AVG(CASE WHEN p.status = 'Entregue' THEN p.valor_pedido END) as valor_medio_entregues,
    AVG(CASE WHEN p.status = 'Cancelado' THEN p.valor_pedido END) as valor_medio_cancelados
FROM restaurantes r
JOIN pedidos p ON r.id = p.restaurante_id
GROUP BY r.categoria, r.cidade
HAVING COUNT(p.id) >= 20
ORDER BY taxa_cancelamento DESC;

-- 7. OPORTUNIDADES DE CRESCIMENTO
-- Cidades com potencial de expansão (baixa penetração, alta demanda)
WITH city_metrics AS (
    SELECT 
        r.cidade,
        COUNT(DISTINCT r.id) as total_restaurantes,
        COUNT(DISTINCT p.usuario_id) as usuarios_ativos,
        COUNT(p.id) as total_pedidos,
        SUM(p.valor_pedido) as receita_total,
        AVG(p.valor_pedido) as ticket_medio,
        COUNT(p.id) * 1.0 / COUNT(DISTINCT r.id) as pedidos_por_restaurante
    FROM restaurantes r
    LEFT JOIN pedidos p ON r.id = p.restaurante_id AND p.status = 'Entregue'
    GROUP BY r.cidade
)
SELECT 
    cidade,
    total_restaurantes,
    usuarios_ativos,
    total_pedidos,
    receita_total,
    ticket_medio,
    pedidos_por_restaurante,
    CASE 
        WHEN pedidos_por_restaurante > 100 AND total_restaurantes < 30 THEN 'Alto Potencial'
        WHEN pedidos_por_restaurante > 50 AND total_restaurantes < 50 THEN 'Médio Potencial'
        ELSE 'Saturado'
    END as classificacao_potencial
FROM city_metrics
ORDER BY pedidos_por_restaurante DESC;
