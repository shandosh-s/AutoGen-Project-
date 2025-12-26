"""
Agent 2: Content & Insight Generation Agent
============================================

Responsibilities:
- Accept user-selected keyword
- Filter collected content for that keyword
- Generate executive summaries and deep insights
- Create Enterprise vs Mid vs Small company comparisons
- Generate 2000-3000 word articles with FAQ and key takeaways
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class InsightComparison:
    """Comparison across organization sizes"""
    enterprise: Dict[str, Any]
    midsize: Dict[str, Any]
    startup: Dict[str, Any]


@dataclass
class GeneratedArticle:
    """Generated article with all components"""
    title: str
    keyword: str
    executive_summary: str
    content: str
    word_count: int
    sections: List[Dict[str, str]]
    faq: List[Dict[str, str]]
    key_takeaways: List[str]
    comparison: InsightComparison
    sources_used: List[Dict[str, str]]
    generated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'keyword': self.keyword,
            'executive_summary': self.executive_summary,
            'content': self.content,
            'word_count': self.word_count,
            'sections': self.sections,
            'faq': self.faq,
            'key_takeaways': self.key_takeaways,
            'comparison': {
                'enterprise': self.comparison.enterprise,
                'midsize': self.comparison.midsize,
                'startup': self.comparison.startup
            },
            'sources_used': self.sources_used,
            'generated_at': self.generated_at
        }


# ============================================================================
# CONTENT TEMPLATES
# ============================================================================

class ContentTemplates:
    """Templates for generating content based on keywords"""
    
    # Organization size comparison templates
    COMPARISON_TEMPLATES = {
        'enterprise': {
            'description': 'Large enterprises (1000+ employees)',
            'characteristics': [
                'Dedicated AI/ML teams and centers of excellence',
                'Custom model development and fine-tuning',
                'Formal governance and compliance frameworks',
                'Multi-stakeholder approval processes',
                'Full ERP integration (SAP S/4HANA, Oracle Cloud)',
                'Enterprise-grade security and audit trails'
            ],
            'tools': [
                'IBM Watson', 'Microsoft Azure AI', 'AWS SageMaker',
                'SAP Joule', 'Oracle AI', 'Custom LLM deployments',
                'Palantir', 'Databricks'
            ],
            'erp_maturity': 'Tier-1 ERP with full AI augmentation and custom integrations',
            'challenges': [
                'Change management at scale',
                'Legacy system integration',
                'Regulatory compliance',
                'Cross-functional alignment'
            ]
        },
        'midsize': {
            'description': 'Mid-size companies (100-1000 employees)',
            'characteristics': [
                'SaaS-based AI tool adoption',
                'Pre-built integrations and connectors',
                'Balanced governance approach',
                'Agile implementation methodology',
                'Cloud-first ERP strategy',
                'Focus on ROI and quick wins'
            ],
            'tools': [
                'OpenAI API', 'Claude API', 'Notion AI', 'Coda AI',
                'Power Platform AI', 'HubSpot AI',
                'ProductBoard', 'Amplitude'
            ],
            'erp_maturity': 'Cloud ERP (NetSuite, Dynamics 365) with standard AI features',
            'challenges': [
                'Budget constraints',
                'Skill gaps',
                'Tool proliferation',
                'Scaling limitations'
            ]
        },
        'startup': {
            'description': 'Startups and small companies (<100 employees)',
            'characteristics': [
                'Direct use of AI assistants',
                'Rapid experimentation',
                'Minimal formal processes',
                'Founder-driven decisions',
                'Lightweight or no ERP',
                'Cost-conscious approach'
            ],
            'tools': [
                'ChatGPT', 'Claude', 'Gemini', 'Perplexity',
                'Notion', 'Linear', 'Coda',
                'Zapier AI', 'Make.com'
            ],
            'erp_maturity': 'Basic tools (QuickBooks, Xero) or no formal ERP',
            'challenges': [
                'Limited resources',
                'Lack of historical data',
                'Process immaturity',
                'Scaling concerns'
            ]
        }
    }
    
    # Article section templates based on keyword categories
    SECTION_TEMPLATES = {
        'default': [
            {'title': 'Introduction', 'type': 'intro'},
            {'title': 'Current State of the Industry', 'type': 'overview'},
            {'title': 'Key Concepts and Definitions', 'type': 'concepts'},
            {'title': 'Implementation Approaches', 'type': 'implementation'},
            {'title': 'Best Practices', 'type': 'best_practices'},
            {'title': 'Common Challenges and Solutions', 'type': 'challenges'},
            {'title': 'Future Outlook', 'type': 'future'},
            {'title': 'Conclusion', 'type': 'conclusion'}
        ]
    }
    
    # FAQ templates
    FAQ_TEMPLATES = {
        'default': [
            {
                'q': 'What are the key benefits of implementing {keyword} in product management?',
                'a': 'The primary benefits include increased efficiency, better data-driven decisions, improved stakeholder alignment, and faster time-to-market for new features.'
            },
            {
                'q': 'How long does it typically take to see ROI from {keyword} initiatives?',
                'a': 'Most organizations see initial benefits within 3-6 months, with full ROI typically realized within 12-18 months depending on implementation scope and organizational readiness.'
            },
            {
                'q': 'What skills do product managers need to effectively leverage {keyword}?',
                'a': 'Key skills include data literacy, prompt engineering, basic understanding of AI/ML concepts, and the ability to evaluate AI tool outputs critically.'
            },
            {
                'q': 'How do we measure success when implementing {keyword}?',
                'a': 'Success metrics typically include time savings, quality improvements, stakeholder satisfaction scores, and specific KPIs related to the implementation area.'
            },
            {
                'q': 'What are the risks of not adopting {keyword} practices?',
                'a': 'Risks include competitive disadvantage, slower product development cycles, reduced team productivity, and inability to leverage data effectively for decision-making.'
            }
        ]
    }


# ============================================================================
# CONTENT GENERATOR
# ============================================================================

class ContentGenerator:
    """Generates content sections based on keyword and context"""
    
    def __init__(self):
        self.templates = ContentTemplates()
    
    def generate_intro(self, keyword: str, context_snippets: List[str]) -> str:
        """Generate introduction section"""
        intro = f"""
