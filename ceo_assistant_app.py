"""
CEO Assistant Web Interface
A Streamlit-based web application for the CEO Assistant

Run with: streamlit run ceo_assistant_app.py
"""

import streamlit as st
import os
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from ceo_assistant_starter import CEOAssistant, AgentResponse
import logging

# Configure page
st.set_page_config(
    page_title="CEO Assistant - Colppy",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .agent-response {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .recommendation {
        background-color: #fff3cd;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border-left: 3px solid #ffc107;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = None
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'dashboard_data' not in st.session_state:
        st.session_state.dashboard_data = None

def setup_assistant():
    """Setup the CEO Assistant with API keys"""
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key inputs
        openai_key = st.text_input("OpenAI API Key", type="password", 
                                  value=os.getenv("OPENAI_API_KEY", ""))
        hubspot_key = st.text_input("HubSpot API Key (Optional)", type="password",
                                   value=os.getenv("HUBSPOT_API_KEY", ""))
        mixpanel_id = st.text_input("Mixpanel Project ID (Optional)",
                                   value=os.getenv("MIXPANEL_PROJECT_ID", ""))
        mixpanel_secret = st.text_input("Mixpanel API Secret (Optional)", type="password",
                                       value=os.getenv("MIXPANEL_API_SECRET", ""))
        
        if st.button("Initialize Assistant"):
            if openai_key:
                try:
                    st.session_state.assistant = CEOAssistant(
                        openai_api_key=openai_key,
                        hubspot_api_key=hubspot_key if hubspot_key else None,
                        mixpanel_project_id=mixpanel_id if mixpanel_id else None,
                        mixpanel_api_secret=mixpanel_secret if mixpanel_secret else None
                    )
                    st.success("✅ CEO Assistant initialized successfully!")
                    
                    # Get dashboard data
                    st.session_state.dashboard_data = st.session_state.assistant.get_dashboard_summary()
                    
                except Exception as e:
                    st.error(f"❌ Error initializing assistant: {e}")
            else:
                st.error("❌ OpenAI API Key is required")

def display_dashboard():
    """Display the main dashboard with key metrics"""
    st.markdown('<div class="main-header">🚀 CEO Assistant Dashboard</div>', unsafe_allow_html=True)
    
    if st.session_state.dashboard_data:
        data = st.session_state.dashboard_data
        
        # Connection status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = "🟢 Connected" if data.get('hubspot_connected') else "🔴 Disconnected"
            st.metric("HubSpot", status)
        
        with col2:
            status = "🟢 Connected" if data.get('mixpanel_connected') else "🔴 Disconnected"
            st.metric("Mixpanel", status)
        
        with col3:
            st.metric("Last Updated", data.get('timestamp', 'N/A')[:19])
        
        # Key metrics
        if 'customer_metrics' in data:
            st.subheader("📊 Customer Metrics")
            metrics = data['customer_metrics']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("New Customers", metrics.get('new_customers_this_month', 'N/A'))
            with col2:
                st.metric("Churn Rate", f"{metrics.get('churn_rate', 0)*100:.1f}%")
            with col3:
                st.metric("Customer LTV", f"${metrics.get('customer_lifetime_value', 0):,.0f}")
            with col4:
                st.metric("Acquisition Cost", f"${metrics.get('acquisition_cost', 0):,.0f}")
        
        if 'engagement_metrics' in data:
            st.subheader("📈 User Engagement")
            metrics = data['engagement_metrics']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Daily Active Users", f"{metrics.get('daily_active_users', 0):,}")
            with col2:
                st.metric("Weekly Active Users", f"{metrics.get('weekly_active_users', 0):,}")
            with col3:
                st.metric("Monthly Active Users", f"{metrics.get('monthly_active_users', 0):,}")
            
            # Retention chart
            retention_data = {
                'Period': ['D7', 'D30'],
                'Retention Rate': [
                    metrics.get('user_retention_d7', 0) * 100,
                    metrics.get('user_retention_d30', 0) * 100
                ]
            }
            
            fig = px.bar(retention_data, x='Period', y='Retention Rate',
                        title='User Retention Rates',
                        color='Retention Rate',
                        color_continuous_scale='Blues')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def chat_interface():
    """Main chat interface for interacting with agents"""
    st.subheader("💬 Chat with Your CEO Assistant")
    
    if not st.session_state.assistant:
        st.warning("⚠️ Please initialize the assistant first using the sidebar.")
        return
    
    # Quick action buttons
    st.subheader("🎯 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Weekly Report", use_container_width=True):
            process_quick_action("Generate this week's operational intelligence report")
    
    with col2:
        if st.button("🚀 Growth Analysis", use_container_width=True):
            process_quick_action("Analyze our growth opportunities and provide strategic recommendations")
    
    with col3:
        if st.button("📋 Board Update", use_container_width=True):
            process_quick_action("Prepare content for next board meeting presentation")
    
    # Chat input
    user_input = st.text_area("Ask your CEO Assistant:", 
                             placeholder="e.g., What are our top growth opportunities this quarter?",
                             height=100)
    
    if st.button("Send", type="primary"):
        if user_input:
            process_user_input(user_input)
        else:
            st.warning("Please enter a question or request.")
    
    # Display conversation history
    display_conversation_history()

def process_quick_action(action_text):
    """Process a quick action button click"""
    process_user_input(action_text)

def process_user_input(user_input):
    """Process user input and get agent response"""
    try:
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.assistant.process_request(user_input)
        
        # Add to conversation history
        st.session_state.conversation_history.append({
            "user": user_input,
            "assistant": response,
            "timestamp": datetime.now()
        })
        
        # Display the response
        display_agent_response(response)
        
    except Exception as e:
        st.error(f"❌ Error processing request: {e}")

def display_agent_response(response: AgentResponse):
    """Display agent response with formatting"""
    st.markdown(f"""
    <div class="agent-response">
        <h4>🤖 {response.agent_type} Agent</h4>
        <p>{response.content}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display recommendations if available
    if response.recommendations:
        st.subheader("💡 Recommendations")
        for rec in response.recommendations:
            st.markdown(f"""
            <div class="recommendation">
                • {rec}
            </div>
            """, unsafe_allow_html=True)
    
    # Display next actions if available
    if response.next_actions:
        st.subheader("📋 Next Actions")
        for action in response.next_actions:
            st.markdown(f"- {action}")
    
    # Display data if available
    if response.data and st.checkbox("Show raw data", key=f"data_{len(st.session_state.conversation_history)}"):
        st.json(response.data)

def display_conversation_history():
    """Display conversation history"""
    if st.session_state.conversation_history:
        st.subheader("📜 Conversation History")
        
        for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Show last 5
            with st.expander(f"💬 {conv['timestamp'].strftime('%H:%M:%S')} - {conv['user'][:50]}..."):
                st.markdown(f"**You:** {conv['user']}")
                st.markdown(f"**Assistant ({conv['assistant'].agent_type}):** {conv['assistant'].content}")

def analytics_page():
    """Analytics and insights page"""
    st.header("📊 Analytics & Insights")
    
    if not st.session_state.assistant:
        st.warning("⚠️ Please initialize the assistant first.")
        return
    
    # Refresh data button
    if st.button("🔄 Refresh Data"):
        st.session_state.dashboard_data = st.session_state.assistant.get_dashboard_summary()
        st.success("✅ Data refreshed!")
    
    if st.session_state.dashboard_data:
        data = st.session_state.dashboard_data
        
        # Create sample charts for demonstration
        st.subheader("📈 Growth Trends")
        
        # Sample growth data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        growth_data = pd.DataFrame({
            'Month': dates,
            'Revenue': [100000 + i*5000 + (i**1.5)*1000 for i in range(len(dates))],
            'Customers': [500 + i*25 + (i**1.2)*10 for i in range(len(dates))],
            'MRR': [50000 + i*2500 + (i**1.3)*500 for i in range(len(dates))]
        })
        
        # Revenue chart
        fig_revenue = px.line(growth_data, x='Month', y='Revenue',
                             title='Monthly Revenue Growth',
                             line_shape='spline')
        fig_revenue.update_layout(height=400)
        st.plotly_chart(fig_revenue, use_container_width=True)
        
        # Customer acquisition
        fig_customers = px.bar(growth_data, x='Month', y='Customers',
                              title='Customer Acquisition',
                              color='Customers',
                              color_continuous_scale='Blues')
        fig_customers.update_layout(height=400)
        st.plotly_chart(fig_customers, use_container_width=True)
        
        # Key insights
        st.subheader("🔍 Key Insights")
        insights = [
            "Customer acquisition cost has decreased by 15% this quarter",
            "Product-led growth initiatives showing 23% improvement in trial conversion",
            "Argentina market expansion opportunity identified in financial services sector",
            "Team productivity metrics indicate 18% improvement in development velocity"
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div class="recommendation">
                💡 {insight}
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Sidebar setup
    setup_assistant()
    
    # Main navigation
    tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "💬 Chat Assistant", "📊 Analytics"])
    
    with tab1:
        display_dashboard()
    
    with tab2:
        chat_interface()
    
    with tab3:
        analytics_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        🚀 CEO Assistant for Colppy.com | Built with Streamlit & OpenAI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 