"""
Agent 1: Trend Discovery & Source Intelligence Agent
=====================================================
"""

import os
import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentItem:
    """Represents a single piece of collected content"""
    def __init__(self, id: str, topic: str, source_name: str, source_url: str,
                 content_type: str, date: str, timestamp: str, snippet: str,
                 keywords: List[str] = None, image_url: str = None,
                 video_url: str = None, raw_content: str = None):
        self.id = id
        self.topic = topic
        self.source_name = source_name
        self.source_url = source_url
        self.content_type = content_type
        self.date = date
        self.timestamp = timestamp
        self.snippet = snippet
        self.keywords = keywords or []
        self.image_url = image_url
        self.video_url = video_url
        self.raw_content = raw_content
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'topic': self.topic,
            'source_name': self.source_name,
            'source_url': self.source_url,
            'content_type': self.content_type,
            'date': self.date,
            'timestamp': self.timestamp,
            'snippet': self.snippet,
            'keywords': self.keywords,
            'image_url': self.image_url,
            'video_url': self.video_url,
            'raw_content': self.raw_content
        }


class BaseSourceCollector:
    """Base class for source collectors"""
    
    def __init__(self, name: str):
        self.name = name
        self.last_fetched = None
        self.items = []
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        pm_keywords = [
            'product management', 'product manager', 'roadmap', 'backlog',
            'user story', 'requirements', 'stakeholder', 'agile', 'scrum',
            'sprint', 'kanban', 'okr', 'kpi', 'metrics', 'analytics',
            'customer feedback', 'user research', 'mvp', 'feature',
            'prioritization', 'release', 'deployment', 'a/b testing'
        ]
        
        ai_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'natural language processing', 'nlp', 'llm', 'gpt', 'chatgpt',
            'claude', 'gemini', 'copilot', 'automation', 'neural network',
            'transformer', 'embedding', 'vector', 'rag', 'fine-tuning',
            'prompt engineering', 'generative ai', 'computer vision'
        ]
        
        erp_keywords = [
            'erp', 'sap', 'oracle', 'dynamics', 'netsuite', 'workday',
            'salesforce', 'hubspot', 'zoho', 'odoo', 'integration',
            'enterprise', 'digital transformation', 'legacy', 'migration'
        ]
        
        all_keywords = pm_keywords + ai_keywords + erp_keywords
        text_lower = text.lower()
        
        found_keywords = []
        for keyword in all_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword.title())
        
        return list(set(found_keywords))[:10]


class GoogleTrendsCollector(BaseSourceCollector):
    """Collector for Google Trends data"""
    
    def __init__(self):
        super().__init__("Google Trends")
    
    def fetch(self, query: str = "AI product management", limit: int = 10) -> List[ContentItem]:
        """Fetch trending topics - using simulated data"""
        return self._get_simulated_data(query, limit)
    
    def _get_simulated_data(self, query: str, limit: int) -> List[ContentItem]:
        simulated_topics = [
            ("AI Product Roadmap Tools", 340),
            ("ChatGPT for Product Managers", 280),
            ("ERP AI Integration", 195),
            ("Automated User Story Generation", 175),
            ("AI-Powered Sprint Planning", 150),
            ("Machine Learning Product Analytics", 130),
            ("LLM Requirements Gathering", 125),
            ("Generative AI in SAP", 110),
            ("Product Manager AI Assistant", 95),
            ("Natural Language Processing ERP", 85)
        ]
        
        items = []
        for idx, (topic, increase) in enumerate(simulated_topics[:limit]):
            items.append(ContentItem(
                id=f"gt_sim_{idx}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                topic=topic,
                source_name="Google Trends",
                source_url=f"https://trends.google.com/trends/explore?q={topic.replace(' ', '+')}",
                content_type="Text",
                date=datetime.now().strftime("%Y-%m-%d"),
                timestamp=datetime.now().strftime("%H:%M:%S"),
                snippet=f"Rising search interest in '{topic}' showing {increase}% increase over the past week",
                keywords=self.extract_keywords(topic)
            ))
        
        return items


