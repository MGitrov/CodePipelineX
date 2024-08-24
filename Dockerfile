FROM python

# Setting the working directory in the container.
WORKDIR /app

COPY . .

# Installing any needed packages specified in "requirements.txt" file.
RUN pip install -r app/requirements.txt

# Exposing port 5000 which is the port on which the Flask application runs.
EXPOSE 5000

# Will run the "app.py" script using Python.
CMD ["python", "app/app.py"]