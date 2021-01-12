# PyTools

<img align="right" src="pytools.jpeg" alt="fagci python tools">

Handy tools written in Python.

__Purpose:__ web development helpers, pentesting, data analysis and modification.

PyTools stores process results, for ex.: scan results to analyze them later.

Also admin interface can help you perform some actions in future:  
`./pt admin` (user: `admin`, password: `ptpass` by default) 

## Tools included by 2021-01-12

|Command|Description|Functions|
|---|---|---|
|admin|Runs web interface||
|cht|Get cheat, example: python named tuple||
|dns|Perform DNS related actions|fastest|
|fortune|Wide IP range actions|ftp, http, list, ips|
|html|HTML utilities|ahrefs, sel, xpath, src|
|http|HTTP related commands|server, headers, ttfb|
|net|Network tools|localip|
|netroot|Various network tools using raw sockets|arp, sniff|
|scan|Various network scanners|ports|
|seo|SEO tools|all, sitemap|

PyTools uses `fire` module to start tools and my microframework to use with fire.  
See `./pt` or `python pt` for tools list and short descriptions.

## Some usage examples

<details>
  <summary>./pt html ahrefs</summary>
  
  ```
./pt html ahrefs https://mikhail-yudin.ru/blog/
https://mikhail-yudin.ru/
https://mikhail-yudin.ru/about/
https://mikhail-yudin.ru/blog/
https://mikhail-yudin.ru/blog/frontend/
https://mikhail-yudin.ru/blog/hardware/
https://mikhail-yudin.ru/blog/linux/
https://mikhail-yudin.ru/blog/backend/
https://mikhail-yudin.ru/blog/android/
https://mikhail-yudin.ru/blog/lifehacks/
https://mikhail-yudin.ru/notes/
https://mikhail-yudin.ru/projects/
https://mikhail-yudin.ru/contact/
...
```
</details>

<details>
  <summary>./pt dns fastest</summary>
  
  ```
./pt dns fastest
77.88.8.88       87 ms safe.dns.yandex.ru.
156.154.70.1     90 ms rdns1.ultradns.net.
87.213.100.113   97 ms unlabelled-113-100-213-87.versatel.net.
193.190.213.42   99 ms www3.vvkso-ict.com.
37.152.45.194   102 ms -
64.6.65.6       103 ms recpubns2.nstld.net.
1.1.1.1         110 ms one.one.one.one.
195.10.195.195  115 ms -
144.76.83.104   117 ms static.104.83.76.144.clients.your-server.de.
204.97.212.10   119 ms ns3.sprintlink.net.
1.0.0.2         123 ms -
208.67.220.222  124 ms resolver4.opendns.com.
77.88.8.1       125 ms secondary.dns.yandex.ru.
...
  ```
</details>

<details>
  <summary>./pt fortune http --t=120 --ips_count=5000</summary>
  
  ```
./pt fortune http --t=120
[*] create generator of 5000 ips...
[*] Gathering ips with 80 port, using 120 workers...
100%|██████| 5000/5000 [00:15<00:00, 316.33ips/s]
Got 42 ips.
[*] Filtering service: 42 ips...
100%|██████| 42/42 [00:08<00:00,  4.77ips/s]
Got 28 ips.
2.133.XXX.XXX    GPON Home Gateway
13.225.XXX.XXX  ERROR: The request could not be satisfied
13.226.XXX.XXX  ERROR: The request could not be satisfied
167.71.XXX.XXX   503 Service Temporarily Unavailable
52.66.XXX.XXX   Apache2 Ubuntu Default Page: It works
217.84.XXX.XXX  Redirect to New Page
  ```
</details>

## Prerequisites

```sh
pip install -r requirements.txt
```

## Tools structure

|Directory|Description|
|---|---|
|[modules](/modules)|Each module is command with functions. [More info](/modules)|
|[lib](/lib)|PyTools libraries to make code clean & reusable|
|[local](/local)|For now here can be your custom models named models.py ... and other stuff, which will not pushed to repo.|

## :exclamation: Caution

Use tools carefully. Some of them can be harmful. Check source code first.

Run it with according permissions from network/system administrator or ISP if needeed.

I am not responsible for your bad usage of this tools.
