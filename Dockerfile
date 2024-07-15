FROM selenium/standalone-chrome

USER root
RUN sudo apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install selenium webdriver_manager

COPY web-watcher.py /web-watcher.py

COPY start.sh /start.sh 

ENV TARGET_URL="https://example.com"
ENV TARGET_XPATH="/html/body/div/h1"
ENV TARGET_EXPECTED_TEXT="Example Domain"
ENV SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/XXXXXXXXXXXXXXXX"
ENV SLACK_NOTIFY_TEXT="Expected text was found"

CMD ["/start.sh"]
