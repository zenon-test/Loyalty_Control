SELECT
    [Client ID],
    [Prin ID],
    [Prin Description],
    [As of Date],
    [Transaction Amount],
    [Actual Points Awarded],
    [Expected Points],
    [Actual Points Awarded] - [Expected Points] AS [Difference],
    CASE WHEN [Expected Points] != 0 THEN 
        CAST(([Actual Points Awarded] - [Expected Points]) * 1.0 / [Expected Points] AS FLOAT) 
    ELSE 
        0 
    END AS [% Difference],
    CASE WHEN [Actual Points Awarded] = [Expected Points] THEN 'Pass' ELSE 'Fail' END AS [Monitoring]
FROM 
    Transactions
WHERE 
    [As of Date] = '2023-03-02';
