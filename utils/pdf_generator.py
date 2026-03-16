from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.units import inch

class ResumePDF:
    def __init__(self, data, template_id="template1"):
        self.data = data
        self.template_id = template_id
        self.styles = getSampleStyleSheet()

    def generate(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=LETTER)
        story = []

        if self.template_id == "template1":
            self._render_template1(story)
        elif self.template_id == "template2":
            self._render_template2(story)
        else:
            self._render_template1(story) # Default

        doc.build(story)

    def _render_template1(self, story):
        # Professional Modern
        header_style = ParagraphStyle(
            'Header',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor("#4f46e5"),
            spaceAfter=10
        )
        
        story.append(Paragraph(self.data.get('full_name', 'No Name'), header_style))
        contact = f"{self.data.get('email')} | {self.data.get('phone')} | {self.data.get('address')}"
        story.append(Paragraph(contact, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        story.append(Paragraph("Professional Summary", self.styles['Heading2']))
        story.append(Paragraph(self.data.get('summary', ''), self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Skills
        story.append(Paragraph("Skills", self.styles['Heading2']))
        skills_text = ", ".join(self.data.get('skills', []))
        story.append(Paragraph(skills_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

    def _render_template2(self, story):
        # Clean Minimalist
        header_style = ParagraphStyle(
            'Header',
            parent=self.styles['Heading1'],
            fontSize=22,
            alignment=1, # Center
            spaceAfter=12
        )
        story.append(Paragraph(self.data.get('full_name', '').upper(), header_style))
        story.append(Paragraph(f"{self.data.get('email')} • {self.data.get('phone')}", ParagraphStyle('Sub', alignment=1)))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("SUMMARY", self.styles['Heading3']))
        story.append(Paragraph(self.data.get('summary', ''), self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

        story.append(Paragraph("CORE SKILLS", self.styles['Heading3']))
        story.append(Paragraph(", ".join(self.data.get('skills', [])), self.styles['Normal']))
