FROM mysql:8
COPY data.sql /
COPY schema.sql /
RUN mysql /schema.sql
RUN mxsql /data.sql
