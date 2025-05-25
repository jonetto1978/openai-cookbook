"""
Intercom Data Explorer
Helps you understand the structure of your Intercom export data

Run this script to see what data you have available for the CEO assistant.
"""

import os
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List

def explore_intercom_export(intercom_path: str = "/Users/virulana/Downloads/intercom-export"):
    """
    Explore your Intercom export data structure
    """
    
    if not os.path.exists(intercom_path):
        print(f"❌ Intercom export path not found: {intercom_path}")
        print("Please update the path to your intercom-export folder")
        return
    
    print("🔍 INTERCOM DATA EXPLORER")
    print("=" * 50)
    
    # Get all files in the export
    all_files = os.listdir(intercom_path)
    total_files = len(all_files)
    
    print(f"📁 Total files in export: {total_files}")
    print(f"📍 Export location: {intercom_path}")
    
    # Categorize files by type
    file_types = {}
    for file in all_files:
        ext = file.split('.')[-1].lower() if '.' in file else 'no_extension'
        if ext not in file_types:
            file_types[ext] = []
        file_types[ext].append(file)
    
    print(f"\n📊 File types found:")
    for ext, files in file_types.items():
        print(f"  • {ext.upper()}: {len(files)} files")
    
    # Look for key data types
    key_data_types = {
        'conversations': ['conversation', 'message', 'chat'],
        'users': ['user', 'contact', 'customer', 'lead'],
        'companies': ['company', 'organization', 'account'],
        'events': ['event', 'activity', 'action'],
        'tags': ['tag', 'label'],
        'segments': ['segment', 'cohort'],
        'articles': ['article', 'help', 'knowledge']
    }
    
    print(f"\n🎯 Key data types identified:")
    found_data = {}
    
    for data_type, keywords in key_data_types.items():
        matching_files = []
        for file in all_files:
            if any(keyword in file.lower() for keyword in keywords):
                matching_files.append(file)
        
        if matching_files:
            found_data[data_type] = matching_files
            print(f"  • {data_type.title()}: {len(matching_files)} files")
            for file in matching_files[:3]:  # Show first 3 files
                file_path = os.path.join(intercom_path, file)
                file_size = os.path.getsize(file_path) / 1024 / 1024  # MB
                print(f"    - {file} ({file_size:.1f} MB)")
            if len(matching_files) > 3:
                print(f"    ... and {len(matching_files) - 3} more")
    
    # Analyze CSV files in detail
    csv_files = file_types.get('csv', [])
    if csv_files:
        print(f"\n📋 CSV FILES ANALYSIS:")
        print("-" * 30)
        
        for csv_file in csv_files[:5]:  # Analyze first 5 CSV files
            try:
                file_path = os.path.join(intercom_path, csv_file)
                df = pd.read_csv(file_path)
                
                print(f"\n📄 {csv_file}")
                print(f"   Rows: {len(df):,}")
                print(f"   Columns: {len(df.columns)}")
                print(f"   Size: {os.path.getsize(file_path) / 1024 / 1024:.1f} MB")
                
                # Show column names
                print(f"   Columns: {', '.join(df.columns[:10])}")
                if len(df.columns) > 10:
                    print(f"            ... and {len(df.columns) - 10} more")
                
                # Show sample data
                if len(df) > 0:
                    print(f"   Sample data:")
                    for col in df.columns[:3]:  # Show first 3 columns
                        sample_val = str(df[col].iloc[0])[:50]
                        print(f"     {col}: {sample_val}")
                
                # Look for date columns
                date_columns = [col for col in df.columns if any(date_word in col.lower() for date_word in ['date', 'time', 'created', 'updated'])]
                if date_columns:
                    print(f"   Date columns: {', '.join(date_columns)}")
                
            except Exception as e:
                print(f"   ❌ Error reading {csv_file}: {e}")
    
    # Analyze JSON files
    json_files = file_types.get('json', [])
    if json_files:
        print(f"\n🔧 JSON FILES ANALYSIS:")
        print("-" * 30)
        
        for json_file in json_files[:3]:  # Analyze first 3 JSON files
            try:
                file_path = os.path.join(intercom_path, json_file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                print(f"\n📄 {json_file}")
                print(f"   Size: {os.path.getsize(file_path) / 1024 / 1024:.1f} MB")
                
                if isinstance(data, list):
                    print(f"   Type: Array with {len(data)} items")
                    if len(data) > 0 and isinstance(data[0], dict):
                        print(f"   Sample keys: {', '.join(list(data[0].keys())[:5])}")
                elif isinstance(data, dict):
                    print(f"   Type: Object with {len(data)} keys")
                    print(f"   Keys: {', '.join(list(data.keys())[:5])}")
                
            except Exception as e:
                print(f"   ❌ Error reading {json_file}: {e}")
    
    # Generate recommendations
    print(f"\n💡 RECOMMENDATIONS FOR CEO ASSISTANT:")
    print("-" * 50)
    
    if 'conversations' in found_data:
        print("✅ Conversations data found - Great for customer support insights!")
        print("   Use for: Support resolution times, customer satisfaction, common issues")
    
    if 'users' in found_data:
        print("✅ User data found - Perfect for customer analysis!")
        print("   Use for: Customer segmentation, lifecycle analysis, churn prediction")
    
    if 'companies' in found_data:
        print("✅ Company data found - Excellent for B2B insights!")
        print("   Use for: Account health, expansion opportunities, industry analysis")
    
    if 'events' in found_data:
        print("✅ Event data found - Valuable for behavior analysis!")
        print("   Use for: User journey mapping, feature adoption, engagement scoring")
    
    # Suggest next steps
    print(f"\n🚀 NEXT STEPS:")
    print("1. Choose the most relevant files for your CEO assistant")
    print("2. Update the intercom_path in your MCP connector")
    print("3. Modify the load_intercom_data() function to read your specific files")
    print("4. Test the integration with a small dataset first")
    
    return found_data

def create_sample_loader(found_data: Dict[str, List[str]], intercom_path: str):
    """
    Generate sample code for loading your specific Intercom data
    """
    
    print(f"\n🔧 SAMPLE CODE FOR YOUR DATA:")
    print("=" * 50)
    
    print("""
def load_colppy_intercom_data(data_type: str = "conversations") -> pd.DataFrame:
    \"\"\"Load Colppy-specific Intercom data\"\"\"
    import pandas as pd
    import os
    
    intercom_path = "/Users/virulana/Downloads/intercom-export"
    
    try:""")
    
    if 'conversations' in found_data:
        conv_file = found_data['conversations'][0]
        print(f"""
        if data_type == "conversations":
            # Load conversation data
            return pd.read_csv(os.path.join(intercom_path, "{conv_file}"))""")
    
    if 'users' in found_data:
        user_file = found_data['users'][0]
        print(f"""
        elif data_type == "users":
            # Load user/customer data  
            return pd.read_csv(os.path.join(intercom_path, "{user_file}"))""")
    
    if 'companies' in found_data:
        company_file = found_data['companies'][0]
        print(f"""
        elif data_type == "companies":
            # Load company data
            return pd.read_csv(os.path.join(intercom_path, "{company_file}"))""")
    
    print("""
        else:
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error loading Intercom data: {e}")
        return pd.DataFrame()
""")

def main():
    """Main function to run the explorer"""
    
    print("🚀 Starting Intercom Data Exploration...")
    
    # Default path - update this to match your actual path
    intercom_path = "/Users/virulana/Downloads/intercom-export"
    
    # Check if path exists, if not, try to find it
    if not os.path.exists(intercom_path):
        # Try to find intercom-export folder in Downloads
        downloads_path = "/Users/virulana/Downloads"
        if os.path.exists(downloads_path):
            for item in os.listdir(downloads_path):
                if "intercom" in item.lower():
                    potential_path = os.path.join(downloads_path, item)
                    if os.path.isdir(potential_path):
                        intercom_path = potential_path
                        print(f"📍 Found Intercom data at: {intercom_path}")
                        break
    
    # Run the exploration
    found_data = explore_intercom_export(intercom_path)
    
    if found_data:
        create_sample_loader(found_data, intercom_path)
    
    print(f"\n✅ Exploration complete!")
    print(f"💡 Use this information to customize your CEO assistant integration.")

if __name__ == "__main__":
    main() 