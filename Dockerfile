FROM python:3
COPY agent.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "agent.py" ]
