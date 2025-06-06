#!/usr/bin/env python3
"""
Test script for real HubSpot deals data - June 2025
"""

from ceo_assistant_enhanced import MCPDataConnector
import json

def test_real_hubspot_deals():
    """Test the real HubSpot deals data"""
    print("=== REAL HUBSPOT DEALS DATA - JUNE 2025 ===")
    
    # Initialize connector
    connector = MCPDataConnector()
    
    # Get real deals data from June 2025
    deals_data = connector.get_hubspot_deals_data(limit=50, month='2025-06')
    
    # Basic stats
    results = deals_data.get('results', [])
    print(f"Total deals found: {len(results)}")
    print()
    
    # Calculate metrics
    total_value = 0
    deal_stages = {}
    deal_types = {}
    
    for deal in results:
        props = deal.get('properties', {})
        
        # Calculate total pipeline value
        amount = props.get('amount')
        if amount and amount != 'null':
            total_value += float(amount)
        
        # Count deal stages
        stage = props.get('dealstage', 'unknown')
        deal_stages[stage] = deal_stages.get(stage, 0) + 1
        
        # Count deal types  
        deal_type = props.get('dealtype', 'unknown')
        deal_types[deal_type] = deal_types.get(deal_type, 0) + 1
    
    print(f"💰 Total Pipeline Value: ARS ${total_value:,.0f}")
    print(f"📊 Deal Stages: {json.dumps(deal_stages, indent=2)}")
    print(f"🎯 Deal Types: {json.dumps(deal_types, indent=2)}")
    print()
    
    # Show top 3 deals
    print("🏆 TOP 3 DEALS BY VALUE:")
    deals_with_amounts = [(d, float(d['properties'].get('amount', 0))) for d in results if d['properties'].get('amount') and d['properties']['amount'] != 'null']
    deals_with_amounts.sort(key=lambda x: x[1], reverse=True)
    
    for i, (deal, amount) in enumerate(deals_with_amounts[:3], 1):
        props = deal['properties']
        print(f"{i}. {props.get('dealname', 'N/A')} - ARS ${amount:,.0f} ({props.get('dealstage', 'N/A')})")
    
    return deals_data

if __name__ == "__main__":
    test_real_hubspot_deals() 