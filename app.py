# ... (Keep your imports and PDF engine as they are)

with col_in:
    st.subheader("📋 Input Details")
    c_name = st.text_input("Company Name", value="BG CONSULTANCY PTE LTD")
    c_reg = st.text_input("Registration Number", value="200517609N")
    r_type = st.selectbox("Resolution Type", RESOLUTIONS)
    r_date = st.date_input("Resolution Date", value=date.today())

    st.divider()
    
    # --- FIX: Initialize 'sentence' here so it ALWAYS exists ---
    sentence = "" 
    directors_data = []
    
    if "2. Resignation" in r_type:
        st.write("**Resigning Directors**")
        n_res = st.number_input("Number of Resigning Directors", 1, 5, 1)
        for i in range(int(n_res)):
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                name = st.text_input(f"Resigning Director {i+1} Name", key=f"rname{i}")
            with d_col2:
                id_num = st.text_input(f"NRIC/Passport {i+1}", key=f"rid{i}")
            directors_data.append({"name": name, "id": id_num})
            
        res_strings = [f"{d['name'].upper()} (NRIC/Passport No. {d['id']})" for d in directors_data if d['name']]
        if res_strings:
            names_joined = " and ".join(res_strings)
            verb = "resignation" if len(res_strings) == 1 else "resignations"
            sentence = f"RESOLVED THAT the {verb} of {names_joined} as a director of the company, effective {r_date.strftime('%d/%m/%Y')}, be and is hereby accepted."
    
    else:
        st.write("**Signing Directors**")
        n_dirs = st.number_input("Number of Signing Directors", 1, 5, 2)
        for i in range(int(n_dirs)):
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                name = st.text_input(f"Director {i+1} Name", key=f"dname{i}")
            with d_col2:
                id_num = st.text_input(f"NRIC/Passport {i+1}", key=f"did{i}")
            directors_data.append({"name": name, "id": id_num})

        st.divider()
        
        # --- Logic for other types ---
        if "1. Appointment" in r_type:
            n = st.text_input("New Director Name")
            i = st.text_input("New Director NRIC/Passport")
            sentence = f"RESOLVED THAT {n}, NRIC/Passport No. {i}, be and is hereby appointed as a director of the company, effective {r_date.strftime('%d/%m/%Y')}."
        elif "3. Change of Registered Office" in r_type:
            addr = st.text_area("New Address")
            sentence = f"RESOLVED THAT the registered office of the company be changed to {addr}, with effect from {r_date.strftime('%d/%m/%Y')}."
        elif "4. Issuance of New Shares" in r_type:
            n = st.text_input("Subscriber Name")
            q = st.text_input("Quantity")
            p = st.text_input("Price")
            sentence = f"RESOLVED THAT the company issue {q} new ordinary shares at a price of {p} each, to {n}."
        elif "5. Transfer of Shares" in r_type:
            q = st.text_input("No. of Shares")
            f = st.text_input("From")
            t = st.text_input("To")
            sentence = f"RESOLVED THAT the transfer of {q} shares from {f} to {t} be and is hereby approved."
        elif "6. Declaration of Dividends" in r_type:
            a = st.text_input("Amount per share")
            sentence = f"RESOLVED THAT a final dividend of {a} per ordinary share be declared."
        elif "7. Approval of Financial Statements" in r_type:
            sentence = f"RESOLVED THAT the financial statements of the company for the financial year ended {r_date.strftime('%d/%m/%Y')} be approved."
        elif "8. Appointment/Reappointment of Auditors" in r_type:
            a = st.text_input("Auditor Name")
            sentence = f"RESOLVED THAT {a} be and is hereby appointed as auditors of the company."
        elif "9. Change of Company Name" in r_type:
            n = st.text_input("New Proposed Name")
            sentence = f"RESOLVED THAT the name of the company be changed to {n}."
        elif "10. Amendments" in r_type: # Added this elif specifically
            sentence = "RESOLVED THAT the amendments to the company’s constitution be and are hereby approved."
        elif "11. Dissolution" in r_type:
            l = st.text_input("Liquidator Name")
            sentence = f"RESOLVED THAT the company be and is hereby voluntarily wound up and that {l} be appointed as liquidator."

with col_pre:
    st.subheader("📄 Preview & Download")
    # Now 'sentence' is guaranteed to exist
    if sentence:
        with st.container(border=True):
            st.markdown(f"<h3 style='text-align: center;'>{c_name.upper()}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Reg: {c_reg}</p>", unsafe_allow_html=True)
            st.write(f"**Resolution Text:**")
            st.write(sentence)
        
        pdf = generate_pdf(c_name, c_reg, r_date, r_type, sentence, directors_data)
        st.download_button("📥 Download PDF", data=pdf, file_name=f"Resolution_{c_name.replace(' ', '_')}.pdf", mime="application/pdf")
    else:
        st.info("Please fill in the required details to generate the resolution.")