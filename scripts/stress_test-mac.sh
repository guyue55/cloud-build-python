#!/bin/bash

# 在 Mac 上，强烈推荐使用 hey（Google 员工开发的，非常适合测 Cloud Run）或 ab (Apache Benchmark)：
# 安装: brew install hey
# 运行: 总共 200 个请求，并发 10 个
hey -n 200 -c 10 https://cloud-build-python-382604666102.us-central1.run.app/health