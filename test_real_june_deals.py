#!/usr/bin/env python3
"""
Test script that calls real HubSpot MCP tools directly for June 2025 deals
No cached or mock data - only real API calls
"""

import json
from datetime import datetime

def test_real_june_deals():
    """Test with real MCP calls for June 2025 deals"""
    print("🚀 REAL HUBSPOT DATA TEST - JUNE 2025")
    print("=" * 50)
    print("⚠️  Making real API calls - no mock/cached data")
    print()
    
    try:
        # Real MCP call for June 2025 deals
        print("📞 Calling HubSpot MCP search for June 2025...")
        
        result = mcp_hubspot_hubspot_search_objects(
            objectType="deals",
            filterGroups=[{
                "filters": [{
                    "propertyName": "createdate",
                    "operator": "BETWEEN", 
                    "value": "2025-06-01",
                    "highValue": "2025-06-30"
                }]
            }],
            properties=["dealname", "amount", "dealstage", "closedate", "createdate", "hs_object_id", "pipeline", "dealtype", "hubspot_owner_id"],
            limit=100
        )
        
        deals = result.get("results", [])
        print(f"✅ Retrieved {len(deals)} real deals from HubSpot")
        print()
        
        if not deals:
            print("❌ No deals found for June 2025")
            return result
        
        # Analyze real data
        total_value = 0
        deal_stages = {}
        deal_types = {}
        closed_won_deals = []
        
        for deal in deals:
            props = deal.get('properties', {})
            
            # Calculate total pipeline value
            amount = props.get('amount')
            if amount and amount != 'null' and amount != '':
                try:
                    total_value += float(amount)
                except:
                    pass
            
            # Count deal stages
            stage = props.get('dealstage', 'unknown')
            deal_stages[stage] = deal_stages.get(stage, 0) + 1
            
            # Count deal types  
            deal_type = props.get('dealtype', 'unknown')
            deal_types[deal_type] = deal_types.get(deal_type, 0) + 1
            
            # Track closed won deals
            if stage == 'closedwon':
                closed_won_deals.append(deal)
        
        # Display real results
        print("💰 REAL FINANCIAL METRICS:")
        print(f"   Total Pipeline Value: ARS ${total_value:,.0f}")
        print(f"   Average Deal Size: ARS ${total_value/len(deals):,.0f}")
        print()
        
        print("📊 REAL DEAL DISTRIBUTION:")
        for stage, count in deal_stages.items():
            percentage = (count/len(deals))*100
            print(f"   {stage}: {count} deals ({percentage:.1f}%)")
        print()
        
        print("🎯 REAL DEAL TYPES:")
        for deal_type, count in deal_types.items():
            percentage = (count/len(deals))*100
            print(f"   {deal_type or 'Not specified'}: {count} deals ({percentage:.1f}%)")
        print()
        
        # Show top deals by value
        print("🏆 TOP 5 REAL DEALS BY VALUE:")
        deals_with_amounts = []
        for deal in deals:
            amount = deal['properties'].get('amount')
            if amount and amount != 'null' and amount != '':
                try:
                    deals_with_amounts.append((deal, float(amount)))
                except:
                    pass
        
        deals_with_amounts.sort(key=lambda x: x[1], reverse=True)
        
        for i, (deal, amount) in enumerate(deals_with_amounts[:5], 1):
            props = deal['properties']
            print(f"   {i}. {props.get('dealname', 'N/A')} - ARS ${amount:,.0f} ({props.get('dealstage', 'N/A')})")
        
        print()
        print("🇦🇷 ARGENTINA SMB ANALYSIS:")
        print(f"   Total SMB deals: {len(deals)}")
        print(f"   Closed won: {len(closed_won_deals)} deals")
        if len(deals) > 0:
            conversion_rate = (len(closed_won_deals) / len(deals)) * 100
            print(f"   Conversion rate: {conversion_rate:.1f}%")
        
        return result
        
    except Exception as e:
        print(f"❌ Real MCP call failed: {e}")
        print("⚠️  This indicates MCP tools are not available in this context")
        return {"error": str(e)}

if __name__ == "__main__":
    test_real_june_deals() 