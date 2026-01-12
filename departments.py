from flask import render_template, request, redirect, url_for
from db import get_connection


def register_department_routes(app):

    @app.get("/departments")
    def departments():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                d.dep_id,
                d.department_name,
                d.location,
                d.mgr_id,
                d.hiring_date
            FROM Department d
            ORDER BY d.dep_id
        """)

        departments = []
        for row in cur.fetchall():
            departments.append({
                "dep_id": row[0],
                "department_name": row[1],
                "location": row[2],
                "mgr_id": row[3],
                "hiring_date": row[4]
            })

        cur.close()
        conn.close()
        return render_template("departments.html", departments=departments)

    @app.post("/departments/add")
    def add_department():
        dep_id = request.form["dep_id"]
        department_name = request.form["department_name"]
        location = request.form["location"]
        mgr_id = request.form.get("mgr_id", "").strip()
        hiring_date = request.form["hiring_date"]

        conn = get_connection()
        cur = conn.cursor()

        # mgr_id optional
        mgr_id_val = None if mgr_id == "" else mgr_id

        cur.execute("""
            INSERT INTO Department (dep_id, department_name, location, mgr_id, hiring_date)
            VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'))
        """, (dep_id, department_name, location, mgr_id_val, hiring_date))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("departments"))

    @app.post("/departments/update")
    def update_department():
        dep_id = request.form["dep_id"]
        department_name = request.form["department_name"]
        location = request.form["location"]
        mgr_id = request.form.get("mgr_id", "").strip()
        hiring_date = request.form["hiring_date"]

        conn = get_connection()
        cur = conn.cursor()

        mgr_id_val = None if mgr_id == "" else mgr_id

        cur.execute("""
            UPDATE Department
            SET department_name = :1,
                location = :2,
                mgr_id = :3,
                hiring_date = TO_DATE(:4, 'YYYY-MM-DD')
            WHERE dep_id = :5
        """, (department_name, location, mgr_id_val, hiring_date, dep_id))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("departments"))

    @app.post("/departments/delete")
    def delete_department():
        dep_id = request.form["dep_id"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Department WHERE dep_id = :1", (dep_id,))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("departments"))
