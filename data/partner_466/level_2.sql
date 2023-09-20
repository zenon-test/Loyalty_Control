SELECT
    [Prin ID],
    [acc_id],
    [txn_id],
    [Transaction Type],
    [Transaction Amount],
    [Actual Points Awarded],
    [Expected Points],
    [Actual Points Awarded] - [Expected Points] AS [Leakage]
FROM 
    Transactions
WHERE 
    [Prin ID] = 466 AND [acc_id] = 29 AND [txn_id] = 29;
