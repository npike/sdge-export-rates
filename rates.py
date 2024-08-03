import csv
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# Path to your CSV file
CSV_FILE_PATH = 'rates.csv'

# Function to find the current export rate
def get_current_export_rate():
    now = datetime.datetime.now()
    current_date = now.date()
    current_time = now.time()
    
    with open(CSV_FILE_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_start = datetime.datetime.strptime(row['DateStart'], '%Y-%m-%d').date()
            time_start = datetime.datetime.strptime(row['TimeStart'], '%H:%M:%S').time()
            date_end = datetime.datetime.strptime(row['DateEnd'], '%Y-%m-%d').date()
            time_end = datetime.datetime.strptime(row['TimeEnd'], '%H:%M:%S').time()

            if (date_start <= current_date <= date_end) and (time_start <= current_time <= time_end):
                return row['Value']
    
    return 'Rate not found'

class RequestHandler(BaseHTTPRequestHandler):
    
    
    def do_GET(self):
        csvfile = open(CSV_FILE_PATH, newline='')
        now = datetime.datetime.now()
        current_date = now.date()
        current_time = now.time()
        rate = None
        if self.path == '/current_export_rate':
            print("Loading csv file...")
            reader = csv.DictReader(csvfile)
            print("Loaded.")
            print(f"Looking for rate for {current_date} @ {current_time}")
            for row in reader:
                date_start = datetime.datetime.strptime(row['DateStart'], '%m/%d/%Y').date()
                time_start = datetime.datetime.strptime(row['TimeStart'], '%H:%M:%S').time()
                date_end = datetime.datetime.strptime(row['DateEnd'], '%m/%d/%Y').date()
                time_end = datetime.datetime.strptime(row['TimeEnd'], '%H:%M:%S').time()

                if (date_start <= current_date <= date_end) and (time_start <= current_time <= time_end):
                    rate = row['Value']
                    print(f"Found {row}")
                    break
        
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(rate.encode())
        elif self.path == '/highest_export_rate':
            csvfile = open(CSV_FILE_PATH, newline='')
            print("Loading csv file...")
            reader = csv.DictReader(csvfile)
            print("Loaded.")
            print(f"Looking for highest rate for {current_date}")
            highest_rate = 0.0
            highest_rate_row = None
            for row in reader:
                date_start = datetime.datetime.strptime(row['DateStart'], '%m/%d/%Y').date()
                time_start = datetime.datetime.strptime(row['TimeStart'], '%H:%M:%S').time()
                date_end = datetime.datetime.strptime(row['DateEnd'], '%m/%d/%Y').date()
                time_end = datetime.datetime.strptime(row['TimeEnd'], '%H:%M:%S').time()

                if (date_start <= current_date <= date_end):
                    rate = float(row['Value'])
                    if rate > highest_rate:
                        highest_rate = rate
                        highest_rate_row = row

                else:
                    if (highest_rate_row != None):
                        print(highest_rate_row)
                        break
        
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write((highest_rate_row['TimeStart'] + " - " + str(highest_rate)).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8383):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
