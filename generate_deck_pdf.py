"""
Generates a professional presentation PDF deck for the Snowflake CoCo CLI Hackathon submission.
"""
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(colors.HexColor("#00E5FF"))
        # Top banner accent
        self.rect(0, 590, 792, 22, fill=True, stroke=False)
        self.setFillColor(colors.HexColor("#0B0F19"))
        self.drawString(20, 597, "SNOWFLAKE CoCo CLI HACKATHON 2026 | SUBMISSION DECK")
        
        # Footer
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(20, 15, "EquiSaaS BD — Intelligent Workflow Automation Agents")
        self.drawRightString(772, 15, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def create_presentation_pdf(output_path="submission_deck.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=30,
        rightMargin=30,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0B0F19"),
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitle',
        fontName='Helvetica',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0088CC"),
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        'Heading2',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0B0F19"),
        spaceBefore=10,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=15,
        spaceAfter=4
    )

    story = []

    # SLIDE 1: Title & Overview
    story.append(Paragraph("Snowflake CoCo CLI Enterprise SupplyGuard Agent", title_style))
    story.append(Paragraph("Category: <b>Intelligent Workflow Automation Agents</b> | Team: <b>EquiSaaS BD</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#00E5FF"), spaceAfter=15))
    
    story.append(Paragraph("<b>Executive Overview:</b>", h2_style))
    story.append(Paragraph("Global supply chains suffer millions in losses due to unexpected shipping delays, vendor lead-time anomalies, and unmonitored stockout risks. Traditional BI tools only alert after line stoppage occurs.", body_style))
    story.append(Paragraph("Our solution, <b>Cortex-SupplyGuard</b>, leverages <b>Snowflake CoCo CLI Agent Skills</b> to autonomously scan enterprise warehouse data, synthesize unstructured incident logs using Snowflake Cortex AI, and execute policy-bounded transactional mitigations in seconds.", body_style))
    
    story.append(Spacer(1, 10))
    table_data = [
        ["Key Business Metric", "Traditional Manual Process", "Autonomous CoCo Agent"],
        ["Resolution Time (MTTR)", "2 - 5 Days of manual triage", "<b>Instant (< 3 Seconds)</b>"],
        ["Stockout Prevention", "Reactive after production halt", "<b>100% Proactive Buffer Reroute</b>"],
        ["Quantified Risk Avoided", "High financial leakage", "<b>$200,000+ per incident</b>"],
        ["Governance & Policy", "Prone to manual oversight", "<b>100% Auditable Ledger</b>"]
    ]
    t1 = Table(table_data, colWidths=[200, 260, 270])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t1)
    story.append(PageBreak())

    # SLIDE 2: 3 CoCo Agent Skills Architecture
    story.append(Paragraph("Modular CoCo Agent Skills Architecture", title_style))
    story.append(Paragraph("Built using standardized <code>SKILL.md</code> CoCo specification format", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#00E5FF"), spaceAfter=15))

    skill_table_data = [
        ["Skill Name & Directory", "Role & Capabilities", "Input / Output Schema"],
        [
            "<b>data-anomaly-detector</b><br/><font size=8 color='#64748B'>skills/data_anomaly_detector/</font>",
            "• Autonomous structured warehouse data scan<br/>• Lead-time delay & burn rate analysis<br/>• Composite risk scoring (0-100)",
            "<b>In:</b> Warehouse tables<br/><b>Out:</b> Prioritized anomaly list with severity (CRITICAL, WARNING)"
        ],
        [
            "<b>cortex-reasoner</b><br/><font size=8 color='#64748B'>skills/cortex_reasoner/</font>",
            "• Snowflake Cortex AI multi-modal reasoning<br/>• Synthesizes unstructured incident logs (emails, weather)<br/>• Root-cause analysis & $ loss estimation",
            "<b>In:</b> Anomaly metrics + incident logs<br/><b>Out:</b> Synthesized root cause & 2-3 mitigation options"
        ],
        [
            "<b>action-executor</b><br/><font size=8 color='#64748B'>skills/action_executor/</font>",
            "• Enforces policy guardrails (<$50k auto-approve)<br/>• Issues emergency POs & updates stock<br/>• Immutable audit trail logging",
            "<b>In:</b> Selected option + policy budget<br/><b>Out:</b> Transaction status & PO audit record"
        ]
    ]
    t2 = Table(skill_table_data, colWidths=[200, 300, 230])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0088CC")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # SLIDE 3: End-to-End Multi-Step Orchestration & Interfaces
    story.append(Paragraph("Multi-Step Orchestration & User Interfaces", title_style))
    story.append(Paragraph("Stateful execution engine, interactive CLI, and Glassmorphism Web Dashboard", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#00E5FF"), spaceAfter=15))

    story.append(Paragraph("<b>Stateful Workflow Execution Flow:</b>", h2_style))
    story.append(Paragraph("1. <b>Data Ingestion:</b> Skill 1 scans Snowflake warehouse inventory for critical lead-time anomalies.", bullet_style))
    story.append(Paragraph("2. <b>Cortex Reasoning:</b> Skill 2 fuses metrics with unstructured logistics logs via Snowflake Cortex AI to synthesize root causes.", bullet_style))
    story.append(Paragraph("3. <b>Decision Branching:</b> Policy engine evaluates budget thresholds (Auto-Approve < $50,000 vs Human Escalation >= $50,000).", bullet_style))
    story.append(Paragraph("4. <b>Action & Audit:</b> Skill 3 issues emergency POs, updates warehouse buffer stock, and records audit trail.", bullet_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Dual User Interfaces Included:</b>", h2_style))
    
    ui_data = [
        ["Interface Mode", "Features & Capability", "Execution Command"],
        ["<b>Rich Interactive CLI</b>", "ANSI tables, step progress bars, trace logs, interactive query prompt", "<code>python main.py --demo</code> / <code>run_demo.bat</code>"],
        ["<b>Glassmorphism Web UI</b>", "Live metric cards, interactive DAG animation, real-time reasoning console, audit ledger", "<code>python main.py --web</code> / <code>run_web_dashboard.bat</code>"]
    ]
    t3 = Table(ui_data, colWidths=[160, 370, 200])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t3)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF slide deck at: {output_path}")

if __name__ == "__main__":
    create_presentation_pdf()