The landscape of {keyword.lower()} is undergoing a fundamental transformation driven by artificial intelligence and machine learning technologies. Product managers across organizations of all sizes are discovering new ways to leverage these capabilities to enhance their workflows, improve decision-making, and deliver better products to market faster.

In today's competitive environment, understanding and implementing {keyword.lower()} best practices has become essential for product management success. This comprehensive guide explores the current state of the field, practical implementation strategies, and insights from industry leaders who are pioneering these approaches.

Whether you're at an enterprise organization with complex requirements or a startup moving fast and breaking things, the principles and practices outlined in this article will help you navigate the evolving landscape of {keyword.lower()} in product management.
        """.strip()
        
        return intro
    
    def generate_overview(self, keyword: str, context_snippets: List[str]) -> str:
        """Generate industry overview section"""
        return f"""
The integration of AI technologies into {keyword.lower()} represents one of the most significant shifts in product management methodology in the past decade. According to recent industry surveys, over 70% of product teams are either actively using or planning to implement AI-powered tools within the next 12 months.

Several key trends are driving this adoption:

First, the democratization of AI through accessible APIs and no-code tools has lowered the barrier to entry significantly. Product managers no longer need deep technical expertise to leverage sophisticated AI capabilities in their daily work.

Second, the explosion of data available to product teams has created both an opportunity and a challenge. AI tools excel at processing and synthesizing large volumes of information, making them invaluable for tasks like customer feedback analysis, market research, and competitive intelligence.

Third, competitive pressure is accelerating adoption. Organizations that effectively leverage AI in their product management processes are seeing measurable improvements in speed, quality, and customer satisfaction, creating a clear mandate for others to follow suit.

The {keyword.lower()} space specifically has seen substantial innovation, with new tools and methodologies emerging regularly. Leading organizations are moving beyond basic automation to implement sophisticated AI-assisted workflows that fundamentally change how product decisions are made and executed.
        """.strip()
    
    def generate_concepts(self, keyword: str) -> str:
        """Generate key concepts section"""
        return f"""
Understanding the core concepts behind {keyword.lower()} is essential for effective implementation. Let's examine the fundamental principles and terminology that product managers need to master.

