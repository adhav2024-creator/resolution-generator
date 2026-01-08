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

# --- 2. PDF ENGINE ---
def generate_pdf(comp_name, reg_num, res_date, res_type, res_text, directors):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header Section
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 50, comp_name.upper()) # [cite: 2]
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 65, f"Company Registration No. {reg_num}") # [cite: 3]
    c.drawCentredString(width/2, height - 78, "Incorporated in Singapore") # [cite: 4]
    c.line(50, height - 90, width - 50, height - 90) # [cite: 5]
    
    # Resolution Title
    c.setFont("Helvetica-Bold", 11)
    y = height - 120
    title = f"Directors’ Meeting Resolution in writing pursuant to the Company’s Articles of Association dated {res_date.strftime('%d/%m/%Y')}" # [cite: 6]
    lines = simpleSplit(title, "Helvetica-Bold", 11, width - 100)
    for line in lines:
        c.drawString(50, y, line)
        y -= 15
        
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, res_type.upper().split('. ')[1]) # [cite: 7]
    
    # Body Text
    y -= 30
    c.setFont("Helvetica", 11)
    res_lines = simpleSplit(res_text, "Helvetica", 11, width - 100) # [cite: 8]
    for line in res_lines:
        c.drawString(50, y, line)
        y -= 15
        
    # Closing
    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "CLOSE OF MEETING") # [cite: 9]
    y -= 15
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "There being no other business, the meeting closed.") # [cite: 10]
    
    # Signatures
    y -= 50
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Certified as true record") # [cite: 11]
    y -= 15
    c.drawString(50, y, "Of Minutes") # [cite: 12]
    
    for name in directors:
        if name:
            y -= 60
            c.drawString(50, y, "…………………………………………………………………") # [cite: 13]
            y -= 15
            c.drawString(50, y, name.upper()) # [cite: 14, 17]
            y -= 15
            c.setFont("Helvetica", 10)
            c.drawString(50, y, "Director") # [cite: 15, 18]
            c.setFont("Helvetica-Bold", 11)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- 3. UI LOGIC ---
st.title("📜 Corporate Resolution Generator")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📋 Input Details")
    c_name = st.text_input("Company Name", value="BG CONSULTNACY PTE LTD")
    c_reg = st.text_input("Registration Number", value="200517609N")
    r_type = st.selectbox("Resolution Type", RESOLUTIONS)
    r_date = st.date_input("Resolution Date", value=date.today())

    st.divider()
    n_dirs = st.number_input("Number of Directors", 1, 5, 2)
    d_names = [st.text_input(f"Director {i+1} Name", key=f"d{i}") for i in range(n_dirs)]
    
    st.divider()
    sentence = ""
    # Dynamic Logic for all 11 types
    if "1. Appointment" in r_type:
        n = st.text_input("New Director Name")
        i = st.text_input("NRIC/Passport")
        sentence = f"RESOLVED THAT {n}, NRIC/Passport No. {i}, be and is hereby appointed as a director of the company, effective {r_date.strftime('%d/%m/%Y')}."
    elif "2. Resignation" in r_type:
        n = st.text_input("Resigning Director Name")
        i = st.text_input("NRIC/Passport")
        sentence = f"RESOLVED THAT the resignation of {n}, NRIC/Passport No. {i}, as a director of the company, effective {r_date.strftime('%d/%m/%Y')}, be and is hereby accepted."
    elif "3. Change of Registered Office" in r_type:
        addr = st.text_area("New Address")
        sentence = f"RESOLVED THAT the registered office of the company be changed to {addr}, with effect from {r_date.strftime('%d/%m/%Y')}."
    elif "4. Issuance of New Shares" in r_type:
        n = st.text_input("Name")
        q = st.text_input("Quantity")
        p = st.text_input("Price")
        sentence = f"RESOLVED THAT the company issue {q} new ordinary shares at a price of {p} each, to {n}, with the corresponding share capital to be increased accordingly."
    elif "5. Transfer of Shares" in r_type:
        q = st.text_input("No. of Shares")
        f = st.text_input("From (Name)")
        t = st.text_input("To (Name)")
        sentence = f"RESOLVED THAT the transfer of {q} shares from {f} to {t} be and is hereby approved and that the necessary updates be made to the company’s register of members."
    elif "6. Declaration of Dividends" in r_type:
        a = st.text_input("Amount per share")
        sentence = f"RESOLVED THAT a final dividend of {a} per ordinary share be declared, payable on {r_date.strftime('%d/%m/%Y')}."
    elif "7. Approval of Financial Statements" in r_type:
        sentence = f"RESOLVED THAT the financial statements of the company for the financial year ended {r_date.strftime('%d/%m/%Y')} be and are hereby approved and adopted."
    elif "8. Appointment/Reappointment of Auditors" in r_type:
        a = st.text_input("Auditor Name")
        sentence = f"RESOLVED THAT {a} be and is hereby appointed as auditors of the company for the financial year ending {r_date.strftime('%d/%m/%Y')}."
    elif "9. Change of Company Name" in r_type:
        n = st.text_input("New Name")
        sentence = f"RESOLVED THAT the name of the company be changed to {n}, subject to the approval of ACRA."
    elif "10. Amendments" in r_type:
        sentence = "RESOLVED THAT the amendments to the company’s constitution as set out in the document presented to this meeting be and are hereby approved."
    elif "11. Dissolution" in r_type:
        l = st.text_input("Liquidator Name")
        sentence = f"RESOLVED THAT the company be and is hereby voluntarily wound up, and that {l} be appointed as liquidator."

with col_pre:
    st.subheader("📄 Preview & Download")
    if sentence:
        with st.container(border=True):
            st.markdown(f"<h3 style='text-align: center;'>{c_name.upper()}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Reg: {c_reg}</p>", unsafe_allow_html=True)
            st.write(sentence)
            st.write("**Certified as True Record**")
        
        pdf = generate_pdf(c_name, c_reg, r_date, r_type, sentence, d_names)
        st.download_button("📥 Download PDF", data=pdf, file_name="Resolution.pdf", mime="application/pdf")