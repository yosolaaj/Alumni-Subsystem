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
        "Events",
        "Generate Mailing List",
        "Manage Alumni Records",
        "Admin Login"
    ]
)

st.header(page)

if page == "Dashboard":
    st.write("Welcome to the Alumni Dashboard!")
    connection = get_connection()

    total_alumni = connection.execute(
        "SELECT COUNT(*) FROM ALUMNI"
    ).fetchone()[0]

    connection.close()

    st.metric("Total Registered Alumni", total_alumni)
    connection = get_connection()

    total_memberships = connection.execute(
        "SELECT COUNT(*) FROM MEMBERSHIP"
    ).fetchone()[0]

    connection.close()

    st.metric("Total Memberships", total_memberships)
    connection = get_connection()

    total_events = connection.execute(
        "SELECT COUNT(*) FROM EVENTS"
    ).fetchone()[0]

    connection.close()

    st.metric("Total Events", total_events)
    connection = get_connection()

    total_contributions = connection.execute(
        "SELECT COUNT(*) FROM CONTRIBUTION"
    ).fetchone()[0]

    connection.close()

    st.metric("Total Contributions", total_contributions)
    connection = get_connection()

    total_donations = connection.execute(
        "SELECT SUM(amount) FROM CONTRIBUTION"
    ).fetchone()[0]

    connection.close()

    if total_donations is None:
        total_donations = 0

    st.metric("Total Money Donated", f"${total_donations:,.2f}")
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
    st.header("Add Professional Affiliation")

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

        with st.form("affiliation_form"):
            selected_alumni = st.selectbox(
                "Select Alumni",
                list(alumni_options.keys())
            )
            organization_name = st.text_input("Organization Name")
            position = st.text_input("Position or Role")
            submitted = st.form_submit_button("Save Professional Affiliation")

        if submitted:
            if not organization_name.strip():
                st.error("Organization Name is required.")
            else:
                connection = get_connection()
                connection.execute(
                    """
                    INSERT INTO PROFESSIONAL_AFFILIATION
                    (alumni_id, organization_name, position)
                    VALUES (?, ?, ?)
                    """,
                    (
                        alumni_options[selected_alumni],
                        organization_name,
                        position
                    )
                )
                connection.commit()
                connection.close()
                st.success("Professional affiliation saved successfully!")
    else:
        st.warning("Register an alumnus before adding affiliations.")
elif page == "Membership":
    st.header("Add Alumni Membership")

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

        with st.form("membership_form"):
            selected_alumni = st.selectbox(
                "Select Alumni",
                list(alumni_options.keys())
            )
            membership_type = st.selectbox(
                "Membership Type",
                ["Annual", "Young Alumni", "Lifetime"]
            )
            start_date = st.date_input("Start Date")
            expiration_date = st.date_input("Expiration Date")
            submitted = st.form_submit_button("Save Membership")

        if submitted:
            if expiration_date < start_date:
                st.error("Expiration Date cannot be before Start Date.")
            else:
                connection = get_connection()
                connection.execute(
                    """
                    INSERT INTO MEMBERSHIP
                    (alumni_id, membership_type, start_date, expiration_date)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        alumni_options[selected_alumni],
                        membership_type,
                        str(start_date),
                        str(expiration_date)
                    )
                )
                connection.commit()
                connection.close()
                st.success("Membership saved successfully!")
    else:
        st.warning("Register an alumnus before adding memberships.")    



elif page == "Contributions":
    st.header("Add Alumni Contribution")

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

        with st.form("contribution_form"):
            selected_alumni = st.selectbox(
                "Select Alumni",
                list(alumni_options.keys())
            )

            amount = st.number_input(
                "Contribution Amount ($)",
                min_value=0.01,
                step=1.00
            )

            contribution_date = st.date_input(
                "Contribution Date"
            )

            payment_method = st.selectbox(
                "Payment Method",
                ["Credit Card", "PayPal", "Cash", "Bank Transfer"]
            )

            submitted = st.form_submit_button(
                "Save Contribution"
            )

        if submitted:
            connection = get_connection()

            connection.execute(
                """
                INSERT INTO CONTRIBUTION
                (alumni_id, amount, contribution_date, payment_method)
                VALUES (?, ?, ?, ?)
                """,
                (
                    alumni_options[selected_alumni],
                    amount,
                    str(contribution_date),
                    payment_method
                )
            )

            connection.commit()
            connection.close()

            st.success("Contribution saved successfully!")

    else:
        st.warning("Register an alumnus before adding contributions.")

elif page == "Events":
    st.header("Add Alumni Event")

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

        with st.form("event_form"):
            selected_alumni = st.selectbox(
                "Select Alumni",
                list(alumni_options.keys())
            )

            event_name = st.text_input(
                "Event Name"
            )

            event_date = st.date_input(
                "Event Date"
            )

            location = st.text_input(
                "Event Location"
            )

            submitted = st.form_submit_button(
                "Save Event"
            )

        if submitted:
            if not event_name.strip():
                st.error("Event Name is required.")
            else:
                connection = get_connection()

                connection.execute(
                    """
                    INSERT INTO EVENTS
                    (alumni_id, event_name, event_date, location)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        alumni_options[selected_alumni],
                        event_name,
                        str(event_date),
                        location
                    )
                )

                connection.commit()
                connection.close()

                st.success("Event saved successfully!")

    else:
        st.warning("Register an alumnus before adding events.")

elif page == "Generate Mailing List":
    st.subheader("Generate Alumni Mailing List")

    connection = get_connection()

    alumni = connection.execute(
        "SELECT first_name, last_name, email FROM ALUMNI"
    ).fetchall()

    connection.close()

    if alumni:
        import pandas as pd

        df = pd.DataFrame(
            alumni,
            columns=["First Name", "Last Name", "Email"]
        )

        st.dataframe(df)

        csv = df.to_csv(index=False)

        st.download_button(
            label="Download Mailing List",
            data=csv,
            file_name="howard_alumni_mailing_list.csv",
            mime="text/csv"
        )

    else:
        st.warning("No alumni records found.")

elif page == "Manage Alumni Records":
    st.subheader("Manage Alumni Records")

    connection = get_connection()

    alumni = connection.execute(
        "SELECT * FROM ALUMNI"
    ).fetchall()

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

    selected_id = st.selectbox(
        "Select Alumni ID to Edit",
        [row[0] for row in alumni]
    )
    selected_alumni = next(
        row for row in alumni if row[0] == selected_id
    )

    st.write("Selected Alumni:", selected_alumni[1], selected_alumni[2])
    with st.form("edit_alumni_form"):

        first_name = st.text_input(
            "First Name",
            value=selected_alumni[1]
        )

        last_name = st.text_input(
            "Last Name",
            value=selected_alumni[2]
        )

        email = st.text_input(
            "Email",
            value=selected_alumni[3]
        )

        phone = st.text_input(
            "Phone Number",
            value=selected_alumni[4]
        )

        submitted = st.form_submit_button("Update Alumni")
    if submitted:
        connection = get_connection()

        connection.execute(
            """
            UPDATE ALUMNI
            SET first_name = ?,
                last_name = ?,
                email = ?,
                phone = ?
            WHERE alumni_id = ?
            """,
            (
                first_name,
                last_name,
                email,
                phone,
                selected_id
            )
        )

        connection.commit()
        connection.close()

        st.success("Alumni information updated successfully!")
        st.rerun()

else:
    st.warning("No alumni records found.")

if page == "Admin Login":
     st.subheader("Admin Login")

with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

if login:
        if username == "admin" and password == "admin123":
            st.success("Login successful!")
        else:
            st.error("Incorrect username or password.")
