# 大众点评字体反爬破解:

可用时间至

1.需要找到两个css文件，分别存储节点名对应的节点坐标。与文字坐标图。
  
2.使用re.sub将节点名替换为节点坐标，再根据节点坐标替换节点内容。
  
3.重新解析html文件。

# 注：

1.大众点评两种字体反爬，分别是基于坐标的反爬和页面加载字体的反爬。本文只破解基于坐标的反爬。
