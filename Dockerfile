FROM python:3.9

# Setup environment
ENV VAR1=10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /app
COPY . /app

# Creates a non-root user and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" aquavitae && chown -R aquavitae /app
USER aquavitae

# During debugging, this entry point will be overridden.
CMD ["python", "src/main.py"]
