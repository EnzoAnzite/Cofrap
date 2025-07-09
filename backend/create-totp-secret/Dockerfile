FROM ghcr.io/openfaas/classic-watchdog:0.3.3 AS watchdog

FROM python:3.10-slim

RUN pip install --no-cache-dir pyotp qrcode pillow

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

WORKDIR /home/app

COPY handler.py /home/app/handler.py
RUN chmod +x /home/app/handler.py

ENV fprocess="python3 handler.py"

EXPOSE 8080
HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
