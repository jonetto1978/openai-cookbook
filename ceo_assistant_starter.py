"""
CEO Assistant - Starter Implementation
A practical LLM agent-based assistant for SaaS B2B CEOs

This implementation provides:
1. Strategic Planning Agent - Market analysis and growth insights
2. Operational Intelligence Agent - KPI monitoring and team performance
3. Communication Agent - Meeting prep and stakeholder updates
4. Integration with HubSpot and Mixpanel APIs
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentResponse:
    """Structured response from agents"""
    agent_type: str
    content: str
    data: Optional[Dict] = None
    recommendations: Optional[List[str]] = None
    next_actions: Optional[List[str]] = None

class ConversationMemory:
    """Simple memory system for maintaining context"""
    
    def __init__(self):
        self.conversation_history = []
        self.context_data = {}
        self.key_insights = []
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
    
    def add_insight(self, insight: str, category: str):
        """Store key insights for future reference"""
        self.key_insights.append({
            "insight": insight,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_recent_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation context"""
        return self.conversation_history[-limit:]

class HubSpotConnector:
    """HubSpot API integration for customer and sales data"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_deals_pipeline(self, days_back: int = 30) -> Dict:
        """Get deals pipeline data"""
        try:
            # This is a simplified example - adjust based on your HubSpot setup
            url = f"{self.base_url}/crm/v3/objects/deals"
            params = {
                "properties": "dealname,amount,dealstage,closedate,createdate",
                "limit": 100
            }
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"HubSpot API error: {e}")
            return {"error": str(e)}
    
    def get_customer_metrics(self) -> Dict:
        """Get customer acquisition and retention metrics"""
        try:
            # Placeholder for customer metrics
            # Implement based on your specific HubSpot properties
            return {
                "new_customers_this_month": 25,
                "churn_rate": 0.05,
                "customer_lifetime_value": 2400,
                "acquisition_cost": 180
            }
        except Exception as e:
            logger.error(f"Error getting customer metrics: {e}")
            return {"error": str(e)}

class MixpanelConnector:
    """Mixpanel API integration for product analytics"""
    
    def __init__(self, project_id: str, api_secret: str):
        self.project_id = project_id
        self.api_secret = api_secret
        self.base_url = "https://mixpanel.com/api/2.0"
    
    def get_user_engagement(self, days_back: int = 30) -> Dict:
        """Get user engagement metrics"""
        try:
            # Placeholder for Mixpanel integration
            # Implement based on your specific events and properties
            return {
                "daily_active_users": 1250,
                "weekly_active_users": 3200,
                "monthly_active_users": 8500,
                "feature_adoption_rate": 0.65,
                "user_retention_d7": 0.45,
                "user_retention_d30": 0.28
            }
        except Exception as e:
            logger.error(f"Mixpanel API error: {e}")
            return {"error": str(e)}
    
    def get_conversion_funnel(self) -> Dict:
        """Get conversion funnel data"""
        try:
            return {
                "trial_signup": 100,
                "first_login": 85,
                "feature_usage": 65,
                "paid_conversion": 22,
                "conversion_rate": 0.22
            }
        except Exception as e:
            logger.error(f"Error getting conversion funnel: {e}")
            return {"error": str(e)}

class StrategicPlanningAgent:
    """Agent focused on strategic planning and market analysis"""
    
    def __init__(self, openai_client: OpenAI, hubspot: HubSpotConnector, mixpanel: MixpanelConnector):
        self.client = openai_client
        self.hubspot = hubspot
        self.mixpanel = mixpanel
        self.system_prompt = """
        You are a strategic planning AI assistant for a SaaS B2B CEO. Your role is to:
        1. Analyze market data and competitive positioning
        2. Provide growth strategy recommendations
        3. Identify opportunities and threats
        4. Support product roadmap decisions
        
        Always provide actionable insights with specific metrics and timelines.
        Focus on Product-Led Growth strategies and data-driven decisions.
        Consider the Argentina market context for Colppy.com operations.
        """
    
    def analyze_growth_opportunities(self) -> AgentResponse:
        """Analyze current metrics and identify growth opportunities"""
        
        # Gather data from integrations
        hubspot_data = self.hubspot.get_customer_metrics()
        mixpanel_data = self.mixpanel.get_user_engagement()
        conversion_data = self.mixpanel.get_conversion_funnel()
        
        # Prepare context for LLM
        context = f"""
        Current Business Metrics:
        - Customer Acquisition Cost: ${hubspot_data.get('acquisition_cost', 'N/A')}
        - Customer Lifetime Value: ${hubspot_data.get('customer_lifetime_value', 'N/A')}
        - Monthly Churn Rate: {hubspot_data.get('churn_rate', 'N/A')}%
        - Daily Active Users: {mixpanel_data.get('daily_active_users', 'N/A')}
        - Trial to Paid Conversion: {conversion_data.get('conversion_rate', 'N/A')}%
        - D7 Retention: {mixpanel_data.get('user_retention_d7', 'N/A')}%
        
        Analyze these metrics and provide:
        1. Top 3 growth opportunities
        2. Specific action items with timelines
        3. Expected impact on key metrics
        4. Resource requirements
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": context}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            return AgentResponse(
                agent_type="Strategic Planning",
                content=content,
                data={
                    "hubspot_metrics": hubspot_data,
                    "mixpanel_metrics": mixpanel_data,
                    "conversion_metrics": conversion_data
                },
                recommendations=[
                    "Optimize trial-to-paid conversion funnel",
                    "Implement user retention improvement program",
                    "Expand product-led growth initiatives"
                ]
            )
            
        except Exception as e:
            logger.error(f"Strategic planning analysis error: {e}")
            return AgentResponse(
                agent_type="Strategic Planning",
                content=f"Error analyzing growth opportunities: {e}",
                data={"error": str(e)}
            )

