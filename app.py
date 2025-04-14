from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = MongoClient("mongodb://localhost:27017/nikhildb")
db = client.travel_tourism
contact_collection = db.contact_us
booking_collection = db.bookings

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/destinations')
def destinations():
    return render_template('destinations.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if name and email and message:
            contact_collection.insert_one({
                'name': name,
                'email': email,
                'message': message,
                'timestamp': datetime.utcnow()
            })
            flash('Message sent successfully!', 'success')
        else:
            flash('Please fill in all fields.', 'danger')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        destination = request.form['destination']
        date = request.form['date']

        if name and email and destination and date:
            db.bookings.insert_one({
                'name': name,
                'email': email,
                'destination': destination,
                'date': date,
                'timestamp': datetime.utcnow()
            })
            flash('Booking submitted successfully!', 'success')
        else:
            flash('Please fill in all fields.', 'danger')
        return redirect(url_for('booking'))

    return render_template('booking.html')


if __name__ == '__main__':
    app.run(debug=True)
