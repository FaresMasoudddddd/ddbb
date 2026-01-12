from flask import render_template, request, redirect, url_for
from db import get_connection


def register_reservation_routes(app):

    @app.route("/reservations")
    def reservations():
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT
                    r.reservation_id,
                    r.check_in,
                    r.check_out,
                    r.guest_id,
                    r.room_id
                FROM Reservation r
                ORDER BY r.reservation_id
            """)
            rows = cur.fetchall()

            res_list = []
            for row in rows:
                res_list.append({
                    "reservation_id": row[0],
                    "check_in": row[1],
                    "check_out": row[2],
                    "guest_id": row[3],
                    "room_id": row[4],
                })

            return render_template("reservations.html", reservations=res_list)
        finally:
            cur.close()
            conn.close()


    @app.route("/reservations/add", methods=["POST"])
    def add_reservation():
        reservation_id = request.form["reservation_id"]
        guest_id = request.form["guest_id"]
        room_id = request.form["room_id"]
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO Reservation (reservation_id, check_in, check_out, guest_id, room_id)
                VALUES (:1, TO_DATE(:2,'YYYY-MM-DD'), TO_DATE(:3,'YYYY-MM-DD'), :4, :5)
            """, (reservation_id, check_in, check_out, guest_id, room_id))
            conn.commit()
            return redirect(url_for("reservations"))
        finally:
            cur.close()
            conn.close()


    @app.route("/reservations/update", methods=["POST"])
    def update_reservation():
        reservation_id = request.form["reservation_id"]
        guest_id = request.form["guest_id"]
        room_id = request.form["room_id"]
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE Reservation
                SET check_in = TO_DATE(:1,'YYYY-MM-DD'),
                    check_out = TO_DATE(:2,'YYYY-MM-DD'),
                    guest_id = :3,
                    room_id = :4
                WHERE reservation_id = :5
            """, (check_in, check_out, guest_id, room_id, reservation_id))
            conn.commit()
            return redirect(url_for("reservations"))
        finally:
            cur.close()
            conn.close()


    @app.route("/reservations/delete", methods=["POST"])
    def delete_reservation():
        reservation_id = request.form["reservation_id"]

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Reservation WHERE reservation_id = :1", (reservation_id,))
            conn.commit()
            return redirect(url_for("reservations"))
        finally:
            cur.close()
            conn.close()
