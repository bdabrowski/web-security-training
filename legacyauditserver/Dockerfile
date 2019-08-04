FROM gcc:4.9
COPY . /usr/src/ser
WORKDIR /usr/src/ser
RUN gcc -o server_c server.c
EXPOSE 4001
CMD ["./server_c"]
