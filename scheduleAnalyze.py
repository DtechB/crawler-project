import schedule
import time
import Analyzer

def job():
    Analyzer.analyze()

# schedule.every(1).hour.do(job)
schedule.every().day.at("12:16:55").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)