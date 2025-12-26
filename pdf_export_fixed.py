"""
PDF Export Module - BULLETPROOF v6
==================================
Enhanced error handling for FPDF character rendering issues
"""

import os
import re
import logging
from datetime import datetime
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean(text) -> str:
    """Aggressively clean text - ONLY allow basic ASCII"""
    if text is None:
        return ""
    
    text = str(text)
    
    # Only keep basic printable ASCII (32-126)
    result = ""
    for char in text:
        code = ord(char)
        if 32 <= code <= 126:  # Printable ASCII only
            result += char
        elif char in '\n\r\t':  # Keep basic whitespace
            result += ' '
        else:
            result += ' '  # Replace everything else with space
    
    # Clean up multiple spaces
    result = ' '.join(result.split())
    
    # Extra safety: remove any remaining problematic characters
    result = result.encode('ascii', 'ignore').decode('ascii')
    
    return result.strip()


class PDFGenerator:
    """Simple, robust PDF generator with enhanced error handling"""
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate(self, article: Dict[str, Any], seo_report: Dict[str, Any],
                 quality_report: Dict[str, Any], plagiarism_report: Dict[str, Any],
                 filename: str = None) -> str:
        
        from fpdf import FPDF
        
        # Create filename
        if not filename:
            kw = article.get('keyword', 'article')
            kw = re.sub(r'[^a-zA-Z0-9]', '_', str(kw))[:20]
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{kw}_{ts}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF with explicit settings
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_margins(left=15, top=15, right=15)
        
        # === COVER PAGE ===
        pdf.add_page()
        
        # Title
        pdf.set_font('Helvetica', 'B', 18)
        pdf.set_text_color(30, 60, 100)
        title = clean(article.get('title', 'Article'))[:80]
        if title:  # Only write if not empty
            self._safe_multi_cell(pdf, 0, 10, title, align='C')
        pdf.ln(15)
        
        # Info box
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(60, 60, 60)
        
        info = [
            f"Keyword: {clean(article.get('keyword', 'N/A'))}",
            f"Word Count: {article.get('word_count', 0)}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            f"SEO Score: {seo_report.get('overall_score', 0)}%",
            f"Quality Score: {quality_report.get('overall_score', 0)}%",
            f"Originality: {plagiarism_report.get('originality_score', 0)}%",
        ]
        
        for line in info:
            self._safe_cell(pdf, 0, 7, line, ln=True)
        
        # === EXECUTIVE SUMMARY ===
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(30, 60, 100)
        self._safe_cell(pdf, 0, 10, "Executive Summary", ln=True)
        pdf.ln(3)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(50, 50, 50)
        
        summary = clean(article.get('executive_summary', 'No summary available.'))
        if summary:
            self._write_text(pdf, summary)
        
        # === MAIN SECTIONS ===
        sections = article.get('sections', [])
        
        for section in sections:
            title = clean(section.get('title', ''))
            content = clean(section.get('content', ''))
            
            if not title or not content:
                continue
            
            pdf.add_page()
            
            # Section title
            pdf.set_font('Helvetica', 'B', 13)
            pdf.set_text_color(30, 60, 100)
            self._safe_cell(pdf, 0, 10, title[:60], ln=True)
            pdf.ln(2)
            
            # Section content
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(50, 50, 50)
            self._write_text(pdf, content)
        
        # === FAQ ===
        faq_list = article.get('faq', [])
        if faq_list:
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 14)
            pdf.set_text_color(30, 60, 100)
            self._safe_cell(pdf, 0, 10, "Frequently Asked Questions", ln=True)
            pdf.ln(5)
            
            for i, faq in enumerate(faq_list[:5], 1):
                q = clean(faq.get('question', ''))
                a = clean(faq.get('answer', ''))
                
                if q and a:
                    pdf.set_font('Helvetica', 'B', 10)
                    pdf.set_text_color(30, 60, 100)
                    self._safe_multi_cell(pdf, 0, 6, f"Q{i}: {q[:150]}")
                    
                    pdf.set_font('Helvetica', '', 10)
                    pdf.set_text_color(50, 50, 50)
                    self._safe_multi_cell(pdf, 0, 5, f"A: {a[:300]}")
                    pdf.ln(4)
        
        # === KEY TAKEAWAYS ===
        takeaways = article.get('key_takeaways', [])
        if takeaways:
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(30, 60, 100)
            self._safe_cell(pdf, 0, 8, "Key Takeaways", ln=True)
            pdf.ln(2)
            
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(50, 50, 50)
            
            for i, item in enumerate(takeaways[:7], 1):
                text = clean(item)[:120]
                if text:
                    self._safe_cell(pdf, 0, 6, f"{i}. {text}", ln=True)
        
        # === ORIGINALITY REPORT ===
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(30, 60, 100)
        self._safe_cell(pdf, 0, 10, "Originality Report", ln=True)
        pdf.ln(15)
        
        orig = plagiarism_report.get('originality_score', 0)
        passed = plagiarism_report.get('passed', False)
        
        # Status
        pdf.set_font('Helvetica', 'B', 20)
        if passed:
            pdf.set_text_color(0, 150, 0)
            self._safe_cell(pdf, 0, 12, "STATUS: PASSED", ln=True, align='C')
        else:
            pdf.set_text_color(200, 0, 0)
            self._safe_cell(pdf, 0, 12, "STATUS: FAILED", ln=True, align='C')
        
        # Score
        pdf.set_font('Helvetica', 'B', 40)
        self._safe_cell(pdf, 0, 25, f"{orig}%", ln=True, align='C')
        
        # Details
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(80, 80, 80)
        pdf.ln(10)
        self._safe_cell(pdf, 0, 7, f"Required Threshold: {plagiarism_report.get('threshold', 80)}%", ln=True, align='C')
        pdf.ln(10)
        
        self._safe_cell(pdf, 0, 7, f"N-gram Similarity: {plagiarism_report.get('ngram_similarity', 0)}%", ln=True)
        self._safe_cell(pdf, 0, 7, f"Cosine Similarity: {plagiarism_report.get('cosine_similarity', 0)}%", ln=True)
        self._safe_cell(pdf, 0, 7, f"Sentence Duplication: {plagiarism_report.get('sentence_duplication', 0)}%", ln=True)
        
        # Footer
        pdf.ln(20)
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(150, 150, 150)
        self._safe_cell(pdf, 0, 5, "Generated by AI for Product Managers", ln=True, align='C')
        self._safe_cell(pdf, 0, 5, "Powered by Microsoft AutoGen", ln=True, align='C')
        
        # Save PDF
        pdf.output(filepath)
        logger.info(f"PDF created: {filepath}")
        
        return filepath
    
    def _safe_cell(self, pdf, w, h, txt='', border=0, ln=0, align='', fill=False):
        """Safely write a cell with error handling"""
        try:
            txt = clean(str(txt))
            if not txt:
                txt = " "
            pdf.cell(w, h, txt, border, ln, align, fill)
        except Exception as e:
            logger.warning(f"Cell write error: {e}. Trying fallback.")
            try:
                # Fallback: write simplified text
                pdf.cell(w, h, "[content]", border, ln, align, fill)
            except:
                # Last resort: just move to next line
                if ln:
                    pdf.ln(h)
    
    def _safe_multi_cell(self, pdf, w, h, txt='', border=0, align='L', fill=False):
        """Safely write a multi_cell with error handling"""
        try:
            txt = clean(str(txt))
            if not txt:
                txt = " "
            pdf.multi_cell(w, h, txt, border, align, fill)
        except Exception as e:
            logger.warning(f"Multi-cell write error: {e}. Trying fallback.")
            try:
                # Fallback: write simplified text
                pdf.multi_cell(w, h, "[content unavailable]", border, align, fill)
            except:
                # Last resort: skip this content
                pdf.ln(h)
    
    def _write_text(self, pdf, text: str):
        """Write text in manageable chunks with error handling"""
        text = clean(text).strip()
        
        if not text:
            return
        
        # Split into smaller chunks (max 800 chars each)
        while len(text) > 0:
            chunk = text[:800]
            text = text[800:]
            
            # Find a good break point
            if text and len(chunk) == 800:
                last_space = chunk.rfind(' ')
                if last_space > 600:
                    text = chunk[last_space:] + text
                    chunk = chunk[:last_space]
            
            chunk = clean(chunk)
            if chunk:
                self._safe_multi_cell(pdf, 0, 5, chunk)
                pdf.ln(2)


