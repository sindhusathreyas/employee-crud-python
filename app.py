from flask import Flask, render_template, request, redirect, url_for
from db import get_db_connection
import os


app = Flask(__name__)


# -------------------------
# HOME / READ
# -------------------------

@app.route("/")
def index():

    search = request.args.get("search", "")

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    if search:

        search_term = f"%{search}%"

        query = """
            SELECT *
            FROM employees
            WHERE name LIKE %s
            OR email LIKE %s
            OR department LIKE %s
            OR designation LIKE %s
            ORDER BY id DESC
        """

        cursor.execute(
            query,
            (search_term, search_term, search_term, search_term)
        )

    else:

        cursor.execute(
            "SELECT * FROM employees ORDER BY id DESC"
        )

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        employees=employees,
        search=search
    )


# -------------------------
# CREATE
# -------------------------

@app.route("/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        designation = request.form["designation"]
        salary = request.form["salary"]

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO employees
            (name, email, phone, department, designation, salary)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                name,
                email,
                phone,
                department,
                designation,
                salary
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("index"))

    return render_template("add.html")


# -------------------------
# UPDATE
# -------------------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        designation = request.form["designation"]
        salary = request.form["salary"]

        query = """
            UPDATE employees
            SET
                name = %s,
                email = %s,
                phone = %s,
                department = %s,
                designation = %s,
                salary = %s
            WHERE id = %s
        """

        cursor.execute(
            query,
            (
                name,
                email,
                phone,
                department,
                designation,
                salary,
                id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("index"))

    cursor.execute(
        "SELECT * FROM employees WHERE id = %s",
        (id,)
    )

    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit.html",
        employee=employee
    )


# -------------------------
# DELETE
# -------------------------

@app.route("/delete/<int:id>")
def delete_employee(id):

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id = %s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("index"))


# -------------------------
# RUN APPLICATION
# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))