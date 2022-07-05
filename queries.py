VOTE_QUERY = """
select block_timestamp, 
event_inputs:proposalId as proposalId, 
event_inputs:reason as reason,
event_inputs:support as support,
event_inputs:voter as voter,
to_numeric(event_inputs:votes) as votes,
1 as event
from ethereum.core.fact_event_logs fe
where block_number >= 12000000 
and fe.contract_address = lower('0x6f3E6272A167e8AcCb32072d08E0957F9c79223d')
and event_name = 'VoteCast';
"""
TRAIT_QUERY = """
select 
block_number as mint_block,
block_timestamp as mint_time,
tx_hash as mint_hash,
tokenflow_eth.hextoint(topics[1])::integer as tokenID
from ethereum.core.fact_event_logs
where block_number > 12000000
and contract_address = '0x9c8ff314c9bc7f6e59a9d9225fb22946427edc03'
and topics[0]::string = '0x1106ee9d020bfbb5ee34cf5535a5fbf024a011bd130078088cbf124ab3092478'
order by tokenId desc;
"""