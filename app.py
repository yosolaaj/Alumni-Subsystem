import sqlite3
import streamlit as st
import plotly.graph_objects as go
from database import create_tables, get_connection
create_tables()

st.set_page_config(
    page_title="Alumni Management System",
    page_icon="🎓",
    layout="wide"
)
st.markdown("""
<style>

/* Fix form labels */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stSelectbox label,
.stCheckbox label {
    color: #092A55 !important;
    font-weight: 600 !important;
}

/* Fix text input fields */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background-color: #FFFFFF !important;
    color: #092A55 !important;
    -webkit-text-fill-color: #092A55 !important;
}

/* Fix dropdown fields */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #092A55 !important;
    border: 1px solid #D1D5DB !important;
}

[data-baseweb="select"] span {
    color: #092A55 !important;
}

/* Fix date and number controls */
.stDateInput button,
.stNumberInput button {
    color: #092A55 !important;
}

/* Fix form buttons */
.stButton button,
.stFormSubmitButton button {
    background-color: #B3082A !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.stButton button p,
.stFormSubmitButton button p {
    color: #FFFFFF !important;
}

.stApp {
    background-color: #F7F8FA;
    color: #092A55;
}

[data-testid="stSidebar"] {
    background-color: #092A55;
}

/* Howard red for the second and fourth cards */
[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"],
[data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"] {
    background-color: #B3082A;
}


[data-testid="stSidebar"] * {
    color: white;
}

h1, h2, h3 {
    color: #092A55;
}

.stButton > button {
    background-color: #B3082A;
    color: white;
    border-radius: 8px;
}

[data-testid="stMetric"] {
    background-color: #092A55;
    padding: 20px;
    border-radius: 12px;
}

[data-testid="stMetric"] * {
    color: white;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div style="background: linear-gradient(110deg, #092A55, #163E73); padding: 40px; border-left: 7px solid #B3082A; border-radius: 12px; margin-bottom: 25px;">
<h1 style="color: white; font-size: 42px; font-family: Georgia, serif; margin: 0;">HOWARD UNIVERSITY</h1>
<h2 style="color: white; font-size: 28px; font-family: Georgia, serif; font-style: italic; margin-top: 12px;">Alumni Management System</h2>
<p style="color: #E8EDF5; font-size: 17px; margin-top: 20px;">Connect &nbsp; | &nbsp; Engage &nbsp; | &nbsp; Support &nbsp; | &nbsp; Give Back</p>
</div>
""", unsafe_allow_html=True)


st.sidebar.title("Navigation")

pages = [
    "Dashboard", "Alumni Registration", "Employment", "Professional Affiliations",
    "Membership", "Contributions", "Events", "Generate Mailing List",
    "Manage Alumni Records"
]
if st.session_state.get("page") not in pages:
    st.session_state["page"] = "Dashboard"
def navigate_to(destination):
    st.session_state["page"] = destination

page = st.sidebar.radio("Select a Page", pages, key="page")

st.header(page)

if page == "Dashboard":
    st.write("Welcome to the Alumni Dashboard!")
    col1, col2, col3, col4, col5 = st.columns(5)
    connection = get_connection()

    total_alumni = connection.execute(
        "SELECT COUNT(*) FROM ALUMNI"
    ).fetchone()[0]

    connection.close()

    with col1:
        st.metric("Total Registered Alumni", total_alumni)
    connection = get_connection()

    total_memberships = connection.execute(
        "SELECT COUNT(*) FROM MEMBERSHIP"
    ).fetchone()[0]

    connection.close()

    with col2:
        st.metric("Total Memberships", total_memberships)
    connection = get_connection()

    total_events = connection.execute(
        "SELECT COUNT(*) FROM EVENTS"
    ).fetchone()[0]

    connection.close()

    with col3:
        st.metric("Total Events", total_events)
    connection = get_connection()

    total_contributions = connection.execute(
        "SELECT COUNT(*) FROM CONTRIBUTION"
    ).fetchone()[0]

    connection.close()

    with col4:
        st.metric("Total Contributions", total_contributions)
    connection = get_connection()

    total_donations = connection.execute(
        "SELECT SUM(amount) FROM CONTRIBUTION"
    ).fetchone()[0]

    connection.close()

    if total_donations is None:
        total_donations = 0

    with col5:
        st.metric("Total Money Donated", f"${total_donations:,.2f}")
    

    # Dashboard Charts
    st.subheader("Alumni Analytics")

    chart1, chart2, chart3 = st.columns([1.1, 1.3, 0.9])

    # Doughnut Chart
    with chart1:
        st.markdown("#### Alumni by Degree")

        degree_counts = {
            "Bachelor's": 2,
            "Master's": 1
        }

        fig1 = go.Figure(data=[
            go.Pie(
                labels=["Bachelor's (67%)", "Master's (33%)"],
                values=list(degree_counts.values()),
                hole=0.65,
                marker=dict(
                    colors=["#092A55", "#B3082A"]
                ),
                textinfo="none",
                hoverinfo="label+percent+value"

            )
        ])

        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#092A55"),
            margin=dict(l=10, r=10, t=20, b=10),
            
