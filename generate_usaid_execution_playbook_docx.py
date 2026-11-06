"""
Generates the Microsoft Word (.docx) version of the AgroBiometrix USAID DIV Post-Award Master Operational Playbook.
Target File: AgroBiometrix_USAID_DIV_Post_Award_Execution_Master_Playbook.docx
Now updated with the full Step-by-Step SAM.gov & NCAGE Guide for Nigerian Organizations.
"""

import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_FILENAME = "AgroBiometrix_USAID_DIV_Post_Award_Execution_Master_Playbook.docx"
ARTIFACT_DIRS = [
    r"C:\Users\USER\.gemini\antigravity\brain\d802ae47-5651-4f17-a2ea-7d8c7b8085d8",
    r"C:\Users\USER\.gemini\antigravity\brain\1e91af0e-0faf-4a71-9df3-64f967526da0"
]


def set_cell_background(cell, fill_hex):
    """Sets background shading of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets inner padding for a table cell (in dxa: 20 dxa = 1 pt)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)


def add_callout_box(doc, title, body_text, fill_hex="F0F4F8", border_hex="002F6C"):
    """Adds a formatted callout box in Word."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r_title = p.add_run(title)
    r_title.font.bold = True
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(0, 47, 108)
    
    p_body = cell.add_paragraph()
    p_body.paragraph_format.space_before = Pt(2)
    p_body.paragraph_format.space_after = Pt(2)
    p_body.paragraph_format.line_spacing = 1.15
    r_body = p_body.add_run(body_text)
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = RGBColor(33, 33, 33)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def build_docx():
    doc = docx.Document()

    # Set 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(33, 33, 33)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Header Stamp
    p_stamp = doc.add_paragraph()
    r_stamp = p_stamp.add_run("USAID DEVELOPMENT INNOVATION VENTURES (DIV) • POST-AWARD IMPLEMENTATION DIRECTIVE")
    r_stamp.font.bold = True
    r_stamp.font.size = Pt(9.5)
    r_stamp.font.color.rgb = RGBColor(186, 12, 47)  # USAID Red
    p_stamp.paragraph_format.space_after = Pt(4)

    # Document Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("What to Do When You Win the USAID DIV Fund: The Complete Technical, Financial, and Operational Roadmap (Start-to-Finish)")
    r_title.font.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(0, 47, 108)  # USAID Blue
    p_title.paragraph_format.space_after = Pt(4)

    # Subtitle
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("AgroBiometrix Implementation Protocol: A 24-Month Master Execution Plan from Award Negotiation to DIV Stage 2 ($1.5M) Scale-Up")
    r_sub.font.bold = True
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(27, 94, 32)
    p_sub.paragraph_format.space_after = Pt(4)

    # Metadata
    p_meta = doc.add_paragraph()
    meta_text = (
        "Award Mechanism: USAID DIV Stage 1 Proof of Concept ($150,000 / 24 Months) • Target Reach: 10,000+ Smallholders\n"
        "Lead Implementing Organization: AgroBiometrix Engineering Unit / Naysa-84 Labs in consortium with FUNAAB, OOU, FPI, and UGA\n"
        "Principal Investigator / Project Director: Dr. Young Imienwain Irivboje (FUNAAB / Naysa-84 Labs)\n"
        "NATO Commercial and Government Entity (NCAGE) Code: STZZ1 (Active on NATO NSPA Portal)\n"
        "Fiscal Year End Date: December 31 (12/31)\n"
        "SAM.gov Entity Validation Incident / Case ID: INC-GSAFSD21864803 (Documents Submitted, 1.5–3.5 Business Days Review)"
    )
    r_meta = p_meta.add_run(meta_text)
    r_meta.font.italic = True
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(84, 110, 122)
    p_meta.paragraph_format.space_after = Pt(12)

    # Executive Mandate Callout Box
    add_callout_box(
        doc,
        "EXECUTIVE MANDATE: THE FUNDAMENTAL PHILOSOPHY OF USAID DIV",
        "Winning a USAID DIV grant is fundamentally different from receiving traditional charity or humanitarian aid. DIV operates as an evidence-driven venture fund within the United States Government. USAID is investing $150,000 into AgroBiometrix to rigorously answer one core question: 'Can an Africa-first, sovereign biometrical operating system with last-mile vernacular voice dissemination produce statistically verified yield and revenue gains among smallholders at a dramatically lower unit cost than traditional extension?'\n\n"
        "If you prove this with gold-standard causal evidence (Difference-in-Differences), rigorous unit economics ($0.02 radio / $0.20 voice robocall), and operational fidelity, AgroBiometrix unlocks the gateway to USAID DIV Stage 2 ($1,500,000) and nationwide government adoption. This master playbook defines your exact roadmap from Day 1 to Month 24.",
        fill_hex="F0F4F8",
        border_hex="002F6C"
    )

    # -------------------------------------------------------------
    # PHASE 0: PRE-AWARD
    # -------------------------------------------------------------
    h1 = doc.add_paragraph()
    r1 = h1.add_run("Phase 0: Pre-Award Due Diligence & Negotiation (Months -2 to 0 / Post-Notification)")
    r1.font.bold = True
    r1.font.size = Pt(13)
    r1.font.color.rgb = RGBColor(0, 47, 108)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "Upon receiving notification of selection from the DIV Agreement Officer (AO), the formal negotiation and pre-award compliance phase commences. This phase typically spans 60 to 90 days before initial funds are disbursed:\n"
        "• SAM.gov & Unique Entity Identifier (UEI) Validation: Ensure active registration on the US Government System for Award Management (SAM.gov). Naysa-84 / AgroBiometrix must maintain valid NCAGE and UEI codes.\n"
        "• Non-US Organization Pre-Award Survey (NUPAS) / Financial Risk Review: USAID will evaluate your internal financial management, segregation of duties, procurement policies, and anti-fraud protocols.\n"
        "• Award Mechanism Selection (Fixed Amount Award vs. Cooperative Agreement): Stage 1 DIV awards are predominantly structured as Fixed Amount Awards (FAAs). Under an FAA, disbursements are milestone-based rather than reimbursement-based. You are paid tranches upon verification of delivered milestones (e.g., approved MEL plan, baseline completed, vernacular audio engine deployed).\n"
        "• Designated Bank Account Establishment: Open a segregated, dedicated institutional bank account (USD and local currency NGN) exclusively for USAID project funds. Never commingle grant funds with personal or general organizational capital.\n"
        "• Assignment of Key Personnel & Agreement Officer Representative (AOR): Finalize the formal designation of Dr. Young Irivboje as PI / Project Director and establish weekly communication protocols with your assigned USAID AOR in Washington."
    )

    # -------------------------------------------------------------
    # SECTION 1B: STEP-BY-STEP SAM.GOV & NCAGE GUIDE FOR NIGERIAN ORGANIZATIONS
    # -------------------------------------------------------------
    h1b = doc.add_paragraph()
    r1b = h1b.add_run("Special Directive: Step-by-Step SAM.gov & NCAGE Guide for Nigerian Entities")
    r1b.font.bold = True
    r1b.font.size = Pt(13)
    r1b.font.color.rgb = RGBColor(0, 47, 108)
    h1b.paragraph_format.space_before = Pt(12)
    h1b.paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "Federal regulation (2 CFR Part 25) strictly mandates that foreign recipients of US grants hold an active registration in SAM.gov with a Unique Entity Identifier (UEI). SAM.gov replaced the legacy DUNS number in April 2022. Registration is 100% free of charge; beware of commercial third-party scams charging $500–$2,500."
    )

    tbl_ncage = doc.add_table(rows=6, cols=3)
    tbl_ncage.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ncage.autofit = False

    nc_headers = ["Registration Step & Field", "Exact Input / Action for Naysa-84 Labs / AgroBiometrix", "Strategic Rationale & Critical Notes"]
    nc_col_widths = [Inches(1.8), Inches(2.6), Inches(2.1)]

    for i, h in enumerate(nc_headers):
        cell = tbl_ncage.cell(0, i)
        cell.width = nc_col_widths[i]
        set_cell_background(cell, "002F6C")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    nc_rows = [
        ["Step 1: NCAGE Code Request\n(NATO NSPA Portal)\nSTATUS: ASSIGNED (STZZ1)",
         "• Official NCAGE Code: STZZ1 (Active on NATO Directory).\n• Verified URL: https://eportal.nspa.nato.int/Codification/CageTool/cage-view/STZZ1.\n• Legal Name & Address verified against CAC records.\n• ISIC: 7210 | NAICS: 541715 (Life Sciences R&D).",
         "Prerequisite Achieved. NATO Support and Procurement Agency has codified the entity. Code STZZ1 is active and ready for entry into SAM.gov for direct US DLA validation."],
        ["Future Business & SAM Question\n(NCAGE Questionnaires)",
         "• 'NCAGE code needed for invitation to tender?' → Select NO.\n• 'The NCAGE code is requested by SAM?' → Select YES.",
         "Selecting 'Yes' to tender forces you to provide military bid numbers. Selecting 'Yes' to SAM triggers an automated data bridge syncing NATO with the US Defense Logistics Agency (DLA) and SAM.gov."],
        ["Step 2: Login.gov Account\n(Administrative Credentials)",
         "• Register with dedicated entity email: n84labs@gmail.com.\n• Activate Multi-Factor Authentication (Google Authenticator / SMS).\n• Record and store the 16-character Emergency Recovery Key.",
         "Entity-dedicated Gmail accounts are fully accepted and prevent administrative lockout when personal or student university email accounts expire. The 16-character key is required if your device is lost."],
        ["Step 3: Document Readiness & Exact-Match Rule",
         "• CAC Certificate of Incorporation / Business Name Registration.\n• CAC Status Report / Form CAC 1.1 showing official registered address.\n• Official Nigerian Bank Statement or Utility Bill (supplementary if requested).\n• Federal Tax Identification Number (TIN) from FIRS.",
         "The Exact-Match Rule: SAM.gov compares inputs against government registries. Discrepancies in spelling, punctuation, or suite numbers trigger manual reviews that cause 3–4 week delays."],
        ["Step 4: SAM.gov Validation & UEI Generation\nSTATUS: SUBMITTED (INC-GSAFSD21864803)",
         "• Purpose: Financial Assistance Awards Only (Selected).\n• Fiscal Year End: 12/31 | Matched NCAGE: STZZ1.\n• Uploaded official CAC incorporation and registration documents.\n• Reference Number: INC-GSAFSD21864803 submitted for GSA review (1.5–3.5 business days).\n• 12-character alphanumeric UEI unlocks immediately upon validation approval.",
         "Financial Assistance registration is streamlined for grants and cooperative agreements. GSA Federal Service Desk is actively reviewing documents. Once cleared, UEI is assigned and remaining modules unlock."]
    ]

    for row_idx, r_data in enumerate(nc_rows, start=1):
        bg = "FFFFFF" if row_idx % 2 != 0 else "F0F4F8"
        for col_idx, val in enumerate(r_data):
            cell = tbl_ncage.cell(row_idx, col_idx)
            cell.width = nc_col_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Action Sequence Table: What to Do Next on SAM.gov
    h_act = doc.add_paragraph()
    r_act = h_act.add_run("Action Protocol: Step-by-Step What to Do Next on SAM.gov (Using NCAGE STZZ1)")
    r_act.font.bold = True
    r_act.font.size = Pt(12)
    r_act.font.color.rgb = RGBColor(27, 94, 32)
    h_act.paragraph_format.space_before = Pt(8)
    h_act.paragraph_format.space_after = Pt(3)

    doc.add_paragraph(
        "Now that NATO CAGE code STZZ1 is active, follow this exact sequential walkthrough on SAM.gov to claim your 12-character Unique Entity Identifier (UEI) and finalize entity registration:"
    )

    tbl_sam_steps = doc.add_table(rows=8, cols=3)
    tbl_sam_steps.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sam_steps.autofit = False

    s_headers = ["Seq #", "Operational Phase on SAM.gov", "Exact User Actions, Click Paths & Practical Tips"]
    s_col_widths = [Inches(0.6), Inches(2.2), Inches(3.7)]

    for i, h in enumerate(s_headers):
        cell = tbl_sam_steps.cell(0, i)
        cell.width = s_col_widths[i]
        set_cell_background(cell, "1B5E20")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    s_rows = [
        ["1", "Sign In via Login.gov\nhttps://sam.gov",
         "• Click 'Sign In' at top right of SAM.gov.\n• Authenticate using dedicated email: n84labs@gmail.com.\n• Enter your Multi-Factor Authentication (MFA) code (Google Authenticator or SMS)."],
        ["2", "Initiate Entity Registration\nWorkspace > Entities",
         "• From your SAM.gov Workspace home screen, locate the 'Entities' widget box.\n• Click the green 'Get Started' button (or select 'Register Entity').\n• Do not select search-only; choose the option to fully register the entity."],
        ["3", "Select Purpose of Registration\nFinancial Assistance Only",
         "• When prompted: 'What do you want to do?', select: 'Financial Assistance Awards Only'.\n• Critical Note: Do NOT select 'All Awards / Federal Contracts'. Financial Assistance is tailored for grants/cooperative agreements (like USAID DIV), skipping hundreds of complex defense FAR clauses."],
        ["4", "Enter Details, Address & NCAGE STZZ1\nSTATUS: COMPLETED",
         "• Selected: Directly with U.S. Federal Government > Financial Assistance Awards Only.\n• Government Entity: No | Department of Defense Assistance: No | Fiscal Year End: 12/31.\n• Entered NCAGE Code: STZZ1 matching CAC corporate record."],
        ["5", "Upload Validation Documents & Submit\nSTATUS: SUBMITTED (INC-GSAFSD21864803)",
         "• Uploaded official CAC incorporation certificate and status report.\n• Official Reference Number: INC-GSAFSD21864803 generated.\n• Review Turnaround: 1.5 to 3.5 business days by GSA Federal Service Desk.\n• Monitor n84labs@gmail.com for notification of validation approval."],
        ["6", "Claim 12-Character UEI & Complete Locked Sections\nPending Validation Approval",
         "• Log back in upon email confirmation to claim your 12-character alphanumeric UEI.\n• Complete unlocked modules: Taxpayer Information (TIN), Business Types, Financial Information (EFT bank account), Legal Proceedings, Business Operations, Points of Contact (POC), and Financial Assistance Response.\n• Designate Dr. Young Irivboje as Government Business & Electronic Business POC."],
        ["7", "Submit GSA Notarized Letter\nFinal Activation Step",
         "• Download the official GSA 'Template for Non-US Entities' from FSD.gov.\n• Print on Naysa-84 Labs letterhead appointing Dr. Young Irivboje as Entity Administrator.\n• Have letter signed and stamped by a Nigerian Notary Public or High Court Commissioner.\n• Open a ticket on FSD.gov, attach the notarized PDF, and submit for final ACTIVE status."]
    ]

    for row_idx, r_data in enumerate(s_rows, start=1):
        bg = "FFFFFF" if row_idx % 2 != 0 else "F1F8F2"
        for col_idx, val in enumerate(r_data):
            cell = tbl_sam_steps.cell(row_idx, col_idx)
            cell.width = s_col_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # PHASES 1 TO 5 CHRONOLOGICAL TABLE
    # -------------------------------------------------------------
    h2 = doc.add_paragraph()
    r2 = h2.add_run("The 24-Month Chronological Execution Lifecycle (Phases 1 to 5)")
    r2.font.bold = True
    r2.font.size = Pt(13)
    r2.font.color.rgb = RGBColor(0, 47, 108)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)

    tbl_phases = doc.add_table(rows=7, cols=4)
    tbl_phases.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_phases.autofit = False

    p_headers = ["Timeline", "Phase & Focus", "Core Technical & Operational Deliverables", "Disbursement Trigger"]
    p_col_widths = [Inches(1.0), Inches(1.5), Inches(2.7), Inches(1.3)]

    for i, h in enumerate(p_headers):
        cell = tbl_phases.cell(0, i)
        cell.width = p_col_widths[i]
        set_cell_background(cell, "002F6C")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    p_rows = [
        ["Months 1–4\nPhase 1", "Inception, Governance & Baseline Survey",
         "• AOR Kickoff Conference & Approval of Year 1 Work Plan.\n• Finalize Monitoring, Evaluation & Learning (MEL) Plan.\n• Secure Institutional Review Board (IRB) ethical clearance (FUNAAB).\n• Register Pre-Analysis Plan (PAP) on AEA / OSF Registry.\n• Deploy digital enumerators (ODK/Kobo); complete Baseline Survey of N=3,000 smallholders across 30 agrarian clusters.",
         "Milestone 1\nApproved MEL Plan + IRB Clearance + Baseline Dataset ($35,000)"],
        ["Months 5–8\nPhase 2", "Technical Engineering & Broadcast Setup",
         "• Production deployment of Suite 8: Last-Mile Vernacular Radio Engine.\n• Integrate Africa's Talking API for 2G GSM cellular voice robocalls.\n• Onboard 10–15 rural community FM radio stations (ZaraRadio/Rivendell automated RSS podcast polling).\n• Ingest NARS soil acidity titration & SAMMAZ maize trial datasets.\n• Complete colloquial translation & voice QA (Hausa, Yoruba, Swahili, French).",
         "Milestone 2\nVerified Telephony & Radio Pipeline + Station MoUs ($30,000)"],
        ["Months 9–14\nPhase 3A", "Season 1 Rollout (Major Wet Season)",
         "• Launch dawn/dusk FM radio advisories (lime neutralization + SAMMAZ-15 seed).\n• Dispatch targeted 2G GSM voice robocalls to 1,500 treatment smallholders.\n• Real-time telemetry monitoring (call completions, radio transmission logs).\n• Mid-season crop health monitoring & Fall Armyworm alert broadcast.\n• Quarterly Progress Report (QPR 1 & 2) submitted to USAID AOR.",
         "Milestone 3\nSeason 1 Broadcast Logs + 10k Farmer Reach Audit ($30,000)"],
        ["Months 15–18\nPhase 3B", "Season 2 Rollout (Minor Wet / Dry Season)",
         "• Deploy dry-season irrigation advisory via FAO-56 Penman-Monteith (ET0).\n• Broadcast hermetic storage post-harvest alerts & livestock THI heat stress.\n• Conduct intermediate pulse surveys to measure input purchase and lime adoption.\n• Annual Review Conference with USAID DIV team; submit Annual Report.",
         "Milestone 4\nAnnual Performance Report + Season 2 Deployment ($25,000)"],
        ["Months 19–21\nPhase 4", "Endline Survey & DiD Econometric Analysis",
         "• Execute Endline Survey of all 3,000 farming households (target attrition < 5%).\n• Estimate causal treatment effect (δ) via Difference-in-Differences (DiD).\n• Calculate verified Benefit-Cost Ratio (BCR) and cost-per-farmer-contact.\n• Draft publication-grade evaluation manuscript for academic journal submission.",
         "Milestone 5\nEconometric Evaluation Report + Clean Datasets ($20,000)"],
        ["Months 22–24\nPhase 5", "Closeout, Dissemination & Stage 2 Preparation",
         "• Host National Policy Dissemination Workshop in Abuja with FMAFS and NARS.\n• Upload de-identified datasets to USAID Development Data Library (DDL).\n• Publish technical evaluation on USAID Development Experience Clearinghouse (DEC).\n• Final Performance Report (FPR) and financial audit sign-off.\n• Submit USAID DIV Stage 2 Application ($1,500,000 Scaling Grant).",
         "Milestone 6\nFinal Closeout Report + DEC/DDL Submission ($10,000)"]
    ]

    for row_idx, r_data in enumerate(p_rows, start=1):
        bg = "FFFFFF" if row_idx % 2 != 0 else "F0F4F8"
        for col_idx, val in enumerate(r_data):
            cell = tbl_phases.cell(row_idx, col_idx)
            cell.width = p_col_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # DETAILED $150,000 BUDGET ALLOCATION
    # -------------------------------------------------------------
    h3 = doc.add_paragraph()
    r3 = h3.add_run("Detailed $150,000 Budget Allocation Across the 24-Month Grant")
    r3.font.bold = True
    r3.font.size = Pt(13)
    r3.font.color.rgb = RGBColor(0, 47, 108)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)

    tbl_budget = doc.add_table(rows=7, cols=4)
    tbl_budget.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_budget.autofit = False

    b_headers = ["Budget Category & Line Item", "Allocation ($)", "% Total", "Strategic Operational Description"]
    b_col_widths = [Inches(1.8), Inches(0.9), Inches(0.7), Inches(3.1)]

    for i, h in enumerate(b_headers):
        cell = tbl_budget.cell(0, i)
        cell.width = b_col_widths[i]
        set_cell_background(cell, "1B5E20")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    b_rows = [
        ["1. Personnel & Scientific Leadership\n• PI (Dr. Young Irivboje) - 25% LOE\n• Co-Investigators (Agronomy, Econ)\n• Full-Stack Cloud/Telephony Engineer",
         "$42,000", "28.0%", "Covers key personnel Level of Effort (LOE) to direct operations, supervise multi-agent engineering, ensure biometrical rigor, oversee field enumerators, and lead econometric modeling across the 24-month grant period."],
        ["2. Field Surveys & Impact Evaluation\n• Baseline Survey (N=3,000 households)\n• Endline Survey (N=3,000 households)\n• 20 Agricultural Enumerator Stipends\n• Tablets, Mobile Data & ODK setup",
         "$45,000", "30.0%", "The core evidence engine of Stage 1. Covers enumerator training, field logistics, household surveys, GPS mapping of trial clusters, farmer respondent time compensations, and data quality audits."],
        ["3. Telephony, Voice & Radio Engine\n• Africa's Talking Outbound GSM Voice\n• 10–15 FM Radio Broadcast MoUs\n• Vernacular Voice Recording & QA\n• Cloud Storage & RFC 2.0 RSS Hosting",
         "$28,000", "18.7%", "Funds ~60,000–80,000 outbound cellular voice robocall minutes to smallholder basic feature phones, dawn/dusk broadcast slot partnerships with 10–15 rural FM stations, and vernacular voice talent."],
        ["4. Field Logistics, Travel & Workshops\n• Agrarian cluster town halls\n• Inter-state travel (Oyo, Osun, Kaduna)\n• Vehicle fueling & rural mobility\n• Extension agent briefing days",
         "$18,000", "12.0%", "Enables physical monitoring, cluster sensitization meetings with cooperative heads, ground-truthing of soil acidity and Fall Armyworm outbreaks, and safe researcher field mobility."],
        ["5. Compliance, Ethics, Auditing & Closeout\n• IRB ethical clearance (FUNAAB)\n• Independent external financial audits\n• National Policy Convening (Abuja)\n• SAM.gov, banking & administration",
         "$17,000", "11.3%", "Guarantees bulletproof USAID audit readiness, independent accounting verification, ethical human research compliance, and high-visibility policy dissemination in Abuja with federal ministry leaders."],
        ["TOTAL GRANT OPERATING BUDGET", "$150,000", "100.0%", "Fully balanced budget satisfying USAID DIV cost-efficiency requirements."]
    ]

    for row_idx, r_data in enumerate(b_rows, start=1):
        bg = "FFFFFF" if row_idx % 2 != 0 else "F1F8F2"
        if row_idx == 6:
            bg = "002F6C"
        for col_idx, val in enumerate(r_data):
            cell = tbl_budget.cell(row_idx, col_idx)
            cell.width = b_col_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            if row_idx == 6:
                r.font.bold = True
                r.font.size = Pt(8.5)
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                r.font.size = Pt(8.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # USAID COMPLIANCE & LEGAL GUARDRAILS
    # -------------------------------------------------------------
    h4 = doc.add_paragraph()
    r4 = h4.add_run("USAID Compliance, Financial Regulations & Reporting Requirements")
    r4.font.bold = True
    r4.font.size = Pt(13)
    r4.font.color.rgb = RGBColor(0, 47, 108)
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "Managing US Government funding demands strict adherence to federal regulations (2 CFR 200 and USAID ADS 303). Failure to comply can result in clawbacks, suspension, or debarment:\n"
        "• Mandatory Reporting Cycles: Quarterly Progress Reports (QPRs) submitted within 30 days of each quarter end detailing reach metrics and technical milestones; Quarterly Financial Reports (SF-425) tracking milestone completion; Annual Performance Reports; and the Final Performance Report with datasets deposited in the USAID Development Data Library (DDL).\n"
        "• Segregated Banking & Timesheets: All grant funds must flow through the dedicated, segregated project account. All personnel billing time must maintain signed, auditable bi-weekly timesheets documenting actual Level of Effort (LOE).\n"
        "• Unallowable Costs: Federal regulations strictly prohibit using grant funds for: luxury goods, alcoholic beverages, entertainment, lobbying government officials, purchasing real estate or unapproved motor vehicles, or paying customs tariffs.\n"
        "• Competitive Procurement & Sanctions Screening: Any single service contract or equipment procurement exceeding $10,000 must follow transparent three-quote competitive bidding and undergo mandatory SAM.gov / OFAC sanctions screening."
    )

    # -------------------------------------------------------------
    # STAGE 2 SCALING BLUEPRINT ($1.5M)
    # -------------------------------------------------------------
    h5 = doc.add_paragraph()
    r5 = h5.add_run("The Grand Strategy: Transitioning Stage 1 Evidence into a $1,500,000 DIV Stage 2 Award")
    r5.font.bold = True
    r5.font.size = Pt(13)
    r5.font.color.rgb = RGBColor(0, 47, 108)
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(4)

    add_callout_box(
        doc,
        "THE STAGE 2 SCALING BLUEPRINT ($1.5M USD)",
        "The ultimate purpose of DIV Stage 1 is not simply to conclude a 2-year project, but to position AgroBiometrix for USAID DIV Stage 2: Testing and Positioning for Scale ($1,500,000) or institutional scaling with sovereign ministries. DIV explicitly favors Stage 1 grantees who prove their case:\n\n"
        "1. Rigorous Causal Evidence: An econometrically sound Difference-in-Differences evaluation proving that smallholders receiving AgroBiometrix advice increased net farm yields (+8–15%) and certified seed/lime adoption (+20 percentage points) relative to control clusters.\n"
        "2. Cost-Effectiveness Superiority: Empirical proof that AgroBiometrix delivers advisory at ~$0.02 (FM Radio) and ~$0.20 (2G GSM Robocalls), outperforming physical extension ($15–$25 per contact) by orders of magnitude.\n"
        "3. Demonstrated Demand Signals: 10,000+ farmers reached, high broadcast listenership, cooperative willingness-to-pay or government co-financing commitments.\n\n"
        "With this evidence in hand by Month 22, you submit the $1.5M Stage 2 application to scale AgroBiometrix across 1,000,000+ farmers across Nigeria, Ghana, and Kenya.",
        fill_hex="F1F8F2",
        border_hex="1B5E20"
    )

    # Immediate Checklist for the PI
    h6 = doc.add_paragraph()
    r6 = h6.add_run("Immediate Practical Checklist for the Principal Investigator")
    r6.font.bold = True
    r6.font.size = Pt(13)
    r6.font.color.rgb = RGBColor(0, 47, 108)
    h6.paragraph_format.space_before = Pt(12)
    h6.paragraph_format.space_after = Pt(4)

    doc.add_paragraph(
        "1. Verify SAM.gov / UEI Status: Confirm that your organization's registration on SAM.gov is active and compliant for federal awards.\n"
        "2. Formalize Consortium Sub-Agreements: Draft preliminary Memoranda of Understanding (MoUs) with FUNAAB, OOU, FPI, and UGA clarifying exact roles and LOE.\n"
        "3. Draft the IRB Protocol Early: Prepare the household survey informed consent protocols for expedited FUNAAB ethics review.\n"
        "4. Engage Telecom & Radio Partners: Secure expressions of interest from Africa's Talking and 10 regional community radio stations.\n"
        "5. Maintain Technical Documentation: Preserve the exact mathematical benchmarks, journal manuscripts, and whitepapers we have established."
    )

    alt_docx = "AgroBiometrix_USAID_DIV_Post_Award_Execution_Master_Playbook_Updated.docx"
    saved_path = DOCX_FILENAME
    try:
        doc.save(DOCX_FILENAME)
        print(f"Word Playbook (.docx) generated successfully: {DOCX_FILENAME}")
    except PermissionError:
        doc.save(alt_docx)
        saved_path = alt_docx
        print(f"Notice: '{DOCX_FILENAME}' is currently open in Word. Saved updated copy to '{alt_docx}'.")

    for ad in ARTIFACT_DIRS:
        if os.path.exists(ad):
            dest1 = os.path.join(ad, DOCX_FILENAME)
            dest2 = os.path.join(ad, alt_docx)
            for d in [dest1, dest2]:
                try:
                    shutil.copy(saved_path, d)
                    print(f"Mirrored Word document to artifact: {d}")
                except Exception as e:
                    pass


if __name__ == "__main__":
    build_docx()
