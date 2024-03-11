from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
toolbar = DebugToolbarExtension(app)

# List of currencies
currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CNY', 'AUD', 'CAD', 'CHF', 'HKD', 'SGD', 'SEK', 'KRW', 'NOK', 'NZD',
              'INR', 'MXN', 'TWD', 'ZAR', 'BRL', 'DKK', 'PLN', 'THB', 'ILS', 'IDR', 'CZK', 'AED', 'TRY', 'HUF',
              'CLP', 'SAR', 'PHP', 'MYR', 'COP', 'RUB', 'RON', 'PEN', 'BHD', 'BGN', 'ARS']

@app.route('/')
def index():
    error_message = ''
    return render_template('index.html', currencies=currencies, error_message=error_message)

@app.route('/plot', methods=['POST'])
def plot():
    currency1 = request.form['currency1']
    currency2 = request.form['currency2']
    start_date = pd.to_datetime(request.form['start_date'])
    end_date = pd.to_datetime(request.form['end_date'])
    print("Start Date:", start_date)

    if currency1 == currency2:
        error_message = "Please select different currencies."
        return render_template('index.html', currencies=currencies, error_message=error_message)
    if pd.isna(start_date) or pd.isna(end_date):
        error_message = "Please select dates."
        return render_template('index.html', currencies=currencies, error_message=error_message)

    pair = f'{currency1}{currency2}=X'
    data = yf.download(pair, start=start_date, end=end_date)

    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'])
    plt.title(f'Historical Data for {currency1}/{currency2}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.grid(True)

    # Convert plot to base64 to embed in HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template('plot.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True)
