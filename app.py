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
    c.drawCentredString(width/2, height - 65, f"Company Registration No. {reg_num}")
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
    c.drawString(50, y, res_type.split('. ')[1].upper()) #
    
    # Body
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
            id_info = f"Director (NRIC/Passport: {director['id']})" if director['id'] else "Director"
            c.drawString(50, y, id_info)
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
    r_date = st.date_input("Resolution Date", value=date.today(), format="DD/MM/YYYY")

    st.divider()
    
    # Variables initialized
    sentence = ""
    signing_directors = []

    # --- BLOCK 1: SIGNING DIRECTORS (Always needed for the signature block) ---
    st.write("**Signing Directors (to appear on PDF bottom)**")
    n_sign = st.number_input("How many directors are signing?", 1, 10, 2)
    for i in range(int(n_sign)):
        sc1, sc2 = st.columns(2)
        with sc1: s_name = st.text_input(f"Signing Dir {i+1} Name", key=f"sname{i}")
        with sc2: s_id = st.text_input(f"Signing Dir {i+1} NRIC", key=f"sid{i}")
        signing_directors.append({"name": s_name, "id": s_id})

    st.divider()

    # --- BLOCK 2: DYNAMIC RESOLUTION ENTITIES ---
    
    # 1. APPOINTMENT OF DIRECTORS
    if "1. Appointment" in r_type:
        n_new = st.number_input("Number of New Directors to Appoint", 1, 10, 1)
        new_list = []
        for i in range(int(n_new)):
            nc1, nc2 = st.columns(2)
            with nc1: nn = st.text_input(f"New Dir {i+1} Name", key=f"nn{i}")
            with nc2: ni = st.text_input(f"New Dir {i+1} NRIC", key=f"ni{i}")
            if nn: new_list.append(f"{nn.upper()} (NRIC/Passport No. {ni})")
        
        if new_list:
            sentence = f"RESOLVED THAT {', '.join(new_list)} be and is/are hereby appointed as director(s) of the company, effective {r_date.strftime('%d/%m/%Y')}."

    # 2. RESIGNATION OF DIRECTORS
    elif "2. Resignation" in r_type:
        n_res = st.number_input("Number of Resigning Directors", 1, 10, 1)
        res_list = []
        for i in range(int(n_res)):
            rc1, rc2 = st.columns(2)
            with rc1: rn = st.text_input(f"Resigning Dir {i+1} Name", key=f"rn{i}")
            with rc2: ri = st.text_input(f"Resigning Dir {i+1} NRIC", key=f"ri{i}")
            if rn: res_list.append(f"{rn.upper()} (NRIC/Passport No. {ri})")
        
        if res_list:
            sentence = f"RESOLVED THAT the resignation(s) of {', '.join(res_list)} as director(s) of the company, effective {r_date.strftime('%d/%m/%Y')}, be and is/are hereby accepted."

    # 4. ISSUANCE OF NEW SHARES
    elif "4. Issuance of New Shares" in r_type:
        n_sh = st.number_input("Number of Shareholders receiving shares", 1, 10, 1)
        sh_list = []
        for i in range(int(n_sh)):
            shc1, shc2, shc3 = st.columns([2, 1, 1])
            with shc1: sn = st.text_input(f"Shareholder {i+1} Name", key=f"sn{i}")
            with shc2: sq = st.text_input(f"Qty", key=f"sq{i}")
            with shc3: sp = st.text_input(f"Price", key=f"sp{i}")
            if sn: sh_list.append(f"{sq} shares to {sn.upper()} at ${sp} each")
        
        if sh_list:
            sentence = f"RESOLVED THAT the company issue new ordinary shares as follows: {'; '.join(sh_list)}, with the corresponding share capital to be increased accordingly."

    # 5. TRANSFER OF SHARES
    elif "5. Transfer of Shares" in r_type:
        n_tr = st.number_input("Number of Transfers", 1, 10, 1)
        tr_list = []
        for i in range(int(n_tr)):
            tc1, tc2, tc3 = st.columns([1, 2, 2])
            with tc1: tq = st.text_input(f"Qty", key=f"tq{i}")
            with tc2: tf = st.text_input(f"From", key=f"tf{i}")
            with tc3: tt = st.text_input(f"To", key=f"tt{i}")
            if tf: tr_list.append(f"{tq} shares from {tf.upper()} to {tt.upper()}")
        
        if tr_list:
            sentence = f"RESOLVED THAT the following share transfers be approved: {', '.join(tr_list)}."

    # For all other resolutions, use a single input or standard text
    elif "3. Change of Registered Office" in r_type:
        addr = st.text_area("New Registered Office Address")
        sentence = f"RESOLVED THAT the registered office of the company be changed to {addr}, with effect from {r_date.strftime('%d/%m/%Y')}."
    elif "7. Approval of Financial Statements" in r_type:
        sentence = f"RESOLVED THAT the financial statements of the company for the financial year ended {r_date.strftime('%d/%m/%Y')} be approved and adopted."
    elif "9. Change of Company Name" in r_type:
        n = st.text_input("New Proposed Name")
        sentence = f"RESOLVED THAT the name of the company be changed to {n.upper()}, subject to ACRA approval."
    else:
        # Generic fallback for simple types (10, 11 etc)
        sentence = "RESOLVED THAT the proposed matters as presented to the directors be and are hereby approved."

with col_pre:
    st.subheader("📄 Preview & Download")
    if sentence:
        with st.container(border=True):
            st.markdown(f"<h3 style='text-align: center;'>{c_name.upper()}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Reg: {c_reg}</p>", unsafe_allow_html=True)
            st.write(f"**Final Resolution Text:**")
            st.write(sentence)
        
        pdf = generate_pdf(c_name, c_reg, r_date, r_type, sentence, signing_directors)
        st.download_button("📥 Download PDF", data=pdf, file_name=f"Resolution_{c_name.replace(' ', '_')}.pdf", mime="application/pdf")
    else:
        st.info("Fill in the details to generate the preview.")