class RedditCollector(BaseSourceCollector):
    """Collector for Reddit posts"""
    
    def __init__(self):
        super().__init__("Reddit")
    
    def fetch(self, query: str = "AI", limit: int = 10) -> List[ContentItem]:
        return self._get_simulated_data(query, limit)
    
    def _get_simulated_data(self, query: str, limit: int) -> List[ContentItem]:
        simulated_posts = [
            {
                "subreddit": "ProductManagement",
                "title": "How are you using AI to improve requirements gathering?",
                "snippet": "I've been experimenting with ChatGPT to help synthesize user interviews and extract key requirements. Curious what tools others are using...",
                "hours_ago": 3
            },
            {
                "subreddit": "ProductManagement",
                "title": "AI tools that actually help with roadmap planning?",
                "snippet": "Looking for recommendations on AI-powered roadmap tools that integrate with Jira. We're a mid-size SaaS company...",
                "hours_ago": 8
            },
            {
                "subreddit": "agile",
                "title": "Using LLMs to auto-generate user stories from stakeholder notes",
                "snippet": "Just built a simple workflow that takes meeting transcripts and generates user stories. Here's my approach...",
                "hours_ago": 12
            },
            {
                "subreddit": "MachineLearning",
                "title": "Fine-tuning models for product management tasks",
                "snippet": "Has anyone fine-tuned a model specifically for PM use cases like feature prioritization or customer feedback analysis?",
                "hours_ago": 24
            },
            {
                "subreddit": "SaaS",
                "title": "AI-powered analytics dashboards for product metrics",
                "snippet": "We just integrated an AI layer into our analytics stack. It automatically surfaces anomalies and suggests actions...",
                "hours_ago": 36
            },
            {
                "subreddit": "prodmgmt",
                "title": "ERP modernization with AI - lessons learned",
                "snippet": "Just completed a 2-year ERP modernization project. Key insight: AI copilots reduced training time by 40%...",
                "hours_ago": 48
            },
            {
                "subreddit": "ProductManagement",
                "title": "Best practices for AI-assisted competitive analysis",
                "snippet": "Using Claude to analyze competitor products and generate comparison matrices. Here's my prompt template...",
                "hours_ago": 60
            },
            {
                "subreddit": "agile",
                "title": "Sprint retrospectives enhanced with AI sentiment analysis",
                "snippet": "We started running retro feedback through an NLP model to identify patterns. Results have been eye-opening...",
                "hours_ago": 72
            }
        ]
        
        items = []
        for idx, post in enumerate(simulated_posts[:limit]):
            post_time = datetime.now() - timedelta(hours=post['hours_ago'])
            items.append(ContentItem(
                id=f"reddit_sim_{idx}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                topic=post['title'],
                source_name=f"Reddit - r/{post['subreddit']}",
                source_url=f"https://reddit.com/r/{post['subreddit']}/comments/example{idx}",
                content_type="Text",
                date=post_time.strftime("%Y-%m-%d"),
                timestamp=post_time.strftime("%H:%M:%S"),
                snippet=post['snippet'],
                keywords=self.extract_keywords(post['title'] + " " + post['snippet'])
            ))
        
        return items


class YouTubeCollector(BaseSourceCollector):
    """Collector for YouTube videos"""
    
    def __init__(self):
        super().__init__("YouTube")
    
    def fetch(self, query: str = "AI product management", limit: int = 10) -> List[ContentItem]:
        return self._get_simulated_data(query, limit)
    
    def _get_simulated_data(self, query: str, limit: int) -> List[ContentItem]:
        simulated_videos = [
            {"title": "How AI is Transforming Product Management in 2024", "channel": "Product School", "views": "45K", "days_ago": 2},
            {"title": "Top 10 AI Tools Every Product Manager Should Know", "channel": "Lenny's Podcast", "views": "128K", "days_ago": 5},
            {"title": "Building AI-Powered Features: A PM's Guide", "channel": "Y Combinator", "views": "89K", "days_ago": 7},
            {"title": "ERP Integration with Generative AI - Complete Tutorial", "channel": "SAP Learning", "views": "23K", "days_ago": 10},
            {"title": "Sprint Planning with AI Copilots - Live Demo", "channel": "Atlassian", "views": "67K", "days_ago": 14},
            {"title": "From Requirements to User Stories with LLMs", "channel": "Pragmatic Institute", "views": "34K", "days_ago": 18},
            {"title": "AI Product Metrics That Actually Matter", "channel": "Reforge", "views": "56K", "days_ago": 21},
            {"title": "Enterprise AI Adoption: PM Perspective", "channel": "Mind the Product", "views": "41K", "days_ago": 25}
        ]
        
        items = []
        for idx, video in enumerate(simulated_videos[:limit]):
            video_time = datetime.now() - timedelta(days=video['days_ago'])
            video_id = f"vid_{idx}"
            
            items.append(ContentItem(
                id=f"yt_{video_id}",
                topic=video['title'],
                source_name="YouTube",
                source_url=f"https://youtube.com/watch?v={video_id}",
                content_type="Video",
                date=video_time.strftime("%Y-%m-%d"),
                timestamp=video_time.strftime("%H:%M:%S"),
                snippet=f"Video by {video['channel']} • {video['views']} views",
                keywords=self.extract_keywords(video['title']),
                image_url=f"https://via.placeholder.com/320x180.png?text=Video",
                video_url=f"https://youtube.com/watch?v={video_id}"
            ))
        
        return items


