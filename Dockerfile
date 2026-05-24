FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY app.py .
COPY code/ ./code
COPY scraping/ ./scraping
COPY data/ ./data
COPY styles/ ./styles
COPY TechSight.png ./TechSight.png
COPY TechSight-sidebar.png ./TechSight-sidebar.png

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]