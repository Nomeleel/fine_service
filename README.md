# Fine Service

与Fine Client相对的服务端，这里是一个服务端集合，使用相同架构会整合到一起。Python方向的目前考虑使用Flask，其他方向等到有需求了在考虑。

## Run In Docker

```shell
cd fine

# 构建本地镜像
docker build -t nomeleel/fine . 

# 运行镜像并启动服务
docker run -p 8160:8160 nomeleel/fine 
```