class ExportManager:
    """Export manager with plagiarism gate"""
    
    def __init__(self, output_dir: str = "exports"):
        self.pdf_generator = PDFGenerator(output_dir)
        self.output_dir = output_dir
    
    def can_export(self, plagiarism_report: Dict) -> tuple:
        orig = plagiarism_report.get('originality_score', 0)
        threshold = plagiarism_report.get('threshold', 80)
        
        if orig < threshold:
            return False, f"Blocked: {orig}% below {threshold}%"
        return True, "Ready"
    
    def export_pdf(self, article: Dict, analysis_report: Dict) -> tuple:
        plag = analysis_report.get('plagiarism_report', {})
        
        can, msg = self.can_export(plag)
        if not can:
            return False, msg
        
        try:
            path = self.pdf_generator.generate(
                article=article,
                seo_report=analysis_report.get('seo_report', {}),
                quality_report=analysis_report.get('quality_report', {}),
                plagiarism_report=plag
            )
            return True, path
        except Exception as e:
            logger.error(f"PDF export error: {e}", exc_info=True)
            return False, f"Error: {str(e)}"
    
    def get_export_status(self, analysis_report: Dict) -> Dict:
        plag = analysis_report.get('plagiarism_report', {})
        seo = analysis_report.get('seo_report', {})
        qual = analysis_report.get('quality_report', {})
        
        can, msg = self.can_export(plag)
        
        return {
            'can_export': can,
            'message': msg,
            'originality_score': plag.get('originality_score', 0),
            'originality_threshold': plag.get('threshold', 80),
            'seo_passed': seo.get('passed', False),
            'quality_passed': qual.get('passed', False),
            'plagiarism_passed': plag.get('passed', False),
        }