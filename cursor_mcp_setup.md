# 🖱️ Testing MCP Helpers in Cursor

This guide explains how to run the new MCP helper functions using the [Cursor](https://cursor.sh/) editor.

## 1. Open the repository
1. Install Cursor from the website.
2. Launch Cursor and choose **"Open Folder"** to load this repository.

## 2. Set up a Python environment
1. Open the integrated terminal in Cursor.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 3. Configure the Intercom export path
Set the `INTERCOM_EXPORT_PATH` environment variable in a `.env` file or directly in the terminal:
```bash
echo "INTERCOM_EXPORT_PATH=/path/to/your/intercom-export" >> .env
```

## 4. Run the helper
Inside Cursor's terminal run:
```bash
python helpers/intercom_mcp_helper.py
```
You should see the number of conversations and customers loaded from your export folder.

This confirms that the MCP helper can read your local Intercom data. Repeat similar steps when you implement HubSpot or Mixpanel helpers.
