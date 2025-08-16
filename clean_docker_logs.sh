#!/bin/bash

# Docker容器日志清理脚本

# 设置Docker日志件存储路径
log_path="/var/lib/docker/containers"

# 获取所有容器ID
container_ids=$(ls -1 $log_path)

# 循环处理每个容器
for container_id in $container_ids; do
    # 构造日志文件路径
    log_file="${log_path}/${container_id}/${container_id}-json.log"

    # 检查日志文件是否存在
    if [ -f "$log_file" ]; then
        echo "清理容器 ${container_id} 的日志文件: ${log_file}"
        
        # 清空日志文件
        truncate -s 0 "$log_file"
    else
        echo "未找到容器 ${container_id} 的日志文件: ${log_file}"
    fi
done

echo "日志清理完成。"文
