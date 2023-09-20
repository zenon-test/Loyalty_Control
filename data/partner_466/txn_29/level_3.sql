SELECT
    txn_id,
    clientNumber,
    [Prin ID],
    [Prin Description],
    program_name,
    a,
    transactionAmount,
    merchantSystemIdentifier,
    merchantPrincipalIdentifier,
    merchantAgentIdentifier,
    transactionCode,
    merchantCategoryCode,
    principalNumber,
    associatedMerchantSystemNumber,
    associatedMerchantPrinNumber,
    clientControl18,
    cardAcceptorCode,
    earn_rule_flg,
    excl_rule_flg,
    calculation_multiplier,
    expected_points,
    actual_points
FROM 
    TransactionDetails
WHERE 
    txn_id = 29 AND clientNumber = 1201 AND [Prin ID] = 466;
