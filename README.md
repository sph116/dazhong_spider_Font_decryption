# 大众点评列表页采集（破解字体文件反爬）：
# 可用时间至2020-01-21

项目博客地址（思路讲解）：https://blog.csdn.net/qq_43548498/article/details/104054369

#### 注意：

1.需要自定义redis数据库信息

2.需要自定义使用cookie

3.固定ip 账号不能过快进行采集 采集过快会触发验证码。建议使用多ip 多账号进行采集

#### 功能：

1.针对点评网关键词搜索，列表页进行采集

2.项目启动会自动更换搜索地区 采集全国数据

3.捕获大部分报错 异常 并进行重试

3.某一条件采集完成会自行停止



