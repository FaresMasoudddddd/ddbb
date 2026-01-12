from flask import render_template, request, redirect, url_for
from db import get_connection


def register_payment_routes(app):

    @app.route('/payments')
    def payments():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                p.payment_id,
                p.payment_date,
                p.amount,
                p.payment_method,
                g.first_name || ' ' || g.last_name AS guest_name
            FROM Payment p
            JOIN Guest g ON p.guest_id = g.guest_id
            ORDER BY p.payment_id
        """)

        payments = []
        for row in cur.fetchall():
            payments.append({
                "id": row[0],
                "date": row[1],
                "amount": row[2],
                "method": row[3],
                "guest_name": row[4]
            })

        cur.close()
        conn.close()

        return render_template("payments.html", payments=payments)


    @app.route('/payments/add', methods=['POST'])
    def add_payment():
        guest_id = request.form['guest_id']
        amount = request.form['amount']
        method = request.form['method']
        date = request.form['date']

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Payment (payment_id, guest_id, amount, payment_method, payment_date)
            VALUES (payment_seq.NEXTVAL, :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))
        """, (guest_id, amount, method, date))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('payments'))


    @app.route('/payments/update', methods=['POST'])
    def update_payment():
        payment_id = request.form['payment_id']
        guest_id = request.form['guest_id']
        amount = request.form['amount']
        method = request.form['method']
        date = request.form['date']

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE Payment
            SET guest_id = :1,
                amount = :2,
                payment_method = :3,
                payment_date = TO_DATE(:4, 'YYYY-MM-DD')
            WHERE payment_id = :5
        """, (guest_id, amount, method, date, payment_id))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('payments'))


    @app.route('/payments/delete', methods=['POST'])
    def delete_payment():
        payment_id = request.form['payment_id']

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM Payment
            WHERE payment_id = :1
        """, (payment_id,))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('payments'))
