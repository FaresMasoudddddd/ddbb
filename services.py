# services.py
from flask import render_template, request, redirect, url_for
from db import get_connection


def register_service_routes(app):

    # ---------- LIST ----------
    @app.route("/services", endpoint="services")
    def services():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT service_id,
                   service_name,
                   price,
                   spa_service_flag,
                   room_service_flag,
                   restaurant_service_flag,
                   laundry_service_flag
            FROM Service
            ORDER BY service_id
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        services_list = []
        for r in rows:
            services_list.append({
                "service_id": r[0],
                "service_name": r[1],
                "price": r[2],
                "spa": r[3],
                "room": r[4],
                "restaurant": r[5],
                "laundry": r[6],
            })

        return render_template("services.html", services=services_list)

    # ---------- ADD ----------
    @app.route("/services/add", methods=["POST"], endpoint="add_service")
    def add_service():
        service_id = request.form.get("service_id")
        service_name = request.form.get("service_name")
        price = request.form.get("price")

        spa = request.form.get("spa", "N").upper().strip()
        room = request.form.get("room", "N").upper().strip()
        restaurant = request.form.get("restaurant", "N").upper().strip()
        laundry = request.form.get("laundry", "N").upper().strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Service (
                service_id, service_name, price,
                spa_service_flag, room_service_flag, restaurant_service_flag, laundry_service_flag
            )
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, (service_id, service_name, price, spa, room, restaurant, laundry))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("services"))

    # ---------- UPDATE ----------
    @app.route("/services/update", methods=["POST"], endpoint="update_service")
    def update_service():
        service_id = request.form.get("service_id")
        service_name = request.form.get("service_name")
        price = request.form.get("price")

        spa = request.form.get("spa", "N").upper().strip()
        room = request.form.get("room", "N").upper().strip()
        restaurant = request.form.get("restaurant", "N").upper().strip()
        laundry = request.form.get("laundry", "N").upper().strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE Service
               SET service_name = :1,
                   price = :2,
                   spa_service_flag = :3,
                   room_service_flag = :4,
                   restaurant_service_flag = :5,
                   laundry_service_flag = :6
             WHERE service_id = :7
        """, (service_name, price, spa, room, restaurant, laundry, service_id))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("services"))

    # ---------- DELETE ----------
    @app.route("/services/delete", methods=["POST"], endpoint="delete_service")
    def delete_service():
        service_id = request.form.get("service_id")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Service WHERE service_id = :1", (service_id,))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("services"))
