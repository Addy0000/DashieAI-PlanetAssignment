import streamlit as st
from exa_py import Exa
from autogen import AssistantAgent
from dotenv import load_dotenv
import os
import json
import re
from datetime import datetime

# Load environment variables
load_dotenv()

class MarketResearchAgent:
    def __init__(self):
        # Load API keys from Streamlit Secrets
        self.exa = Exa(api_key=st.secrets["env"]["EXA_API_KEY"])
        self.llm_config = {
            "config_list": [{
                "model": "gpt-4o-mini",
                "api_key": st.secrets["env"]["OPENAI_API_KEY"]
            }]
        }

    def determine_industry(self, company_name):
        """Determine the industry of a company using AI analysis"""
        industry_prompt = f"""
        Analyze the company {company_name} and determine its primary industry.
        Return only the industry name without any explanation or additional text.
        Example response format: "Electric Vehicles" or "Cloud Computing"
        """
        
        assistant = AssistantAgent("industry_analyzer", llm_config=self.llm_config)
        industry = assistant.generate_reply(messages=[{"content": industry_prompt, "role": "user"}])
        return str(industry).strip()

    def research_company(self, company_name):
        """Conduct comprehensive company and industry research"""
        # First determine the industry
        industry = self.determine_industry(company_name)
        
        search_queries = [
            f"{industry} industry overview and trends",
            f"{company_name} strategic focus and market position",
            f"{industry} technological innovations and future outlook"
        ]
        
        research_results = {}
        for query in search_queries:
            try:
                results = self.exa.search(query, num_results=3, type="neural")
                research_results[query] = [
                    {"title": res.title, "url": res.url, "snippet": res.summary} 
                    for res in results.results
                ]
            except Exception as e:
                st.error(f"Research error for query '{query}': {e}")
        
        return research_results, industry

    def generate_use_cases(self, company_name, industry, research_insights):
        """Generate AI/ML use cases based on company research"""
        use_case_prompt = f"""
        Based on the analysis of {company_name} in the {industry} industry, generate innovative AI/ML use cases.
        Research insights: {json.dumps(research_insights)}
        Focus on:
        - Operational efficiency
        - Customer experience enhancement
        - Technological innovation
        Give at least 5 detailed distinct use cases.
        Avoid giving code or implementation details.
        Provide specific, actionable recommendations.
        """
        
        assistant = AssistantAgent("use_case_generator", llm_config=self.llm_config)
        use_cases = assistant.generate_reply(messages=[{"content": use_case_prompt, "role": "user"}])
        
        return [case.strip() for case in re.split(r'\d+\.', str(use_cases)) if case.strip()]

    def collect_resource_assets(self, use_cases):
        """Collect dataset resources for each use case"""
        resource_map = {}
        platforms = [
            "kaggle.com/datasets", 
            "huggingface.co/datasets", 
            "github.com/datasets"
        ]
        
        for use_case in use_cases:
            resources = []
            for platform in platforms:
                query = f'"{use_case}" dataset site:{platform}'
                try:
                    results = self.exa.search(query, num_results=3)
                    platform_resources = [
                        {"url": res.url, "title": res.title}
                        for res in results.results
                        if platform in res.url and any(keyword in res.url.lower() for keyword in ['dataset', 'data'])
                    ]
                    resources.extend(platform_resources)
                except Exception as e:
                    st.warning(f"Resource collection error for '{use_case}': {e}")
            
            resource_map[use_case] = resources[:3]
        
        return resource_map

    def generate_final_proposal(self, company_name, industry, use_cases, resource_map, research_insights):
        """Create comprehensive markdown proposal"""
        proposal = f"# AI Strategy Analysis for {company_name}\n\n"
        proposal += f"## Industry: {industry}\n\n"
        proposal += f"*Generated on {datetime.now().strftime('%B %d, %Y')}*\n\n"
        
        # Add research context
        proposal += "## Market Research Insights\n"
        for query, insights in research_insights.items():
            proposal += f"### {query.title()}\n\n"
            for insight in insights:
                date_str = f" ({insight.get('published_date', 'N/A')})" if 'published_date' in insight and insight.get('published_date', 'N/A') != 'N/A' else ""
                proposal += f"#### {insight['title']}{date_str}\n\n"
                proposal += f"{insight['snippet']}\n\n"
                proposal += f"[Read more]({insight['url']})\n\n"
                proposal += "---\n\n"
        
        # Add use cases and resources
        proposal += "## Recommended AI/ML Use Cases\n\n"
        for idx, use_case in enumerate(use_cases, 1):
            proposal += f"### Use Case {idx}: {use_case}\n\n"
            
            if use_case in resource_map and resource_map[use_case]:
                proposal += "#### Recommended Datasets:\n"
                for resource in resource_map[use_case]:
                    proposal += f"- [{resource['title']}]({resource['url']})\n"
            
            proposal += "\n"
        
        return proposal

