#!/usr/bin/env python3
"""
Comprehensive Deals Analysis: 2024 vs 2025 (Jan-May Comparison)
Analyzes all deals data retrieved from HubSpot to provide insights on:
- Deals generated, closed, conversion rates
- Pipeline performance, deal stages
- Revenue analysis, average deal size
- Lead sources and attribution analysis
- Monthly trends and growth metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class DealsAnalyzer:
    def __init__(self):
        self.deals_2024 = []
        self.deals_2025 = []
        self.df_2024 = None
        self.df_2025 = None
        
    def add_deals_data(self, deals_data, year):
        """Add deals data to the appropriate year list"""
        if year == 2024:
            self.deals_2024.extend(deals_data)
        elif year == 2025:
            self.deals_2025.extend(deals_data)
            
    def process_deals_data(self):
        """Convert deals data to DataFrames and process"""
        # Process 2024 data
        if self.deals_2024:
            self.df_2024 = pd.DataFrame(self.deals_2024)
            self.df_2024 = self._clean_dataframe(self.df_2024, 2024)
            
        # Process 2025 data
        if self.deals_2025:
            self.df_2025 = pd.DataFrame(self.deals_2025)
            self.df_2025 = self._clean_dataframe(self.df_2025, 2025)
            
    def _clean_dataframe(self, df, year):
        """Clean and standardize dataframe"""
        # Convert dates
        if 'createdate' in df.columns:
            df['createdate'] = pd.to_datetime(df['createdate'])
        if 'closedate' in df.columns:
            df['closedate'] = pd.to_datetime(df['closedate'])
            
        # Convert amount to numeric
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            
        # Add year column
        df['year'] = year
        
        # Process deal stages for won/lost identification
        if 'dealstage' in df.columns:
            df['is_closed_won'] = df['dealstage'].str.contains('closedwon|won', case=False, na=False)
            df['is_closed_lost'] = df['dealstage'].str.contains('closedlost|lost', case=False, na=False)
            df['is_closed'] = df['is_closed_won'] | df['is_closed_lost']
            
        # Add month for trending
        if 'createdate' in df.columns:
            df['create_month'] = df['createdate'].dt.month
            df['create_month_name'] = df['createdate'].dt.strftime('%B')
            
        return df
        
    def calculate_key_metrics(self):
        """Calculate key metrics for comparison"""
        metrics = {}
        
        for year, df in [(2024, self.df_2024), (2025, self.df_2025)]:
            if df is not None and not df.empty:
                total_deals = len(df)
                closed_won = df['is_closed_won'].sum() if 'is_closed_won' in df.columns else 0
                closed_lost = df['is_closed_lost'].sum() if 'is_closed_lost' in df.columns else 0
                closed_total = df['is_closed'].sum() if 'is_closed' in df.columns else 0
                
                # Revenue metrics
                total_revenue = df[df['is_closed_won'] == True]['amount'].sum() if 'amount' in df.columns else 0
                avg_deal_size = df[df['is_closed_won'] == True]['amount'].mean() if 'amount' in df.columns else 0
                
                # Conversion rates
                conversion_rate = (closed_won / total_deals * 100) if total_deals > 0 else 0
                close_rate = (closed_total / total_deals * 100) if total_deals > 0 else 0
                win_rate = (closed_won / closed_total * 100) if closed_total > 0 else 0
                
                metrics[year] = {
                    'total_deals_generated': total_deals,
                    'deals_closed_won': closed_won,
                    'deals_closed_lost': closed_lost,
                    'deals_closed_total': closed_total,
                    'total_revenue': total_revenue,
                    'avg_deal_size': avg_deal_size,
                    'conversion_rate_percent': conversion_rate,
                    'close_rate_percent': close_rate,
                    'win_rate_percent': win_rate
                }
                
        return metrics
        
    def analyze_monthly_trends(self):
        """Analyze monthly trends for both years"""
        monthly_data = {}
        
        for year, df in [(2024, self.df_2024), (2025, self.df_2025)]:
            if df is not None and not df.empty:
                monthly = df.groupby('create_month').agg({
                    'dealname': 'count',  # Total deals
                    'is_closed_won': 'sum',  # Won deals
                    'amount': lambda x: x[df.loc[x.index, 'is_closed_won'] == True].sum()  # Revenue
                }).rename(columns={'dealname': 'total_deals', 'is_closed_won': 'won_deals', 'amount': 'revenue'})
                
                monthly['conversion_rate'] = (monthly['won_deals'] / monthly['total_deals'] * 100)
                monthly_data[year] = monthly
                
        return monthly_data
        
    def analyze_lead_sources(self):
        """Analyze lead sources and attribution"""
        source_data = {}
        
        for year, df in [(2024, self.df_2024), (2025, self.df_2025)]:
            if df is not None and not df.empty and 'hs_analytics_source' in df.columns:
                sources = df.groupby('hs_analytics_source').agg({
                    'dealname': 'count',
                    'is_closed_won': 'sum',
                    'amount': lambda x: x[df.loc[x.index, 'is_closed_won'] == True].sum()
                }).rename(columns={'dealname': 'total_deals', 'is_closed_won': 'won_deals', 'amount': 'revenue'})
                
                sources['conversion_rate'] = (sources['won_deals'] / sources['total_deals'] * 100)
                source_data[year] = sources.sort_values('total_deals', ascending=False)
                
        return source_data
        
    def generate_comprehensive_report(self):
        """Generate comprehensive comparison report"""
        print("=" * 80)
        print("COMPREHENSIVE DEALS ANALYSIS: 2024 vs 2025 (January - May)")
        print("=" * 80)
        
        # Calculate metrics
        metrics = self.calculate_key_metrics()
        
        print("\n🎯 KEY PERFORMANCE INDICATORS")
        print("-" * 50)
        
        if 2024 in metrics and 2025 in metrics:
            m24, m25 = metrics[2024], metrics[2025]
            
            print(f"📊 DEALS GENERATED:")
            print(f"   2024: {m24['total_deals_generated']:,} deals")
            print(f"   2025: {m25['total_deals_generated']:,} deals")
            growth = ((m25['total_deals_generated'] - m24['total_deals_generated']) / m24['total_deals_generated'] * 100)
            print(f"   Growth: {growth:+.1f}%")
            
            print(f"\n💰 DEALS CLOSED WON:")
            print(f"   2024: {m24['deals_closed_won']:,} deals")
            print(f"   2025: {m25['deals_closed_won']:,} deals")
            won_growth = ((m25['deals_closed_won'] - m24['deals_closed_won']) / m24['deals_closed_won'] * 100) if m24['deals_closed_won'] > 0 else 0
            print(f"   Growth: {won_growth:+.1f}%")
            
            print(f"\n🎯 CONVERSION RATES:")
            print(f"   2024: {m24['conversion_rate_percent']:.1f}%")
            print(f"   2025: {m25['conversion_rate_percent']:.1f}%")
            conv_change = m25['conversion_rate_percent'] - m24['conversion_rate_percent']
            print(f"   Change: {conv_change:+.1f} percentage points")
            
            print(f"\n💵 REVENUE PERFORMANCE:")
            print(f"   2024: ${m24['total_revenue']:,.2f}")
            print(f"   2025: ${m25['total_revenue']:,.2f}")
            rev_growth = ((m25['total_revenue'] - m24['total_revenue']) / m24['total_revenue'] * 100) if m24['total_revenue'] > 0 else 0
            print(f"   Growth: {rev_growth:+.1f}%")
            
            print(f"\n📈 AVERAGE DEAL SIZE:")
            print(f"   2024: ${m24['avg_deal_size']:,.2f}")
            print(f"   2025: ${m25['avg_deal_size']:,.2f}")
            deal_size_change = ((m25['avg_deal_size'] - m24['avg_deal_size']) / m24['avg_deal_size'] * 100) if m24['avg_deal_size'] > 0 else 0
            print(f"   Change: {deal_size_change:+.1f}%")
            
        # Monthly trends
        monthly_data = self.analyze_monthly_trends()
        if monthly_data:
            print(f"\n📅 MONTHLY TRENDS")
            print("-" * 50)
            
            months = ['January', 'February', 'March', 'April', 'May']
            for i, month in enumerate(months, 1):
                print(f"\n{month}:")
                for year in [2024, 2025]:
                    if year in monthly_data and i in monthly_data[year].index:
                        data = monthly_data[year].loc[i]
                        print(f"   {year}: {data['total_deals']:,} deals | {data['won_deals']:,} won | {data['conversion_rate']:.1f}% conv | ${data['revenue']:,.0f} revenue")
                        
        # Lead sources analysis
        source_data = self.analyze_lead_sources()
        if source_data:
            print(f"\n🎯 LEAD SOURCES PERFORMANCE")
            print("-" * 50)
            
            for year in [2024, 2025]:
                if year in source_data:
                    print(f"\n{year} Top Sources:")
                    for source, data in source_data[year].head(5).iterrows():
                        print(f"   {source}: {data['total_deals']:,} deals | {data['won_deals']:,} won | {data['conversion_rate']:.1f}% conv")
                        
        print(f"\n🎁 STRATEGIC INSIGHTS & RECOMMENDATIONS")
        print("-" * 50)
        
        if 2024 in metrics and 2025 in metrics:
            m24, m25 = metrics[2024], metrics[2025]
            
            # Volume insights
            if m25['total_deals_generated'] > m24['total_deals_generated']:
                print(f"✅ Deal generation is UP {growth:.1f}% - excellent demand generation performance")
            else:
                print(f"⚠️ Deal generation is DOWN {growth:.1f}% - need to focus on demand generation")
                
            # Conversion insights
            if m25['conversion_rate_percent'] > m24['conversion_rate_percent']:
                print(f"✅ Conversion rate improved by {conv_change:.1f}pp - sales process is getting better")
            else:
                print(f"⚠️ Conversion rate declined by {conv_change:.1f}pp - need to optimize sales process")
                
            # Revenue insights
            if rev_growth > 0:
                print(f"✅ Revenue growth of {rev_growth:.1f}% shows strong business momentum")
            else:
                print(f"⚠️ Revenue declined {rev_growth:.1f}% - need immediate attention")
                
        print(f"\nDataset processed: {len(self.deals_2024)} deals (2024) + {len(self.deals_2025)} deals (2025)")
        print("Analysis completed with NO limitations on deal count")
        
    def export_data(self):
        """Export processed data to CSV for further analysis"""
        output_dir = Path("tools/outputs/csv_data/hubspot/deals")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.df_2024 is not None:
            self.df_2024.to_csv(output_dir / "deals_2024_jan_may_complete.csv", index=False)
            
        if self.df_2025 is not None:
            self.df_2025.to_csv(output_dir / "deals_2025_jan_may_complete.csv", index=False)
            
        # Export summary metrics
        metrics = self.calculate_key_metrics()
        with open(output_dir / "comparison_metrics_2024_vs_2025.json", 'w') as f:
            json.dump(metrics, f, indent=2, default=str)
            
        print(f"✅ Data exported to {output_dir}")

# Sample data structure based on HubSpot API response
# This would be populated with actual data from the API calls
sample_deal_2024 = {
    'id': '123',
    'properties': {
        'dealname': 'Sample Deal',
        'amount': '50000',
        'dealstage': 'closedwon',
        'createdate': '2024-03-15T10:00:00.000Z',
        'closedate': '2024-04-15T10:00:00.000Z',
        'hs_analytics_source': 'ORGANIC_SEARCH'
    }
}

def main():
    """Main execution function"""
    print("Starting comprehensive deals analysis...")
    
    analyzer = DealsAnalyzer()
    
    # TODO: This is where we would add all the actual deals data from the API calls
    # For now, using sample structure to show the analysis framework
    
    # Example of how to add data:
    # analyzer.add_deals_data([sample_deal_2024], 2024)
    
    print("⚠️ Please populate with actual deals data from HubSpot API calls")
    print("The framework is ready to process unlimited deals data")
    
    # Process and analyze
    # analyzer.process_deals_data()
    # analyzer.generate_comprehensive_report()
    # analyzer.export_data()

if __name__ == "__main__":
    main() 