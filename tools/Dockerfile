FROM python:3.6
RUN pip install pip setuptools --upgrade
RUN git clone https://github.com/zaja1kun/local-chat.git -b docker-image
RUN pip install local-chat/

EXPOSE 13998/udp
CMD ["local-chat"]
