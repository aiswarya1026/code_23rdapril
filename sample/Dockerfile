FROM python:3.12.3-slim
 
WORKDIR /app
COPY requirements.txt .
 
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
 
COPY static/ /app/static
COPY templates/ /app/templates/
COPY main.py /app/
 
EXPOSE 8080
 
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
 
CMD ["python", "main.py"]
