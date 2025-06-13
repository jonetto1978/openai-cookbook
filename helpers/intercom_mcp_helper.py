import os
import pandas as pd
from typing import Optional, Dict

class IntercomMCPHelper:
    """Simple helper to load Intercom export data for testing."""

    def __init__(self, export_path: Optional[str] = None):
        self.export_path = export_path or os.getenv("INTERCOM_EXPORT_PATH", "./intercom-export")

    def _load_csv_or_json(self, filename: str) -> pd.DataFrame:
        file_path = os.path.join(self.export_path, filename)
        if os.path.isfile(file_path):
            if filename.endswith(".csv"):
                return pd.read_csv(file_path)
            if filename.endswith(".json"):
                return pd.read_json(file_path)
        return pd.DataFrame()

    def load_conversations(self) -> pd.DataFrame:
        """Load the first conversations file found in the export."""
        for f in os.listdir(self.export_path):
            if "conversation" in f.lower():
                return self._load_csv_or_json(f)
        return pd.DataFrame()

    def load_customers(self) -> pd.DataFrame:
        """Load the first users/customers file found in the export."""
        for f in os.listdir(self.export_path):
            name = f.lower()
            if any(term in name for term in ["user", "customer", "contact"]):
                return self._load_csv_or_json(f)
        return pd.DataFrame()

if __name__ == "__main__":
    helper = IntercomMCPHelper()
    conversations = helper.load_conversations()
    print("Conversations loaded:", len(conversations))
    customers = helper.load_customers()
    print("Customers loaded:", len(customers))
