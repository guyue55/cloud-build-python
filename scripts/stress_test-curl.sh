#!/bin/bash

# 总共发送 200 个请求，最大并发数为 10
echo "Starting stress test..."
start_time=$(date +%s)

seq 200 | xargs -I{} -P 10 curl -o /dev/null -s -w "%{http_code} " --max-time 5 https://cloud-build-python-382604666102.us-central1.run.app/health


end_time=$(date +%s)
duration=$((end_time - start_time))

echo ""
echo "----------------------------------------"
echo "Test completed."
echo "Total Duration: ${duration} seconds"
