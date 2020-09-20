## How to run

```sh
source bin/activate
cd tutorial
scrapy crawl posts -o posts.json -a start_urls="https://yu.ctu.edu.vn/dtn.html" -a allowed_domains="yu.ctu.edu.vn" -a follow_pages="dtn\.html*"
```