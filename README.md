# pytools

My various handy tools written in Python.

Toolset uses `fire` module to start tools and my microframework to use with fire.  
See `./pt` or `python pt` for tools list and short descriptions.

## Tools included by 2021-01-12

### admin

Runs web interface

### cht

Get cheat, example: python named tuple

### dns

Perform DNS related actions

- fastest

### fortune

Wide IP range actions.

- ftp
- http
- list
- ips

### html

HTML utilities

- ahrefs
- sel
- xpath
- src

### http

HTTP related commands

- server
- headers
- ttfb

### net

Network tools

- localip

### netroot

Various network tools using raw sockets

- arp
- sniff

### scan

Various network scanners

- ports

### seo

SEO tools

- all
- sitemap

## Some usage examples

```sh
./pt dns fastest
```

```sh
./pt fortune http --t=120 --ips_count=1000
```

## Prerequisites

```sh
pip install -r requirements.txt
```

## :exclamation: Caution

Use tools carefully. Some of them can be harmful. Check source code first.

Run it with according permissions from network/system administrator or ISP if needeed.

I am not responsible for your bad usage of this tools.
