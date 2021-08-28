FROM python:3.9
EXPOSE 8051
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
#replace 8501 with $PORT if on heroku
CMD ["sh", "-c", "streamlit run app.py"]

# to run with Docker:
# docker build -f Dockerfile -t app:latest .
# docker run -p 8501:8501 app:latest

# to run with Heroku:
# heroku container:login
# heroku create (only need to do this once)
# heroku container:push web
# heroku container:release web
# heroku open

#gcloud builds submit --tag gcr.io/unpauseffrk/unpauseffrk --project=unpauseffrk
#gcloud run deploy --image gcr.io/unpauseffrk/unpauseffrk --platform managed --project=unpauseffrk --allow-unauthenticated