class OperationalIntelligenceAgent:
    """Agent focused on operational metrics and team performance"""
    
    def __init__(self, openai_client: OpenAI, hubspot: HubSpotConnector, mixpanel: MixpanelConnector):
        self.client = openai_client
        self.hubspot = hubspot
        self.mixpanel = mixpanel
        self.system_prompt = """
        You are an operational intelligence AI assistant for a SaaS B2B CEO. Your role is to:
        1. Monitor key performance indicators (KPIs)
        2. Identify operational bottlenecks
        3. Provide team performance insights
        4. Suggest process improvements
        
        Focus on actionable operational insights that drive efficiency and growth.
        Consider team culture and employee satisfaction in your recommendations.
        """
    
    def generate_weekly_report(self) -> AgentResponse:
        """Generate weekly operational intelligence report"""
        
        # Gather operational data
        deals_data = self.hubspot.get_deals_pipeline()
        engagement_data = self.mixpanel.get_user_engagement()
        
        context = f"""
        Weekly Operational Data:
        - Active Deals in Pipeline: {len(deals_data.get('results', []))}
        - Daily Active Users: {engagement_data.get('daily_active_users', 'N/A')}
        - Weekly Active Users: {engagement_data.get('weekly_active_users', 'N/A')}
        - Feature Adoption Rate: {engagement_data.get('feature_adoption_rate', 'N/A')}%
        
        Generate a weekly operational report including:
        1. Key performance highlights
        2. Areas requiring attention
        3. Team productivity insights
        4. Recommended actions for next week
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": context}
                ],
                temperature=0.5
            )
            
            content = response.choices[0].message.content
            
            return AgentResponse(
                agent_type="Operational Intelligence",
                content=content,
                data={
                    "deals_pipeline": deals_data,
                    "user_engagement": engagement_data
                },
                next_actions=[
                    "Review team capacity planning",
                    "Optimize customer onboarding process",
                    "Schedule team performance reviews"
                ]
            )
            
        except Exception as e:
            logger.error(f"Weekly report generation error: {e}")
            return AgentResponse(
                agent_type="Operational Intelligence",
                content=f"Error generating weekly report: {e}",
                data={"error": str(e)}
            )

class CommunicationAgent:
    """Agent focused on communication, meetings, and stakeholder updates"""
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.system_prompt = """
        You are a communication AI assistant for a SaaS B2B CEO. Your role is to:
        1. Prepare meeting agendas and talking points
        2. Draft stakeholder updates and board reports
        3. Create presentation content
        4. Suggest communication strategies
        
        Maintain a professional, data-driven communication style.
        Focus on clarity, actionable insights, and strategic messaging.
        """
    
    def prepare_board_update(self, metrics_data: Dict) -> AgentResponse:
        """Prepare board meeting update content"""
        
        context = f"""
        Prepare a board update presentation covering:
        
        Business Metrics:
        {json.dumps(metrics_data, indent=2)}
        
        Include:
        1. Executive summary (2-3 key points)
        2. Financial performance highlights
        3. Product and user growth metrics
        4. Strategic initiatives progress
        5. Key challenges and mitigation plans
        6. Next quarter priorities
        
        Format for presentation slides with clear, concise bullet points.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": context}
                ],
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            
            return AgentResponse(
                agent_type="Communication",
                content=content,
                data=metrics_data,
                recommendations=[
                    "Schedule follow-up meetings with key stakeholders",
                    "Prepare detailed financial projections",
                    "Create visual dashboards for metrics presentation"
                ]
            )
            
        except Exception as e:
            logger.error(f"Board update preparation error: {e}")
            return AgentResponse(
                agent_type="Communication",
                content=f"Error preparing board update: {e}",
                data={"error": str(e)}
            )

