ffmpeg -f image2 -i /Users/choonlay/Desktop/out/%06d.png -vcodec libx264 -r 25 -t 15 /Users/choonlay/Desktop/output.mp4

# -vcodec 解码器
# -r 一秒几帧
# -t 时长（秒）