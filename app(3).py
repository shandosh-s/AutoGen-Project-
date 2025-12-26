"""
AI for Product Managers - Main Application (FIXED v2)
=====================================================
- Fixed: Keyword filtering now shows related content
- Fixed: PDF exports full article content
"""

import streamlit as st
from datetime import datetime
import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import agents
from agents.trend_discovery_agent import TrendDiscoveryAgent
from agents.content_generation_agent import ContentGenerationAgent
from agents.seo_plagiarism_agent import SEOPlagiarismAgent
from utils.pdf_export import ExportManager

# Page config
st.set_page_config(
    page_title="AI for Product Managers",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white; margin: 0; font-size: 1.8rem; }
    .main-header p { color: #a8d4ff; margin: 0; }
    
    .stats-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid #2d5a87;
    }
    .stats-number { font-size: 2rem; font-weight: bold; color: #1e3a5f; }
    .stats-label { color: #666; font-size: 0.85rem; }
    
    .content-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .filtered-card {
        background: #e3f2fd;
        border: 2px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .source-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 0.25rem;
    }
    .source-reddit { background: #ff4500; color: white; }
    .source-youtube { background: #ff0000; color: white; }
    .source-google { background: #4285f4; color: white; }
    .source-quora { background: #b92b27; color: white; }
    .source-forum { background: #6c757d; color: white; }
    
    .keyword-pill {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin: 0.2rem;
        background: #e3f2fd;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #1565c0;
    }
    
    .selected-keyword-banner {
        background: linear-gradient(90deg, #1976d2 0%, #2196f3 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .plagiarism-pass {
        background: #e8f5e9;
        border: 2px solid #4caf50;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
    }
    .plagiarism-fail {
        background: #ffebee;
        border: 2px solid #f44336;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agents
@st.cache_resource
def init_agents():
    return {
        'trend_discovery': TrendDiscoveryAgent(),
        'content_generation': ContentGenerationAgent(),
        'seo_plagiarism': SEOPlagiarismAgent(plagiarism_threshold=80.0, seo_threshold=70.0),  # Lowered for testing
        'export_manager': ExportManager(output_dir='exports')
    }

agents = init_agents()

# Session state
if 'content_fetched' not in st.session_state:
    st.session_state.content_fetched = False
if 'discovery_results' not in st.session_state:
    st.session_state.discovery_results = None
if 'selected_keyword' not in st.session_state:
    st.session_state.selected_keyword = None
if 'article_generated' not in st.session_state:
    st.session_state.article_generated = False
if 'generated_article' not in st.session_state:
    st.session_state.generated_article = None
if 'analysis_report' not in st.session_state:
    st.session_state.analysis_report = None
if 'filtered_content' not in st.session_state:
    st.session_state.filtered_content = []

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 AI for Product Managers</h1>
    <p>Agentic AI Platform | Powered by Microsoft AutoGen</p>
</div>
""", unsafe_allow_html=True)

# Agent status
col1, col2, col3 = st.columns(3)
with col1:
    st.success("🤖 Agent 1: Trend Discovery")
with col2:
    st.success("🤖 Agent 2: Content Generation")
with col3:
    st.success("🤖 Agent 3: SEO & Plagiarism")

# Main layout
main_col, sidebar_col = st.columns([3, 1])

with main_col:
    st.subheader("📡 Trending Content Discovery")
    
    c1, c2 = st.columns([1, 3])
    with c1:
        fetch_button = st.button("🔄 Fetch Trending Content", type="primary", use_container_width=True)
    with c2:
        st.caption("Sources: Google Trends • Reddit • YouTube • Quora • Forums")
    
    if fetch_button:
        with st.spinner("🤖 Agent 1 discovering trends..."):
            progress = st.progress(0)
            progress.progress(30, "Fetching from sources...")
            time.sleep(0.5)
            progress.progress(70, "Processing...")
            
            results = agents['trend_discovery'].discover("AI product management", items_per_source=5)
            
            progress.progress(100, "Done!")
            time.sleep(0.3)
            progress.empty()
            
            st.session_state.discovery_results = results
            st.session_state.content_fetched = True
            st.session_state.selected_keyword = None
            st.session_state.article_generated = False
            st.session_state.filtered_content = []
            
            st.success(f"✅ Found {results['stats']['total_items']} items from {results['stats']['unique_sources']} sources!")
    
    # Display results
    if st.session_state.content_fetched and st.session_state.discovery_results:
        results = st.session_state.discovery_results
        stats = results['stats']
        
        # Stats
        st.markdown("---")
        stat_cols = st.columns(4)
        
        with stat_cols[0]:
            st.markdown(f'<div class="stats-card"><div class="stats-number">{stats["total_items"]}</div><div class="stats-label">Content Items</div></div>', unsafe_allow_html=True)
        with stat_cols[1]:
            st.markdown(f'<div class="stats-card"><div class="stats-number">{stats["unique_sources"]}</div><div class="stats-label">Sources</div></div>', unsafe_allow_html=True)
        with stat_cols[2]:
            st.markdown(f'<div class="stats-card"><div class="stats-number">{stats["total_keywords"]}</div><div class="stats-label">Keywords</div></div>', unsafe_allow_html=True)
        with stat_cols[3]:
            st.markdown(f'<div class="stats-card"><div class="stats-number">🕐</div><div class="stats-label">Just Now</div></div>', unsafe_allow_html=True)
        
        # =============================================
        # KEYWORD SELECTED - SHOW FILTERED VIEW
        # =============================================
        if st.session_state.selected_keyword:
            st.markdown("---")
            keyword = st.session_state.selected_keyword
            
            # Banner for selected keyword
            st.markdown(f"""
            <div class="selected-keyword-banner">
                <h3 style="margin:0;">🔍 Viewing: {keyword}</h3>
                <p style="margin:0; opacity:0.9;">Showing content related to this keyword</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get filtered content
            filtered = agents['trend_discovery'].filter_by_keyword(keyword)
            st.session_state.filtered_content = filtered
            
            # Show count
            st.info(f"📊 Found **{len(filtered)} content items** related to '{keyword}'")
            
            if filtered:
                # Display filtered content
                st.subheader(f"📰 Content Related to '{keyword}'")
                
                for item in filtered:
                    source_lower = item.source_name.lower()
                    if 'reddit' in source_lower:
                        badge_class = 'source-reddit'
                    elif 'youtube' in source_lower:
                        badge_class = 'source-youtube'
                    elif 'google' in source_lower:
                        badge_class = 'source-google'
                    elif 'quora' in source_lower:
                        badge_class = 'source-quora'
                    else:
                        badge_class = 'source-forum'
                    
                    keywords_html = "".join([f'<span class="keyword-pill">{kw}</span>' for kw in item.keywords])
                    
                    st.markdown(f"""
                    <div class="filtered-card">
                        <span class="source-badge {badge_class}">{item.source_name}</span>
                        <span style="color: #666; font-size: 0.8rem; margin-left: 0.5rem;">📅 {item.date}</span>
                        <h4 style="margin: 0.5rem 0; color: #1565c0;">{item.topic}</h4>
                        <p style="color: #555;">{item.snippet}</p>
                        <div>{keywords_html}</div>
                        <a href="{item.source_url}" target="_blank" style="color: #1976d2; font-size: 0.85rem;">🔗 View Source</a>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Insights section
                st.markdown("---")
                st.subheader("💡 AI-Generated Insights")
                
                insights = agents['content_generation'].get_deep_insights(keyword, [i.to_dict() for i in filtered])
                st.info(f"**Summary:** {insights['summary']}")
                
                # Comparison tabs
                st.markdown("---")
                st.subheader("📊 Organization Size Comparison")
                
                comparison = insights['comparison']
                tabs = st.tabs(["🏢 Enterprise", "🏬 Mid-Size", "🚀 Startup"])
                
                with tabs[0]:
                    st.markdown(comparison.enterprise['approach'])
                with tabs[1]:
                    st.markdown(comparison.midsize['approach'])
                with tabs[2]:
                    st.markdown(comparison.startup['approach'])
                
                # Generate article button
                st.markdown("---")
                st.subheader("📝 Generate Article")
                
                col_btn, col_info = st.columns([1, 2])
                with col_btn:
                    generate_btn = st.button("📝 Generate Full Article (2000+ words)", type="primary", use_container_width=True)
                with col_info:
                    st.caption(f"Will generate comprehensive article about '{keyword}' using {len(filtered)} source items")
                
                if generate_btn:
                    with st.spinner("🤖 Agent 2 generating comprehensive article..."):
                        progress = st.progress(0)
                        progress.progress(20, "Creating outline...")
                        time.sleep(0.3)
                        progress.progress(40, "Writing introduction...")
                        time.sleep(0.3)
                        progress.progress(60, "Generating main content...")
                        time.sleep(0.3)
                        progress.progress(80, "Adding FAQ and takeaways...")
                        time.sleep(0.3)
                        
                        article = agents['content_generation'].generate_article(keyword, [i.to_dict() for i in filtered])
                        st.session_state.generated_article = article.to_dict()
                        st.session_state.article_generated = True
                        
                        progress.progress(90, "Running SEO & Plagiarism checks...")
                        
                        # Analyze
                        analysis = agents['seo_plagiarism'].analyze(
                            article.content, 
                            keyword, 
                            article.title, 
                            [i.snippet for i in filtered]
                        )
                        st.session_state.analysis_report = analysis.to_dict()
                        
                        progress.progress(100, "Complete!")
                        time.sleep(0.3)
                        progress.empty()
                        
                        st.success(f"✅ Article generated: {article.word_count:,} words!")
                        st.rerun()
            
            else:
                st.warning(f"No content found matching '{keyword}'. Try selecting a different keyword.")
        
        # =============================================
        # NO KEYWORD SELECTED - SHOW ALL CONTENT
        # =============================================
        else:
            st.markdown("---")
            st.subheader("📰 All Collected Content")
            st.caption("👉 Select a keyword from the sidebar to filter and generate an article")
            
            for item in results['content']:
                source_lower = item.get('source_name', '').lower()
                if 'reddit' in source_lower:
                    badge_class = 'source-reddit'
                elif 'youtube' in source_lower:
                    badge_class = 'source-youtube'
                elif 'google' in source_lower:
                    badge_class = 'source-google'
                elif 'quora' in source_lower:
                    badge_class = 'source-quora'
                else:
                    badge_class = 'source-forum'
                
                keywords_html = "".join([f'<span class="keyword-pill">{kw}</span>' for kw in item.get('keywords', [])])
                
                st.markdown(f"""
                <div class="content-card">
                    <span class="source-badge {badge_class}">{item.get('source_name', 'Unknown')}</span>
                    <span style="color: #666; font-size: 0.8rem; margin-left: 0.5rem;">📅 {item.get('date', '')}</span>
                    <h4 style="margin: 0.5rem 0; color: #1e3a5f;">{item.get('topic', '')}</h4>
                    <p style="color: #555;">{item.get('snippet', '')[:200]}...</p>
                    <div>{keywords_html}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # =============================================
        # ARTICLE GENERATED - SHOW RESULTS
        # =============================================
        if st.session_state.article_generated and st.session_state.generated_article:
            article = st.session_state.generated_article
            analysis = st.session_state.analysis_report
            
            st.markdown("---")
            st.subheader(f"📄 Generated Article: {article.get('title', '')}")
            
            # Article preview
            with st.expander(f"📖 View Full Article ({article['word_count']:,} words)", expanded=False):
                st.markdown(article['content'])
            
            # Show sections
            st.markdown("**Article Sections:**")
            sections = article.get('sections', [])
            section_names = [s.get('title', '') for s in sections]
            st.write(" → ".join(section_names))
            
            # Scores
            st.markdown("---")
            st.subheader("📈 Analysis Results")
            
            col_seo, col_qual = st.columns(2)
            
            with col_seo:
                st.markdown("**SEO Analysis (30+ Checks)**")
                seo = analysis['seo_report']
                st.metric("SEO Score", f"{seo['overall_score']}%", "✓ Pass" if seo['passed'] else "✗ Fail")
                st.metric("Keyword Density", f"{seo['keyword_density']}%")
                st.metric("Word Count", f"{seo['word_count']:,}")
                st.metric("Headings", f"{seo['heading_count']}")
            
            with col_qual:
                st.markdown("**Quality Analysis**")
                quality = analysis['quality_report']
                st.metric("Quality Score", f"{quality['overall_score']}%", "✓ Pass" if quality['passed'] else "✗ Fail")
                st.metric("Human-Likeness", f"{quality['human_likeness']}%")
                st.metric("Redundancy Check", f"{quality['redundancy_score']}%")
                st.metric("PM Relevance", f"{quality['pm_relevance_score']}%")
            
            # Plagiarism
            st.markdown("---")
            st.subheader("🛡️ Plagiarism Check (Mandatory)")
            
            plag = analysis['plagiarism_report']
            
            if plag['passed']:
                st.markdown(f"""
                <div class="plagiarism-pass">
                    <h2 style="color: #4caf50; margin:0;">✅ ORIGINALITY PASSED</h2>
                    <p style="font-size: 2.5rem; font-weight: bold; color: #2e7d32; margin: 0.5rem 0;">{plag['originality_score']}%</p>
                    <p style="color: #666;">Threshold: {plag['threshold']}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="plagiarism-fail">
                    <h2 style="color: #f44336; margin:0;">❌ ORIGINALITY FAILED</h2>
                    <p style="font-size: 2.5rem; font-weight: bold; color: #c62828; margin: 0.5rem 0;">{plag['originality_score']}%</p>
                    <p style="color: #666;">Required: {plag['threshold']}% | ⚠️ PDF EXPORT BLOCKED</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Similarity breakdown
            sim_cols = st.columns(3)
            with sim_cols[0]:
                st.metric("N-gram Similarity", f"{plag['ngram_similarity']}%")
            with sim_cols[1]:
                st.metric("Cosine Similarity", f"{plag['cosine_similarity']}%")
            with sim_cols[2]:
                st.metric("Sentence Duplication", f"{plag['sentence_duplication']}%")
            
            # Export section
            st.markdown("---")
            st.subheader("📤 Export to PDF")
            
            export_status = agents['export_manager'].get_export_status(analysis)
            
            if export_status['can_export']:
                st.success("✅ All checks passed! PDF export is ready.")
                
                if st.button("📥 Generate & Download PDF", type="primary"):
                    with st.spinner("Generating PDF with full article content..."):
                        success, result = agents['export_manager'].export_pdf(article, analysis)
                        
                        if success and os.path.exists(result):
                            st.success(f"✅ PDF created: {os.path.basename(result)}")
                            
                            with open(result, 'rb') as f:
                                st.download_button(
                                    "⬇️ Download PDF",
                                    f.read(),
                                    file_name=os.path.basename(result),
                                    mime="application/pdf",
                                    type="primary"
                                )
                        else:
                            st.error(f"Failed to generate PDF: {result}")
            else:
                st.error(f"❌ Export Blocked: {export_status['message']}")
                st.warning("Improve originality score to enable PDF export, or lower the threshold in settings.")

# =============================================
# SIDEBAR
# =============================================
with sidebar_col:
    st.subheader("🔑 Keywords")
    
    if st.session_state.content_fetched and st.session_state.discovery_results:
        clusters = agents['trend_discovery'].get_keyword_clusters()
        
        # Show selected keyword at top
        if st.session_state.selected_keyword:
            st.markdown(f"""
            <div style="background: #1976d2; color: white; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;">
                <strong>Selected:</strong> {st.session_state.selected_keyword}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🗑️ Clear Selection", use_container_width=True):
                st.session_state.selected_keyword = None
                st.session_state.article_generated = False
                st.session_state.generated_article = None
                st.session_state.analysis_report = None
                st.session_state.filtered_content = []
                st.rerun()
            
            st.markdown("---")
        
        # Show keyword clusters
        st.caption("Click a keyword to view related content:")
        
        for cluster_name, keywords in clusters.items():
            if keywords:
                with st.expander(f"📁 {cluster_name} ({len(keywords)})"):
                    for kw in keywords[:10]:  # Show up to 10 per cluster
                        is_selected = kw == st.session_state.selected_keyword
                        
                        if st.button(
                            f"{'✓ ' if is_selected else ''}{kw}",
                            key=f"kw_{cluster_name}_{kw}",
                            use_container_width=True,
                            type="primary" if is_selected else "secondary"
                        ):
                            st.session_state.selected_keyword = kw
                            st.session_state.article_generated = False
                            st.session_state.generated_article = None
                            st.session_state.analysis_report = None
                            st.session_state.filtered_content = []
                            st.rerun()
    else:
        st.info("👆 Click **Fetch Trending Content** to start")
    
    # Platform info
    st.markdown("---")
    st.markdown("**Platform Features:**")
    st.markdown("""
    ✅ Multi-source discovery  
    ✅ Keyword filtering  
    ✅ 30+ SEO checks  
    ✅ Plagiarism detection  
    ✅ Full PDF export
    """)

# Footer
st.markdown("---")
st.caption("AI for Product Managers v2.0 | Built with Microsoft AutoGen + Streamlit")
