# CEO Assistant Setup Instructions

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- HubSpot API key (optional but recommended)
- Mixpanel project credentials (optional but recommended)

### Step 1: Environment Setup

1. **Clone or download the OpenAI Cookbook** (you already have this)
2. **Navigate to your project directory**
   ```bash
   cd /Users/virulana/openai-cookbook
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv ceo_assistant_env
   source ceo_assistant_env/bin/activate  # On macOS/Linux
   # or
   ceo_assistant_env\Scripts\activate  # On Windows
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: API Keys Configuration

Create a `.env` file in your project root:

```bash
# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# HubSpot Configuration (Optional - for customer data)
HUBSPOT_API_KEY=your_hubspot_api_key_here

# Mixpanel Configuration (Optional - for product analytics)
MIXPANEL_PROJECT_ID=your_mixpanel_project_id_here
MIXPANEL_API_SECRET=your_mixpanel_api_secret_here
```

### Step 3: Getting Your API Keys

#### OpenAI API Key (Required)
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy and paste it into your `.env` file

#### HubSpot API Key (Recommended)
1. Log into your HubSpot account
2. Go to Settings → Integrations → API Key
3. Generate a new API key
4. Copy and paste it into your `.env` file

#### Mixpanel Credentials (Recommended)
1. Log into your Mixpanel account
2. Go to Project Settings
3. Find your Project ID and API Secret
4. Copy and paste them into your `.env` file

### Step 4: Test Your Setup

Run the basic test:

```bash
python ceo_assistant_starter.py
```

If everything is configured correctly, you should see:
- CEO Assistant initialized successfully
- Demo interactions with different agents
- Dashboard summary with your connected services

### Step 5: Customize for Colppy

#### Update HubSpot Integration
Edit the `HubSpotConnector` class in `ceo_assistant_starter.py`:

```python
def get_customer_metrics(self) -> Dict:
    """Get customer acquisition and retention metrics"""
    try:
        # Replace with your actual HubSpot properties
        url = f"{self.base_url}/crm/v3/objects/contacts"
        params = {
            "properties": "createdate,hs_lead_status,lifecyclestage",
            "limit": 100
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        # Process your specific metrics here
        data = response.json()
        # Calculate your specific KPIs
        
        return {
            "new_customers_this_month": calculated_value,
            "churn_rate": calculated_value,
            "customer_lifetime_value": calculated_value,
            "acquisition_cost": calculated_value
        }
    except Exception as e:
        logger.error(f"Error getting customer metrics: {e}")
        return {"error": str(e)}
```

#### Update Mixpanel Integration
Edit the `MixpanelConnector` class to use your specific events:

```python
def get_user_engagement(self, days_back: int = 30) -> Dict:
    """Get user engagement metrics"""
    try:
        # Use your actual Mixpanel events
        # Examples: "Invoice Created", "User Login", "Feature Used"
        
        # Make actual API calls to Mixpanel
        # Process your specific events and properties
        
        return {
            "daily_active_users": calculated_value,
            "weekly_active_users": calculated_value,
            "monthly_active_users": calculated_value,
            "feature_adoption_rate": calculated_value,
            "user_retention_d7": calculated_value,
            "user_retention_d30": calculated_value
        }
    except Exception as e:
        logger.error(f"Mixpanel API error: {e}")
        return {"error": str(e)}
```

## 🎯 Next Steps for Learning

### Week 1: Foundation
1. **Study the OpenAI Cookbook examples**:
   ```bash
   jupyter notebook examples/Orchestrating_agents.ipynb
   jupyter notebook examples/How_to_call_functions_with_chat_models.ipynb
   jupyter notebook examples/Structured_Outputs_Intro.ipynb
   ```

2. **Understand agent architecture**:
   - Read through `ceo_assistant_starter.py`
   - Experiment with different prompts
   - Test with your actual data

3. **Customize for your needs**:
   - Modify agent prompts for Colppy context
   - Add Argentina market-specific insights
   - Include SaaS B2B best practices

### Week 2: Enhancement
1. **Add more sophisticated routing**:
   - Implement intent classification
   - Add more specialized agents
   - Create workflow orchestration

2. **Improve data integration**:
   - Connect to your actual HubSpot data
   - Integrate real Mixpanel events
   - Add financial data sources

3. **Build memory persistence**:
   - Store conversation history
   - Maintain context across sessions
   - Track insights and recommendations

### Week 3: Production
1. **Create a web interface**:
   ```bash
   streamlit run ceo_assistant_app.py
   ```

2. **Add scheduling and automation**:
   - Weekly report generation
   - Automated insights delivery
   - Alert systems for key metrics

3. **Scale to team usage**:
   - Multi-user support
   - Role-based access
   - Team collaboration features

## 🛠 Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Verify your `.env` file is in the correct location
   - Check that API keys are valid and have proper permissions
   - Ensure you have sufficient API credits

2. **Import Errors**:
   - Make sure you're in the correct virtual environment
   - Reinstall requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **HubSpot/Mixpanel Connection Issues**:
   - Verify API permissions in your accounts
   - Check rate limits and quotas
   - Test API endpoints manually first

### Getting Help

1. **OpenAI Cookbook Issues**: Check the GitHub repository
2. **API Documentation**: 
   - [OpenAI API Docs](https://platform.openai.com/docs)
   - [HubSpot API Docs](https://developers.hubspot.com/)
   - [Mixpanel API Docs](https://developer.mixpanel.com/)

## 📊 Success Metrics

Track your progress with these metrics:

### Week 1 Goals:
- [ ] Successfully run the basic assistant
- [ ] Connect to at least one data source (HubSpot or Mixpanel)
- [ ] Generate your first strategic analysis

### Week 2 Goals:
- [ ] Customize agents for Colppy-specific insights
- [ ] Integrate with your actual data
- [ ] Create weekly operational reports

### Week 3 Goals:
- [ ] Deploy a web interface
- [ ] Automate routine reports
- [ ] Measure time savings and decision quality

## 🎓 Learning Resources

### Essential Reading:
1. **Agent Architecture**: Study the NVIDIA guides linked in the learning guide
2. **OpenAI Function Calling**: Master tool integration patterns
3. **SaaS Metrics**: Understand key KPIs for your business

### Recommended Papers:
1. "Generative Agents: Interactive Simulacra of Human Behavior"
2. "MRKL Systems: A modular, neuro-symbolic architecture"
3. "AutoGPT: An Autonomous GPT-4 Experiment"

### Community Resources:
1. OpenAI Developer Community
2. LangChain Discord
3. AI Agent development forums

Remember: Start simple, iterate quickly, and focus on solving real problems for your CEO role at Colppy! 