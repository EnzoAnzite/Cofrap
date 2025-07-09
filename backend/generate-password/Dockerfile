# generate-password/Dockerfile

FROM ghcr.io/openfaas/classic-watchdog:0.3.3 AS watchdog

FROM alpine:3.21.3

RUN apk add --no-cache python3 py3-pip

RUN mkdir -p /home/app

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

RUN addgroup -S app && adduser app -S -G app
RUN chown app /home/app

WORKDIR /home/app

USER app

COPY handler.py .

ENV fprocess="python3 handler.py"

ENV write_debug="false"

EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
