-- Expect zero offending rows except separately documented signal checks.
SELECT 'invalid_arm' AS check_name,COUNT(*) AS issue_count FROM experiment_customers
WHERE segment NOT IN('No E-Mail','Mens E-Mail','Womens E-Mail')
UNION ALL
SELECT 'out_of_range_recency',COUNT(*) FROM experiment_customers WHERE recency NOT BETWEEN 1 AND 12
UNION ALL
SELECT 'positive_spend_nonconversion',COUNT(*) FROM experiment_customers WHERE spend>0 AND conversion=0
UNION ALL
SELECT 'conversion_without_visit',COUNT(*) FROM experiment_customers WHERE conversion=1 AND visit=0;
