# 1. specify base image
FROM python:3.12.9-slim-bookworm

# 2. define (and create) working directory
WORKDIR /app

# 3. copy requirements.txt  (for caching sake)
COPY requirements.txt .

# 4. upgrade pip (so it keep working in the future)
RUN pip install --root-user-action=ignore --upgrade pip

# 5. install python packages
RUN pip install --root-user-action=ignore -r requirements.txt 

# 6. copy app files
COPY . .

# 7. expose port 8140 for application server
EXPOSE 8140

# 8. define entrypoint command to start the application-server
ENTRYPOINT [ "gunicorn", "wsgi:app" ]