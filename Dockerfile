FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY barcode_app.py .
COPY barcode_generator_ui.html .
RUN mkdir -p uploads outputs
EXPOSE 5000
CMD ["python", "barcode_app.py"]