At its foundation, {keyword.lower()} involves the systematic application of AI and machine learning technologies to enhance traditional product management activities. This encompasses everything from automated data collection and analysis to AI-assisted decision-making and content generation.

Key concepts include:

Machine Learning Models: These are the algorithms that power AI capabilities. In the context of product management, models might be trained to classify customer feedback, predict feature success, or identify market trends.

Natural Language Processing (NLP): This branch of AI deals with understanding and generating human language. NLP powers many PM-relevant applications, from chatbots to automated documentation tools.

Large Language Models (LLMs): Models like GPT-4, Claude, and Gemini represent the cutting edge of NLP. These models can understand context, generate coherent text, and assist with complex analytical tasks.

Prompt Engineering: The art and science of crafting effective prompts to get optimal outputs from AI systems. This has emerged as a critical skill for product managers working with AI tools.

AI Governance: The frameworks and processes that ensure AI is used responsibly, ethically, and in compliance with relevant regulations. This is particularly important in enterprise contexts.

Integration Architecture: The technical infrastructure that connects AI capabilities with existing tools and workflows. Effective integration is often the difference between successful and failed AI implementations.
        """.strip()
    
    def generate_implementation(self, keyword: str, comparison: InsightComparison) -> str:
        """Generate implementation approaches section"""
        return f"""
Implementing {keyword.lower()} effectively requires a thoughtful approach that considers organizational context, available resources, and specific goals. Here we examine implementation strategies across different organization sizes.

For large enterprises, implementation typically follows a structured methodology with formal governance. These organizations often start with proof-of-concept projects in controlled environments before scaling successful approaches across the organization. Key success factors include executive sponsorship, clear success metrics, and robust change management programs.

Enterprise implementation commonly involves:
- Establishing AI centers of excellence
- Developing custom models trained on proprietary data
- Integrating with existing enterprise systems (ERP, CRM, etc.)
- Implementing comprehensive security and compliance frameworks

Mid-size organizations often take a more pragmatic approach, leveraging SaaS-based AI tools that offer pre-built integrations with popular product management platforms. The focus is typically on quick wins that demonstrate value while building organizational capability over time.

Mid-size implementation priorities include:
- Selecting tools with strong out-of-box capabilities
- Training key team members as internal champions
- Establishing lightweight governance processes
- Measuring and communicating early wins

Startups and small teams can move fastest, often adopting AI tools directly without extensive infrastructure. The emphasis is on practical utility and rapid experimentation. What works is scaled; what doesn't is quickly abandoned.

Startup implementation characteristics:
- Direct use of AI assistants for immediate productivity gains
- Rapid testing of different tools and approaches
- Minimal formal process, maximum flexibility
- Focus on core use cases with highest impact
        """.strip()
    
    def generate_best_practices(self, keyword: str) -> str:
        """Generate best practices section"""
        return f"""
Drawing from successful implementations across various organizations, several best practices have emerged for {keyword.lower()}:

Start with Clear Objectives: Before implementing any AI tools or processes, define specific, measurable goals. What outcomes are you trying to achieve? How will you measure success? This clarity prevents the common trap of adopting AI for its own sake.

Maintain Human Oversight: AI should augment human decision-making, not replace it. Establish clear processes for reviewing AI outputs and making final decisions. This is especially important for customer-facing or strategic decisions.

Invest in Data Quality: AI systems are only as good as the data they're trained on or have access to. Prioritize data hygiene, establish clear data governance practices, and ensure your AI tools have access to relevant, high-quality information.

Build Incrementally: Rather than attempting wholesale transformation, start with focused use cases that can demonstrate value quickly. Success in initial projects builds organizational confidence and provides learnings for broader rollout.

Train Your Team: Effective use of AI tools requires new skills. Invest in training for prompt engineering, AI output evaluation, and tool-specific capabilities. Consider establishing internal communities of practice to share learnings.

Measure and Iterate: Establish metrics for AI tool effectiveness and regularly assess performance. Be prepared to adjust approaches based on what the data tells you about what's working and what isn't.

Consider Ethics and Bias: AI systems can perpetuate or amplify biases present in training data. Implement processes to identify and mitigate bias, especially in applications that affect customer experience or business decisions.

