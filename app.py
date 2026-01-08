import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Corporate Resolution Generator", layout="wide")

RESOLUTIONS = [
    "1. Appointment of Directors", "2. Resignation of Directors", 
    "3. Change of Registered Office", "4. Issuance of New Shares",
    "5. Transfer of Shares", "6. Declaration of Dividends",
    "7. Approval of Financial Statements", "8. Appointment/Reappointment of Auditors",
    "9. Change of Company Name", "10. Amendments to the Company Constitution",
    "11. Dissolution of the Company"
]

# --- 2. PDF GENERATION ENGINE ---
def generate_pdf(comp_name, reg_num, res_date, res_type, res_text, directors):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header - Centered Company Name
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 50, comp_name.upper())
    
    # Registration Info
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 65, f"Company Registration No. {reg_num}")
    c.drawCentredString(width/2, height - 78, "Incorporated in Singapore")
    
    # Horizontal Line
    c.setLineWidth(1)
    c.line(50, height - 90, width - 50, height - 90)
    
    # Meeting Title
    c.setFont("Helvetica-Bold", 11)
    title_text = f"Directors’ Meeting Resolution in writing pursuant to the Company’s Articles of Association dated {res_date.strftime('%d/%m/%Y')}"
    lines = simpleSplit(title_text, "Helvetica-Bold", 11, width - 100)
    y = height - 120
    for line in lines:
        c.drawString(50, y, line)
        y -= 15
        
    # Resolution Type
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, res_type.upper().split('. ')[1])
    
    # Resolution Sentence
    y -= 30
    c.setFont("Helvetica", 11)
    res_lines = simpleSplit(res_text, "Helvetica", 11, width - 100)
    for line in res_lines:
        c.drawString(50, y, line)
        y -= 15
        
    # Close of Meeting
    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "CLOSE OF MEETING")
    y -= 15
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "There being no other business, the meeting closed.")
    
    # Signature Section
    y -= 50
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Certified as true record")
    y -= 15
    c.drawString(50, y, "Of Minutes")
    
    for name in directors:
        if name:
            if y < 100: # New page if running out of space
                c.showPage()
                y = height - 50
            y -= 60
            c.drawString(50, y, "…………………………………………………………………")
            y -= 15
            c.drawString(50, y, name.upper())
            y -= 15
            c.setFont("Helvetica", 10)
            c.drawString(50, y, "Director")
            c.setFont("Helvetica-Bold", 11)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- 3. APP INTERFACE ---
st.title("📜 Singapore Corporate Resolution Generator")

col_input, col_preview = st.columns([1, 1.2])

with col_input:
    st.subheader("📋 Resolution Data")
    comp_name = st.text_input("Name of the company", value="BG CONSULTNACY PTE LTD")
    reg_num = st.text_input("Registration number", value="200517609N")
    res_type = st.selectbox("Type of resolution", RESOLUTIONS)
    res_date = st.date_input("Date of the resolution", value=date.today())

    st.divider()
    
    # Dynamic Fields for Directors/Shareholders
    num_dirs = st.number_input("Total No. of Directors", 1, 10, 2)
    dir_names = [st.text_input(f"Director Name {i+1}", key=f"d_{i}") for i in range(num_dirs)]
    
    st.divider()
    
    # Resolution Logic
    res_sentence = ""
    if "1. Appointment" in res_type:
        name = st.text_input("Appointee Name")
        id_no = st.text_input("NRIC/Passport No.")
        res_sentence = f"RESOLVED THAT {name}, NRIC/Passport No. {id_no}, be and is hereby appointed as a director of the company, effective {res_date.strftime('%d/%m/%Y')}."
    
    elif "2. Resignation" in res_type:
        name = st.text_input("Resigning Director Name")
        id_no = st.text_input("NRIC/Passport No.")
        res_sentence = f"RESOLVED THAT the resignation of {name}, NRIC/Passport No. {id_no}, as a director of the company, effective {res_date.strftime('%d/%m/%Y')}, be and is hereby accepted."

    elif "3. Change of Registered Office" in res_type:
        addr = st.text_area("New Office Address")
        res_sentence = f"RESOLVED THAT the registered office of the company be changed to {addr}, with effect from {res_date.strftime('%d/%m/%Y')}."

    elif "4. Issuance of New Shares" in res_type:
        name = st.text_input("Recipient Name")
        qty = st.text_input("No. of Shares")
        price = st.text_input("Price per Share")
        res_sentence = f"RESOLVED THAT the company issue {qty} new ordinary shares at a price of {price} each, to {name}, with the corresponding share capital to be increased accordingly."

    elif "5. Transfer of Shares" in res_type:
        qty = st.text_input("No. of Shares")
        f_name = st.text_input("From (Name)")
        t_name = st.text_input("To (Name)")
        res_sentence = f"RESOLVED THAT the transfer of {qty} shares from {f_name} to {t_name} be and is hereby approved and that the necessary updates be made to the company’s register of members."

    elif "6. Declaration of Dividends" in res_type:
        amt = st.text_input("Amount per Share")
        res_sentence = f"RESOLVED THAT a final dividend of {amt} per ordinary share be declared, payable on {res_date.strftime('%d/%m/%Y')}."

    elif "7. Approval of Financial Statements" in res_type:
        res_sentence = f"RESOLVED THAT the financial statements of the company for the financial year ended {res_date.strftime('%d/%m/%Y')} be and are hereby approved and adopted."

    elif "8. Appointment/Reappointment of Auditors" in res_type:
        auditor = st.text_input("Audit Firm Name")
        res_sentence = f"RESOLVED THAT {auditor} be and is hereby appointed as auditors of the company for the financial year ending {res_date.strftime('%d/%m/%Y')}."

    elif "9. Change of Company Name" in res_type:
        new_name = st.text_input("Proposed New Name")
        res_sentence = f"RESOLVED THAT the name of the company be changed to {new_name}, subject to the approval of ACRA."

    elif "10. Amendments to the Company Constitution" in res_type:
        res_sentence = "RESOLVED THAT the amendments to the company’s constitution as set out in the document presented to this meeting be and are hereby approved."

    elif "11. Dissolution of the Company" in res_type:
        liq = st.text_input("Liquidator Name")
        res_sentence = f"RESOLVED THAT the company be and is hereby voluntarily wound up, and that {liq} be appointed as liquidator."

# --- 4. PREVIEW & DOWNLOAD ---
with col_preview:
    st.subheader("📄 Document Preview")
    if res_sentence:
        # Visual Box
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center;'>{comp_name.upper()}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Registration No: {reg_num}</p>", unsafe_allow_html=True)
            st.divider()
            st.write(f"**Resolution Type:** {res_type}")
            st.write(res_sentence)
            st.write("**Certified as true record of Minutes**")
            for d in dir_names:
                if d: st.write(f"--- {d.upper()} (Director)")

        # PDF Download
        pdf_file = generate_pdf(comp_name, reg_num, res_date, res_type, res_sentence, dir_names)
        st.download_button(
            label="📥 Download as Professional PDF",
            data=pdf_file,
            file_name=f"Resolution_{res_type[:2]}.pdf",
            mime="application/pdf"
        )