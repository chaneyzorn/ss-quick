# ss-quick

ss-quick 是一个为 `ss-local` 自动加载 `gui-config.json` 的工具。

它通过测试多个服务器的连接延迟，自动选择延迟最低的服务器，并输出为 `ss-local` 的选项。

你也可以直接指定要使用的服务器配置。

# USAGE

```
ss-quick -h
usage: ss-quick [-h] [-c CONFIG_FILE] [-n N]

A tool to load gui-config.json for ss-local.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        path to gui-config.json
  -n N                  choose (1-n)th config to start ss-local.
```

查看测试延迟：
```
ss-quick -c /path/to/gui-config.json

12-26 21:42:39 INFO: Loading config file from /path/to/gui-config.json
12-26 21:42:39 INFO: >>> Start Connection Latency Test
12-26 21:42:39 INFO: [1] unreachable         test1.host:test1线路
12-26 21:42:39 INFO: [3] 89.28 ms            test4.host:test3线路
12-26 21:42:39 INFO: [2] server not know     test3.host:test2线路
12-26 22:03:14 INFO: [4] timeout             test5.host:test4线路
```

直接输出 flags 作为 ss-local 的启动参数：
```
ss-local -v -l 1080 `ss-quick -c /path/to/gui-config.json`
```

选择第2个服务器：
```
ss-local -v -l 1080 `ss-quick -c /path/to/gui-config.json -n2`
```

# License
MIT