def main():
    st.set_page_config(
        page_title="Dashie | AI Strategy Analysis",
        page_icon="favicon.png",
    )

    # Custom CSS for modern UI with purple buttons
    st.markdown("""<style>
        .stApp { background-color: #111121; }
        .main { padding: 2rem; }
        .st-emotion-cache-16idsys p { font-size: 1.1rem; }
        .stButton > button {
            background-color: #9933FF;
            color: white;
            border: none;
        }
        .stButton > button:hover {
            background-color: #7F00FF;
            color: white;
        }
    </style>""", unsafe_allow_html=True)

    # Header Section
    col1, col2 = st.columns([2, 3])
    with col1:
        st.image("dashie.svg", width=260)  # Replace with your logo
    with col2:
        st.title("Dashie")
        st.markdown("*AI-Powered Company Analysis Engine*")

    # Initialize Research Agent
    research_agent = MarketResearchAgent(api_key=os.getenv("EXA_API_KEY"))

    # Main Input Section
    st.markdown("### 🎯 Company Analysis")
    company_name = st.text_input(
        "",
        placeholder="Enter company name (e.g., Tesla, Microsoft, Apple)",
        help="Enter the company you want to analyze"
    )

    # Analysis Process
    if st.button("Generate Analysis", type="primary"):
        if company_name:
            # Progress Handling
            progress_placeholder = st.empty()
            progress_bar = st.progress(0)

            with st.spinner("Analyzing company data..."):
                # Phase 1: Research and Industry Determination
                progress_placeholder.markdown("🔍 **Phase 1:** Identifying industry and gathering intelligence...")
                research_insights, industry = research_agent.research_company(company_name)
                st.sidebar.success(f"Industry Identified: {industry}")
                progress_bar.progress(25)

                # Phase 2: Use Cases
                progress_placeholder.markdown("💡 **Phase 2:** Identifying strategic opportunities...")
                use_cases = research_agent.generate_use_cases(company_name, industry, research_insights)
                progress_bar.progress(50)

                # Phase 3: Resources
                progress_placeholder.markdown("📚 **Phase 3:** Collecting supporting resources...")
                resource_map = research_agent.collect_resource_assets(use_cases)
                progress_bar.progress(75)

                # Phase 4: Proposal
                progress_placeholder.markdown("📊 **Phase 4:** Generating comprehensive report...")
                final_proposal = research_agent.generate_final_proposal(
                    company_name, industry, use_cases, resource_map, research_insights
                )
                progress_bar.progress(100)
                progress_placeholder.empty()

                # Display Results
                st.markdown("---")
                st.markdown(f"## Analysis Results for {company_name}")
                st.markdown(f"**Industry:** {industry}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Research Sources", len(research_insights))
                with col2:
                    st.metric("Strategic Opportunities", len(use_cases))
                with col3:
                    total_resources = sum(len(resources) for resources in resource_map.values())
                    st.metric("Supporting Resources", total_resources)

                # Detailed Tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📈 Market Research",
                    "💡 Strategic Use Cases",
                    "🔗 Resources",
                    "📑 Full Report"
                ])
                
                with tab1:

                    for query, insights in research_insights.items():
                        st.subheader(query.title())
                        for insight in insights:
                            with st.expander(f"📑 {insight['title']}"):
                                if 'published_date' in insight and insight['published_date'] != 'N/A':
                                    st.caption(f"Published: {insight['published_date']}")
                    
                                st.markdown(f"[Read full article]({insight['url']})")
                        st.markdown("---")

                with tab2:

                    for idx, case in enumerate(use_cases, 1):
                        st.markdown(f"### Opportunity {idx}")
                        st.markdown(case)

                with tab3:

                    for use_case, resources in resource_map.items():
                        with st.expander(f"Resources for: {use_case[:100]}..."):
                            for resource in resources:
                                st.markdown(f"- [{resource['title']}]({resource['url']})")

                with tab4:
                    
                    st.markdown(final_proposal)
                    with open("ai_strategy_proposal.md", "w") as file:
                        file.write(final_proposal)
                    with open("ai_strategy_proposal.md", "rb") as md_file:
                        st.download_button(
                            label="📥 Download Full Report",
                            data=md_file,
                            file_name=f"{company_name}_analysis_{datetime.now().strftime('%Y%m%d')}.md",
                            mime='text/markdown'
                        )
        else:
            st.warning("Please enter a company name to begin the analysis.")

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'>"
                "<small>Powered by AI | Made by Adarsh</small></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()