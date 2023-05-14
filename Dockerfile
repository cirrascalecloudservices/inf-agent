FROM python:3
COPY inf-agent.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "inf-agent.py" ]
