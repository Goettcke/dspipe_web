FROM python:3.8

COPY . .
COPY requirements.txt ./ 
RUN pip install DS_Pipe-0.0.1-py3-none-any.whl 
RUN pip install --no-cache-dir -r requirements.txt 

ENTRYPOINT ["python", "./runner.py"]

