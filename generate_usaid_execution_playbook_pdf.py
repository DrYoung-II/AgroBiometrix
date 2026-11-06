"""
AgroBiometrix USAID DIV Post-Award Master Operational Playbook Generator (Expanded Edition)
Generates a comprehensive, publication-grade executive technical roadmap (PDF)
detailing the exact start-to-finish execution of the USAID DIV Stage 1 Award ($150,000 / 24 Months),
now including the exhaustive Step-by-Step SAM.gov & NCAGE Registration Guide for Nigerian Organizations.
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "AgroBiometrix_USAID_DIV_Post_Award_Execution_Master_Playbook.pdf"
DOCX_FILENAME = "AgroBiometrix_USAID_DIV_Post_Award_Execution_Master_Playbook.docx"

ARTIFACT_DIRS = [
    r"C:\Users\USER\.gemini\antigravity\brain\d802ae47-5651-4f17-a2ea-7d8c7b8085d8",
    r"C:\Users\USER\.gemini\antigravity\brain\1e91af0e-0faf-4a71-9df3-64f967526da0"
]


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute total page count and draw running headers/footers."""
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
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0D47A1"))  # USAID Blue
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "USAID DIV STAGE 1 POST-AWARD MASTER OPERATIONAL PLAYBOOK")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(558, 755, "AgroBiometrix Consortium • $150,000 Implementation & SAM.gov Guide")
            self.setStrokeColor(colors.HexColor("#90CAF9"))
            self.setLineWidth(0.7)
            self.line(54, 748, 558, 748)
            
        # Footer (all pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#1B5E20"))
        self.drawString(54, 34, "AgroBiometrix Research & Engineering Consortium • Confidential Strategic Playbook")
        self.drawRightString(558, 34, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 44, 558, 44)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Colors
    usaid_blue = colors.HexColor("#002F6C")       # Deep USAID Navy
    usaid_red = colors.HexColor("#BA0C2F")        # USAID Red
    forest_green = colors.HexColor("#1B5E20")     # AgroBiometrix Primary
    leaf_green = colors.HexColor("#2E7D32")
    pale_blue_bg = colors.HexColor("#F0F4F8")
    pale_green_bg = colors.HexColor("#F1F8F2")
    border_gray = colors.HexColor("#CFD8DC")
    text_dark = colors.HexColor("#212121")
    text_muted = colors.HexColor("#546E7A")

    header_stamp_style = ParagraphStyle(
        'HeaderStamp',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=usaid_red,
        spaceAfter=2
    )

    doc_title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14.5,
        leading=18.5,
        textColor=usaid_blue,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.0,
        textColor=forest_green,
        spaceAfter=3
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=10.5,
        textColor=text_muted,
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=usaid_blue,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.0,
        leading=12.0,
        textColor=forest_green,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=11.0,
        textColor=text_dark,
        spaceAfter=3.5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=text_dark,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=9.2,
        textColor=text_dark
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.4,
        leading=9.5,
        textColor=colors.white
    )

    callout_text_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.5,
        textColor=colors.HexColor("#0D3311")
    )

    def make_callout(title, body_text, bg_color=pale_green_bg, border_color=forest_green):
        content = [
            Paragraph(f"<b>{title}</b>", ParagraphStyle('CalloutT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.0, leading=10.2, textColor=border_color)),
            Spacer(1, 2),
            Paragraph(body_text, callout_text_style)
        ]
        t = Table([[content]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('BOX', (0, 0), (-1, -1), 0.8, border_color),
            ('PADDING', (0, 0), (-1, -1), 4.5),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ]))
        return t

    story = []

    # -------------------------------------------------------------
    # HEADER BANNER & METADATA
    # -------------------------------------------------------------
    story.append(Paragraph("USAID DEVELOPMENT INNOVATION VENTURES (DIV) • POST-AWARD IMPLEMENTATION DIRECTIVE", header_stamp_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=usaid_blue, spaceAfter=5, spaceBefore=2))
    
    story.append(Paragraph("What to Do When You Win the USAID DIV Fund: The Complete Technical, Financial, and Operational Roadmap (Start-to-Finish)", doc_title_style))
    story.append(Paragraph("<b>AgroBiometrix Implementation Protocol:</b> A 24-Month Master Execution Plan from Award Negotiation to DIV Stage 2 ($1.5M) Scale-Up", subtitle_style))
    
    meta_info = (
        "<b>Award Mechanism</b>: USAID DIV Stage 1 Proof of Concept ($150,000 / 24 Months) • <b>Target Reach</b>: 10,000+ Smallholders<br/>"
        "<b>Lead Implementing Organization</b>: AgroBiometrix Engineering Unit / Naysa-84 Labs in consortium with FUNAAB, OOU, FPI, and UGA<br/>"
        "<b>Principal Investigator / Project Director</b>: Dr. Young Imienwain Irivboje (FUNAAB / Naysa-84 Labs)<br/>"
        "<b>NATO CAGE (NCAGE) Code</b>: <b>STZZ1</b> (Active on NATO NSPA Portal) • <b>Fiscal Year End</b>: December 31 (12/31)<br/>"
        "<b>SAM.gov Entity Validation Incident ID</b>: <b>INC-GSAFSD21864803</b> (Documentation Submitted, 1.5–3.5 Business Days Review)"
    )
    story.append(Paragraph(meta_info, meta_style))
    story.append(Spacer(1, 3))

    # -------------------------------------------------------------
    # EXECUTIVE SUMMARY CALLOUT
    # -------------------------------------------------------------
    callout_summary = (
        "<b>The Fundamental Philosophy of USAID DIV:</b> Winning a USAID DIV grant is fundamentally different from receiving traditional donor aid or charity. "
        "DIV operates as an <b>evidence-driven venture fund</b> within the US Government. USAID is investing $150,000 into AgroBiometrix to answer one decisive question: "
        "<i>'Can an Africa-first, sovereign biometrical operating system with last-mile vernacular voice dissemination produce statistically verified yield and revenue gains among smallholders at a dramatically lower unit cost than traditional extension?'</i><br/>"
        "If you prove this with gold-standard causal evidence (Difference-in-Differences), rigorous unit economics ($0.02 radio / $0.20 voice robocall), and operational fidelity, "
        "AgroBiometrix unlocks the gateway to <b>USAID DIV Stage 2 ($1,500,000)</b> and nationwide government adoption. This master playbook defines your exact roadmap from Day 1 to Month 24."
    )
    story.append(make_callout("EXECUTIVE MANDATE: TURNING $150K SEED EVIDENCE INTO A $1.5M SCALING ENGINE", callout_summary, pale_blue_bg, usaid_blue))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 1: PRE-AWARD DUE DILIGENCE & NEGOTIATION
    # -------------------------------------------------------------
    story.append(Paragraph("Phase 0: Pre-Award Due Diligence & Negotiation (Months -2 to 0 / Post-Notification)", h1_style))
    story.append(Paragraph(
        "Upon receiving notification of selection from the DIV Agreement Officer (AO), the formal negotiation and pre-award compliance phase commences. This phase typically spans 60 to 90 days before initial funds are disbursed.",
        body_style
    ))
    story.append(Paragraph("<b>Key Action Items & Requirements:</b>", h2_style))
    story.append(Paragraph("• <b>SAM.gov & Unique Entity Identifier (UEI) Validation</b>: Ensure active registration on the US Government System for Award Management (SAM.gov). Naysa-84 / AgroBiometrix must maintain valid NCAGE and UEI codes.", bullet_style))
    story.append(Paragraph("• <b>Non-US Organization Pre-Award Survey (NUPAS) / Financial Risk Review</b>: USAID evaluates internal financial management, segregation of duties, procurement policies, and anti-fraud protocols.", bullet_style))
    story.append(Paragraph("• <b>Award Mechanism Selection (Fixed Amount Award vs. Cooperative Agreement)</b>: Stage 1 DIV awards are predominantly structured as <b>Fixed Amount Awards (FAAs)</b>. Under an FAA, disbursements are <i>milestone-based</i> rather than reimbursement-based. You are paid tranches upon verification of delivered milestones (e.g., approved MEL plan, baseline completed, vernacular audio engine deployed).", bullet_style))
    story.append(Paragraph("• <b>Designated Bank Account Establishment</b>: Open a segregated, dedicated institutional bank account (USD and local currency NGN) exclusively for USAID project funds. Never commingle grant funds with personal or general organizational capital.", bullet_style))
    story.append(Paragraph("• <b>Assignment of Key Personnel & Agreement Officer Representative (AOR)</b>: Finalize the formal designation of Dr. Young Irivboje as PI / Project Director and establish weekly communication protocols with your assigned USAID AOR in Washington.", bullet_style))
    story.append(Spacer(1, 4))

    # -------------------------------------------------------------
    # SECTION 1B: STEP-BY-STEP SAM.GOV & NCAGE GUIDE FOR NIGERIAN ORGANIZATIONS
    # -------------------------------------------------------------
    story.append(Paragraph("Special Directive: Step-by-Step SAM.gov & NCAGE Guide for Nigerian Entities", h1_style))
    story.append(Paragraph(
        "Federal regulation (2 CFR Part 25) strictly mandates that foreign recipients of US grants hold an active registration in <b>SAM.gov</b> with a <b>Unique Entity Identifier (UEI)</b>. SAM.gov replaced the legacy DUNS number in April 2022. <b>Registration is 100% free of charge; beware of commercial third-party scams charging $500–$2,500.</b>",
        body_style
    ))

    # NCAGE Field Instructions Table
    ncage_guide_data = [
        [
            Paragraph("<b>Registration Step & Field</b>", table_header_style),
            Paragraph("<b>Exact Input / Action for Naysa-84 Labs / AgroBiometrix</b>", table_header_style),
            Paragraph("<b>Strategic Rationale & Critical Notes</b>", table_header_style)
        ],
        [
            Paragraph("<b>Step 1: NCAGE Code Request</b><br/>(NATO NSPA Portal)<br/><font size='6.0' color='#2E7D32'><b>STATUS: ASSIGNED (STZZ1)</b></font>", table_cell_style),
            Paragraph("• Official NCAGE Code: <b>STZZ1</b> (Active on NATO Codification Directory).<br/>• Verified URL: <code>https://eportal.nspa.nato.int/Codification/CageTool/cage-view/STZZ1</code>.<br/>• Legal Name & Physical Address verified against CAC records.<br/>• ISIC: <code>7210</code> | NAICS: <code>541715</code> (Life Sciences R&D).", table_cell_style),
            Paragraph("<b>Prerequisite Achieved.</b> NATO Support and Procurement Agency has codified the entity. Code STZZ1 is active and ready for entry into SAM.gov for direct US DLA validation.", table_cell_style)
        ],
        [
            Paragraph("<b>Future Business & SAM Question</b><br/>(NCAGE Questionnaires)", table_cell_style),
            Paragraph("• <i>'NCAGE code needed for invitation to tender?'</i> → <b>Select NO</b>.<br/>• <i>'The NCAGE code is requested by SAM?'</i> → <b>Select YES</b>.", table_cell_style),
            Paragraph("Selecting 'Yes' to tender forces you to provide military bid numbers. Selecting 'Yes' to SAM triggers an automated data bridge syncing NATO with the US Defense Logistics Agency (DLA) and SAM.gov.", table_cell_style)
        ],
        [
            Paragraph("<b>Step 2: Login.gov Account</b><br/>(Administrative Credentials)", table_cell_style),
            Paragraph("• Register with dedicated entity email: <code>n84labs@gmail.com</code>.<br/>• Activate Multi-Factor Authentication (Google Authenticator / SMS).<br/>• <b>Record and store the 16-character Emergency Recovery Key.</b>", table_cell_style),
            Paragraph("Entity-dedicated Gmail accounts are fully accepted and prevent administrative lockout when personal or student university email accounts expire. The 16-character key is required if your device is lost.", table_cell_style)
        ],
        [
            Paragraph("<b>Step 3: Document Readiness & Exact-Match Rule</b>", table_cell_style),
            Paragraph("• CAC Certificate of Incorporation / Business Name Registration.<br/>• CAC Status Report / Form CAC 1.1 showing official registered address.<br/>• Official Nigerian Bank Statement or Utility Bill (supplementary if requested).<br/>• Federal Tax Identification Number (TIN) from FIRS.", table_cell_style),
            Paragraph("<b>The Exact-Match Rule:</b> SAM.gov compares inputs against government registries. Discrepancies in spelling, punctuation, or suite numbers trigger manual reviews that cause 3–4 week delays.", table_cell_style)
        ],
        [
            Paragraph("<b>Step 4: SAM.gov Validation & UEI Generation</b><br/><font size='6.0' color='#1565C0'><b>SUBMITTED: INC-GSAFSD21864803</b></font>", table_cell_style),
            Paragraph("• Select: <b>'Financial Assistance Awards Only'</b>; Fiscal Year End: <b>12/31</b>.<br/>• Matched NCAGE: <b>STZZ1</b>; uploaded official CAC incorporation documents.<br/>• Incident Number: <b>INC-GSAFSD21864803</b> submitted for GSA review.<br/>• Turnaround estimate: <b>1.5–3.5 business days</b> to unlock UEI.", table_cell_style),
            Paragraph("Financial Assistance registration is streamlined for grants and cooperative agreements. Documentation is under active review by the GSA Federal Service Desk (FSD). Once verified, the 12-character UEI unlocks immediately.", table_cell_style)
        ],
        [
            Paragraph("<b>Step 5: GSA Notarized Letter & Annual Renewal</b>", table_cell_style),
            Paragraph("• Prepare GSA 'Template for Non-US Entities' on organization letterhead.<br/>• Appoint Dr. Young Irivboje as authorized Entity Administrator.<br/>• Stamp and sign before a Nigerian Notary Public / High Court Commissioner.<br/>• Upload PDF to Federal Service Desk (FSD.gov) for active status.", table_cell_style),
            Paragraph("Mandatory anti-fraud control. Once approved, status becomes <b>ACTIVE</b>. Valid for exactly 365 days; must be renewed annually via a 10-minute online click-through to remain eligible for disbursements.", table_cell_style)
        ]
    ]

    t_ncage = Table(ncage_guide_data, colWidths=[120, 214, 170])
    t_ncage.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), usaid_blue),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#90CAF9")),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, border_gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_blue_bg]),
        ('PADDING', (0, 0), (-1, -1), 2.8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_ncage)
    story.append(Spacer(1, 5))

    # Action Sequence Table: What to Do Next on SAM.gov
    story.append(Paragraph("Action Protocol: Step-by-Step What to Do Next on SAM.gov (Using NCAGE STZZ1)", h2_style))
    story.append(Paragraph(
        "Now that NATO CAGE code <b>STZZ1</b> is active, follow this exact sequential walkthrough on <b>SAM.gov</b> to claim your 12-character Unique Entity Identifier (UEI) and finalize entity registration:",
        body_style
    ))

    sam_steps_data = [
        [
            Paragraph("<b>Seq #</b>", table_header_style),
            Paragraph("<b>Operational Phase on SAM.gov</b>", table_header_style),
            Paragraph("<b>Exact User Actions, Click Paths & Practical Tips</b>", table_header_style)
        ],
        [
            Paragraph("<b>1</b>", table_cell_style),
            Paragraph("<b>Sign In via Login.gov</b><br/><font size='6.0' color='#555555'>https://sam.gov</font>", table_cell_style),
            Paragraph("• Click <b>'Sign In'</b> at top right of SAM.gov.<br/>• Authenticate using dedicated email: <code>n84labs@gmail.com</code>.<br/>• Enter your Multi-Factor Authentication (MFA) code (Google Authenticator or SMS).", table_cell_style)
        ],
        [
            Paragraph("<b>2</b>", table_cell_style),
            Paragraph("<b>Initiate Entity Registration</b><br/><font size='6.0' color='#555555'>Workspace &gt; Entities</font>", table_cell_style),
            Paragraph("• From your SAM.gov Workspace home screen, locate the <b>'Entities'</b> widget box.<br/>• Click the green <b>'Get Started'</b> button (or select <b>'Register Entity'</b>).<br/>• Do not select search-only; choose the option to fully register the entity.", table_cell_style)
        ],
        [
            Paragraph("<b>3</b>", table_cell_style),
            Paragraph("<b>Select Purpose of Registration</b><br/><font size='6.0' color='#1B5E20'><b>Financial Assistance Only</b></font>", table_cell_style),
            Paragraph("• When prompted: <i>'What do you want to do?'</i>, select: <b>'Financial Assistance Awards Only'</b>.<br/>• <b>Critical Note:</b> Do NOT select 'All Awards / Federal Contracts'. Financial Assistance is tailored for grants/cooperative agreements (like USAID DIV), skipping hundreds of complex defense FAR clauses.", table_cell_style)
        ],
        [
            Paragraph("<b>4</b>", table_cell_style),
            Paragraph("<b>Enter Entity Name, Address & NCAGE STZZ1</b><br/><font size='6.0' color='#2E7D32'><b>COMPLETED</b></font>", table_cell_style),
            Paragraph("• Selected: <i>Directly with U.S. Federal Government</i> → <i>Financial Assistance Awards Only</i>.<br/>• Government entity: <i>No</i> | DoD assistance: <i>No</i> | Fiscal Year End: <i>12/31</i>.<br/>• Matched verified NATO CAGE code: <b>STZZ1</b> against CAC legal record.", table_cell_style)
        ],
        [
            Paragraph("<b>5</b>", table_cell_style),
            Paragraph("<b>Submit Validation Documents</b><br/><font size='6.0' color='#1565C0'><b>INC-GSAFSD21864803</b></font>", table_cell_style),
            Paragraph("• Official CAC incorporation certificates and status report submitted.<br/>• Official GSA FSD Incident Reference: <b>INC-GSAFSD21864803</b>.<br/>• Review turnaround estimate: <b>1.5 to 3.5 business days</b>.<br/>• Monitor <code>n84labs@gmail.com</code> for the FSD entity validation clearance email.", table_cell_style)
        ],
        [
            Paragraph("<b>6</b>", table_cell_style),
            Paragraph("<b>Claim UEI & Complete Locked Sections</b><br/><font size='6.0' color='#555555'>Unlocks After Validation</font>", table_cell_style),
            Paragraph("• Upon validation clearance, log in to claim your <b>12-character alphanumeric UEI</b>.<br/>• Complete unlocked modules: Taxpayer Information (TIN), Business Types, Financial Information (EFT bank account), Legal Proceedings, Business Operations, Points of Contact (POC), and Financial Assistance Response.<br/>• Assign <b>Dr. Young Imienwain Irivboje</b> as Electronic and Government Business POC.", table_cell_style)
        ],
        [
            Paragraph("<b>7</b>", table_cell_style),
            Paragraph("<b>Submit GSA Notarized Letter</b><br/><font size='6.0' color='#BA0C2F'><b>Final Activation Step</b></font>", table_cell_style),
            Paragraph("• Download the official GSA <i>'Template for Non-US Entities'</i> from FSD.gov.<br/>• Print on Naysa-84 Labs letterhead appointing Dr. Young Irivboje as Entity Administrator.<br/>• Have letter signed and stamped by a <b>Nigerian Notary Public</b> or High Court Commissioner.<br/>• Open a ticket on <b>FSD.gov</b>, attach the notarized PDF, and submit for final <b>ACTIVE</b> status.", table_cell_style)
        ]
    ]

    t_sam_steps = Table(sam_steps_data, colWidths=[30, 150, 324])
    t_sam_steps.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), forest_green),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#A5D6A7")),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, border_gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_green_bg]),
        ('PADDING', (0, 0), (-1, -1), 2.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_sam_steps)
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 2: 24-MONTH MASTER CHRONOLOGICAL IMPLEMENTATION ROADMAP
    # -------------------------------------------------------------
    story.append(Paragraph("Phase 1 to 5: The 24-Month Chronological Execution Lifecycle", h1_style))
    story.append(Paragraph(
        "Project execution spans five structured phases across two full agricultural cropping cycles (Wet and Dry seasons):",
        body_style
    ))

    # Phase Table
    phases_data = [
        [
            Paragraph("<b>Timeline</b>", table_header_style),
            Paragraph("<b>Phase & Focus</b>", table_header_style),
            Paragraph("<b>Core Technical & Operational Deliverables</b>", table_header_style),
            Paragraph("<b>Disbursement Trigger</b>", table_header_style)
        ],
        [
            Paragraph("<b>Months 1–4</b><br/><font color='#555555' size='6.5'>Phase 1</font>", table_cell_style),
            Paragraph("<b>Inception, Governance & Baseline Survey</b>", table_cell_style),
            Paragraph("• AOR Kickoff Conference & Approval of Year 1 Work Plan.<br/>• Finalize Monitoring, Evaluation & Learning (MEL) Plan.<br/>• Secure Institutional Review Board (IRB) ethical clearance (FUNAAB).<br/>• Register Pre-Analysis Plan (PAP) on AEA / OSF Registry.<br/>• Deploy digital enumerators (ODK/Kobo); complete Baseline Survey of N=3,000 smallholders across 30 agrarian clusters.", table_cell_style),
            Paragraph("<b>Milestone 1</b><br/>Approved MEL Plan + IRB Clearance + Baseline Dataset ($35,000)", table_cell_style)
        ],
        [
            Paragraph("<b>Months 5–8</b><br/><font color='#555555' size='6.5'>Phase 2</font>", table_cell_style),
            Paragraph("<b>Technical Engineering & Broadcast Setup</b>", table_cell_style),
            Paragraph("• Production deployment of Suite 8: Last-Mile Vernacular Radio Engine.<br/>• Integrate Africa's Talking API for 2G GSM cellular voice robocalls.<br/>• Onboard 10–15 rural community FM radio stations (ZaraRadio/Rivendell automated RSS podcast polling).<br/>• Ingest NARS soil acidity titration & SAMMAZ maize trial datasets.<br/>• Complete colloquial translation & voice QA (Hausa, Yoruba, Swahili, French).", table_cell_style),
            Paragraph("<b>Milestone 2</b><br/>Verified Telephony & Radio Pipeline + Station MoUs ($30,000)", table_cell_style)
        ],
        [
            Paragraph("<b>Months 9–14</b><br/><font color='#555555' size='6.5'>Phase 3A</font>", table_cell_style),
            Paragraph("<b>Season 1 Rollout (Major Wet Season)</b>", table_cell_style),
            Paragraph("• Launch dawn/dusk FM radio advisories (lime neutralization + SAMMAZ-15 seed).<br/>• Dispatch targeted 2G GSM voice robocalls to 1,500 treatment smallholders.<br/>• Real-time telemetry monitoring (call completions, radio transmission logs).<br/>• Mid-season crop health monitoring & Fall Armyworm alert broadcast.<br/>• Quarterly Progress Report (QPR 1 & 2) submitted to USAID AOR.", table_cell_style),
            Paragraph("<b>Milestone 3</b><br/>Season 1 Broadcast Logs + 10k Farmer Reach Audit ($30,000)", table_cell_style)
        ],
        [
            Paragraph("<b>Months 15–18</b><br/><font color='#555555' size='6.5'>Phase 3B</font>", table_cell_style),
            Paragraph("<b>Season 2 Rollout (Minor Wet / Dry Season)</b>", table_cell_style),
            Paragraph("• Deploy dry-season irrigation advisory via FAO-56 Penman-Monteith (ET0).<br/>• Broadcast hermetic storage post-harvest alerts & livestock THI heat stress.<br/>• Conduct intermediate pulse surveys to measure input purchase and lime adoption.<br/>• Annual Review Conference with USAID DIV team; submit Annual Report.", table_cell_style),
            Paragraph("<b>Milestone 4</b><br/>Annual Performance Report + Season 2 Deployment ($25,000)", table_cell_style)
        ],
        [
            Paragraph("<b>Months 19–21</b><br/><font color='#555555' size='6.5'>Phase 4</font>", table_cell_style),
            Paragraph("<b>Endline Survey & DiD Econometric Analysis</b>", table_cell_style),
            Paragraph("• Execute Endline Survey of all 3,000 farming households (target attrition &lt; 5%).<br/>• Estimate causal treatment effect (δ) via Difference-in-Differences (DiD).<br/>• Calculate verified Benefit-Cost Ratio (BCR) and cost-per-farmer-contact.<br/>• Draft publication-grade evaluation manuscript for academic journal submission.", table_cell_style),
            Paragraph("<b>Milestone 5</b><br/>Econometric Evaluation Report + Clean Datasets ($20,000)", table_cell_style)
        ],
        [
            Paragraph("<b>Months 22–24</b><br/><font color='#555555' size='6.5'>Phase 5</font>", table_cell_style),
            Paragraph("<b>Closeout, Dissemination & Stage 2 Preparation</b>", table_cell_style),
            Paragraph("• Host National Policy Dissemination Workshop in Abuja with FMAFS and NARS.<br/>• Upload de-identified datasets to USAID Development Data Library (DDL).<br/>• Publish technical evaluation on USAID Development Experience Clearinghouse (DEC).<br/>• Final Performance Report (FPR) and financial audit sign-off.<br/>• <b>Submit USAID DIV Stage 2 Application ($1,500,000 Scaling Grant)</b>.", table_cell_style),
            Paragraph("<b>Milestone 6</b><br/>Final Closeout Report + DEC/DDL Submission ($10,000)", table_cell_style)
        ]
    ]

    t_phases = Table(phases_data, colWidths=[65, 115, 224, 100])
    t_phases.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), usaid_blue),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#90CAF9")),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, border_gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_blue_bg]),
        ('PADDING', (0, 0), (-1, -1), 2.8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_phases)
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 3: DETAILED $150,000 BUDGET ALLOCATION & DEPLOYMENT
    # -------------------------------------------------------------
    story.append(Paragraph("Detailed $150,000 Budget Allocation Across the 24-Month Grant", h1_style))
    story.append(Paragraph(
        "Every dollar of the $150,000 grant must be strategically allocated across technical engineering, field evaluation rigor, last-mile voice delivery, and compliance governance:",
        body_style
    ))

    budget_data = [
        [
            Paragraph("<b>Budget Category & Line Item</b>", table_header_style),
            Paragraph("<b>Allocation ($)</b>", table_header_style),
            Paragraph("<b>% Total</b>", table_header_style),
            Paragraph("<b>Strategic Operational Justification & Description</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Personnel & Scientific Leadership</b><br/>• Principal Investigator / PI (Dr. Young Irivboje) - 25% LOE<br/>• Co-Investigators (Agronomy, Economics, Breeding)<br/>• Full-Stack Cloud/Telephony AI Software Engineer (pt)", table_cell_style),
            Paragraph("<b>$42,000</b>", table_cell_style),
            Paragraph("<b>28.0%</b>", table_cell_style),
            Paragraph("Covers key personnel Level of Effort (LOE) to direct operations, supervise multi-agent engineering, ensure biometrical rigor, oversee field enumerators, and lead econometric modeling across the 24-month grant period.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Field Surveys & Impact Evaluation</b><br/>• Baseline Survey (N=3,000 households, 30 clusters)<br/>• Endline Survey (N=3,000 households with tracking)<br/>• 20 Agricultural Enumerator Stipends & Training<br/>• Field Supervisors, Tablets, Mobile Data & ODK setup", table_cell_style),
            Paragraph("<b>$45,000</b>", table_cell_style),
            Paragraph("<b>30.0%</b>", table_cell_style),
            Paragraph("The core evidence engine of Stage 1. Covers enumerator training, field logistics, household surveys, GPS mapping of trial clusters, farmer respondent time compensations, and data quality audits.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Telephony, Voice & Vernacular Audio Engine</b><br/>• Africa's Talking Outbound 2G GSM Voice Airtime<br/>• 10–15 Community FM Radio Partnership Broadcast MoUs<br/>• Vernacular Voice Recording, Dialect QA & Studio Fees<br/>• Cloud Storage & Automated RFC 2.0 RSS Hosting", table_cell_style),
            Paragraph("<b>$28,000</b>", table_cell_style),
            Paragraph("<b>18.7%</b>", table_cell_style),
            Paragraph("Funds ~60,000–80,000 outbound cellular voice robocall minutes to smallholder basic feature phones, dawn/dusk broadcast slot partnerships with 10–15 rural FM stations, and vernacular voice talent.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Field Logistics, Travel & Workshops</b><br/>• Agrarian cluster community town halls & farmer meetings<br/>• Inter-state travel (Oyo, Osun, Ogun, Kaduna trial zones)<br/>• Vehicle fueling, rural mobility, field per diems<br/>• Extension agent / cooperative leadership briefing days", table_cell_style),
            Paragraph("<b>$18,000</b>", table_cell_style),
            Paragraph("<b>12.0%</b>", table_cell_style),
            Paragraph("Enables physical monitoring, cluster sensitization meetings with cooperative heads, ground-truthing of soil acidity and Fall Armyworm outbreaks, and safe researcher field mobility.", table_cell_style)
        ],
        [
            Paragraph("<b>5. Compliance, Ethics, Auditing & Closeout</b><br/>• Institutional Review Board (IRB) ethical clearance<br/>• Independent external financial audits (Year 1 & 2)<br/>• National Policy Dissemination Convening (Abuja)<br/>• SAM.gov, legal compliance, banking & administration", table_cell_style),
            Paragraph("<b>$17,000</b>", table_cell_style),
            Paragraph("<b>11.3%</b>", table_cell_style),
            Paragraph("Guarantees bulletproof USAID audit readiness, independent accounting verification, ethical human research compliance, and high-visibility policy dissemination in Abuja with federal ministry leaders.", table_cell_style)
        ],
        [
            Paragraph("<b>TOTAL GRANT OPERATING BUDGET</b>", table_header_style),
            Paragraph("<b>$150,000</b>", table_header_style),
            Paragraph("<b>100.0%</b>", table_header_style),
            Paragraph("<b>Fully balanced budget satisfying USAID DIV cost-efficiency requirements.</b>", table_header_style)
        ]
    ]

    t_budget = Table(budget_data, colWidths=[150, 60, 45, 249])
    t_budget.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), forest_green),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#A5D6A7")),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, border_gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, pale_green_bg]),
        ('BACKGROUND', (0, -1), (-1, -1), usaid_blue),
        ('PADDING', (0, 0), (-1, -1), 2.8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_budget)
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 4: USAID REPORTING, COMPLIANCE & LEGAL GUARDRAILS
    # -------------------------------------------------------------
    story.append(Paragraph("USAID Compliance, Financial Regulations & Reporting Requirements", h1_style))
    story.append(Paragraph(
        "Managing US Government funding demands strict adherence to federal regulations (2 CFR 200 and USAID ADS 303). Failure to comply can result in clawbacks, suspension, or debarment.",
        body_style
    ))

    story.append(Paragraph("<b>1. Mandatory Reporting Cycles:</b>", h2_style))
    story.append(Paragraph("• <b>Quarterly Progress Reports (QPRs)</b>: Submitted within 30 days of each fiscal quarter end. Must detail milestone progress, smallholders reached, audio syndication metrics, qualitative challenges, and corrective actions.", bullet_style))
    story.append(Paragraph("• <b>Quarterly Financial Reports (SF-425)</b>: Standard federal financial disclosure documenting expenditures against approved budget line items and tracking milestone completion tranches.", bullet_style))
    story.append(Paragraph("• <b>Annual Performance Reports</b>: Synthesizes annual agronomic trial progress, preliminary survey insights, and operational refinements.", bullet_style))
    story.append(Paragraph("• <b>Final Evaluation Report & Data Upload</b>: Submitted within 90 days of project closeout, accompanied by de-identified raw datasets deposited into the <b>USAID Development Data Library (DDL)</b> and public reports published to the <b>Development Experience Clearinghouse (DEC)</b>.", bullet_style))

    story.append(Paragraph("<b>2. Strict Financial & Procurement Rules (Allowable vs. Unallowable):</b>", h2_style))
    story.append(Paragraph("• <b>Segregated Banking & Timesheets</b>: All grant transactions must run through the dedicated project account. All personnel charging time must maintain signed, auditable bi-weekly timesheets documenting actual Level of Effort (LOE).", bullet_style))
    story.append(Paragraph("• <b>Unallowable Costs</b>: US federal regulations strictly prohibit using grant funds for: luxury goods, alcoholic beverages, entertainment, lobbying government officials, purchasing real estate or unapproved motor vehicles, or paying customs duties/tariffs.", bullet_style))
    story.append(Paragraph("• <b>Competitive Procurement & Anti-Terrorism Vetting</b>: Any single service contract or equipment procurement exceeding $10,000 must follow transparent three-quote competitive bidding and undergo mandatory SAM.gov / OFAC sanctions screening.", bullet_style))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 5: THE ULTIMATE PRIZE: TRANSITIONING TO STAGE 2 ($1.5M)
    # -------------------------------------------------------------
    story.append(Paragraph("The Grand Strategy: Transitioning Stage 1 Evidence into a $1,500,000 DIV Stage 2 Award", h1_style))
    story.append(Paragraph(
        "The ultimate purpose of DIV Stage 1 is not simply to conclude a 2-year project, but to position AgroBiometrix for <b>DIV Stage 2: Testing and Positioning for Scale ($1,500,000)</b> or institutional scaling with sovereign ministries. DIV explicitly favors Stage 1 grantees who prove their case.",
        body_style
    ))

    scale_callout = (
        "<b>What USAID DIV Looks for in Stage 2 Applicants:</b><br/>"
        "1. <b>Rigorous Causal Evidence:</b> An econometrically sound Difference-in-Differences evaluation proving that smallholders receiving AgroBiometrix advice increased net farm yields (+8–15%) and certified seed/lime adoption (+20 percentage points) relative to control clusters.<br/>"
        "2. <b>Cost-Effectiveness Superiority:</b> Empirical proof that AgroBiometrix delivers advisory at ~$0.02 (FM Radio) and ~$0.20 (2G GSM Robocalls), outperforming physical extension ($15–$25 per contact) by orders of magnitude.<br/>"
        "3. <b>Demonstrated Demand Signals:</b> 10,000+ farmers reached, high broadcast listenership, cooperative willingness-to-pay or government co-financing commitments.<br/>"
        "<b>With this evidence in hand by Month 22, you submit the $1.5M Stage 2 application to scale AgroBiometrix across 1,000,000+ farmers across Nigeria, Ghana, and Kenya.</b>"
    )
    story.append(make_callout("THE STAGE 2 SCALING BLUEPRINT ($1.5M USD)", scale_callout, pale_green_bg, forest_green))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 6: PRACTICAL SUMMARY & ACTION CHECKLIST FOR THE PI
    # -------------------------------------------------------------
    story.append(Paragraph("Immediate Practical Checklist for the Principal Investigator", h1_style))
    story.append(Paragraph("To ensure operational readiness when the award notification arrives, execute the following steps:", body_style))
    story.append(Paragraph("1. <b>Verify SAM.gov / UEI Status</b>: Confirm that your organization's registration on SAM.gov is active and compliant for federal awards.", bullet_style))
    story.append(Paragraph("2. <b>Formalize Consortium Sub-Agreements</b>: Draft preliminary Memoranda of Understanding (MoUs) with FUNAAB, OOU, FPI, and UGA clarifying exact roles and LOE.", bullet_style))
    story.append(Paragraph("3. <b>Draft the IRB Protocol Early</b>: Prepare the household survey informed consent protocols for expedited FUNAAB ethics review.", bullet_style))
    story.append(Paragraph("4. <b>Engage Telecom & Radio Partners</b>: Secure expressions of interest from Africa's Talking and 10 regional community radio stations.", bullet_style))
    story.append(Paragraph("5. <b>Maintain Technical Documentation</b>: Preserve the exact mathematical benchmarks, journal manuscripts, and whitepapers we have established.", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"USAID DIV Execution Playbook PDF generated successfully: {PDF_FILENAME}")

    # Mirror to artifacts directories
    for ad in ARTIFACT_DIRS:
        if os.path.exists(ad):
            art_dest = os.path.join(ad, PDF_FILENAME)
            try:
                shutil.copy(PDF_FILENAME, art_dest)
                print(f"Artifact mirrored successfully: {art_dest}")
            except Exception as e:
                print(f"Warning: Could not mirror to {art_dest}: {e}")


if __name__ == "__main__":
    build_pdf()
