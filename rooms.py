from flask import render_template, request, redirect, url_for
from db import get_connection


def register_room_routes(app):

    @app.route("/rooms")
    def rooms():
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT room_id, price_per_night, room_type, floor_number, floor_section, current_status
                FROM Rooms
                ORDER BY room_id
            """)
            rows = cur.fetchall()

            rooms_list = []
            for r in rows:
                rooms_list.append({
                    "room_id": r[0],
                    "price_per_night": r[1],
                    "room_type": r[2],
                    "floor_number": r[3],
                    "floor_section": r[4],
                    "current_status": r[5]
                })

            return render_template("rooms.html", rooms=rooms_list)
        finally:
            cur.close()
            conn.close()


    @app.route("/rooms/add", methods=["POST"])
    def add_room():
        room_id = request.form["room_id"]
        price_per_night = request.form["price_per_night"]
        room_type = request.form["room_type"]
        floor_number = request.form["floor_number"]
        floor_section = request.form.get("floor_section", "")
        current_status = request.form["current_status"]

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO Rooms (room_id, price_per_night, room_type, floor_number, floor_section, current_status)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, (room_id, price_per_night, room_type, floor_number, floor_section, current_status))
            conn.commit()
            return redirect(url_for("rooms"))
        finally:
            cur.close()
            conn.close()


    @app.route("/rooms/update", methods=["POST"])
    def update_room():
        room_id = request.form["room_id"]
        price_per_night = request.form["price_per_night"]
        room_type = request.form["room_type"]
        floor_number = request.form["floor_number"]
        floor_section = request.form.get("floor_section", "")
        current_status = request.form["current_status"]

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE Rooms
                SET price_per_night = :1,
                    room_type = :2,
                    floor_number = :3,
                    floor_section = :4,
                    current_status = :5
                WHERE room_id = :6
            """, (price_per_night, room_type, floor_number, floor_section, current_status, room_id))
            conn.commit()
            return redirect(url_for("rooms"))
        finally:
            cur.close()
            conn.close()


    @app.route("/rooms/delete", methods=["POST"])
    def delete_room():
        room_id = request.form["room_id"]

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Rooms WHERE room_id = :1", (room_id,))
            conn.commit()
            return redirect(url_for("rooms"))
        finally:
            cur.close()
            conn.close()
