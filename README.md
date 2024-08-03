docker build -t sdge-export-rates .
docker run -d -p 8383:8383 sdge-export-rates