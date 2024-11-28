from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import MySQLdb
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="kiragg0101",
    db="AutoDealerDB"
)
cursor = db.cursor()

@app.route('/')
def index():
    tables = ["Vehicles", "Customers", "Sales", "Services", "Suppliers"]
    return render_template('index.html', tables=tables)

@app.route('/view_table/<table>')
def view_table(table):
    try:
        cursor.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        return render_template('view_table.html', table=table, columns=columns, data=data)
    except MySQLdb.Error as e:
        flash(f"Помилка під час завантаження таблиці: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/add_record/<table>', methods=['GET', 'POST'])
def add_record(table):
    try:
        cursor.execute(f"DESCRIBE {table}")
        columns = [desc[0] for desc in cursor.fetchall() if desc[3] != 'auto_increment']

        if request.method == 'POST':
            values = [request.form.get(column) for column in columns]
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            db.commit()
            flash("Запис успішно додано!", "success")
            return redirect(url_for('view_table', table=table))

        return render_template('add_record.html', table=table, columns=columns)
    except MySQLdb.Error as e:
        flash(f"Помилка під час додавання запису: {e}", "danger")
        return redirect(url_for('view_table', table=table))

@app.route('/delete/<table>/<int:record_id>')
def delete_record(table, record_id):
    try:
        if table == 'Customers':
            query = f"DELETE FROM {table} WHERE customer_id = %s"
        else:
            query = f"DELETE FROM {table} WHERE {table[:-1]}_id = %s"
        cursor.execute(query, (record_id,))
        db.commit()
        flash("Запис успішно видалено!", "success")
    except MySQLdb.Error as e:
        flash(f"Помилка під час видалення запису: {e}", "danger")
    return redirect(url_for('view_table', table=table))

@app.route('/report/<table>')
def generate_report(table):
    try:
        cursor.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        df = pd.DataFrame(data, columns=columns)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=table)
        output.seek(0)

        return send_file(output, download_name=f"{table}_report.xlsx", as_attachment=True)
    except MySQLdb.Error as e:
        flash(f"Помилка під час створення звіту: {e}", "danger")
        return redirect(url_for('view_table', table=table))

if __name__ == '__main__':
    app.run(debug=True)



