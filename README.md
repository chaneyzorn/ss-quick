# ss-quick

ss-quick 是一个为 [`ss-local`](https://github.com/shadowsocks/shadowsocks-libev) 自动加载 `gui-config.json` 的工具。

它通过测试多个服务器的连接延迟，自动选择延迟最低的服务器，并输出为 `ss-local` 的选项。

你也可以直接指定要使用的服务器配置。

![screenshot](screenshot.gif)

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
  --uri                 print config in the form of uri to stdout.
  --debug               print debug information.
```

查看测试延迟：
```
ss-quick -c /path/to/gui-config.json

12-26 21:42:39 INFO: Loading config file from /path/to/gui-config.json
12-26 21:42:39 INFO: Start Connection Latency Test
[1] unreachable         test1.host:test1线路
[2] server not know     test3.host:test2线路
[3] 89.28 ms            test4.host:test3线路
[4] timeout             test5.host:test4线路

-s test3.host -p 1234 -k passwwwwwd -m aes-256-cfb
```

直接输出 flags 作为 ss-local 的启动参数：
```
ss-local -v -l 1080 `ss-quick -c /path/to/gui-config.json`
```

选择第2个服务器：
```
ss-local -v -l 1080 `ss-quick -c /path/to/gui-config.json -n2`
```

输出指定配置为 `ss://` 形式的 uri :
```
ss-quick -c /path/to/gui-config.json -n2 --uri
```

配合 [qrcode](https://github.com/lincolnloop/python-qrcode) 输出为二维码：
```
qr `ss-quick -c /path/to/gui-config.json --uri`
```

# BUG

1. 如果线路列表过长，滚出终端显示范围的部分，测试延迟的结果将不会得到刷新。

# License
MIT
