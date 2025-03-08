from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
from datetime import datetime
from update import update_tote

app = Flask(__name__)
app.secret_key = "your_secret_key"

# File path to the CSV
file_path = '/Users/isaacbattles/Desktop/TrimApp/App/Data/Tote Log 2024.csv'

# Home route with form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get form data
            tote_number = int(request.form["tote_number"])
            trimmer = request.form["trimmer"]
            flower = float(request.form["flower"])
            smalls = float(request.form["smalls"])
            weight = float(request.form["weight"])
            trim = float(request.form["trim"])
            trash = float(request.form["trash"])

            # Automatically set the current date
            current_date = datetime.now().strftime("%Y-%m-%d")

            # Prepare updates dictionary
            updates = {
                "Date": current_date,
                "Trimmer #": trimmer,
                "Flower": flower,
                "Smalls": smalls,
                "Original Tote Wt.": weight,
                "Trim": trim,
                "Trash": trash,
            }

            # Load the CSV data
            data = pd.read_csv(file_path)
            data['Tote #'] = pd.to_numeric(data['Tote #'], errors='coerce').dropna().astype(int)

            # Update the tote
            result = update_tote(data, file_path, tote_number, updates)

            # Flash messages based on the result
            if result == "success":
                flash("Tote updated successfully!", "success")
            elif result == "duplicate":
                flash("Duplicate entry detected! No changes were made.", "warning")
            else:
                flash("Tote number not found!", "error")

        except ValueError as e:
            # Handle invalid input (e.g., non-numeric values)
            flash(f"Invalid input: {str(e)}", "error")
        except Exception as e:
            # Handle any other unexpected errors
            flash(f"An error occurred: {str(e)}", "error")

        # Redirect back to the form
        return redirect(url_for("index"))

    # Render the form template for GET requests
    return render_template("index.html")

# API endpoint to check tote number
@app.route("/check_tote", methods=["GET"])
def check_tote():
    tote_number = request.args.get("tote_number")
    data = pd.read_csv(file_path)

    # Convert 'Tote #' column to integers
    data['Tote #'] = pd.to_numeric(data['Tote #'], errors='coerce').dropna().astype(int)

    # Check if the tote number exists (compare as strings)
    tote_row = data[data['Tote #'].astype(str) == str(tote_number)]
    if tote_row.empty:
        return jsonify({"status": "not_found"})

    # Check if the row is empty (excluding the 'Date' column)
    is_empty = tote_row.iloc[:, 1:].isnull().all().all()

    if is_empty:
        return jsonify({"status": "empty"})
    else:
        return jsonify({"status": "duplicate"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)