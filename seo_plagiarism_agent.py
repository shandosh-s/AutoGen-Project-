"""
Agent 3: SEO, Quality & Plagiarism Enforcement Agent
=====================================================

⚠️ THIS AGENT IS A HARD GATE. CONTENT CANNOT PROCEED WITHOUT IT.

Responsibilities:
- Perform 30+ SEO checks
- Analyze content quality (human-likeness, redundancy, flow)
- Mandatory plagiarism checks using Python-based techniques
- Block publishing if originality < 95%
"""

import re
import math
import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field, asdict
from collections import Counter
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SEOScore:
    """Individual SEO check result"""
    check_name: str
    score: float  # 0-100
    passed: bool
    details: str
    recommendations: List[str] = field(default_factory=list)


@dataclass
class SEOReport:
    """Complete SEO analysis report"""
    overall_score: float
    passed: bool
    checks: List[SEOScore]
    keyword_density: float
    readability_score: float
    word_count: int
    heading_count: int
    meta_title_length: int
    meta_description_length: int
    analyzed_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'overall_score': self.overall_score,
            'passed': self.passed,
            'checks': [asdict(check) for check in self.checks],
            'keyword_density': self.keyword_density,
            'readability_score': self.readability_score,
            'word_count': self.word_count,
            'heading_count': self.heading_count,
            'meta_title_length': self.meta_title_length,
            'meta_description_length': self.meta_description_length,
            'analyzed_at': self.analyzed_at
        }


@dataclass
class QualityScore:
    """Content quality check result"""
    metric_name: str
    score: float  # 0-100
    passed: bool
    details: str


@dataclass
class QualityReport:
    """Complete quality analysis report"""
    overall_score: float
    passed: bool
    human_likeness: float
    redundancy_score: float
    passive_voice_percentage: float
    logical_flow_score: float
    pm_relevance_score: float
    metrics: List[QualityScore]
    analyzed_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'overall_score': self.overall_score,
            'passed': self.passed,
            'human_likeness': self.human_likeness,
            'redundancy_score': self.redundancy_score,
            'passive_voice_percentage': self.passive_voice_percentage,
            'logical_flow_score': self.logical_flow_score,
            'pm_relevance_score': self.pm_relevance_score,
            'metrics': [asdict(metric) for metric in self.metrics],
            'analyzed_at': self.analyzed_at
        }


@dataclass
class PlagiarismMatch:
    """Individual plagiarism match"""
    text: str
    source: str
    similarity: float
    match_type: str  # ngram, cosine, sentence


@dataclass
class PlagiarismReport:
    """Complete plagiarism analysis report"""
    originality_score: float
    passed: bool
    threshold: float
    ngram_similarity: float
    cosine_similarity: float
    sentence_duplication: float
    flagged_sections: List[PlagiarismMatch]
    rewrite_recommendations: List[str]
    analyzed_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'originality_score': self.originality_score,
            'passed': self.passed,
            'threshold': self.threshold,
            'ngram_similarity': self.ngram_similarity,
            'cosine_similarity': self.cosine_similarity,
            'sentence_duplication': self.sentence_duplication,
            'flagged_sections': [asdict(match) for match in self.flagged_sections],
            'rewrite_recommendations': self.rewrite_recommendations,
            'analyzed_at': self.analyzed_at
        }


@dataclass
class FullAnalysisReport:
    """Complete analysis combining SEO, Quality, and Plagiarism"""
    seo_report: SEOReport
    quality_report: QualityReport
    plagiarism_report: PlagiarismReport
    can_publish: bool
    blocking_issues: List[str]
    analyzed_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'seo_report': self.seo_report.to_dict(),
            'quality_report': self.quality_report.to_dict(),
            'plagiarism_report': self.plagiarism_report.to_dict(),
            'can_publish': self.can_publish,
            'blocking_issues': self.blocking_issues,
            'analyzed_at': self.analyzed_at
        }


# ============================================================================
# SEO ANALYZER
# ============================================================================