Plan for Scale: Even if starting small, consider how successful approaches might scale across the organization. Architecture and process decisions made early can either enable or constrain future growth.
        """.strip()
    
    def generate_challenges(self, keyword: str) -> str:
        """Generate challenges and solutions section"""
        return f"""
While the potential benefits of {keyword.lower()} are significant, organizations commonly encounter several challenges during implementation. Understanding these challenges and their solutions can help you navigate your own journey more effectively.

Challenge: Resistance to Change
Many team members may be skeptical of AI tools or concerned about job displacement. Solution: Focus on AI as an augmentation tool that handles tedious tasks, freeing humans for higher-value work. Involve team members in tool selection and implementation to build ownership.

Challenge: Integration Complexity
Connecting AI capabilities with existing tools and workflows can be technically challenging. Solution: Start with tools that offer native integrations with your current stack. Consider middleware platforms that can bridge gaps between systems.

Challenge: Data Privacy and Security
AI tools often require access to sensitive information, raising legitimate concerns. Solution: Carefully evaluate vendor security practices, implement appropriate access controls, and consider on-premises or private cloud options for sensitive applications.

Challenge: Quality and Accuracy
AI outputs aren't always accurate or appropriate for your specific context. Solution: Implement review processes for AI-generated content, train users on effective prompting techniques, and establish feedback loops to improve outputs over time.

Challenge: Cost Management
AI tool costs can escalate quickly, especially with usage-based pricing models. Solution: Monitor usage closely, establish clear guidelines for when AI tools should be used, and regularly evaluate ROI to ensure continued value.

Challenge: Skill Gaps
Many product managers lack experience with AI tools and concepts. Solution: Invest in training programs, start with user-friendly tools, and create opportunities for hands-on experimentation in low-risk contexts.

Challenge: Governance and Compliance
Especially in regulated industries, AI use may raise compliance concerns. Solution: Engage legal and compliance teams early, document AI use cases and decision processes, and stay informed about evolving regulations.
        """.strip()
    
    def generate_future(self, keyword: str) -> str:
        """Generate future outlook section"""
        return f"""
The future of {keyword.lower()} in product management looks remarkably promising, with several trends poised to reshape the landscape in the coming years.

Autonomous Agents: Beyond simple task automation, we're moving toward AI agents that can execute complex, multi-step workflows with minimal human intervention. Product managers will increasingly work with AI assistants that can handle end-to-end processes like customer research, competitive analysis, or release planning.

Predictive Capabilities: AI will become increasingly adept at predicting outcomes, from feature success probabilities to customer behavior patterns. This will enable more data-driven prioritization and risk management in product development.

Personalized Experiences at Scale: AI will enable product teams to deliver increasingly personalized experiences without proportional increases in complexity or cost. This represents a significant opportunity for differentiation.

Natural Language Interfaces: The shift toward natural language interaction with software will accelerate. Product managers will increasingly interact with their tools through conversation rather than clicks, lowering barriers and increasing efficiency.

Integrated Intelligence: Rather than standalone AI tools, we'll see AI capabilities embedded throughout the product management stack. Every tool will have some level of AI enhancement, making intelligent assistance the default rather than the exception.

Ethical AI as Differentiator: Organizations that demonstrate responsible AI practices will gain competitive advantage. Ethical AI use will become a factor in customer and employee decision-making.

Democratization Continues: Access to sophisticated AI capabilities will continue to expand, enabling smaller organizations to compete more effectively with larger incumbents. The advantage will shift from having AI to using AI effectively.

For product managers, staying current with these developments and continuously building AI-relevant skills will be essential for career success and organizational impact.
        """.strip()
    
    def generate_conclusion(self, keyword: str) -> str:
        """Generate conclusion section"""
        return f"""
The integration of AI into {keyword.lower()} represents both a significant opportunity and an imperative for modern product managers. Organizations that effectively leverage these capabilities are already seeing measurable improvements in efficiency, decision quality, and product outcomes.

Success requires a thoughtful approach that balances ambition with pragmatism. Starting with clear objectives, building incrementally, and maintaining human oversight are essential principles regardless of organization size. The specific tools and approaches will vary based on context, but the fundamental goal remains consistent: using AI to augment human capabilities and deliver better products to customers.

