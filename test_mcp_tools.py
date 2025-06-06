#!/usr/bin/env python3
"""
Test Script for Existing MCP Tools - Colppy Analytics
This script demonstrates how to use your existing MCP tools through the MCPDataConnector
"""

import json
from datetime import datetime, timedelta
from ceo_assistant_enhanced import MCPDataConnector

def test_hubspot_mcp_tools():
    """Test HubSpot MCP tools through MCPDataConnector"""
    print("🏢 Testing HubSpot MCP Tools...")
    
    try:
        connector = MCPDataConnector()
        
        # 1. Get user details
        print("\n1. Getting HubSpot user details...")
        user_details = connector.get_hubspot_user_details()
        print(f"✅ User Details: {json.dumps(user_details, indent=2)}")
        
        # 2. Get deals data
        print("\n2. Getting deals data...")
        deals = connector.get_hubspot_deals_data(limit=10)
        print(f"✅ Found {len(deals.get('results', []))} deals")
        
        # 3. Get contacts metrics
        print("\n3. Getting contacts metrics...")
        contacts = connector.get_hubspot_contacts_metrics()
        print(f"✅ Contact metrics: {json.dumps(contacts, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"❌ HubSpot MCP Error: {e}")
        return False

def test_mixpanel_mcp_tools():
    """Test Mixpanel MCP tools through MCPDataConnector"""
    print("\n📊 Testing Mixpanel MCP Tools...")
    
    try:
        connector = MCPDataConnector()
        
        # 1. Get top events
        print("\n1. Getting top events...")
        top_events = connector.get_mixpanel_top_events(limit=10)
        print(f"✅ Top Events: {json.dumps(top_events, indent=2)}")
        
        # 2. Get user engagement
        print("\n2. Getting user engagement...")
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        engagement = connector.get_mixpanel_user_engagement(from_date, to_date)
        print(f"✅ Engagement: {json.dumps(engagement, indent=2)}")
        
        # 3. Get funnel data
        print("\n3. Getting funnel data...")
        funnel = connector.get_mixpanel_conversion_funnel()
        print(f"✅ Funnel: {json.dumps(funnel, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mixpanel MCP Error: {e}")
        return False

def test_colppy_specific_queries():
    """Test Colppy-specific business queries"""
    print("\n🇦🇷 Testing Colppy-Specific Queries...")
    
    try:
        connector = MCPDataConnector()
        
        # 1. Get deals data and analyze
        print("\n1. Analyzing June 2025 deals...")
        deals = connector.get_hubspot_deals_data(month="2025-06")
        
        # Filter for NEW_BUSINESS deals
        new_business_deals = []
        for deal in deals.get('results', []):
            deal_type = deal.get('properties', {}).get('dealtype', '')
            if deal_type == 'NEW_BUSINESS':
                new_business_deals.append(deal)
        
        print(f"✅ Found {len(new_business_deals)} NEW_BUSINESS deals")
        
        # 2. Get Colppy-specific events from Mixpanel
        print("\n2. Getting accounting events...")
        events = connector.get_mixpanel_top_events(limit=10)
        
        # Filter for accounting-related events
        accounting_events = []
        for event in events.get('events', []):
            event_name = event.get('event', '').lower()
            if any(keyword in event_name for keyword in ['invoice', 'login', 'payment', 'report']):
                accounting_events.append(event)
        
        print(f"✅ Found {len(accounting_events)} accounting-related events")
        
        return True
        
    except Exception as e:
        print(f"❌ Colppy-specific query error: {e}")
        return False

def export_sample_data():
    """Export sample data for analysis"""
    print("\n📥 Exporting Sample Data...")
    
    try:
        connector = MCPDataConnector()
        
        # Export deals data
        print("\n1. Exporting deals data...")
        deals = connector.get_hubspot_deals_data(limit=50)
        deals_count = len(deals.get('results', []))
        print(f"✅ Ready to export {deals_count} deals")
        
        # Export Mixpanel events
        print("\n2. Exporting Mixpanel events...")
        events = connector.get_mixpanel_top_events(limit=20)
        events_count = len(events.get('events', []))
        print(f"✅ Ready to export {events_count} events")
        
        return True
        
    except Exception as e:
        print(f"❌ Export error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Existing MCP Tools for Colppy")
    print("=" * 50)
    
    # Test each MCP tool set
    hubspot_ok = test_hubspot_mcp_tools()
    mixpanel_ok = test_mixpanel_mcp_tools()
    colppy_ok = test_colppy_specific_queries()
    export_ok = export_sample_data()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    print(f"   HubSpot MCP: {'✅ Working' if hubspot_ok else '❌ Issues'}")
    print(f"   Mixpanel MCP: {'✅ Working' if mixpanel_ok else '❌ Issues'}")
    print(f"   Colppy Queries: {'✅ Working' if colppy_ok else '❌ Issues'}")
    print(f"   Data Export: {'✅ Working' if export_ok else '❌ Issues'}")
    
    if all([hubspot_ok, mixpanel_ok]):
        print("\n🎉 Your MCP tools are ready to use!")
        print("\nNext steps:")
        print("1. Run 'python ceo_assistant_enhanced.py' to use the enhanced assistant")
        print("2. Use specific MCP calls for data exports")
        print("3. Build custom reports combining HubSpot + Mixpanel data")
    else:
        print("\n⚠️  Some MCP tools need configuration")
        print("Check your API keys and MCP server setup")

if __name__ == "__main__":
    main() 