height=350,
showlegend=True,

legend=dict(
    font=dict(size=13, color="#092A55"),
    orientation="v",
    x=1.0,
    y=0.5,
    xanchor="left",
    yanchor="middle"
),

annotations=[
    dict(
        text="<b>3</b><br>Alumni",
        x=0.5,
        y=0.5,
        font=dict(size=22, color="#092A55"),
        showarrow=False
    )
]
)


        st.plotly_chart(fig1, use_container_width=True)

    # Line Chart
    with chart2:
        st.markdown("#### Alumni Growth")

        months = ["Aug", "Sep", "Oct", "Nov"]
        registrations = [1, 1, 2, 3]

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=months,
            y=registrations,
            mode="lines+markers",
            line=dict(
                color="#B3082A",
                width=4
            ),
            marker=dict(
                color="#092A55",
                size=10
            ),
            fill="tozeroy",
            fillcolor="rgba(179,8,42,0.10)"
        ))

        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#092A55"),
            margin=dict(l=10, r=10, t=20, b=10),
            height=350,
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True,
                gridcolor="#E5E7EB",
                rangemode="tozero"
            )
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Upcoming Events Panel
    with chart3:
            import textwrap

            st.markdown(
            textwrap.dedent("""
            <div style="background:#B3082A; color:white;
            padding:12px 16px; border-radius:8px 8px 0 0;
            font-size:17px; font-weight:bold;">
            📅 Upcoming Events
            </div>
            """),
            unsafe_allow_html=True
        )

            st.markdown(
        textwrap.dedent("""
        <div style="background:white; padding:16px;
        border:1px solid #E5E7EB;
        border-radius:0 0 8px 8px;">

        <div style="display:flex; gap:12px; margin-bottom:22px;">
        <div style="background:#F3F4F6; padding:10px;
        border-radius:6px; text-align:center;">
        <b style="color:#B3082A;">NOV</b><br>
        <b style="font-size:24px; color:#092A55;">22</b>
        </div>

        <div style="color:#092A55;">
        <b>HU Alumni Networking Social</b><br>
        <small>6:00 PM - 9:00 PM | Washington, DC</small>
        </div>
        </div>

        <div style="display:flex; gap:12px;">
        <div style="background:#F3F4F6; padding:10px;
        border-radius:6px; text-align:center;">
        <b style="color:#B3082A;">DEC</b><br>
        <b style="font-size:24px; color:#092A55;">10</b>
        </div>

        <div style="color:#092A55;">
        <b>Alumni Career Panel</b><br>
        <small>7:00 PM - 8:30 PM | Virtual</small>
        </div>
        </div>

        <div style="text-align:center; margin-top:20px;
        color:#092A55; font-weight:bold;">
        View All Events →
        </div>

        </div>
        """),
        unsafe_allow_html=True
    )

        


        

        
        


    
    st.markdown("""
<div style="background:#092A55; color:white;
padding:12px 16px; border-radius:8px 8px 0 0;
display:flex; justify-content:space-between;
align-items:center; font-weight:bold;">
    <span>👥 Registered Alumni</span>
    


</div>
""", unsafe_allow_html=True)
    st.button("View All Alumni →", key="view_all_alumni",
              on_click=navigate_to, args=("Manage Alumni Records",))
    

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM ALUMNI")

    alumni = cursor.fetchall()

    connection.close()

    if alumni:
        import pandas as pd

        columns = [
            "Alumni ID",
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Graduation Year",
            "Degree",
            "Major"
        ]
        

        df = pd.DataFrame(alumni, columns=columns)
        

        
        
        
        styled_df = df.style.set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#F3F4F6"),
                    ("color", "#092A55"),
                    ("font-weight", "bold"),
                    ("text-align", "left"),
                    ("padding", "10px")
                ]
            },
            {
                "selector": "td",
                "props": [
                    ("color", "#092A55"),
                    ("padding", "9px"),
                    ("border-bottom", "1px solid #E5E7EB")
                ]
            },
            {
                "selector": "tr:nth-child(even)",
                "props": [
                    ("background-color", "#F9FAFB")
                ]
            }
        ]).hide(axis="index")

        st.markdown(
            styled_df.to_html(),
            unsafe_allow_html=True
        )

    else:
        st.info("No alumni registered yet.")

    st.subheader("Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("Register New Alumni", use_container_width=True,
                  on_click=navigate_to, args=("Alumni Registration",))

    with col2:
        st.button("View Alumni Records", use_container_width=True,
                  on_click=navigate_to, args=("Manage Alumni Records",))

    with col3:
        st.button("Generate Mailing List", use_container_width=True,
                  on_click=navigate_to, args=("Generate Mailing List",))


