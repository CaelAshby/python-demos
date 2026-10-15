# Python Demos
> 本仓库为Python练习项目合集，包含大模型Web应用、网页爬虫、销售订单数据分析可视化三类Demo，全部代码由本人独立编写。

## 项目环境
- Python 3.10+
- 主要依赖库：`streamlit`、`pandas`、`matplotlib`、`requests`、`lxml`

## 项目目录结构
python-demos/
├── demos/
│   ├── ai/                 # AI智能伴侣
│   ├── crawler/            # TMDB电影榜单爬虫
│   ├── data-analysis/      
│   ├── visualization/      # 店铺销售订单数据分析
│   └── other-scripts/      # 其他脚本
└── README.md


### 🤖 Demo 1｜AI对话Web助手
技术栈：Streamlit + DeepSeek API + JSON本地存储
1. 通过Apifox调试DeepSeek开放API，解析接口返回JSON数据；
2. 使用Streamlit搭建Web交互页面，侧边栏控制面板，支持自定义AI角色昵称、性格设定；
3. 会话管理：新建会话、加载历史会话、删除会话，聊天记录以JSON文件本地持久化，自动创建存储目录，增加异常捕获处理文件读写错误；
4. 对接DeepSeek大模型API实现流式打字机输出，保存多轮对话上下文，维持对话连贯性；
5. 利用`st.session_state`维护页面状态，避免页面刷新后数据丢失；添加终端日志，方便本地调试。

### 🕷️ Demo 2｜电影榜单爬虫
技术栈：requests + lxml + XPath + 正则 + csv
1. 遵循网站抓取协议，requests发送网页请求，循环爬取多页榜单，设置请求超时防止程序卡死；
2. lxml + XPath解析HTML网页，配合正则清洗原始文本，标准化电影时长、上映日期等字段；
3. 进入电影详情页提取：电影名称、上映年份、影片类型、评分、导演、主演、简介；增加容错逻辑，字段缺失自动填充空值，防止程序崩溃；
4. 使用内置csv模块存储数据，设置表头、处理文本换行，采集结果保存为CSV文件，可直接用于后续数据分析。

### 📊 Demo 3｜连锁店销售订单数据分析 & 可视化
技术栈：Pandas + Matplotlib + GridSpec
1. 前期在Jupyter完成逻辑验证，后重构封装为模块化Python函数；
2. 数据清洗：缺失值填充、订单号去重、修正负单价异常数据、统一日期格式；
3. Pandas分组统计指标：每日销售额趋势、各城市累计销量、产品类型订单占比、支付方式订单占比；
4. 使用Matplotlib+GridSpec自定义多子图布局，绘制折线图、柱状图、饼图；解决matplotlib中文乱码问题，自动生成并保存可视化图表。

### 运行说明
1. 克隆仓库到本地
2. 安装项目所需依赖包
3. 进入对应demo文件夹，运行脚本

### 个人简介
跨专业自学Python，练习后端接口调用、网络爬虫、数据清洗与可视化、大模型应用开发，持续积累项目实战代码。
