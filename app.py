from flask import Flask, send_file, request, render_template
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

app = Flask(__name__)

# HTML template for the form
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Barcode Generator</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>Barcode Generator</h1>
        <form action="/" method="post">
            <label for="barcodeText">Enter text for barcode:</label>
            <input type="text" id="barcodeText" name="barcodeText" required>
            <button type="submit">Generate Barcode</button>
        </form>
        {% if barcode_url %}
        <h2>Generated Barcode:</h2>
        <img src="{{ barcode_url }}" alt="Barcode">
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def generate_barcode():
    barcode_url = None
    if request.method == 'POST':
        text = request.form['barcodeText']
        # Generate barcode
        Code128 = barcode.get_barcode_class('code128')
        barcode_instance = Code128(text, writer=ImageWriter())
        
        # Create an in-memory buffer
        buffer = BytesIO()
        barcode_instance.write(buffer)
        buffer.seek(0)

        # Generate a URL for the barcode image
        barcode_url = '/static/barcode.png'
        with open('static/barcode.png', 'wb') as f:
            f.write(buffer.getvalue())
    
    return render_template('index.html', barcode_url=barcode_url)

if __name__ == '__main__':
    app.run(debug=True)