elif page == "Alumni Registration":
    st.subheader("Register New Alumni")
    with st.form("alumni_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        graduation_year = st.number_input("Graduation Year", min_value=1900, max_value=2100, value=2026)
        degree = st.text_input("Degree")
        major = st.text_input("Major")
        submitted = st.form_submit_button("Register Alumni")

    if submitted:
        if not first_name.strip() or not last_name.strip() or not email.strip():
            st.error("Please enter a first name, last name, and email.")
        else:
            connection = get_connection()
            try:
                connection.execute(
                    """INSERT INTO ALUMNI
                       (first_name, last_name, email, phone, graduation_year, degree, major)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (first_name.strip(), last_name.strip(), email.strip(), phone.strip(),
                     graduation_year, degree.strip(), major.strip())
                )
                connection.commit()
                st.success("Alumni registered successfully!")
            except sqlite3.IntegrityError:
                st.error("This email address is already registered.")
            finally:
                connection.close()

elif page == "Employment":
    st.subheader("Add Employment Record")
    connection = get_connection()
    alumni = connection.execute("SELECT alumni_id, first_name, last_name FROM ALUMNI").fetchall()
    connection.close()
    if alumni:
        alumni_options = {f"{person[1]} {person[2]} (ID: {person[0]})": person[0] for person in alumni}
        with st.form("employment_form"):
            selected_alumni = st.selectbox("Select Alumni", list(alumni_options.keys()))
            company_name = st.text_input("Company Name")
            job_title = st.text_input("Job Title")
            start_date = st.date_input("Start Date")
            currently_employed = st.checkbox("Currently Employed")
            end_date = None if currently_employed else st.date_input("End Date")
            submitted = st.form_submit_button("Save Employment Record")
        if submitted:
            if not company_name.strip():
                st.error("Company Name is required.")
            elif end_date is not None and end_date < start_date:
                st.error("End Date cannot be before Start Date.")
            else:
                connection = get_connection()
                connection.execute(
                    """INSERT INTO EMPLOYMENT (alumni_id, company_name, job_title, start_date, end_date)
                       VALUES (?, ?, ?, ?, ?)""",
                    (alumni_options[selected_alumni], company_name, job_title,
                     str(start_date), str(end_date) if end_date else None)
                )
                connection.commit()
                connection.close()
                st.success("Employment record saved successfully!")
    else:
        st.warning("Register an alumnus before adding employment records.")

elif page == "Professional Affiliations":
    st.header("Add Professional Affiliation")
    connection = get_connection()
    alumni = connection.execute("SELECT alumni_id, first_name, last_name FROM ALUMNI").fetchall()
    connection.close()
    if alumni:
        alumni_options = {f"{person[1]} {person[2]} (ID: {person[0]})": person[0] for person in alumni}
        with st.form("affiliation_form"):
            selected_alumni = st.selectbox("Select Alumni", list(alumni_options.keys()))
            organization_name = st.text_input("Organization Name")
            position = st.text_input("Position or Role")
            submitted = st.form_submit_button("Save Professional Affiliation")
        if submitted:
            if not organization_name.strip():
                st.error("Organization Name is required.")
            else:
                connection = get_connection()
                connection.execute(
                    """INSERT INTO PROFESSIONAL_AFFILIATION (alumni_id, organization_name, position)
                       VALUES (?, ?, ?)""",
                    (alumni_options[selected_alumni], organization_name, position)
                )
                connection.commit()
                connection.close()
                st.success("Professional affiliation saved successfully!")
    else:
        st.warning("Register an alumnus before adding professional affiliations.")

elif page == "Membership":
    st.header("Add Alumni Membership")
    connection = get_connection()
    alumni = connection.execute("SELECT alumni_id, first_name, last_name FROM ALUMNI").fetchall()
    connection.close()
    if alumni:
        alumni_options = {f"{person[1]} {person[2]} (ID: {person[0]})": person[0] for person in alumni}
        with st.form("membership_form"):
            selected_alumni = st.selectbox("Select Alumni", list(alumni_options.keys()))
            membership_type = st.text_input("Membership Type")
            start_date = st.date_input("Start Date")
            expiration_date = st.date_input("Expiration Date")
            submitted = st.form_submit_button("Save Membership")
        if submitted:
            if not membership_type.strip():
                st.error("Membership Type is required.")
            elif expiration_date < start_date:
                st.error("Expiration Date cannot be before Start Date.")
            else:
                connection = get_connection()
                connection.execute(
                    """INSERT INTO MEMBERSHIP (alumni_id, membership_type, start_date, expiration_date)
                       VALUES (?, ?, ?, ?)""",
                    (alumni_options[selected_alumni], membership_type, str(start_date), str(expiration_date))
                )
                connection.commit()
                connection.close()
                st.success("Membership saved successfully!")
    else:
        st.warning("Register an alumnus before adding memberships.")

elif page == "Contributions":
    st.header("Add Alumni Contribution")
    connection = get_connection()
    alumni = connection.execute("SELECT alumni_id, first_name, last_name FROM ALUMNI").fetchall()
    connection.close()
    if alumni:
        alumni_options = {f"{person[1]} {person[2]} (ID: {person[0]})": person[0] for person in alumni}
        with st.form("contribution_form"):
            selected_alumni = st.selectbox("Select Alumni", list(alumni_options.keys()))
            amount = st.number_input("Contribution Amount ($)", min_value=0.01, step=1.00)
            contribution_date = st.date_input("Contribution Date")
            payment_method = st.selectbox("Payment Method", ["Credit Card", "PayPal", "Cash", "Bank Transfer"])
            submitted = st.form_submit_button("Save Contribution")
        if submitted:
            connection = get_connection()
            connection.execute(
                """INSERT INTO CONTRIBUTION (alumni_id, amount, contribution_date, payment_method)
                   VALUES (?, ?, ?, ?)""",
                (alumni_options[selected_alumni], amount, str(contribution_date), payment_method)
            )
            connection.commit()
            connection.close()
            st.success("Contribution saved successfully!")
    else:
        st.warning("Register an alumnus before adding contributions.")

elif page == "Events":
    st.header("Add Alumni Event")
    connection = get_connection()
    alumni = connection.execute("SELECT alumni_id, first_name, last_name FROM ALUMNI").fetchall()
    connection.close()
    if alumni:
        alumni_options = {f"{person[1]} {person[2]} (ID: {person[0]})": person[0] for person in alumni}
        with st.form("event_form"):
            selected_alumni = st.selectbox("Select Alumni", list(alumni_options.keys()))
            event_name = st.text_input("Event Name")
            event_date = st.date_input("Event Date")
            location = st.text_input("Event Location")
            submitted = st.form_submit_button("Save Event")
        if submitted:
            if not event_name.strip():
                st.error("Event Name is required.")
            else:
                connection = get_connection()
                connection.execute(
                    """INSERT INTO EVENTS (alumni_id, event_name, event_date, location)
                       VALUES (?, ?, ?, ?)""",
                    (alumni_options[selected_alumni], event_name, str(event_date), location)
                )
                connection.commit()
                connection.close()
                st.success("Event saved successfully!")
    else:
        st.warning("Register an alumnus before adding events.")

elif page == "Generate Mailing List":
    st.subheader("Generate Alumni Mailing List")
    connection = get_connection()
    alumni = connection.execute("SELECT first_name, last_name, email FROM ALUMNI").fetchall()
    connection.close()
    if alumni:
        import pandas as pd
        df = pd.DataFrame(alumni, columns=["First Name", "Last Name", "Email"])
        st.dataframe(df)
        csv = df.to_csv(index=False)
        st.download_button(label="Download Mailing List", data=csv,
                           file_name="howard_alumni_mailing_list.csv", mime="text/csv")
    else:
        st.warning("No alumni records found.")

elif page == "Manage Alumni Records":
    st.subheader("Manage Alumni Records")
    connection = get_connection()
    alumni = connection.execute("SELECT * FROM ALUMNI").fetchall()
    connection.close()
    if alumni:
        import pandas as pd
        df = pd.DataFrame(alumni)
        search = st.text_input("Search Alumni by Name")
        if search:
            df = df[
                df[1].astype(str).str.contains(search, case=False, regex=False) |
                df[2].astype(str).str.contains(search, case=False, regex=False)
            ]
        st.dataframe(df)
        st.subheader("Edit Alumni Information")
        selected_id = st.selectbox("Select Alumni ID to Edit", [row[0] for row in alumni])
        selected_alumni = next(row for row in alumni if row[0] == selected_id)
        st.write("Selected Alumni:", selected_alumni[1], selected_alumni[2])
        with st.form("edit_alumni_form"):
            first_name = st.text_input("First Name", value=selected_alumni[1])
            last_name = st.text_input("Last Name", value=selected_alumni[2])
            email = st.text_input("Email", value=selected_alumni[3])
            phone = st.text_input("Phone Number", value=selected_alumni[4])
            submitted = st.form_submit_button("Update Alumni")
        if submitted:
            connection = get_connection()
            connection.execute(
                """UPDATE ALUMNI SET first_name = ?, last_name = ?, email = ?, phone = ?
                   WHERE alumni_id = ?""",
                (first_name, last_name, email, phone, selected_id)
            )
            connection.commit()
            connection.close()
            st.success("Alumni information updated successfully!")
            st.rerun()
    else:
        st.warning("No alumni records found.")
