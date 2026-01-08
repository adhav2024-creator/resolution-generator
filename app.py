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
def generate_pdf(comp_name, reg_num, res_date, res_type, res_text, directors_data):
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
    
    for director in directors_data:
        if director['name']:
            if y < 120: 
                c.showPage()
                y = height - 50
            y -= 60
            c.drawString(50, y, "…………………………………………………………………")
            y -= 15
            c.drawString(50, y, f"{director['name'].upper()} ({director['id']})")
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
    
    # Updated Director Input with Passport Numbers
    num_dirs = st.number_input("Total No. of Directors", 1, 10, 2)
    directors_info = []
    for i in range(num_dirs):
        col1, col2 = st.columns(2)
        with col1:
            d_name = st.text_input(f"Director {i+1} Name", key=f"dn_{i}")
        with col2:
            d_id = st.text_input(f"Director {i+1} NRIC/Passport", key=f"di_{i}")
        directors_info.append({"name": d_name, "id": d_id})
    
    st.divider()
    
    # Resolution Logic
    res_sentence = ""
    if "1. Appointment" in res_type:
        name = st.text_input("Appointee Name")
        id_no = st.text_input("Appointee NRIC/Passport No.")
        res_sentence = f"RESOLVED THAT {name} ({id_no}), be and is hereby appointed as a director of the company, effective {res_date.strftime('%d/%m/%Y')}."
    
    elif "2. Resignation" in res_type:
        name = st.text_input("Resigning Director Name")
        id_no = st.text_input("Resigning Director NRIC/Passport No.")
        res_sentence = f"RESOLVED THAT the resignation of {name} ({id_no}) as director of the Company be hereby accepted with effect from {res_date.strftime('%d/%m/%Y')}."

    # ... (Other 9 resolution types following the same (ID) format) ...

# --- 4. PREVIEW & DOWNLOAD ---
with col_preview:
    st.subheader("📄 Document Preview")
    if res_sentence:
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center;'>{comp_name.upper()}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Registration No: {reg_num}</p>", unsafe_allow_html=True)
            st.divider()
            st.write(f"**Resolution Type:** {res_type}")
            st.write(res_sentence)
            st.write("**Certified as true record of Minutes**")
            for d in directors_info:
                if d['name']: st.write(f"--- {d['name'].upper()} ({d['id']}) - Director")

        pdf_file = generate_pdf(comp_name, reg_num, res_date, res_type, res_sentence, directors_info)
        st.download_button(label="📥 Download PDF", data=pdf_file, file_name="Resolution.pdf", mime="application/pdf")