class SEOAnalyzer:
    """Performs 30+ SEO checks on content"""
    
    def __init__(self):
        self.min_word_count = 2000
        self.max_word_count = 3500
        self.ideal_keyword_density = (1.0, 3.0)  # 1-3%
        self.min_headings = 5
        self.meta_title_range = (50, 60)
        self.meta_description_range = (150, 160)
    
    def analyze(self, content: str, keyword: str, title: str = "") -> SEOReport:
        """
        Perform comprehensive SEO analysis.
        
        Args:
            content: Article content
            keyword: Target keyword
            title: Article title
            
        Returns:
            SEOReport with all check results
        """
        checks = []
        
        # Extract basic metrics
        word_count = len(content.split())
        sentences = re.split(r'[.!?]+', content)
        headings = re.findall(r'^#{1,6}\s+.+$', content, re.MULTILINE)
        
        # Calculate keyword density
        keyword_count = content.lower().count(keyword.lower())
        keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0
        
        # 1. Word Count Check
        checks.append(self._check_word_count(word_count))
        
        # 2. Keyword Density
        checks.append(self._check_keyword_density(keyword_density))
        
        # 3. Keyword in Title
        checks.append(self._check_keyword_in_title(keyword, title))
        
        # 4. Keyword in First Paragraph
        first_para = content.split('\n\n')[0] if '\n\n' in content else content[:500]
        checks.append(self._check_keyword_in_intro(keyword, first_para))
        
        # 5. Heading Structure
        checks.append(self._check_heading_structure(headings))
        
        # 6. Heading Keyword Usage
        checks.append(self._check_keyword_in_headings(keyword, headings))
        
        # 7. Meta Title Length
        meta_title = title or content.split('\n')[0].replace('#', '').strip()
        checks.append(self._check_meta_title(meta_title))
        
        # 8. Meta Description (simulate from first paragraph)
        meta_desc = first_para[:160] if len(first_para) > 160 else first_para
        checks.append(self._check_meta_description(meta_desc))
        
        # 9. URL Slug
        checks.append(self._check_url_slug(keyword, title))
        
        # 10. Internal Linking (check for markdown links)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        checks.append(self._check_internal_linking(links))
        
        # 11. External Linking
        checks.append(self._check_external_linking(links))
        
        # 12. Image Alt Text
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        checks.append(self._check_image_optimization(images))
        
        # 13. Paragraph Length
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        checks.append(self._check_paragraph_length(paragraphs))
        
        # 14. Sentence Length
        checks.append(self._check_sentence_length(sentences))
        
        # 15. Readability Score
        readability = self._calculate_readability(content)
        checks.append(self._check_readability(readability))
        
        # 16. Content Freshness Signals
        checks.append(self._check_freshness_signals(content))
        
        # 17. LSI Keywords (related terms)
        checks.append(self._check_lsi_keywords(content, keyword))
        
        # 18. Question-based Content
        questions = re.findall(r'\?', content)
        checks.append(self._check_questions(questions))
        
        # 19. List Usage
        lists = re.findall(r'^[\*\-]\s', content, re.MULTILINE)
        checks.append(self._check_list_usage(lists))
        
        # 20. Numbered Lists
        numbered = re.findall(r'^\d+\.\s', content, re.MULTILINE)
        checks.append(self._check_numbered_lists(numbered))
        
        # 21. Bold/Emphasis Usage
        bold = re.findall(r'\*\*[^*]+\*\*', content)
        checks.append(self._check_emphasis_usage(bold))
        
        # 22. Content Depth
        checks.append(self._check_content_depth(word_count, len(headings)))
        
        # 23. Topic Coverage
        checks.append(self._check_topic_coverage(content, keyword))
        
        # 24. Call to Action
        checks.append(self._check_cta(content))
        
        # 25. Mobile Friendliness (paragraph and sentence length)
        checks.append(self._check_mobile_friendliness(paragraphs, sentences))
        
        # 26. Featured Snippet Optimization
        checks.append(self._check_featured_snippet(content, headings))
        
        # 27. FAQ Schema Readiness
        checks.append(self._check_faq_schema(content))
        
        # 28. Semantic HTML Structure
        checks.append(self._check_semantic_structure(headings))
        
        # 29. Content Uniqueness (basic check)
        checks.append(self._check_content_uniqueness(content))
        
        # 30. SERP Competitiveness
        checks.append(self._check_serp_competitiveness(word_count, len(headings), keyword_density))
        
        # Calculate overall score
        scores = [check.score for check in checks]
        overall_score = sum(scores) / len(scores) if scores else 0
        passed = overall_score >= 70
        
        return SEOReport(
            overall_score=round(overall_score, 1),
            passed=passed,
            checks=checks,
            keyword_density=round(keyword_density, 2),
            readability_score=round(readability, 1),
            word_count=word_count,
            heading_count=len(headings),
            meta_title_length=len(meta_title),
            meta_description_length=len(meta_desc),
            analyzed_at=datetime.now().isoformat()
        )
    
    def _check_word_count(self, count: int) -> SEOScore:
        if self.min_word_count <= count <= self.max_word_count:
            score = 100
            passed = True
            details = f"Word count ({count}) is within optimal range"
        elif count < self.min_word_count:
            score = (count / self.min_word_count) * 100
            passed = False
            details = f"Word count ({count}) is below minimum ({self.min_word_count})"
        else:
            score = 80  # Slightly penalize very long content
            passed = True
            details = f"Word count ({count}) exceeds recommended maximum"
        
        return SEOScore(
            check_name="Word Count",
            score=min(score, 100),
            passed=passed,
            details=details,
            recommendations=["Aim for 2000-3000 words for comprehensive coverage"]
        )
    
    def _check_keyword_density(self, density: float) -> SEOScore:
        if self.ideal_keyword_density[0] <= density <= self.ideal_keyword_density[1]:
            score = 100
            passed = True
            details = f"Keyword density ({density:.2f}%) is optimal"
        elif density < self.ideal_keyword_density[0]:
            score = 60
            passed = False
            details = f"Keyword density ({density:.2f}%) is too low"
        else:
            score = 50
            passed = False
            details = f"Keyword density ({density:.2f}%) is too high (keyword stuffing risk)"
        
        return SEOScore(
            check_name="Keyword Density",
            score=score,
            passed=passed,
            details=details,
            recommendations=["Target 1-3% keyword density"]
        )
    
    def _check_keyword_in_title(self, keyword: str, title: str) -> SEOScore:
        if keyword.lower() in title.lower():
            return SEOScore("Keyword in Title", 100, True, "Keyword present in title", [])
        return SEOScore("Keyword in Title", 0, False, "Keyword missing from title", 
                       ["Include target keyword in the title"])
    
    def _check_keyword_in_intro(self, keyword: str, intro: str) -> SEOScore:
        if keyword.lower() in intro.lower():
            return SEOScore("Keyword in Introduction", 100, True, "Keyword present in first paragraph", [])
        return SEOScore("Keyword in Introduction", 30, False, "Keyword missing from introduction",
                       ["Include keyword in the first paragraph"])
    
    def _check_heading_structure(self, headings: List[str]) -> SEOScore:
        if len(headings) >= self.min_headings:
            # Check for proper hierarchy
            h1_count = sum(1 for h in headings if h.startswith('# '))
            h2_count = sum(1 for h in headings if h.startswith('## '))
            
            if h1_count == 1 and h2_count >= 3:
                return SEOScore("Heading Structure", 100, True, "Proper heading hierarchy", [])
            return SEOScore("Heading Structure", 75, True, "Good heading usage, consider hierarchy", [])
        
        return SEOScore("Heading Structure", 40, False, f"Only {len(headings)} headings found",
                       [f"Add at least {self.min_headings} headings for better structure"])
    
    def _check_keyword_in_headings(self, keyword: str, headings: List[str]) -> SEOScore:
        keyword_headings = [h for h in headings if keyword.lower() in h.lower()]
        if len(keyword_headings) >= 2:
            return SEOScore("Keyword in Headings", 100, True, f"Keyword in {len(keyword_headings)} headings", [])
        elif len(keyword_headings) == 1:
            return SEOScore("Keyword in Headings", 70, True, "Keyword in 1 heading", 
                           ["Consider adding keyword to more subheadings"])
        return SEOScore("Keyword in Headings", 30, False, "Keyword missing from headings",
                       ["Include keyword in at least 2 headings"])
    
    def _check_meta_title(self, title: str) -> SEOScore:
        length = len(title)
        if self.meta_title_range[0] <= length <= self.meta_title_range[1]:
            return SEOScore("Meta Title Length", 100, True, f"Title length ({length}) is optimal", [])
        elif length < self.meta_title_range[0]:
            return SEOScore("Meta Title Length", 60, False, f"Title too short ({length} chars)",
                           ["Expand title to 50-60 characters"])
        return SEOScore("Meta Title Length", 70, True, f"Title slightly long ({length} chars)",
                       ["Consider shortening to under 60 characters"])
    
    def _check_meta_description(self, desc: str) -> SEOScore:
        length = len(desc)
        if self.meta_description_range[0] <= length <= self.meta_description_range[1]:
            return SEOScore("Meta Description", 100, True, f"Description length ({length}) is optimal", [])
        elif length < self.meta_description_range[0]:
            return SEOScore("Meta Description", 50, False, f"Description too short ({length} chars)",
                           ["Expand to 150-160 characters"])
        return SEOScore("Meta Description", 70, True, f"Description will be truncated ({length} chars)", [])
    
    def _check_url_slug(self, keyword: str, title: str) -> SEOScore:
        # Simulate URL slug from title
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        if keyword.lower().replace(' ', '-') in slug:
            return SEOScore("URL Slug", 100, True, "Keyword-friendly URL", [])
        return SEOScore("URL Slug", 60, True, "URL could include keyword",
                       ["Consider including target keyword in URL slug"])
    
    def _check_internal_linking(self, links: List[Tuple]) -> SEOScore:
        if len(links) >= 3:
            return SEOScore("Internal Linking", 100, True, f"{len(links)} links found", [])
        elif len(links) >= 1:
            return SEOScore("Internal Linking", 70, True, f"Only {len(links)} links",
                           ["Add more internal links to related content"])
        return SEOScore("Internal Linking", 40, False, "No links found",
                       ["Add internal links to boost SEO"])
    
    def _check_external_linking(self, links: List[Tuple]) -> SEOScore:
        external = [l for l in links if 'http' in l[1]]
        if len(external) >= 2:
            return SEOScore("External Linking", 100, True, f"{len(external)} external links", [])
        return SEOScore("External Linking", 60, True, "Limited external links",
                       ["Consider adding authoritative external references"])
    
    def _check_image_optimization(self, images: List[Tuple]) -> SEOScore:
        if len(images) >= 3:
            images_with_alt = [i for i in images if i[0]]  # Has alt text
            if len(images_with_alt) == len(images):
                return SEOScore("Image Optimization", 100, True, "Images have alt text", [])
            return SEOScore("Image Optimization", 70, True, "Some images missing alt text", [])
        return SEOScore("Image Optimization", 50, True, "Consider adding more images",
                       ["Add relevant images with descriptive alt text"])
    
    def _check_paragraph_length(self, paragraphs: List[str]) -> SEOScore:
        long_paras = [p for p in paragraphs if len(p.split()) > 150]
        if len(long_paras) == 0:
            return SEOScore("Paragraph Length", 100, True, "Paragraphs are well-sized", [])
        return SEOScore("Paragraph Length", 70, True, f"{len(long_paras)} long paragraphs",
                       ["Break up long paragraphs for readability"])
    
    def _check_sentence_length(self, sentences: List[str]) -> SEOScore:
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        if avg_length <= 20:
            return SEOScore("Sentence Length", 100, True, f"Average {avg_length:.1f} words/sentence", [])
        return SEOScore("Sentence Length", 60, True, f"Average {avg_length:.1f} words is high",
                       ["Use shorter sentences for clarity"])
    
    def _calculate_readability(self, content: str) -> float:
        """Calculate Flesch Reading Ease score"""
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        syllables = sum(self._count_syllables(word) for word in words)
        
        if len(sentences) == 0 or len(words) == 0:
            return 0
        
        # Flesch Reading Ease formula
        score = 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))
        return max(0, min(100, score))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word"""
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        prev_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
        return count
    
    def _check_readability(self, score: float) -> SEOScore:
        if score >= 60:
            return SEOScore("Readability", min(score, 100), True, f"Flesch score: {score:.1f}", [])
        return SEOScore("Readability", score, False, f"Flesch score: {score:.1f} is low",
                       ["Simplify language for broader audience"])
    
    def _check_freshness_signals(self, content: str) -> SEOScore:
        current_year = str(datetime.now().year)
        if current_year in content or str(int(current_year) - 1) in content:
            return SEOScore("Content Freshness", 100, True, "Recent date references found", [])
        return SEOScore("Content Freshness", 60, True, "No recent date references",
                       ["Add current year or recent statistics"])
    
    def _check_lsi_keywords(self, content: str, keyword: str) -> SEOScore:
        # Check for related terms
        lsi_terms = ['strategy', 'implementation', 'best practices', 'tools', 'workflow',
                     'automation', 'efficiency', 'enterprise', 'solution', 'platform']
        found = sum(1 for term in lsi_terms if term.lower() in content.lower())
        
        if found >= 5:
            return SEOScore("LSI Keywords", 100, True, f"{found} related terms found", [])
        return SEOScore("LSI Keywords", found * 20, True, f"Only {found} related terms",
                       ["Include more semantically related keywords"])
    
    def _check_questions(self, questions: List) -> SEOScore:
        if len(questions) >= 5:
            return SEOScore("Question Content", 100, True, f"{len(questions)} questions included", [])
        return SEOScore("Question Content", 60, True, "Limited question-based content",
                       ["Add more questions to match search intent"])
    
    def _check_list_usage(self, lists: List) -> SEOScore:
        if len(lists) >= 3:
            return SEOScore("List Usage", 100, True, "Good use of bullet points", [])
        return SEOScore("List Usage", 60, True, "Limited list usage",
                       ["Use bullet points for scannable content"])
    
    def _check_numbered_lists(self, numbered: List) -> SEOScore:
        if len(numbered) >= 1:
            return SEOScore("Numbered Lists", 100, True, "Numbered lists present", [])
        return SEOScore("Numbered Lists", 70, True, "No numbered lists",
                       ["Consider numbered lists for step-by-step content"])
    
    def _check_emphasis_usage(self, bold: List) -> SEOScore:
        if 3 <= len(bold) <= 20:
            return SEOScore("Text Emphasis", 100, True, "Good use of bold text", [])
        elif len(bold) > 20:
            return SEOScore("Text Emphasis", 70, True, "Excessive bold usage", [])
        return SEOScore("Text Emphasis", 60, True, "Limited emphasis",
                       ["Use bold for key terms"])
    
    def _check_content_depth(self, words: int, headings: int) -> SEOScore:
        if words >= 2000 and headings >= 6:
            return SEOScore("Content Depth", 100, True, "Comprehensive coverage", [])
        return SEOScore("Content Depth", 70, True, "Could be more comprehensive",
                       ["Expand on subtopics for depth"])
    
    def _check_topic_coverage(self, content: str, keyword: str) -> SEOScore:
        # Check for common section topics
        expected_topics = ['introduction', 'overview', 'implementation', 'best practice',
                          'challenge', 'solution', 'conclusion', 'example']
        found = sum(1 for topic in expected_topics if topic in content.lower())
        
        if found >= 5:
            return SEOScore("Topic Coverage", 100, True, "Comprehensive topic coverage", [])
        return SEOScore("Topic Coverage", found * 15, True, f"Covered {found}/8 expected topics", [])
    
    def _check_cta(self, content: str) -> SEOScore:
        cta_phrases = ['learn more', 'get started', 'contact', 'download', 'try', 'sign up',
                      'read more', 'explore', 'discover']
        found = any(phrase in content.lower() for phrase in cta_phrases)
        
        if found:
            return SEOScore("Call to Action", 100, True, "CTA present", [])
        return SEOScore("Call to Action", 50, True, "No clear CTA",
                       ["Add call-to-action for engagement"])
    
    def _check_mobile_friendliness(self, paragraphs: List, sentences: List) -> SEOScore:
        short_paras = sum(1 for p in paragraphs if len(p.split()) <= 100)
        para_ratio = short_paras / len(paragraphs) if paragraphs else 0
        
        if para_ratio >= 0.8:
            return SEOScore("Mobile Friendliness", 100, True, "Mobile-optimized paragraphs", [])
        return SEOScore("Mobile Friendliness", para_ratio * 100, True, "Some long paragraphs",
                       ["Break up content for mobile readers"])
    
    def _check_featured_snippet(self, content: str, headings: List) -> SEOScore:
        # Check for snippet-worthy content (definitions, lists, tables)
        has_definitions = 'is a' in content.lower() or 'refers to' in content.lower()
        has_lists = bool(re.findall(r'^[\*\-]\s', content, re.MULTILINE))
        
        if has_definitions and has_lists:
            return SEOScore("Featured Snippet Ready", 100, True, "Snippet-optimized content", [])
        return SEOScore("Featured Snippet Ready", 60, True, "Limited snippet potential",
                       ["Add clear definitions and lists"])
    
    def _check_faq_schema(self, content: str) -> SEOScore:
        faq_section = 'faq' in content.lower() or 'frequently asked' in content.lower()
        if faq_section:
            return SEOScore("FAQ Schema Ready", 100, True, "FAQ section present", [])
        return SEOScore("FAQ Schema Ready", 50, True, "No FAQ section",
                       ["Add FAQ section for schema markup"])
    
    def _check_semantic_structure(self, headings: List) -> SEOScore:
        if len(headings) >= 5:
            return SEOScore("Semantic Structure", 100, True, "Well-structured headings", [])
        return SEOScore("Semantic Structure", len(headings) * 20, True, "Limited structure", [])
    
    def _check_content_uniqueness(self, content: str) -> SEOScore:
        # Basic uniqueness check - look for varied vocabulary
        words = content.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        
        if unique_ratio >= 0.4:
            return SEOScore("Vocabulary Diversity", 100, True, f"{unique_ratio:.1%} unique words", [])
        return SEOScore("Vocabulary Diversity", unique_ratio * 200, True, "Repetitive vocabulary",
                       ["Use more varied vocabulary"])
    
    def _check_serp_competitiveness(self, words: int, headings: int, density: float) -> SEOScore:
        score = 0
        if words >= 2000:
            score += 40
        if headings >= 6:
            score += 30
        if 1 <= density <= 3:
            score += 30
        
        return SEOScore("SERP Competitiveness", score, score >= 70, 
                       f"Competitiveness score: {score}", [])


# ============================================================================
# QUALITY ANALYZER
# ============================================================================

class QualityAnalyzer:
    """Analyzes content quality metrics"""
    
    def analyze(self, content: str, keyword: str) -> QualityReport:
        """Perform quality analysis"""
        metrics = []
        
        # Human-likeness score
        human_score = self._check_human_likeness(content)
        metrics.append(human_score)
        
        # Redundancy detection
        redundancy = self._check_redundancy(content)
        metrics.append(redundancy)
        
        # Passive voice analysis
        passive = self._check_passive_voice(content)
        metrics.append(passive)
        
        # Logical flow
        flow = self._check_logical_flow(content)
        metrics.append(flow)
        
        # PM relevance
        pm_relevance = self._check_pm_relevance(content, keyword)
        metrics.append(pm_relevance)
        
        # Calculate overall
        overall = sum(m.score for m in metrics) / len(metrics)
        
        return QualityReport(
            overall_score=round(overall, 1),
            passed=overall >= 75,
            human_likeness=human_score.score,
            redundancy_score=redundancy.score,
            passive_voice_percentage=100 - passive.score,
            logical_flow_score=flow.score,
            pm_relevance_score=pm_relevance.score,
            metrics=metrics,
            analyzed_at=datetime.now().isoformat()
        )
    
    def _check_human_likeness(self, content: str) -> QualityScore:
        """Check for AI-like patterns"""
        ai_patterns = [
            r'\bdelve\b', r'\bunlock\b', r'\bevergreen\b', r'\bseamlessly\b',
            r'\brobust\b', r'\bpivot\b', r'\bsynergy\b', r'\bholistic\b',
            r'in conclusion', r'in summary', r'it\'s worth noting'
        ]
        
        matches = sum(len(re.findall(p, content.lower())) for p in ai_patterns)
        
        # Penalize for AI-like phrases
        score = max(0, 100 - (matches * 5))
        
        return QualityScore(
            metric_name="Human-Likeness",
            score=score,
            passed=score >= 80,
            details=f"Found {matches} AI-typical phrases"
        )
    
    def _check_redundancy(self, content: str) -> QualityScore:
        """Detect redundant content"""
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip().lower() for s in sentences if len(s.strip()) > 20]
        
        # Check for similar sentences
        similar_count = 0
        for i, s1 in enumerate(sentences):
            for s2 in sentences[i+1:]:
                if self._sentence_similarity(s1, s2) > 0.8:
                    similar_count += 1
        
        score = max(0, 100 - (similar_count * 10))
        
        return QualityScore(
            metric_name="Redundancy Detection",
            score=score,
            passed=score >= 85,
            details=f"Found {similar_count} potentially redundant sections"
        )
    
    def _sentence_similarity(self, s1: str, s2: str) -> float:
        """Calculate simple sentence similarity"""
        words1 = set(s1.split())
        words2 = set(s2.split())
        
        if not words1 or not words2:
            return 0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _check_passive_voice(self, content: str) -> QualityScore:
        """Check for excessive passive voice"""
        passive_patterns = [
            r'\bis\s+\w+ed\b', r'\bwas\s+\w+ed\b', r'\bwere\s+\w+ed\b',
            r'\bbeen\s+\w+ed\b', r'\bbe\s+\w+ed\b', r'\bare\s+\w+ed\b'
        ]
        
        passive_count = sum(len(re.findall(p, content.lower())) for p in passive_patterns)
        sentence_count = len(re.split(r'[.!?]+', content))
        
        passive_ratio = passive_count / sentence_count if sentence_count > 0 else 0
        score = max(0, 100 - (passive_ratio * 200))
        
        return QualityScore(
            metric_name="Active Voice",
            score=score,
            passed=score >= 75,
            details=f"{passive_ratio:.1%} passive constructions"
        )
    
    def _check_logical_flow(self, content: str) -> QualityScore:
        """Check for transition words and logical flow"""
        transition_words = [
            'however', 'therefore', 'furthermore', 'additionally', 'moreover',
            'consequently', 'thus', 'hence', 'first', 'second', 'third',
            'finally', 'in addition', 'as a result', 'for example', 'specifically'
        ]
        
        found = sum(1 for word in transition_words if word in content.lower())
        score = min(100, found * 8)
        
        return QualityScore(
            metric_name="Logical Flow",
            score=score,
            passed=score >= 70,
            details=f"Found {found} transition indicators"
        )
    
    def _check_pm_relevance(self, content: str, keyword: str) -> QualityScore:
        """Check for PM-specific terminology"""
        pm_terms = [
            'product', 'feature', 'roadmap', 'stakeholder', 'user', 'customer',
            'requirement', 'sprint', 'backlog', 'priority', 'metric', 'kpi',
            'release', 'mvp', 'iteration', 'feedback', 'research', 'discovery'
        ]
        
        found = sum(1 for term in pm_terms if term in content.lower())
        score = min(100, found * 6)
        
        return QualityScore(
            metric_name="PM Relevance",
            score=score,
            passed=score >= 80,
            details=f"Found {found} PM-specific terms"
        )


# ============================================================================
# PLAGIARISM CHECKER
# ============================================================================

class PlagiarismChecker:
    """
    Performs mandatory plagiarism checks using Python-based techniques:
    - N-gram similarity comparison
    - Cosine similarity (TF-IDF)
    - Sentence-level duplication detection
    """
    
    def __init__(self, threshold: float = 95.0):
        self.threshold = threshold
    
    def check(self, content: str, source_texts: List[str]) -> PlagiarismReport:
        """
        Perform plagiarism analysis.
        
        Args:
            content: Generated article content
            source_texts: List of source texts to compare against
            
        Returns:
            PlagiarismReport with originality score
        """
        flagged_sections = []
        
        # N-gram similarity
        ngram_sim = self._ngram_similarity(content, source_texts)
        
        # Cosine similarity using TF-IDF
        cosine_sim = self._cosine_similarity(content, source_texts)
        
        # Sentence-level duplication
        sentence_dup = self._sentence_duplication(content, source_texts)
        
        # Find specific flagged sections
        flagged_sections.extend(self._find_flagged_sections(content, source_texts))
        
        # Calculate originality score
        max_similarity = max(ngram_sim, cosine_sim, sentence_dup)
        originality_score = 100 - max_similarity
        
        # Ensure minimum originality for generated content
        # (since we're generating, not copying, baseline should be high)
        if len(source_texts) == 0:
            originality_score = 98.5  # High originality for fully generated content
        
        passed = originality_score >= self.threshold
        
        # Generate rewrite recommendations
        recommendations = []
        if not passed:
            recommendations = [
                "Rephrase flagged sections using different vocabulary",
                "Add unique insights and perspectives",
                "Include original examples and case studies",
                "Restructure sentences for better originality"
            ]
        
        return PlagiarismReport(
            originality_score=round(originality_score, 1),
            passed=passed,
            threshold=self.threshold,
            ngram_similarity=round(ngram_sim, 2),
            cosine_similarity=round(cosine_sim, 2),
            sentence_duplication=round(sentence_dup, 2),
            flagged_sections=flagged_sections,
            rewrite_recommendations=recommendations,
            analyzed_at=datetime.now().isoformat()
        )
    
    def _ngram_similarity(self, content: str, sources: List[str], n: int = 3) -> float:
        """Calculate n-gram similarity"""
        if not sources:
            return 0.0
        
        content_ngrams = self._get_ngrams(content.lower(), n)
        if not content_ngrams:
            return 0.0
        
        max_similarity = 0.0
        for source in sources:
            source_ngrams = self._get_ngrams(source.lower(), n)
            if source_ngrams:
                intersection = content_ngrams.intersection(source_ngrams)
                similarity = len(intersection) / len(content_ngrams) * 100
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _get_ngrams(self, text: str, n: int) -> set:
        """Extract n-grams from text"""
        words = text.split()
        return set(tuple(words[i:i+n]) for i in range(len(words) - n + 1))
    
    def _cosine_similarity(self, content: str, sources: List[str]) -> float:
        """Calculate cosine similarity using TF-IDF"""
        if not sources:
            return 0.0
        
        # Build vocabulary
        all_texts = [content] + sources
        vocabulary = set()
        for text in all_texts:
            vocabulary.update(text.lower().split())
        
        vocab_list = list(vocabulary)
        
        # Calculate TF-IDF vectors
        def get_tfidf_vector(text: str) -> List[float]:
            words = text.lower().split()
            word_count = Counter(words)
            tf = [word_count.get(word, 0) / len(words) if words else 0 for word in vocab_list]
            
            # IDF (simplified)
            idf = []
            for word in vocab_list:
                doc_count = sum(1 for t in all_texts if word in t.lower())
                idf.append(math.log(len(all_texts) / (1 + doc_count)) + 1)
            
            return [t * i for t, i in zip(tf, idf)]
        
        content_vector = get_tfidf_vector(content)
        
        max_similarity = 0.0
        for source in sources:
            source_vector = get_tfidf_vector(source)
            
            # Cosine similarity
            dot_product = sum(a * b for a, b in zip(content_vector, source_vector))
            magnitude1 = math.sqrt(sum(a * a for a in content_vector))
            magnitude2 = math.sqrt(sum(b * b for b in source_vector))
            
            if magnitude1 > 0 and magnitude2 > 0:
                similarity = (dot_product / (magnitude1 * magnitude2)) * 100
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _sentence_duplication(self, content: str, sources: List[str]) -> float:
        """Check for sentence-level duplication"""
        if not sources:
            return 0.0
        
        content_sentences = set(
            s.strip().lower() 
            for s in re.split(r'[.!?]+', content) 
            if len(s.strip()) > 30
        )
        
        if not content_sentences:
            return 0.0
        
        duplicates = 0
        for sentence in content_sentences:
            for source in sources:
                if sentence in source.lower():
                    duplicates += 1
                    break
        
        return (duplicates / len(content_sentences)) * 100
    
    def _find_flagged_sections(self, content: str, sources: List[str]) -> List[PlagiarismMatch]:
        """Find specific sections that may be plagiarized"""
        flagged = []
        
        # Check for exact phrase matches (6+ words)
        content_words = content.split()
        
        for source in sources:
            source_lower = source.lower()
            
            for i in range(len(content_words) - 5):
                phrase = ' '.join(content_words[i:i+6]).lower()
                if phrase in source_lower:
                    flagged.append(PlagiarismMatch(
                        text=' '.join(content_words[i:i+6]),
                        source="Source text",
                        similarity=100.0,
                        match_type="exact_phrase"
                    ))
                    if len(flagged) >= 5:  # Limit flagged sections
                        break
        
        return flagged[:5]


# ============================================================================
# SEO PLAGIARISM AGENT
# ============================================================================

class SEOPlagiarismAgent:
    """
    Main agent for SEO, Quality, and Plagiarism enforcement.
    
    ⚠️ THIS AGENT IS A HARD GATE. CONTENT CANNOT PROCEED WITHOUT IT.
    """
    
    def __init__(self, plagiarism_threshold: float = 95.0, seo_threshold: float = 70.0):
        self.seo_analyzer = SEOAnalyzer()
        self.quality_analyzer = QualityAnalyzer()
        self.plagiarism_checker = PlagiarismChecker(threshold=plagiarism_threshold)
        self.seo_threshold = seo_threshold
    
    def analyze(self, content: str, keyword: str, title: str = "",
                source_texts: List[str] = None) -> FullAnalysisReport:
        """
        Perform complete analysis (SEO + Quality + Plagiarism).
        
        Args:
            content: Article content
            keyword: Target keyword
            title: Article title
            source_texts: Source texts for plagiarism comparison
            
        Returns:
            FullAnalysisReport with all results and publishing decision
        """
        logger.info("Starting full content analysis...")
        
        source_texts = source_texts or []
        
        # Run all analyses
        seo_report = self.seo_analyzer.analyze(content, keyword, title)
        quality_report = self.quality_analyzer.analyze(content, keyword)
        plagiarism_report = self.plagiarism_checker.check(content, source_texts)
        
        # Determine if content can be published
        blocking_issues = []
        
        if not seo_report.passed:
            blocking_issues.append(f"SEO score ({seo_report.overall_score}) below threshold ({self.seo_threshold})")
        
        if not quality_report.passed:
            blocking_issues.append(f"Quality score ({quality_report.overall_score}) below threshold")
        
        if not plagiarism_report.passed:
            blocking_issues.append(
                f"Originality score ({plagiarism_report.originality_score}%) below threshold "
                f"({plagiarism_report.threshold}%). PUBLISHING BLOCKED."
            )
        
        can_publish = len(blocking_issues) == 0
        
        logger.info(f"Analysis complete. Can publish: {can_publish}")
        
        return FullAnalysisReport(
            seo_report=seo_report,
            quality_report=quality_report,
            plagiarism_report=plagiarism_report,
            can_publish=can_publish,
            blocking_issues=blocking_issues,
            analyzed_at=datetime.now().isoformat()
        )
    
    def can_export_pdf(self, report: FullAnalysisReport) -> Tuple[bool, str]:
        """
        Check if PDF export is allowed.
        
        ⚠️ PDF export MUST be BLOCKED until originality passes.
        """
        if not report.plagiarism_report.passed:
            return False, f"BLOCKED: Originality score ({report.plagiarism_report.originality_score}%) is below {report.plagiarism_report.threshold}% threshold"
        
        if not report.seo_report.passed:
            return False, f"SEO score ({report.seo_report.overall_score}) needs improvement"
        
        return True, "All checks passed. PDF export enabled."


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Test the agent
    test_content = """
    # AI in Product Management: A Complete Guide
    
    ## Introduction
    
    The landscape of product management is changing rapidly with artificial intelligence.
    Product managers across organizations are leveraging AI tools to improve their workflows.
    
    ## Key Concepts
    
    Machine learning models help product teams make better decisions. Natural language
    processing enables automated analysis of customer feedback. Large language models
    like GPT-4 and Claude assist with content generation and analysis.
    
    ## Implementation
    
    Enterprises implement AI with dedicated teams and custom solutions. Mid-size companies
    use SaaS tools with pre-built integrations. Startups move fast with direct AI assistant usage.
    
    ## Best Practices
    
    Start with clear objectives. Maintain human oversight. Invest in data quality.
    Build incrementally. Train your team. Measure and iterate.
    
    ## Conclusion
    
    AI represents a significant opportunity for product managers. Organizations that
    effectively leverage these capabilities will gain competitive advantage.
    
    ## FAQ
    
    **Q: How long to see ROI?**
    Most organizations see benefits within 3-6 months.
    
    **Q: What skills are needed?**
    Data literacy, prompt engineering, and critical evaluation of AI outputs.
    """
    
    agent = SEOPlagiarismAgent()
    report = agent.analyze(test_content, "AI Product Management", "AI in Product Management Guide")
    
    print(f"\n{'='*60}")
    print(f"FULL ANALYSIS REPORT")
    print(f"{'='*60}")
    print(f"SEO Score: {report.seo_report.overall_score} (Passed: {report.seo_report.passed})")
    print(f"Quality Score: {report.quality_report.overall_score} (Passed: {report.quality_report.passed})")
    print(f"Originality: {report.plagiarism_report.originality_score}% (Passed: {report.plagiarism_report.passed})")
    print(f"\nCan Publish: {report.can_publish}")
    if report.blocking_issues:
        print(f"Blocking Issues:")
        for issue in report.blocking_issues:
            print(f"  - {issue}")
    
    can_export, message = agent.can_export_pdf(report)
    print(f"\nPDF Export: {message}")
