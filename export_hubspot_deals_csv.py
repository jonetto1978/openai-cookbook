#!/usr/bin/env python3
"""
Export HubSpot Deals to CSV - Real Data Only
Calls MCP functions and exports to CSV for analysis
"""

import csv
import json
from datetime import datetime
import os

def export_deals_to_csv(month="2025-06", limit=100):
    """Export real HubSpot deals to CSV file"""
    
    print(f"🚀 EXPORTING REAL HUBSPOT DEALS - {month}")
    print("=" * 50)
    print("📞 Making real MCP call to HubSpot...")
    
    try:
        # Calculate date range
        year, month_num = month.split("-")
        start_date = f"{year}-{month_num.zfill(2)}-01"
        
        # Calculate last day of month
        if month_num in ["01", "03", "05", "07", "08", "10", "12"]:
            end_date = f"{year}-{month_num.zfill(2)}-31"
        elif month_num in ["04", "06", "09", "11"]:
            end_date = f"{year}-{month_num.zfill(2)}-30"
        else:  # February
            end_date = f"{year}-{month_num.zfill(2)}-28"
        
        # Real MCP call to HubSpot
        result = mcp_hubspot_hubspot_search_objects(
            objectType="deals",
            filterGroups=[{
                "filters": [{
                    "propertyName": "createdate",
                    "operator": "BETWEEN", 
                    "value": start_date,
                    "highValue": end_date
                }]
            }],
            properties=["dealname", "amount", "dealstage", "closedate", "createdate", "hs_object_id", "pipeline", "dealtype", "hubspot_owner_id"],
            limit=limit
        )
        
        deals = result.get("results", [])
        print(f"✅ Retrieved {len(deals)} real deals from HubSpot")
        
        if not deals:
            print("❌ No deals found for the specified period")
            return None
        
        # Prepare CSV file path
        os.makedirs("tools/outputs/csv_data/hubspot/deals", exist_ok=True)
        csv_filename = f"tools/outputs/csv_data/hubspot/deals/deals_{month.replace('-', '_')}_real.csv"
        
        # Export to CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'deal_id', 'deal_name', 'amount', 'deal_stage', 'deal_type', 
                'close_date', 'create_date', 'hubspot_owner_id', 'pipeline'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data
            for deal in deals:
                props = deal.get('properties', {})
                writer.writerow({
                    'deal_id': deal.get('id'),
                    'deal_name': props.get('dealname'),
                    'amount': props.get('amount'),
                    'deal_stage': props.get('dealstage'),
                    'deal_type': props.get('dealtype'),
                    'close_date': props.get('closedate'),
                    'create_date': props.get('createdate'),
                    'hubspot_owner_id': props.get('hubspot_owner_id'),
                    'pipeline': props.get('pipeline')
                })
        
        print(f"✅ Exported to: {csv_filename}")
        print(f"📊 Records exported: {len(deals)}")
        
        # Create metadata file
        metadata = {
            "export_date": datetime.now().isoformat(),
            "source": "HubSpot MCP API",
            "date_range": f"{start_date} to {end_date}",
            "total_records": len(deals),
            "file_path": csv_filename,
            "data_type": "deals",
            "filters": f"createdate BETWEEN {start_date} AND {end_date}"
        }
        
        metadata_filename = csv_filename.replace('.csv', '_metadata.json')
        with open(metadata_filename, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Metadata saved: {metadata_filename}")
        return csv_filename
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return None

def export_deals_via_function_call():
    """Alternative method using function call format"""
    print("🔄 Attempting export via direct function call...")
    
    try:
        # This should work when running in MCP environment
        from datetime import datetime
        
        # Make the call and export result
        csv_file = export_deals_to_csv("2025-06", 100)
        
        if csv_file:
            print(f"🎉 Export successful: {csv_file}")
            return csv_file
        else:
            print("❌ Export failed")
            return None
            
    except NameError as e:
        print(f"⚠️  MCP functions not available in this context: {e}")
        print("📝 Run this script in an MCP-enabled environment")
        return None

if __name__ == "__main__":
    export_deals_via_function_call() 