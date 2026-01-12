from flask import render_template, request
from db import get_connection

def register_report_routes(app):

    @app.route("/reports", methods=["GET"])
    def reports():
        return render_template("reports.html", report=None, report_name="")

    @app.route("/reports", methods=["POST"])
    def generate_report():
        entity = request.form.get("entity")

        conn = get_connection()
        cur = conn.cursor()

        # Simple reports (you can add more later)
        queries = {
            "guests": ("Guests List",
                       "SELECT guest_id, first_name, last_name, email FROM Guest ORDER BY guest_id"),
            "employees": ("Employees List",
                          "SELECT employee_id, emp_first_name, emp_last_name, hourly_rate FROM Employee ORDER BY employee_id"),
            "rooms": ("Rooms List",
                      "SELECT room_id, room_type, price_per_night, current_status FROM Rooms ORDER BY room_id"),
            "reservations": ("Reservations List",
                             "SELECT reservation_id, guest_id, room_id, check_in, check_out FROM Reservation ORDER BY reservation_id"),
            "services": ("Services List",
                         "SELECT service_id, service_name, price FROM Service ORDER BY service_id"),
            "payments": ("Payments List",
                         "SELECT payment_id, guest_id, amount, payment_method, payment_date FROM Payment ORDER BY payment_id"),
            "departments": ("Departments List",
                            "SELECT dep_id, department_name, location, mgr_id FROM Department ORDER BY dep_id"),
        }

        if entity not in queries:
            cur.close()
            conn.close()
            return render_template("reports.html", report=None, report_name="Invalid selection")

        report_name, sql = queries[entity]
        cur.execute(sql)

        cols = [d[0] for d in cur.description]
        data = cur.fetchall()

        cur.close()
        conn.close()

        report = {"columns": cols, "data": data}
        return render_template("reports.html", report=report, report_name=report_name)
