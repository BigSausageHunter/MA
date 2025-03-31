FROM docker.elastic.co/logstash/logstash:8.0.0
COPY logstash.conf /usr/share/logstash/pipeline/logstash.conf
CMD ["logstash", "-f", "/usr/share/logstash/pipeline/logstash.conf"]
