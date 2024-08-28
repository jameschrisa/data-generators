import sys
import subprocess
import pkg_resources

def check_dependencies():
    required = {'Flask', 'Faker'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print("Some required packages are missing. Installing them now...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
        except subprocess.CalledProcessError:
            print("Failed to install required packages. Please install them manually:")
            for package in missing:
                print(f"  pip install {package}")
            sys.exit(1)
    print("All required packages are installed.")

check_dependencies()

import random
from faker import Faker
import json
from flask import Flask, render_template_string, jsonify
import webbrowser
from threading import Timer

fake = Faker()
app = Flask(__name__)

def generate_line_chart_data(num_points=7):
    labels = [fake.date_this_month().strftime("%Y-%m-%d") for _ in range(num_points)]
    datasets = [{
        "label": fake.word(),
        "data": [random.randint(0, 100) for _ in range(num_points)],
        "borderColor": f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 1)",
        "fill": False
    }]
    return {"labels": labels, "datasets": datasets}

def generate_bar_chart_data(num_categories=5):
    labels = [fake.word() for _ in range(num_categories)]
    datasets = [{
        "label": "Sales",
        "data": [random.randint(0, 1000) for _ in range(num_categories)],
        "backgroundColor": [f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.6)" for _ in range(num_categories)]
    }]
    return {"labels": labels, "datasets": datasets}

def generate_pie_chart_data(num_slices=5):
    labels = [fake.color_name() for _ in range(num_slices)]
    data = [random.randint(1, 100) for _ in range(num_slices)]
    backgroundColor = [f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.6)" for _ in range(num_slices)]
    return {"labels": labels, "datasets": [{"data": data, "backgroundColor": backgroundColor}]}

def generate_radar_chart_data(num_attributes=5):
    labels = [fake.word() for _ in range(num_attributes)]
    datasets = [{
        "label": fake.company(),
        "data": [random.randint(0, 100) for _ in range(num_attributes)],
        "backgroundColor": f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.2)",
        "borderColor": f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 1)",
    }]
    return {"labels": labels, "datasets": datasets}

def generate_scatter_chart_data(num_points=20):
    datasets = [{
        "label": fake.word(),
        "data": [{"x": random.uniform(0, 100), "y": random.uniform(0, 100)} for _ in range(num_points)],
        "backgroundColor": f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.6)"
    }]
    return {"datasets": datasets}

def generate_bubble_chart_data(num_points=15):
    datasets = [{
        "label": fake.word(),
        "data": [{"x": random.uniform(0, 100), "y": random.uniform(0, 100), "r": random.uniform(5, 20)} for _ in range(num_points)],
        "backgroundColor": [f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.6)" for _ in range(num_points)]
    }]
    return {"datasets": datasets}

def generate_area_chart_data(num_points=7):
    labels = [fake.date_this_month().strftime("%Y-%m-%d") for _ in range(num_points)]
    datasets = [{
        "label": fake.word(),
        "data": [random.randint(0, 100) for _ in range(num_points)],
        "borderColor": f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 1)",
        "backgroundColor": f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.2)",
        "fill": True
    }]
    return {"labels": labels, "datasets": datasets}

def generate_doughnut_chart_data(num_slices=5):
    return generate_pie_chart_data(num_slices)  # Doughnut chart uses the same data structure as pie chart

chart_types = {
    "1": ("Line Chart", generate_line_chart_data, "line"),
    "2": ("Bar Chart", generate_bar_chart_data, "bar"),
    "3": ("Pie Chart", generate_pie_chart_data, "pie"),
    "4": ("Radar Chart", generate_radar_chart_data, "radar"),
    "5": ("Scatter Chart", generate_scatter_chart_data, "scatter"),
    "6": ("Bubble Chart", generate_bubble_chart_data, "bubble"),
    "7": ("Area Chart", generate_area_chart_data, "line"),  # We use 'line' type but with fill: true
    "8": ("Doughnut Chart", generate_doughnut_chart_data, "doughnut")
}

generated_data = None
chart_type = None

@app.route('/')
def home():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chart.js Data Preview</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Generated Chart Data Preview</h1>
        <div style="width: 80%; margin: auto;">
            <canvas id="myChart"></canvas>
        </div>
        <h2>Generated Data:</h2>
        <pre id="jsonData"></pre>
        
        <script>
            fetch('/data')
                .then(response => response.json())
                .then(data => {
                    const ctx = document.getElementById('myChart').getContext('2d');
                    new Chart(ctx, {
                        type: '{{ chart_type }}',
                        data: data,
                        options: {
                            responsive: true,
                            plugins: {
                                title: {
                                    display: true,
                                    text: '{{ chart_name }}'
                                }
                            }
                        }
                    });
                    document.getElementById('jsonData').textContent = JSON.stringify(data, null, 2);
                });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content, chart_type=chart_type[2], chart_name=chart_type[0])

@app.route('/data')
def data():
    return jsonify(generated_data)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

def main():
    global generated_data, chart_type
    
    print("Welcome to the Chart.js Data Generator!")
    print("Please select the type of chart you want to generate data for:")
    for key, value in chart_types.items():
        print(f"{key}. {value[0]}")

    while True:
        try:
            choice = input("Enter your choice (1-8): ")
            if choice not in chart_types:
                raise ValueError("Invalid choice. Please enter a number between 1 and 8.")
            break
        except ValueError as e:
            print(f"Error: {e}")

    chart_type = chart_types[choice]
    generated_data = chart_type[1]()
    
    print(f"\nGenerated data for {chart_type[0]}:")
    print(json.dumps(generated_data, indent=2))
    
    filename = f"{chart_type[0].lower().replace(' ', '_')}_data.json"
    try:
        with open(filename, 'w') as f:
            json.dump(generated_data, f, indent=2)
        print(f"\nData saved to {filename}")
    except IOError as e:
        print(f"Error saving data to file: {e}")
    
    print("\nStarting web server to preview the chart...")
    try:
        Timer(1, open_browser).start()
        app.run(debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error starting web server: {e}")
        print("You can still view the generated data in the JSON file.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