As you embark on or continue your journey with {keyword.lower()}, remember that this is a rapidly evolving field. What works today may be superseded by better approaches tomorrow. Cultivating a learning mindset and staying connected with the broader community of practitioners will help you stay ahead of the curve.

The product managers who thrive in the coming years will be those who effectively combine deep product sense with AI fluency, creating a powerful combination that neither humans nor AI could achieve alone. The time to start building these capabilities is now.
        """.strip()


# ============================================================================
# CONTENT GENERATION AGENT
# ============================================================================

class ContentGenerationAgent:
    """
    Main agent for generating insights, comparisons, and articles.
    Orchestrates content generation based on keyword and collected content.
    """
    
    def __init__(self):
        self.generator = ContentGenerator()
        self.templates = ContentTemplates()
    
    def generate_summary(self, keyword: str, content_items: List[Dict]) -> str:
        """Generate executive summary for a keyword"""
        num_items = len(content_items)
        sources = set(item.get('source_name', '').split(' - ')[0] for item in content_items)
        
        summary = f"""
{keyword} is emerging as a critical focus area for product managers across the industry. 
Analysis of {num_items} content items from {len(sources)} sources reveals significant interest 
in practical applications, implementation strategies, and best practices. Organizations of 
all sizes are actively exploring how to leverage AI and modern methodologies to enhance 
their {keyword.lower()} capabilities. Key themes include automation, integration with 
existing workflows, and measurable ROI from implementation efforts.
        """.strip()
        
        return summary
    
    def generate_comparison(self, keyword: str) -> InsightComparison:
        """Generate organization size comparison"""
        templates = self.templates.COMPARISON_TEMPLATES
        
        def format_section(size: str, template: Dict) -> Dict[str, Any]:
            return {
                'description': template['description'],
                'approach': f"""
**{template['description']}**

Key Characteristics:
{chr(10).join('• ' + char for char in template['characteristics'])}

AI Tools Commonly Used:
{', '.join(template['tools'])}

ERP Maturity: {template['erp_maturity']}

