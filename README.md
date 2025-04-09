# Receipt Processor API

Follow the steps below to clone the repository, build the Docker image, run the container, and access the API locally

1. Clone the repository
```bash
git clone https://github.com/ZaidBaz/ReceiptProcessor.git
```
2. Change directory into the project directory
```bash
cd ReceiptProcessor/receipt_processor
```
3. Build the Docker image
```bash
docker build --tag python-django .
```
4. Run the Docker container
```bash
docker run --publish 8000:8000 python-django
```

You can now access the API by navigating to the following base URL: http://127.0.0.1:8000/
