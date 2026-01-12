from flask import render_template, request, redirect, url_for
from db import get_connection


def register_employee_routes(app):

    # =========================
    # VIEW ALL EMPLOYEES
    # =========================
    @app.route("/employees")
    def employees():
        conn = get_connection()
        cur = conn.cursor()

        # One row per employee (phone/email via subqueries to avoid duplicates)
        cur.execute("""
            SELECT
                e.employee_id,
                e.emp_first_name,
                e.emp_last_name,
                e.hours_worked,
                e.start_date,
                e.hourly_rate,
                e.emp_date_of_birth,

                (SELECT pn.p_number
                 FROM Phone_Number pn
                 WHERE pn.emp_id = e.employee_id
                 FETCH FIRST 1 ROWS ONLY) AS phone,

                (SELECT em.email
                 FROM Email em
                 WHERE em.emp_id = e.employee_id
                 FETCH FIRST 1 ROWS ONLY) AS email,

                e.super_id,
                (SELECT s.emp_first_name || ' ' || s.emp_last_name
                 FROM Employee s
                 WHERE s.employee_id = e.super_id) AS supervisor_name,

                e.general_staff_flag,
                e.manager_flag,
                e.dep_id,
                (SELECT d.department_name
                 FROM Department d
                 WHERE d.dep_id = e.dep_id) AS dep_name

            FROM Employee e
            ORDER BY e.employee_id
        """)

        employees_list = []
        for row in cur.fetchall():
            employees_list.append({
                "employee_id": row[0],
                "emp_name": f"{row[1]} {row[2]}",
                "hours_worked": row[3],
                "start_date": row[4],
                "hourly_rate": row[5],
                "emp_date_of_birth": row[6],
                "phone": row[7],
                "email": row[8],
                "super_id": row[9],
                "super_name": row[10],
                "general_staff_flag": row[11],
                "manager_flag": row[12],
                "dep_id": row[13],
                "dep_name": row[14],
            })

        cur.close()
        conn.close()
        return render_template("employees.html", employees=employees_list)

    # =========================
    # ADD EMPLOYEE
    # =========================
    @app.route("/employees/add", methods=["POST"])
    def add_employee():
        employee_id = request.form.get("employee_id")
        emp_first_name = request.form.get("emp_first_name")
        emp_last_name = request.form.get("emp_last_name")
        hours_worked = request.form.get("hours_worked")
        start_date = request.form.get("start_date")
        hourly_rate = request.form.get("hourly_rate")
        emp_date_of_birth = request.form.get("emp_date_of_birth")

        phone = request.form.get("phone")
        email = request.form.get("email")

        super_id = request.form.get("super_id")  # optional
        general_staff_flag = request.form.get("general_staff_flag")
        manager_flag = request.form.get("manager_flag")
        dep_id = request.form.get("dep_id")

        # Required fields check
        required = [employee_id, emp_first_name, emp_last_name, hours_worked, start_date,
                    hourly_rate, general_staff_flag, manager_flag, dep_id, phone, email]
        if any(v is None or str(v).strip() == "" for v in required):
            return "Missing required fields", 400

        conn = get_connection()
        cur = conn.cursor()

        # Insert employee
        cur.execute("""
            INSERT INTO Employee (
                employee_id, emp_first_name, emp_last_name, hours_worked,
                start_date, hourly_rate, emp_date_of_birth,
                super_id, general_staff_flag, manager_flag, dep_id
            )
            VALUES (
                :employee_id, :emp_first_name, :emp_last_name, :hours_worked,
                TO_DATE(:start_date, 'YYYY-MM-DD'),
                :hourly_rate,
                CASE
                    WHEN :emp_date_of_birth IS NULL OR :emp_date_of_birth = '' THEN NULL
                    ELSE TO_DATE(:emp_date_of_birth, 'YYYY-MM-DD')
                END,
                CASE
                    WHEN :super_id IS NULL OR :super_id = '' THEN NULL
                    ELSE :super_id
                END,
                :general_staff_flag, :manager_flag, :dep_id
            )
        """, {
            "employee_id": employee_id,
            "emp_first_name": emp_first_name,
            "emp_last_name": emp_last_name,
            "hours_worked": hours_worked,
            "start_date": start_date,
            "hourly_rate": hourly_rate,
            "emp_date_of_birth": emp_date_of_birth,
            "super_id": super_id,
            "general_staff_flag": general_staff_flag,
            "manager_flag": manager_flag,
            "dep_id": dep_id
        })

        # Insert phone + email (composite PK tables)
        cur.execute("""
            INSERT INTO Phone_Number (p_number, emp_id)
            VALUES (:p_number, :emp_id)
        """, {"p_number": phone, "emp_id": employee_id})

        cur.execute("""
            INSERT INTO Email (email, emp_id)
            VALUES (:email, :emp_id)
        """, {"email": email, "emp_id": employee_id})

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("employees"))

    # =========================
    # UPDATE EMPLOYEE
    # =========================
    @app.route("/employees/update", methods=["POST"])
    def update_employee():
        employee_id = request.form.get("employee_id")
        emp_first_name = request.form.get("emp_first_name")
        emp_last_name = request.form.get("emp_last_name")
        hours_worked = request.form.get("hours_worked")
        start_date = request.form.get("start_date")
        hourly_rate = request.form.get("hourly_rate")
        emp_date_of_birth = request.form.get("emp_date_of_birth")

        phone = request.form.get("phone")
        email = request.form.get("email")

        super_id = request.form.get("super_id")
        general_staff_flag = request.form.get("general_staff_flag")
        manager_flag = request.form.get("manager_flag")
        dep_id = request.form.get("dep_id")

        if not employee_id:
            return "Employee ID required", 400

        conn = get_connection()
        cur = conn.cursor()

        # Update employee main row
        cur.execute("""
            UPDATE Employee
            SET
                emp_first_name = :emp_first_name,
                emp_last_name = :emp_last_name,
                hours_worked = :hours_worked,
                start_date = TO_DATE(:start_date, 'YYYY-MM-DD'),
                hourly_rate = :hourly_rate,
                emp_date_of_birth =
                    CASE
                        WHEN :emp_date_of_birth IS NULL OR :emp_date_of_birth = '' THEN NULL
                        ELSE TO_DATE(:emp_date_of_birth, 'YYYY-MM-DD')
                    END,
                super_id =
                    CASE
                        WHEN :super_id IS NULL OR :super_id = '' THEN NULL
                        ELSE :super_id
                    END,
                general_staff_flag = :general_staff_flag,
                manager_flag = :manager_flag,
                dep_id = :dep_id
            WHERE employee_id = :employee_id
        """, {
            "employee_id": employee_id,
            "emp_first_name": emp_first_name,
            "emp_last_name": emp_last_name,
            "hours_worked": hours_worked,
            "start_date": start_date,
            "hourly_rate": hourly_rate,
            "emp_date_of_birth": emp_date_of_birth,
            "super_id": super_id,
            "general_staff_flag": general_staff_flag,
            "manager_flag": manager_flag,
            "dep_id": dep_id
        })

        # Update phone: easiest delete + insert (since composite PK)
        if phone and str(phone).strip() != "":
            cur.execute("DELETE FROM Phone_Number WHERE emp_id = :emp_id", {"emp_id": employee_id})
            cur.execute("""
                INSERT INTO Phone_Number (p_number, emp_id)
                VALUES (:p_number, :emp_id)
            """, {"p_number": phone, "emp_id": employee_id})

        # Update email: delete + insert
        if email and str(email).strip() != "":
            cur.execute("DELETE FROM Email WHERE emp_id = :emp_id", {"emp_id": employee_id})
            cur.execute("""
                INSERT INTO Email (email, emp_id)
                VALUES (:email, :emp_id)
            """, {"email": email, "emp_id": employee_id})

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("employees"))

    # =========================
    # DELETE EMPLOYEE
    # =========================
    @app.route("/employees/delete", methods=["POST"])
    def delete_employee():
        employee_id = request.form.get("employee_id")
        if not employee_id:
            return "Employee ID required", 400

        conn = get_connection()
        cur = conn.cursor()

        # Must delete children first
        cur.execute("DELETE FROM Phone_Number WHERE emp_id = :emp_id", {"emp_id": employee_id})
        cur.execute("DELETE FROM Email WHERE emp_id = :emp_id", {"emp_id": employee_id})

        # If this employee is a manager in department, set mgr_id null first
        cur.execute("UPDATE Department SET mgr_id = NULL WHERE mgr_id = :emp_id", {"emp_id": employee_id})

        # If other employees reference him as supervisor, set super_id null
        cur.execute("UPDATE Employee SET super_id = NULL WHERE super_id = :emp_id", {"emp_id": employee_id})

        cur.execute("DELETE FROM Employee WHERE employee_id = :emp_id", {"emp_id": employee_id})

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("employees"))
