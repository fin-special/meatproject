from flask import Flask     # Flask 라이브러리 선언
from flask import request                                     
from apscheduler.schedulers.background import BackgroundScheduler    # apscheduler 라이브러리 선언

#API서비스 선언
@app.route("/서비스명", methods=["GET", "POST"])
def 서비스의 함수명:
   return 실제참조할 클래스의 함수

#apscheduler 선언
sched = BackgroundScheduler(daemon=True)

#apscheduler실행설정, Cron방식으로, 1주-53주간실행, 월요일부터일요일까지실행, 21시에실행
sched.add_job(서비스의 함수명,'cron', week='1-53', day_of_week='0-6', hour='21')

#apscheduler실행
sched.start()

#API서비스 실행
if__name__ == "__main__":
   app.run(host='0.0.0.0',use_reloader=False)