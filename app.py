import sqlite3
import streamlit as st
from database import create_tables, get_connection
create_tables()

st.set_page_config(
    page_title="Alumni Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Alumni Management System")

st.write("Welcome to the Alumni Management System!")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a Page",
    [
        "Dashboard",
        "Alumni Registration",
        "Employment",
        "Professional Affiliations",
        "Membership",
        "Contributions",
        "Events"
    ]
)

st.header(page)

if page == "Dashboard":
    st.write("Welcome to the Alumni Dashboard!")
    st.subheader("Registered Alumni")

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
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No alumni registered yet.")

elif page == "Alumni Registration":
    st.subheader("Register New Alumni")

    with st.form("alumni_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        graduation_year = st.number_input(
            "Graduation Year",
            min_value=1900,
            max_value=2100,
            value=2026
        )
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
                        """
                        INSERT INTO ALUMNI
                        (first_name, last_name, email, phone,
                         graduation_year, degree, major)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            first_name.strip(),
                            last_name.strip(),
                            email.strip(),
                            phone.strip(),
                            graduation_year,
                            degree.strip(),
                            major.strip()
                        )
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

         alumni = connection.execute(
            "SELECT alumni_id, first_name, last_name FROM ALUMNI"
        ).fetchall()

         connection.close()

         if alumni:
            alumni_options = {
                f"{person[1]} {person[2]} (ID: {person[0]})": person[0]
                for person in alumni
            }

            with st.form("employment_form"):
                selected_alumni = st.selectbox(
                    "Select Alumni",
                    list(alumni_options.keys())
                )

                company_name = st.text_input("Company Name")
                job_title = st.text_input("Job Title")
                start_date = st.date_input("Start Date")

                currently_employed = st.checkbox(
                "Currently Employed"
            )

                if currently_employed:
                  end_date = None
                else:
                  end_date = st.date_input("End Date")

                submitted = st.form_submit_button(
                    "Save Employment Record"
                )

            if submitted:
                if not company_name.strip():
                    st.error("Company Name is required.")
                elif end_date is not None and end_date < start_date:
                    st.error("End Date cannot be before Start Date.")
                else:
                    connection = get_connection()

                    connection.execute(
                        """
                        INSERT INTO EMPLOYMENT
                        (alumni_id, company_name, job_title,
                         start_date, end_date)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            alumni_options[selected_alumni],
                            company_name,
                            job_title,
                            str(start_date),
                            str(end_date) if end_date else None
                        )
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        "Employment record saved successfully!"
                    )

            else:
                    st.warning(
                    "Register an alumnus before adding employment records."
                )

elif page == "Professional Affiliations":
    st.write("Manage professional affiliations.")

elif page == "Membership":
    st.write("Manage alumni memberships.")

elif page == "Contributions":
    st.write("Manage alumni donations and contributions.")

elif page == "Events":
    st.write("Manage alumni events.")