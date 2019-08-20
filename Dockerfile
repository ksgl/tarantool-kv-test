FROM tarantool/tarantool

COPY kv.lua /opt/tarantool
CMD ["tarantool", "/opt/tarantool/kv.lua"]