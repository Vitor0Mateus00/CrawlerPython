FROM python:3.9

ADD PythonCrawler.py .
ADD Requirements.txt .

RUN pip install requests beautifulsoup4 pandas

CMD ["python", "./PythonCrawler.py"]