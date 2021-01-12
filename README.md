# pytools

My various handy tools written in Python.

For example: port scanner, fast dns server finder, HTML source prettifier with selector usage, example site SEO checker.

Toolset uses `fire` module to start tools and my microframework to use with fire, see `./pt` or `python pt` for tools list and short descriptions.

## Tools included by 2021-01-12

```
admin
cht
dns
  fastest
fortune
  ftp
  http
  list
  ips
html
  ahrefs
  sel
  xpath
  src
http
  server
  headers
  ttfb
net
  localip
netroot
  arp
  sniff
scan
  ports
seo
  all
  sitemap
yatop
```

## Usage

```sh
./pt dns fastest
```

## Prerequisites

```sh
pip install -r requirements.txt
```

## :exclamation: Caution

Use tools carefully. Some of them can be harmful. Check source code first.

Run it with according permissions from network/system administrator or ISP if needeed.

I am not responsible for your bad usage of this tools.
