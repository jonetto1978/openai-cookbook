#!/usr/bin/env python3
"""
Analyze HubSpot Deals from CSV - Real Data Only
Reads CSV file exported from HubSpot MCP and performs calculations
"""

import pandas as pd
import json
from datetime import datetime
import os

def analyze_deals_from_csv(csv_file_path="tools/outputs/csv_data/hubspot/deals/deals_2025_06_real.csv"):
    """Analyze deals data from CSV file"""
    
    print("🚀 ANALYZING REAL HUBSPOT DEALS FROM CSV")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(csv_file_path):
        print(f"❌ CSV file not found: {csv_file_path}")
        return None
    
    # Load metadata if available
    metadata_file = csv_file_path.replace('.csv', '_metadata.json')
    metadata = {}
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        print(f"✅ Data Source: {metadata.get('source', 'Unknown')}")
        print(f"✅ Date Range: {metadata.get('date_range', 'Unknown')}")
        print(f"✅ Export Date: {metadata.get('export_date', 'Unknown')}")
    
    print(f"📊 Reading CSV: {csv_file_path}")
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        print(f"✅ Loaded {len(df)} records from CSV")
        print(f"✅ Columns: {list(df.columns)}")
        print()
        
        # Clean data
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['deal_stage'] = df['deal_stage'].fillna('unknown')
        df['deal_type'] = df['deal_type'].fillna('Not specified')
        
        # Calculate metrics
        total_deals = len(df)
        total_value = df['amount'].sum()
        avg_deal_size = df['amount'].mean()
        
        # Deal stage analysis
        stage_counts = df['deal_stage'].value_counts()
        closed_won_deals = df[df['deal_stage'] == 'closedwon']
        closed_won_count = len(closed_won_deals)
        closed_won_value = closed_won_deals['amount'].sum()
        
        # Deal type analysis
        type_counts = df['deal_type'].value_counts()
        
        # Argentina company analysis
        argentina_keywords = ['S.A.', 'SAS', 'SRL', 'LIMITADA', 'ESTUDIO', 'COOPERATIVA']
        df['is_argentina_entity'] = df['deal_name'].str.upper().str.contains('|'.join(argentina_keywords), na=False)
        argentina_deals = df[df['is_argentina_entity'] == True]
        
        # Display analysis
        print("💰 FINANCIAL METRICS (from CSV):")
        print(f"   Total Pipeline Value: ARS ${total_value:,.0f}")
        print(f"   Total Deals: {total_deals}")
        print(f"   Average Deal Size: ARS ${avg_deal_size:,.0f}")
        print(f"   Closed Won Revenue: ARS ${closed_won_value:,.0f}")
        print(f"   Closed Won Count: {closed_won_count} deals")
        print()
        
        print("📊 DEAL STAGE DISTRIBUTION:")
        for stage, count in stage_counts.items():
            percentage = (count/total_deals)*100
            print(f"   {stage.replace('', ' ').title()}: {count} deals ({percentage:.1f}%)")
        print()
        
        print("🎯 DEAL TYPE BREAKDOWN:")
        for deal_type, count in type_counts.items():
            percentage = (count/total_deals)*100
            print(f"   {deal_type}: {count} deals ({percentage:.1f}%)")
        print()
        
        print("🏆 TOP 5 DEALS BY VALUE:")
        top_deals = df.nlargest(5, 'amount')
        for i, (_, deal) in enumerate(top_deals.iterrows(), 1):
            amount_str = f"ARS ${deal['amount']:,.0f}" if pd.notna(deal['amount']) else "No amount"
            print(f"   {i}. {deal['deal_name']} - {amount_str} ({deal['deal_stage']})")
        print()
        
        print("🇦🇷 ARGENTINA SMB ANALYSIS:")
        print(f"   Total SMB deals: {total_deals}")
        print(f"   Argentina entities: {len(argentina_deals)} deals ({len(argentina_deals)/total_deals*100:.1f}%)")
        print(f"   Closed won deals: {closed_won_count} deals")
        print(f"   Conversion rate: {(closed_won_count/total_deals)*100:.1f}%")
        print(f"   Cross-selling deals: {type_counts.get('Cross Selling', 0)} deals")
        print()
        
        print("📈 BUSINESS INSIGHTS:")
        print(f"   • Strong conversion: {closed_won_count}/{total_deals} deals closed ({(closed_won_count/total_deals)*100:.1f}%)")
        print(f"   • Healthy pipeline: {stage_counts.get('qualifiedtobuy', 0)} qualified prospects")
        print(f"   • Active sales: {stage_counts.get('presentationscheduled', 0)} presentations scheduled")
        print(f"   • Cross-sell opportunity: {type_counts.get('Cross Selling', 0)} existing customer upgrades")
        
        new_business_deals = df[df['deal_type'] == 'NEW_BUSINESS']
        if len(new_business_deals) > 0:
            avg_new_business = new_business_deals['amount'].mean()
            print(f"   • Average NEW_BUSINESS deal: ARS ${avg_new_business:,.0f}")
        
        # Return summary for further use
        return {
            "total_deals": total_deals,
            "total_value": float(total_value) if pd.notna(total_value) else 0,
            "closed_won": closed_won_count,
            "conversion_rate": (closed_won_count/total_deals)*100,
            "deal_stages": stage_counts.to_dict(),
            "deal_types": type_counts.to_dict(),
            "argentina_entities": len(argentina_deals),
            "avg_deal_size": float(avg_deal_size) if pd.notna(avg_deal_size) else 0,
            "source_file": csv_file_path,
            "metadata": metadata
        }
        
    except Exception as e:
        print(f"❌ Error analyzing CSV: {e}")
        return None

def export_analysis_summary(analysis_result, output_file="tools/outputs/colppy_analysis/june_2025_analysis.json"):
    """Export analysis summary to JSON"""
    if analysis_result:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        analysis_result['analysis_date'] = datetime.now().isoformat()
        
        with open(output_file, 'w') as f:
            json.dump(analysis_result, f, indent=2)
        
        print(f"✅ Analysis summary exported to: {output_file}")

if __name__ == "__main__":
    # Analyze the deals
    result = analyze_deals_from_csv()
    
    if result:
        print(f"\n📋 CSV ANALYSIS SUMMARY:")
        print(f"   Source: {result['source_file']}")
        print(f"   Deals: {result['total_deals']} worth ARS ${result['total_value']:,.0f}")
        print(f"   Conversion: {result['conversion_rate']:.1f}%")
        print(f"   Argentina entities: {result['argentina_entities']}")
        
        # Export summary
        export_analysis_summary(result) 