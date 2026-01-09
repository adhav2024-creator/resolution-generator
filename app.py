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
def generate_pdf(comp_name, reg_num, res_date, res_type, res_text, directors_data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header Section
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 50, comp_name.upper())
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 65, f"Company Registration No. {reg_num}")
    c.drawCentredString(width/2, height - 78, "Incorporated in Singapore")
    c.line(50, height - 90, width - 50, height - 90)
    
    # Resolution Title
    c.setFont("Helvetica-Bold", 11)
    y = height - 120
    title = f"Directors’ Meeting Resolution in writing pursuant to the Company’s Articles of Association dated {res_date.strftime('%d/%m/%Y')}"
    lines = simpleSplit(title, "Helvetica-Bold", 11, width - 100)
    for line in lines:
        c.drawString(50, y, line)
        y -= 15
        
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    # Correctly handles splitting the resolution name
    c.drawString(50, y, res_type.split('. ')[1].upper())
    
    # Body Text
    y -= 30
    c.setFont("Helvetica", 11)
    res_lines = simpleSplit(res_text, "Helvetica", 11, width - 100)
    for line in res_lines:
        c.drawString(50, y, line)
        y -= 15
        
    # Closing
    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "CLOSE OF MEETING")
    y -= 15
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "There being no other business, the meeting closed.")
    
    # Signatures
    y -= 50
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Certified as true record")
    y -= 15
    c.drawString(50, y, "Of Minutes")
    
    # directors_data is now a list of dictionaries: {'name': ..., 'id': ...}
    for director in directors_data:
        if director['name']:
            if y < 100: # Simple page break check
                c.showPage()
                y = height - 50
                
            y -= 60
            c.drawString(50, y, "…………………………………………………………………")
            y -= 15
            c.drawString(50, y, director['name'].upper())
            y -= 15
            c.setFont("Helvetica", 10)
            # Added ID Number to the PDF signature line
            id_text = f"Director (NRIC/Passport: {director['id']})" if director['id'] else "Director"
            c.drawString(50, y, id_text)
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
    c_name = st.text_input("Company Name", value="BG CONSULTANCY PTE LTD")
    c_reg = st.text_input("Registration Number", value="200517609N")
    r_type = st.selectbox("Resolution Type", RESOLUTIONS)
    r_date = st.date_input("Resolution Date", value=date.today())

    st.divider()
    st.write("**Signing Directors**")
    n_dirs = st.number_input("Number of Signing Directors", 1, 5, 2)
    
    # UPDATED: Collect both Name and ID in a structured way
    directors_data = []
    for i in range(int(n_dirs)):
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            name = st.text_input(f"Director {i+1} Name", key=f"dname{i}")
        with d_col2:
            id_num = st.text_input(f"NRIC/Passport {i+1}", key=f"did{i}")
        directors_data.append({"name": name, "id": id_num})
    
    st.divider()
    sentence = ""
    # Dynamic Logic for resolution body text
    if "1. Appointment" in r_type:
        n = st.text_input("New Director Name")
        i = st.text_input("New Director NRIC/Passport")
        sentence = f"RESOLVED THAT {n}, NRIC/Passport No. {i}, be and is hereby appointed as a director of the company, effective {r_date.strftime('%d/%m/%Y')}."
    elif "2. Resignation" in r_type:
        n = st.text_input("Resigning Director Name")
        i = st.text_input("Resigning Director NRIC/Passport")
        sentence = f"RESOLVED THAT the resignation of {n}, NRIC/Passport No. {i}, as a director of the company, effective {r_date.strftime('%d/%m/%Y')}, be and is hereby accepted."
    elif "3. Change of Registered Office" in r_type:
        addr = st.text_area("New Address")
        sentence = f"RESOLVED THAT the registered office of the company be changed to {addr}, with effect from {r_date.strftime('%d/%m/%Y')}."
    elif "4. Issuance of New Shares" in r_type:
        n = st.text_input("Subscriber Name")
        q = st.text_input("Quantity of Shares")
        p = st.text_input("Price per Share")
        sentence = f"RESOLVED THAT the company issue {q} new ordinary shares at a price of {p} each, to {n}, with the corresponding share capital to be increased accordingly."
    elif "5. Transfer of Shares" in r_type:
        q = st.text_input("No. of Shares")
        f = st.text_input("From (Transferor)")
        t = st.text_input("To (Transferee)")
        sentence = f"RESOLVED THAT the transfer of {q} shares from {f} to {t} be and is hereby approved and that the necessary updates be made to the company’s register of members."
    elif "6. Declaration of Dividends" in r_type:
        a = st.text_input("Amount per share (e.g. $1.00)")
        sentence = f"RESOLVED THAT a final dividend of {a} per ordinary share be declared, payable on {r_date.strftime('%d/%m/%Y')}."
    elif "7. Approval of Financial Statements" in r_type:
        sentence = f"RESOLVED THAT the financial statements of the company for the financial year ended {r_date.strftime('%d/%m/%Y')} be and are hereby approved and adopted."
    elif "8. Appointment/Reappointment of Auditors" in r_type:
        a = st.text_input("Auditor Name")
        sentence = f"RESOLVED THAT {a} be and is hereby appointed as auditors of the company for the financial year ending {r_date.strftime('%d/%m/%Y')}."
    elif "9. Change of Company Name" in r_type:
        n = st.text_input("Proposed New Name")
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
            st.write(f"**Resolution:** {sentence}")
            st.divider()
            st.write("**Signing Directors:**")
            for d in directors_data:
                if d['name']:
                    st.write(f"- {d['name']} ({d['id']})")
        
        pdf = generate_pdf(c_name, c_reg, r_date, r_type, sentence, directors_data)
        st.download_button("📥 Download PDF", data=pdf, file_name=f"Resolution_{c_name.replace(' ', '_')}.pdf", mime="application/pdf")