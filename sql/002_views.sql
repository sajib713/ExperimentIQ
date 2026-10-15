-- SQL/Python KPI parity: all denominators are assigned customers (including non-visitors).
CREATE OR REPLACE VIEW vw_arm_kpis AS
SELECT segment,
       COUNT(*) AS assigned,
       SUM(conversion) AS conversions,
       SUM(visit) AS visits,
       SUM(spend) AS spend_total,
       CAST(SUM(conversion) AS DOUBLE PRECISION)/NULLIF(COUNT(*),0) AS conversion_rate,
       CAST(SUM(visit) AS DOUBLE PRECISION)/NULLIF(COUNT(*),0) AS visit_rate,
       CAST(SUM(spend) AS DOUBLE PRECISION)/NULLIF(COUNT(*),0) AS spend_per_assigned
FROM experiment_customers GROUP BY segment;

CREATE OR REPLACE VIEW vw_segment_kpis AS
SELECT segment, 'channel' AS dimension, channel AS dimension_value, COUNT(*) AS assigned,
       SUM(conversion) AS conversions, SUM(visit) AS visits, SUM(spend) AS spend_total
FROM experiment_customers GROUP BY segment,channel
UNION ALL
SELECT segment,'zip_code',zip_code,COUNT(*),SUM(conversion),SUM(visit),SUM(spend)
FROM experiment_customers GROUP BY segment,zip_code
UNION ALL
SELECT segment,'newbie',CAST(newbie AS TEXT),COUNT(*),SUM(conversion),SUM(visit),SUM(spend)
FROM experiment_customers GROUP BY segment,newbie
UNION ALL
SELECT segment,'mens',CAST(mens AS TEXT),COUNT(*),SUM(conversion),SUM(visit),SUM(spend)
FROM experiment_customers GROUP BY segment,mens
UNION ALL
SELECT segment,'womens',CAST(womens AS TEXT),COUNT(*),SUM(conversion),SUM(visit),SUM(spend)
FROM experiment_customers GROUP BY segment,womens
UNION ALL
SELECT segment,'history_segment',history_segment,COUNT(*),SUM(conversion),SUM(visit),SUM(spend)
FROM experiment_customers GROUP BY segment,history_segment
UNION ALL
SELECT segment,'recency',CAST(recency AS TEXT),COUNT(*),SUM(conversion),SUM(visit),SUM(spend)
FROM experiment_customers GROUP BY segment,recency;

CREATE OR REPLACE VIEW vw_control_lifts AS
SELECT t.segment AS treatment,
       t.assigned AS treatment_assigned, c.assigned AS control_assigned,
       t.conversion_rate AS treatment_conversion_rate,
       c.conversion_rate AS control_conversion_rate,
       100*(t.conversion_rate-c.conversion_rate) AS conversion_lift_pp,
       CASE WHEN c.conversion_rate>0 THEN t.conversion_rate/c.conversion_rate-1 ELSE NULL END AS relative_conversion_lift,
       t.spend_per_assigned-c.spend_per_assigned AS spend_lift_per_assigned
FROM vw_arm_kpis t CROSS JOIN vw_arm_kpis c
WHERE c.segment='No E-Mail' AND t.segment IN('Mens E-Mail','Womens E-Mail');