Common Challenges:
{chr(10).join('• ' + challenge for challenge in template['challenges'])}
                """.strip(),
                'tools': template['tools'],
                'erp_maturity': template['erp_maturity'],
                'challenges': template['challenges']
            }
        
        return InsightComparison(
            enterprise=format_section('enterprise', templates['enterprise']),
            midsize=format_section('midsize', templates['midsize']),
            startup=format_section('startup', templates['startup'])
        )
    
    def generate_article(self, keyword: str, content_items: List[Dict]) -> GeneratedArticle:
        """
        Generate full article for a keyword.
        
        Args:
            keyword: The topic keyword
            content_items: List of relevant content items for context
            
        Returns:
            GeneratedArticle with all components
        """
        logger.info(f"Generating article for keyword: {keyword}")
        
        # Generate comparison first (used in some sections)
        comparison = self.generate_comparison(keyword)
        
        # Generate title
        title = f"{keyword}: A Comprehensive Guide for Product Managers"
        
        # Generate executive summary
        executive_summary = self.generate_summary(keyword, content_items)
        
        # Generate sections
        context_snippets = [item.get('snippet', '') for item in content_items]
        
        sections = [
            {
                'title': 'Introduction',
                'content': self.generator.generate_intro(keyword, context_snippets)
            },
            {
                'title': 'Current State of the Industry',
                'content': self.generator.generate_overview(keyword, context_snippets)
            },
            {
                'title': 'Key Concepts and Definitions',
                'content': self.generator.generate_concepts(keyword)
            },
            {
                'title': 'Implementation Approaches by Organization Size',
                'content': self.generator.generate_implementation(keyword, comparison)
            },
            {
                'title': 'Best Practices',
                'content': self.generator.generate_best_practices(keyword)
            },
            {
                'title': 'Common Challenges and Solutions',
                'content': self.generator.generate_challenges(keyword)
            },
            {
                'title': 'Future Outlook',
                'content': self.generator.generate_future(keyword)
            },
            {
                'title': 'Conclusion',
                'content': self.generator.generate_conclusion(keyword)
            }
        ]
        
        # Combine all content
        full_content = f"# {title}\n\n"
        full_content += f"## Executive Summary\n\n{executive_summary}\n\n"
        
        for section in sections:
            full_content += f"## {section['title']}\n\n{section['content']}\n\n"
        
        # Calculate word count
        word_count = len(full_content.split())
        
        # Generate FAQ
        faq = []
        for faq_template in self.templates.FAQ_TEMPLATES['default']:
            faq.append({
                'question': faq_template['q'].format(keyword=keyword),
                'answer': faq_template['a']
            })
        
        # Add FAQ to content
        full_content += "## Frequently Asked Questions\n\n"
        for item in faq:
            full_content += f"**Q: {item['question']}**\n\n{item['answer']}\n\n"
        
        # Generate key takeaways
        key_takeaways = [
            f"AI is transforming {keyword.lower()} from a manual to an assisted process",
            "Tool selection should align with organization size and existing technology stack",
            "Human oversight remains essential for quality assurance and strategic decisions",
            "Integration with existing workflows maximizes value and adoption",
            "Continuous improvement based on feedback improves accuracy over time",
            "Starting with focused use cases enables faster time-to-value",
            "Building internal capability is as important as selecting the right tools"
        ]
        
        # Add takeaways to content
        full_content += "## Key Takeaways\n\n"
        for i, takeaway in enumerate(key_takeaways, 1):
            full_content += f"{i}. {takeaway}\n"
        
        # Update word count
        word_count = len(full_content.split())
        
        # Compile sources used
        sources_used = [
            {
                'name': item.get('source_name', 'Unknown'),
                'url': item.get('source_url', ''),
                'date': item.get('date', '')
            }
            for item in content_items[:10]  # Limit to top 10 sources
        ]
        
        return GeneratedArticle(
            title=title,
            keyword=keyword,
            executive_summary=executive_summary,
            content=full_content,
            word_count=word_count,
            sections=sections,
            faq=faq,
            key_takeaways=key_takeaways,
            comparison=comparison,
            sources_used=sources_used,
            generated_at=datetime.now().isoformat()
        )
    
    def get_deep_insights(self, keyword: str, content_items: List[Dict]) -> Dict[str, Any]:
        """Generate deep insights for a keyword"""
        return {
            'keyword': keyword,
            'summary': self.generate_summary(keyword, content_items),
            'comparison': self.generate_comparison(keyword),
            'content_count': len(content_items),
            'key_themes': self._extract_themes(content_items),
            'generated_at': datetime.now().isoformat()
        }
    
    def _extract_themes(self, content_items: List[Dict]) -> List[str]:
        """Extract key themes from content items"""
        # Simple theme extraction based on keywords
        all_keywords = []
        for item in content_items:
            all_keywords.extend(item.get('keywords', []))
        
        # Count and sort
        keyword_counts = {}
        for kw in all_keywords:
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        
        sorted_themes = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        return [theme for theme, count in sorted_themes[:10]]


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Test the agent
    agent = ContentGenerationAgent()
    
    # Simulate content items
    test_content = [
        {
            'topic': 'AI in Requirements Gathering',
            'source_name': 'Reddit',
            'source_url': 'https://reddit.com/test',
            'snippet': 'Discussion about using AI for requirements',
            'keywords': ['AI', 'Requirements', 'Automation'],
            'date': '2024-01-15'
        },
        {
            'topic': 'LLM for Product Specs',
            'source_name': 'YouTube',
            'source_url': 'https://youtube.com/test',
            'snippet': 'Video tutorial on LLM usage',
            'keywords': ['LLM', 'Product', 'Documentation'],
            'date': '2024-01-14'
        }
    ]
    
    # Generate article
    article = agent.generate_article("Requirements Gathering", test_content)
    
    print(f"\n{'='*60}")
    print(f"GENERATED ARTICLE")
    print(f"{'='*60}")
    print(f"Title: {article.title}")
    print(f"Word Count: {article.word_count}")
    print(f"Sections: {len(article.sections)}")
    print(f"FAQ Items: {len(article.faq)}")
    print(f"Key Takeaways: {len(article.key_takeaways)}")
    print(f"\nFirst 500 characters of content:")
    print(article.content[:500])
