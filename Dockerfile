# import file 

FROM python:3.11-slim

# set work directory

WORKDIR /app

# dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app code
# copy project for all files
COPY . .

# print logs in real time
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
