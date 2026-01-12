from flask import render_template, request, redirect, url_for
from db import get_connection


def register_guest_routes(app):

    # =========================
    # VIEW ALL GUESTS
    # =========================
    @app.route("/guests")
    def guests():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                guest_id,
                first_name || ' ' || last_name AS full_name,
                date_of_birth,
                email
            FROM Guest
            ORDER BY guest_id
        """)

        guests = []
        for row in cur.fetchall():
            guests.append({
                "guest_id": row[0],
                "name": row[1],
                "date_of_birth": row[2],
                "email": row[3]
            })

        cur.close()
        conn.close()

        return render_template("guests.html", guests=guests)

    # =========================
    # ADD GUEST
    # =========================
    @app.route("/guests/add", methods=["POST"])
    def add_guest():
        guest_id = request.form.get("guest_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        email = request.form.get("email")

        if not guest_id or not first_name or not last_name or not email:
            return "Missing required fields", 400

        conn = get_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO Guest
            (guest_id, first_name, last_name, date_of_birth, email)
            VALUES
            (
                :guest_id,
                :first_name,
                :last_name,
                CASE
                    WHEN :date_of_birth IS NULL OR :date_of_birth = ''
                    THEN NULL
                    ELSE TO_DATE(:date_of_birth, 'YYYY-MM-DD')
                END,
                :email
            )
        """

        cur.execute(sql, {
            "guest_id": guest_id,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "email": email
        })

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("guests"))

    # =========================
    # UPDATE GUEST
    # =========================
    @app.route("/guests/update", methods=["POST"])
    def update_guest():
        guest_id = request.form.get("guest_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        email = request.form.get("email")

        if not guest_id:
            return "Guest ID required", 400

        conn = get_connection()
        cur = conn.cursor()

        sql = """
            UPDATE Guest
            SET
                first_name = :first_name,
                last_name = :last_name,
                date_of_birth =
                    CASE
                        WHEN :date_of_birth IS NULL OR :date_of_birth = ''
                        THEN NULL
                        ELSE TO_DATE(:date_of_birth, 'YYYY-MM-DD')
                    END,
                email = :email
            WHERE guest_id = :guest_id
        """

        cur.execute(sql, {
            "guest_id": guest_id,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "email": email
        })

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("guests"))

    # =========================
    # DELETE GUEST
    # =========================
    @app.route("/guests/delete", methods=["POST"])
    def delete_guest():
        guest_id = request.form.get("guest_id")

        if not guest_id:
            return "Guest ID required", 400

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM Guest WHERE guest_id = :guest_id",
            {"guest_id": guest_id}
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("guests"))