class CEOAssistant:
    """Main CEO Assistant orchestrating all specialized agents"""
    
    def __init__(self, openai_api_key: str, hubspot_api_key: str = None, 
                 mixpanel_project_id: str = None, mixpanel_api_secret: str = None):
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=openai_api_key)
        
        # Initialize connectors
        self.hubspot = HubSpotConnector(hubspot_api_key) if hubspot_api_key else None
        self.mixpanel = MixpanelConnector(mixpanel_project_id, mixpanel_api_secret) if mixpanel_project_id else None
        
        # Initialize agents
        self.strategic_agent = StrategicPlanningAgent(self.openai_client, self.hubspot, self.mixpanel)
        self.operational_agent = OperationalIntelligenceAgent(self.openai_client, self.hubspot, self.mixpanel)
        self.communication_agent = CommunicationAgent(self.openai_client)
        
        # Initialize memory
        self.memory = ConversationMemory()
        
        logger.info("CEO Assistant initialized successfully")
    
    def process_request(self, request: str) -> AgentResponse:
        """Process user request and route to appropriate agent"""
        
        # Add request to memory
        self.memory.add_message("user", request)
        
        # Simple routing logic (can be enhanced with more sophisticated classification)
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in ["growth", "strategy", "market", "opportunity", "competitive"]):
            response = self.strategic_agent.analyze_growth_opportunities()
        elif any(keyword in request_lower for keyword in ["weekly", "report", "kpi", "performance", "operational"]):
            response = self.operational_agent.generate_weekly_report()
        elif any(keyword in request_lower for keyword in ["board", "meeting", "presentation", "update", "communication"]):
            # Gather metrics for communication
            metrics = {}
            if self.hubspot:
                metrics.update(self.hubspot.get_customer_metrics())
            if self.mixpanel:
                metrics.update(self.mixpanel.get_user_engagement())
            response = self.communication_agent.prepare_board_update(metrics)
        else:
            # Default to strategic analysis
            response = self.strategic_agent.analyze_growth_opportunities()
        
        # Add response to memory
        self.memory.add_message("assistant", response.content, {"agent_type": response.agent_type})
        
        return response
    
    def get_dashboard_summary(self) -> Dict:
        """Get high-level dashboard summary"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "hubspot_connected": self.hubspot is not None,
            "mixpanel_connected": self.mixpanel is not None,
            "recent_insights": self.memory.key_insights[-5:] if self.memory.key_insights else []
        }
        
        if self.hubspot:
            summary["customer_metrics"] = self.hubspot.get_customer_metrics()
        
        if self.mixpanel:
            summary["engagement_metrics"] = self.mixpanel.get_user_engagement()
        
        return summary

def main():
    """Example usage of the CEO Assistant"""
    
    # Initialize with your API keys
    # You'll need to set these as environment variables or pass them directly
    openai_api_key = os.getenv("OPENAI_API_KEY")
    hubspot_api_key = os.getenv("HUBSPOT_API_KEY")  # Optional
    mixpanel_project_id = os.getenv("MIXPANEL_PROJECT_ID")  # Optional
    mixpanel_api_secret = os.getenv("MIXPANEL_API_SECRET")  # Optional
    
    if not openai_api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    # Initialize CEO Assistant
    assistant = CEOAssistant(
        openai_api_key=openai_api_key,
        hubspot_api_key=hubspot_api_key,
        mixpanel_project_id=mixpanel_project_id,
        mixpanel_api_secret=mixpanel_api_secret
    )
    
    # Example interactions
    print("=== CEO Assistant Demo ===\n")
    
    # Strategic analysis
    print("1. Strategic Growth Analysis:")
    response = assistant.process_request("Analyze our growth opportunities and provide strategic recommendations")
    print(f"Agent: {response.agent_type}")
    print(f"Response: {response.content}\n")
    
    # Weekly report
    print("2. Weekly Operational Report:")
    response = assistant.process_request("Generate this week's operational intelligence report")
    print(f"Agent: {response.agent_type}")
    print(f"Response: {response.content}\n")
    
    # Board preparation
    print("3. Board Meeting Preparation:")
    response = assistant.process_request("Prepare content for next board meeting presentation")
    print(f"Agent: {response.agent_type}")
    print(f"Response: {response.content}\n")
    
    # Dashboard summary
    print("4. Dashboard Summary:")
    summary = assistant.get_dashboard_summary()
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main() 