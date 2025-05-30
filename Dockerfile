# 1. Use an official Python runtime
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy everything from your local folder to container
COPY . .

# 4. Install dependencies
RUN pip install --no-cache-dir streamlit google-api-python-client pandas pymongo

# 5. Expose Streamlit port
EXPOSE 8501

# 6. Command to run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