class QuoraCollector(BaseSourceCollector):
    """Collector for Quora questions"""
    
    def __init__(self):
        super().__init__("Quora")
    
    def fetch(self, query: str = "AI product management", limit: int = 10) -> List[ContentItem]:
        return self._get_simulated_data(query, limit)
    
    def _get_simulated_data(self, query: str, limit: int) -> List[ContentItem]:
        simulated_questions = [
            {"question": "What AI tools are product managers using for requirements documentation?", "answer_preview": "Based on my experience at a Fortune 500 company, we've been using a combination of...", "hours_ago": 6},
            {"question": "How will AI change the role of product managers in the next 5 years?", "answer_preview": "The role will evolve significantly. PMs will become more like AI orchestrators...", "hours_ago": 18},
            {"question": "Best practices for integrating AI copilots into SAP ERP?", "answer_preview": "We recently completed an SAP S/4HANA implementation with embedded AI. Key learnings...", "hours_ago": 30},
            {"question": "Should product managers learn prompt engineering?", "answer_preview": "Absolutely. Prompt engineering is becoming a core PM skill. Here's why...", "hours_ago": 48},
            {"question": "What metrics should PMs track for AI-powered features?", "answer_preview": "Beyond traditional product metrics, you need to consider AI-specific KPIs like...", "hours_ago": 72},
            {"question": "How do enterprises handle AI governance in product development?", "answer_preview": "Enterprise AI governance requires a structured approach. We implemented...", "hours_ago": 96}
        ]
        
        items = []
        for idx, q in enumerate(simulated_questions[:limit]):
            q_time = datetime.now() - timedelta(hours=q['hours_ago'])
            
            items.append(ContentItem(
                id=f"quora_sim_{idx}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                topic=q['question'],
                source_name="Quora",
                source_url=f"https://quora.com/q/ai-pm-question-{idx}",
                content_type="Text",
                date=q_time.strftime("%Y-%m-%d"),
                timestamp=q_time.strftime("%H:%M:%S"),
                snippet=q['answer_preview'],
                keywords=self.extract_keywords(q['question'] + " " + q['answer_preview'])
            ))
        
        return items


class ForumCollector(BaseSourceCollector):
    """Collector for AI & PM forum discussions"""
    
    def __init__(self):
        super().__init__("AI & PM Forums")
    
    def fetch(self, query: str = "AI", limit: int = 10) -> List[ContentItem]:
        return self._get_simulated_data(query, limit)
    
    def _get_simulated_data(self, query: str, limit: int) -> List[ContentItem]:
        simulated_discussions = [
            {"forum": "Product Coalition", "title": "Weekly Discussion: AI's Impact on PM Workflows", "snippet": "This week we're discussing how AI tools are changing daily PM workflows...", "days_ago": 1},
            {"forum": "Mind the Product Forum", "title": "Case Study: Implementing AI in Enterprise Product Teams", "snippet": "Sharing our journey of rolling out AI tools across 50+ product teams...", "days_ago": 3},
            {"forum": "AI Product Institute", "title": "Framework: AI Feature Prioritization Matrix", "snippet": "Developed a new framework for prioritizing AI-powered features...", "days_ago": 5},
            {"forum": "PM Weekly Forum", "title": "ERP Modernization: AI-First Approach", "snippet": "Discussion thread on taking an AI-first approach to ERP modernization...", "days_ago": 7},
            {"forum": "Product Coalition", "title": "AMA: Building AI Products at Scale", "snippet": "Ask Me Anything session with PM leaders from major tech companies...", "days_ago": 10}
        ]
        
        items = []
        for idx, disc in enumerate(simulated_discussions[:limit]):
            disc_time = datetime.now() - timedelta(days=disc['days_ago'])
            
            items.append(ContentItem(
                id=f"forum_sim_{idx}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                topic=disc['title'],
                source_name=disc['forum'],
                source_url=f"https://{disc['forum'].lower().replace(' ', '')}.com/discussion/{idx}",
                content_type="Text",
                date=disc_time.strftime("%Y-%m-%d"),
                timestamp=disc_time.strftime("%H:%M:%S"),
                snippet=disc['snippet'],
                keywords=self.extract_keywords(disc['title'] + " " + disc['snippet'])
            ))
        
        return items


