#!/usr/bin/env python3
"""
Colppy Data Exporter - Using Existing MCP Tools
Export and analyze data for Colppy's Argentina SMB accounting software business
"""

import json
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Dict, List

class ColppyDataExporter:
    """Export and analyze Colppy data using existing MCP tools"""
    
    def __init__(self):
        self.output_dir = "tools/outputs/colppy_analysis"
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
        
    def export_hubspot_deals_with_accountant_channel(self) -> Dict:
        """Export all deals and identify accountant channel deals"""
        print("🏢 Exporting HubSpot deals with accountant channel analysis...")
        
        try:
            # Load real HubSpot deals data from file
            deals_file = "tools/outputs/colppy_analysis/hubspot_deals_june_2025.json"
            with open(deals_file, 'r') as f:
                deals = json.load(f)
            
            # Process deals to identify accountant channel
            processed_deals = []
            for deal in deals.get('results', []):
                deal_data = {
                    'deal_id': deal.get('id'),
                    'deal_name': deal['properties'].get('dealname', ''),
                    'amount': deal['properties'].get('amount', '0'),
                    'stage': deal['properties'].get('dealstage', ''),
                    'close_date': deal['properties'].get('closedate', ''),
                    'create_date': deal['properties'].get('createdate', ''),
                    'pipeline': deal['properties'].get('pipeline', ''),
                    'is_accountant_channel': False,  # Will be determined by associations
                    'company_associations': []
                }
                
                # Check for company associations (accountant channel)
                associations = deal.get('associations', {})
                if 'companies' in associations:
                    company_ids = [assoc['id'] for assoc in associations['companies']['results']]
                    deal_data['company_associations'] = company_ids
                    
                    # Check if any associated company is an accountant
                    # You would implement your specific logic here based on company properties
                    if len(company_ids) > 0:
                        # This is a simplified check - you'd want to look at company properties
                        deal_data['is_accountant_channel'] = True
                
                processed_deals.append(deal_data)
            
            # Convert to DataFrame and save
            df = pd.DataFrame(processed_deals)
            output_file = f"{self.output_dir}/hubspot_deals_accountant_analysis_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(output_file, index=False)
            
            # Generate summary
            total_deals = len(df)
            accountant_deals = len(df[df['is_accountant_channel'] == True])
            total_value = df['amount'].astype(str).str.replace(',', '').astype(float).sum()
            
            summary = {
                'total_deals': total_deals,
                'accountant_channel_deals': accountant_deals,
                'direct_deals': total_deals - accountant_deals,
                'accountant_channel_percentage': (accountant_deals / total_deals * 100) if total_deals > 0 else 0,
                'total_pipeline_value': total_value,
                'output_file': output_file,
                'export_date': datetime.now().isoformat()
            }
            
            print(f"✅ Exported {total_deals} deals to {output_file}")
            print(f"   📊 {accountant_deals} accountant channel deals ({summary['accountant_channel_percentage']:.1f}%)")
            print(f"   💰 Total pipeline value: ${total_value:,.0f}")
            
            return summary
            
        except Exception as e:
            print(f"❌ Error exporting HubSpot deals: {e}")
            return {"error": str(e)}
    
    def export_mixpanel_user_behavior(self, days_back: int = 30) -> Dict:
        """Export Mixpanel user behavior data for Colppy product analysis"""
        print("📊 Exporting Mixpanel user behavior data...")
        
        try:
            to_date = datetime.now().strftime("%Y-%m-%d")
            from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            # Mock Mixpanel data for demo (replace with real MCP calls when available)
            top_events = {
                "events": [
                    {"event": "Invoice Created", "count": 1250},
                    {"event": "Payment Processed", "count": 980},
                    {"event": "User Login", "count": 3450},
                    {"event": "Report Generated", "count": 750},
                    {"event": "AFIP Integration", "count": 650}
                ]
            }
            
            retention_data = {"day_1": 0.75, "day_7": 0.45, "day_30": 0.25}
            login_events = {"daily_unique_users": 145}
            
            # Focus on accounting-specific events
            accounting_events = []
            if 'events' in top_events:
                for event in top_events['events']:
                    event_name = event.get('event', '').lower()
                    # Look for Colppy-specific accounting events
                    if any(keyword in event_name for keyword in [
                        'invoice', 'factura', 'payment', 'pago', 'report', 'reporte',
                        'cliente', 'customer', 'tax', 'impuesto', 'afip'
                    ]):
                        accounting_events.append(event)
            
            # Export to files
            events_file = f"{self.output_dir}/mixpanel_events_{datetime.now().strftime('%Y%m%d')}.json"
            with open(events_file, 'w') as f:
                json.dump({
                    'top_events': top_events,
                    'retention_data': retention_data,
                    'login_events': login_events,
                    'accounting_specific_events': accounting_events,
                    'date_range': {'from': from_date, 'to': to_date}
                }, f, indent=2)
            
            summary = {
                'total_events': len(top_events.get('events', [])),
                'accounting_events': len(accounting_events),
                'date_range_days': days_back,
                'output_file': events_file,
                'export_date': datetime.now().isoformat()
            }
            
            print(f"✅ Exported Mixpanel data to {events_file}")
            print(f"   📈 {len(top_events.get('events', []))} total events")
            print(f"   🧮 {len(accounting_events)} accounting-specific events")
            
            return summary
            
        except Exception as e:
            print(f"❌ Error exporting Mixpanel data: {e}")
            return {"error": str(e)}
    
    def export_customer_journey_analysis(self) -> Dict:
        """Combine HubSpot and Mixpanel data for customer journey analysis"""
        print("🎯 Creating customer journey analysis...")
        
        try:
            # Mock companies data for demo (use real MCP calls when available)
            companies = {
                "results": [
                    {
                        "id": "9018786352",
                        "properties": {
                            "name": "SMB Contabilidad Rosario",
                            "domain": "smbcontadores.com.ar",
                            "country": "Argentina",
                            "industry": "Accounting Services",
                            "createdate": "2022-01-15T10:00:00Z",
                            "num_employees": "25"
                        }
                    },
                    {
                        "id": "9019073088", 
                        "properties": {
                            "name": "Buenos Aires Tax Solutions",
                            "domain": "batax.com.ar",
                            "country": "Argentina", 
                            "industry": "Tax Consulting",
                            "createdate": "2022-03-20T14:30:00Z",
                            "num_employees": "12"
                        }
                    }
                ]
            }
            
            # Filter for Argentina companies
            argentina_companies = []
            for company in companies.get('results', []):
                props = company.get('properties', {})
                country = props.get('country', '').lower()
                if 'argentina' in country or 'ar' == country:
                    argentina_companies.append({
                        'company_id': company.get('id'),
                        'name': props.get('name', ''),
                        'domain': props.get('domain', ''),
                        'industry': props.get('industry', ''),
                        'employees': props.get('num_employees', ''),
                        'created_date': props.get('createdate', ''),
                        'country': props.get('country', '')
                    })
            
            # Mock funnel data for demo
            funnel_data = {
                "trial_signup": 1000,
                "completed_onboarding": 650,
                "first_invoice": 420,
                "paid_subscription": 180,
                "conversion_rate": 0.18
            }
            
            # Create combined analysis
            analysis = {
                'argentina_companies': argentina_companies,
                'company_count': len(argentina_companies),
                'funnel_analysis': funnel_data,
                'market_segments': self._analyze_market_segments(argentina_companies),
                'export_date': datetime.now().isoformat()
            }
            
            # Export to file
            output_file = f"{self.output_dir}/customer_journey_analysis_{datetime.now().strftime('%Y%m%d')}.json"
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            # Create CSV for easy analysis
            df = pd.DataFrame(argentina_companies)
            csv_file = f"{self.output_dir}/argentina_companies_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(csv_file, index=False)
            
            summary = {
                'argentina_companies': len(argentina_companies),
                'market_segments': len(analysis['market_segments']),
                'output_files': [output_file, csv_file],
                'export_date': datetime.now().isoformat()
            }
            
            print(f"✅ Created customer journey analysis")
            print(f"   🇦🇷 {len(argentina_companies)} Argentina companies")
            print(f"   📁 Files: {output_file}, {csv_file}")
            
            return summary
            
        except Exception as e:
            print(f"❌ Error creating customer journey analysis: {e}")
            return {"error": str(e)}
    
    def _analyze_market_segments(self, companies: List[Dict]) -> Dict:
        """Analyze market segments from company data"""
        segments = {}
        
        for company in companies:
            industry = company.get('industry', 'Unknown').strip()
            if industry:
                if industry not in segments:
                    segments[industry] = 0
                segments[industry] += 1
        
        return segments
    
    def generate_colppy_executive_report(self) -> Dict:
        """Generate comprehensive executive report combining all data sources"""
        print("📋 Generating Colppy Executive Report...")
        
        # Export all data
        hubspot_summary = self.export_hubspot_deals_with_accountant_channel()
        mixpanel_summary = self.export_mixpanel_user_behavior()
        journey_summary = self.export_customer_journey_analysis()
        
        # Combine into executive summary
        executive_report = {
            'report_date': datetime.now().isoformat(),
            'company': 'Colppy.com',
            'market': 'Argentina SMB Accounting Software',
            'data_sources': {
                'hubspot': hubspot_summary,
                'mixpanel': mixpanel_summary,
                'customer_journey': journey_summary
            },
            'key_metrics': {
                'total_deals': hubspot_summary.get('total_deals', 0),
                'accountant_channel_percentage': hubspot_summary.get('accountant_channel_percentage', 0),
                'argentina_companies': journey_summary.get('argentina_companies', 0),
                'total_events_tracked': mixpanel_summary.get('total_events', 0)
            },
            'recommendations': [
                "Focus on accountant channel expansion based on conversion data",
                "Analyze top accounting events to improve product-led growth",
                "Segment Argentina market by company size and industry",
                "Optimize trial-to-paid conversion funnel"
            ]
        }
        
        # Save executive report
        report_file = f"{self.output_dir}/colppy_executive_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(executive_report, f, indent=2)
        
        print(f"✅ Executive report generated: {report_file}")
        
        return executive_report

def main():
    """Main function to run Colppy data export"""
    print("🚀 Colppy Data Exporter - Using Existing MCP Tools")
    print("=" * 60)
    
    exporter = ColppyDataExporter()
    
    try:
        # Generate comprehensive report
        report = exporter.generate_colppy_executive_report()
        
        print("\n" + "=" * 60)
        print("📊 Export Summary:")
        print(f"   📁 Output directory: {exporter.output_dir}")
        print(f"   🏢 Total deals: {report['key_metrics']['total_deals']}")
        print(f"   🤝 Accountant channel: {report['key_metrics']['accountant_channel_percentage']:.1f}%")
        print(f"   🇦🇷 Argentina companies: {report['key_metrics']['argentina_companies']}")
        print(f"   📈 Events tracked: {report['key_metrics']['total_events_tracked']}")
        
        print("\n💡 Next Steps:")
        print("1. Review exported files for detailed analysis")
        print("2. Use data for CEO dashboard and strategic planning")
        print("3. Schedule regular exports for ongoing monitoring")
        print("4. Combine with Intercom data for complete customer view")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        print("Check your MCP tool configuration and try again")

if __name__ == "__main__":
    main() 