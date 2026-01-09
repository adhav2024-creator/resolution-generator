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
    
    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 50, comp_name.upper())
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 65, f"Company Registration Number {reg_num}")
    c.drawCentredString(width/2, height - 78, "Incorporated in Singapore")
    c.line(50, height - 90, width - 50, height - 90)
    
    # Title
    c.setFont("Helvetica-Bold", 11)
    y = height - 120
    title = f"Directors’ Meeting Resolution in writing pursuant to the Company’s Articles of Association dated {res_date.strftime('%d/%m/%Y')}"
    lines = simpleSplit(title, "Helvetica-Bold", 11, width - 100)
    for line in lines:
        c.drawString(50, y, line)
        y -= 15
        
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, res_type.split('. ')[1].upper())
    
    # Body
    y -= 30
    c.setFont("Helvetica", 11)
    res_lines = simpleSplit(res_text, "Helvetica", 11, width - 100)
    for line in res_lines:
        c.drawString(50, y, line)
        y -= 15
        
    # Closing
    y -= 40
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "CLOSE OF MEETING")
    y -= 15
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "There being no other business, the meeting closed.")
    
    # Signatures
    y -= 50
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Certified as true record of Minutes")
    
    for director in directors_data:
        if director['name']:
            if y < 120:
                c.showPage()
                y = height - 50
            y -= 60
            c.drawString(50, y, "…………………………………………………………………")
            y -= 15
            c.drawString(50, y, director['name'].upper())
            y -= 15
            c.setFont("Helvetica", 10)
            id_info = f"Director (NRIC/Passport Number: {director['id']})" if director['id'] else "Director"
            c.drawString(50, y, id_info)
            c.setFont("Helvetica-Bold", 11)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- 3. UI LOGIC ---
st.title("📜 Corporate Resolution Generator")

column_input, column_preview = st.columns([1, 1.2])

with column_input:
    st.subheader("📋 Input Details")
    company_name = st.text_input("Company Name", value="BG CONSULTANCY PTE LTD")
    registration_number = st.text_input("Registration Number", value="200517609N")
    resolution_type = st.selectbox("Resolution Type", RESOLUTIONS)
    resolution_date = st.date_input("Resolution Date", value=date.today(), format="DD/MM/YYYY")

    st.divider()
    
    sentence = ""
    signing_directors_list = []

    # --- SIGNING DIRECTORS ---
    st.write("**Signing Directors**")
    number_of_signing_directors = st.number_input("Number of Directors signing this resolution", 1, 10, 2)
    for i in range(int(number_of_signing_directors)):
        col1, col2 = st.columns(2)
        with col1: 
            name = st.text_input(f"Director {i+1} Full Name", key=f"signing_name_{i}")
        with col2: 
            nric = st.text_input(f"Director {i+1} NRIC/Passport Number", key=f"signing_id_{i}")
        signing_directors_list.append({"name": name, "id": nric})

    st.divider()

    # --- RESOLUTION SPECIFIC LOGIC ---
    
    if "1. Appointment" in resolution_type:
        number_of_new_directors = st.number_input("Number of New Directors to be appointed", 1, 10, 1)
        names_list = []
        for i in range(int(number_of_new_directors)):
            c1, c2 = st.columns(2)
            with c1: n = st.text_input(f"New Director {i+1} Name", key=f"new_name_{i}")
            with c2: i_num = st.text_input(f"New Director {i+1} NRIC/Passport", key=f"new_id_{i}")
            if n: names_list.append(f"{n.upper()} (NRIC/Passport Number {i_num})")
        if names_list:
            sentence = f"RESOLVED THAT {', '.join(names_list)} be and is/are hereby appointed as director(s) of the company, effective {resolution_date.strftime('%d/%m/%Y')}."

    elif "2. Resignation" in resolution_type:
        number_of_resigning_directors = st.number_input("Number of Resigning Directors", 1, 10, 1)
        resigning_list = []
        for i in range(int(number_of_resigning_directors)):
            c1, c2 = st.columns(2)
            with c1: n = st.text_input(f"Resigning Director {i+1} Name", key=f"res_name_{i}")
            with c2: i_num = st.text_input(f"Resigning Director {i+1} NRIC/Passport", key=f"res_id_{i}")
            if n: resigning_list.append(f"{n.upper()} (NRIC/Passport Number {i_num})")
        if resigning_list:
            sentence = f"RESOLVED THAT the resignation(s) of {', '.join(resigning_list)} as director(s) of the company, effective {resolution_date.strftime('%d/%m/%Y')}, be and is/are hereby accepted."

    elif "4. Issuance of New Shares" in resolution_type:
        number_of_shareholders = st.number_input("Number of Shareholders receiving new shares", 1, 10, 1)
        issuance_list = []
        for i in range(int(number_of_shareholders)):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1: sn = st.text_input(f"Shareholder {i+1} Name", key=f"sh_name_{i}")
            with c2: sq = st.text_input(f"Quantity", key=f"sh_qty_{i}")
            with c3: sp = st.text_input(f"Price", key=f"sh_prc_{i}")
            if sn: issuance_list.append(f"{sq} ordinary shares to {sn.upper()} at a price of {sp} per share")
        if issuance_list:
            sentence = f"RESOLVED THAT the company issue new ordinary shares as follows: {'; '.join(issuance_list)}, with the corresponding share capital to be increased accordingly."

    elif "5. Transfer of Shares" in resolution_type:
        number_of_transfers = st.number_input("Number of share transfers", 1, 10, 1)
        transfer_list = []
        for i in range(int(number_of_transfers)):
            c1, c2, c3 = st.columns([1, 2, 2])
            with c1: tq = st.text_input(f"Quantity", key=f"tr_qty_{i}")
            with c2: tf = st.text_input(f"Transferor (From)", key=f"tr_from_{i}")
            with tc3 if 'tc3' in locals() else c3: tt = st.text_input(f"Transferee (To)", key=f"tr_to_{i}")
            if tf: transfer_list.append(f"{tq} shares from {tf.upper()} to {tt.upper()}")
        if transfer_list:
            sentence = f"RESOLVED THAT the following share transfers be and are hereby approved: {', '.join(transfer_list)}."

    elif "3. Change of Registered Office" in resolution_type:
        new_address = st.text_area("New Registered Office Address")
        sentence = f"RESOLVED THAT the registered office of the company be changed to {new_address}, with effect from {resolution_date.strftime('%d/%m/%Y')}."

    elif "9. Change of Company Name" in resolution_type:
        proposed_name = st.text_input("Proposed New Company Name")
        sentence = f"RESOLVED THAT the name of the company be changed to {proposed_name.upper()}, subject to the approval of the Registrar."

    else:
        sentence = "RESOLVED THAT the matters as set out in the document presented to the directors be and are hereby approved."

with column_preview:
    st.subheader("📄 Preview & Download")
    if sentence:
        with st.container(border=True):
            st.markdown(f"<h3 style='text-align: center;'>{company_name.upper()}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Company Registration Number: {registration_number}</p>", unsafe_allow_html=True)
            st.write(f"**Final Resolution Text:**")
            st.write(sentence)
        
        pdf_data = generate_pdf(company_name, registration_number, resolution_date, resolution_type, sentence, signing_directors_list)
        st.download_button("📥 Download PDF", data=pdf_data, file_name=f"Resolution_{company_name.replace(' ', '_')}.pdf", mime="application/pdf")