class TrendDiscoveryAgent:
    """Main agent for discovering trends and collecting content"""
    
    def __init__(self):
        self.collectors = {
            'google_trends': GoogleTrendsCollector(),
            'reddit': RedditCollector(),
            'youtube': YouTubeCollector(),
            'quora': QuoraCollector(),
            'forums': ForumCollector()
        }
        self.all_content: List[ContentItem] = []
        self.all_keywords: List[str] = []
        self.source_metadata: List[Dict] = []
        self.last_discovery_time: Optional[str] = None
        
    def discover(self, query: str = "AI product management", items_per_source: int = 5) -> Dict[str, Any]:
        """Run discovery across all sources"""
        self.all_content = []
        self.all_keywords = []
        self.source_metadata = []
        
        logger.info(f"Starting discovery for query: '{query}'")
        
        for source_name, collector in self.collectors.items():
            try:
                logger.info(f"Fetching from {source_name}...")
                items = collector.fetch(query, items_per_source)
                
                self.all_content.extend(items)
                
                for item in items:
                    self.all_keywords.extend(item.keywords)
                
                self.source_metadata.append({
                    'name': collector.name,
                    'url': f"https://{source_name}.com",
                    'last_fetched': datetime.now().isoformat(),
                    'items_count': len(items),
                    'status': 'success'
                })
                
                logger.info(f"  Fetched {len(items)} items from {source_name}")
                
            except Exception as e:
                logger.error(f"Error fetching from {source_name}: {e}")
                self.source_metadata.append({
                    'name': collector.name,
                    'url': f"https://{source_name}.com",
                    'last_fetched': datetime.now().isoformat(),
                    'items_count': 0,
                    'status': f'error: {str(e)}'
                })
        
        # Deduplicate and count keywords
        keyword_counts = {}
        for kw in self.all_keywords:
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        self.all_keywords = [kw for kw, count in sorted_keywords]
        
        self.last_discovery_time = datetime.now().isoformat()
        
        return self.get_results()
    
    def get_results(self) -> Dict[str, Any]:
        """Get all discovery results"""
        return {
            'content': [item.to_dict() for item in self.all_content],
            'keywords': self.all_keywords,
            'sources': self.source_metadata,
            'stats': {
                'total_items': len(self.all_content),
                'unique_sources': len(self.source_metadata),
                'total_keywords': len(self.all_keywords),
                'last_updated': self.last_discovery_time
            }
        }
    
    def filter_by_keyword(self, keyword: str) -> List[ContentItem]:
        """Filter content by a specific keyword"""
        return [
            item for item in self.all_content
            if keyword.lower() in [kw.lower() for kw in item.keywords] or
               keyword.lower() in item.topic.lower() or
               keyword.lower() in item.snippet.lower()
        ]
    
    def get_keyword_clusters(self) -> Dict[str, List[str]]:
        """Group keywords into clusters"""
        clusters = {
            'AI & Machine Learning': [],
            'Product Management': [],
            'ERP & Enterprise': [],
            'Agile & Process': [],
            'Analytics & Metrics': [],
            'Other': []
        }
        
        ai_terms = ['ai', 'artificial', 'machine', 'learning', 'llm', 'gpt', 'nlp', 'neural', 'deep']
        pm_terms = ['product', 'manager', 'roadmap', 'feature', 'user', 'stakeholder', 'requirements']
        erp_terms = ['erp', 'sap', 'oracle', 'enterprise', 'integration', 'dynamics', 'netsuite']
        agile_terms = ['agile', 'scrum', 'sprint', 'kanban', 'backlog', 'story']
        analytics_terms = ['analytics', 'metrics', 'kpi', 'dashboard', 'data', 'insight']
        
        for keyword in self.all_keywords:
            kw_lower = keyword.lower()
            
            if any(term in kw_lower for term in ai_terms):
                clusters['AI & Machine Learning'].append(keyword)
            elif any(term in kw_lower for term in pm_terms):
                clusters['Product Management'].append(keyword)
            elif any(term in kw_lower for term in erp_terms):
                clusters['ERP & Enterprise'].append(keyword)
            elif any(term in kw_lower for term in agile_terms):
                clusters['Agile & Process'].append(keyword)
            elif any(term in kw_lower for term in analytics_terms):
                clusters['Analytics & Metrics'].append(keyword)
            else:
                clusters['Other'].append(keyword)
        
        return {k: v for k, v in clusters.items() if v}


if __name__ == "__main__":
    agent = TrendDiscoveryAgent()
    results = agent.discover("AI product management", items_per_source=3)
    print(f"Total items: {results['stats']['total_items']}")
    print(f"Keywords: {results['keywords'][:10]}")
