# 课程练习：某连锁店销售订单统计分析
"""
案例：某连锁店销售订单统计分析
需求一：统计每天销售额的变化。（折线图）
需求二：统计对比不同城市的累计销售数量。（柱状图）
需求三：统计不同产品类型对应的订单比例。（饼状图）
需求四：统计不同支付方式对应的订单比例。（饼状图）
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import matplotlib.gridspec as gridspec

# 子图布局参数
ROWS = 4
COLS = 1
FIG_SIZE = (20, 25)
DPI = 100
TITLE = '某连锁店销售订单统计分析'


def load_data():
    """读取销售订单数据。"""
    data = pd.read_csv(
        'data/sales.csv',
        usecols=['订单号', '产品类别', '产品名称', '销售数量', '单价', '客户所在城市', '支付方式', '订单日期'],
    )
    return data


def clean_data(data):
    """数据清洗：缺失值、重复值、异常值、数据格式处理。"""
    # 1. 缺失值处理
    # data.isnull().sum()  # 显示缺失值数量，方便判断如何处理
    data = data.ffill()  # 用上一行数据填充缺失值

    # 2. 重复值处理
    # data['订单号'].duplicated().sum()   # 查看重复值数量,只有订单号列不能重复，仅查看订单号
    # keep='last',保留最后一行重复的值，前面的都删除；keep='first',保留第一行重复的值，后面的值全删除；keep='False'，所有重复的值全部删除
    data = data.drop_duplicates(subset=['订单号'], keep='first')

    # 3. 异常值处理
    # data[data['单价'] < 0]  # 查看异常值
    data['单价'] = data['单价'].abs()  # 修复异常值，取绝对值

    # 4. 数据格式处理
    data['订单日期'] = data['订单日期'].str.replace('/', '-')

    return data


def setup_canvas():
    """二、准备工作：配置运行时参数，创建子图完成基本布局。"""
    # 1. 展示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 2. 创建子图
    fig= plt.figure(figsize=FIG_SIZE, dpi=DPI)
    gs = gridspec.GridSpec(3, 2, height_ratios=[3, 2, 2])
    # 2.1 子图分配
    ax0 = fig.add_subplot(gs[0, :])  # 第1行，全部2列合并 → 折线图
    ax1 = fig.add_subplot(gs[1, :])  # 第2行，全部2列合并 → 柱状图
    ax2 = fig.add_subplot(gs[2, 0])  # 第3行，左列 → 产品饼图
    ax3 = fig.add_subplot(gs[2, 1])  # 第3行，右列 → 支付饼图
    axes = [ax0, ax1, ax2, ax3]

    # 3. 创建标题
    fig.suptitle(TITLE, fontsize='25', x=0.5, y=1)

    # 4. 增大子图之间高度距离，防止文字重合
    plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.92,bottom=0.08)

    return fig, axes


def draw_daily_sale(ax: Axes, data):
    """需求一：统计每天销售额的变化。（折线图）"""
    data['销售额'] = data['销售数量'] * data['单价']

    # 1. 获取x,y轴数据
    # 使用pandas库to_datetime()函数将订单日期转换为pandas的日期类型，从而能对日期进行分组
    data['订单日期'] = pd.to_datetime(data['订单日期'])
    day_sale = data.groupby(data['订单日期'])['销售额'].sum()  # 对订单日期进行分组，对销售额求和

    x1_data = day_sale.index.tolist()
    y1_data = day_sale.values.tolist()

    # 2. 绘制折线图 & 设置图表参数
    ax.plot(x1_data, y1_data, color='green', linewidth=2)  # 绘制子图一
    ax.set_title('每天销售额变化折线图', fontsize=18, y=1.02)  # 添加子图标题
    ax.set_xlabel('订单日期', fontsize=14)  # 添加x轴标签
    ax.set_ylabel('销售额', fontsize=14)  # 添加y轴标签
    ax.tick_params(axis='x', rotation=45, labelsize=10)  # x轴刻度参数调整
    ax.tick_params(axis='y', rotation=0, labelsize=10)  # y轴刻度参数调整
    ax.set_xticks(x1_data[::10])  # 设置x轴刻度间隔
    ax.set_yticks([i for i in range(0, 120001, 20000)])  # 设置y轴刻度间隔
    ax.grid(linestyle='--', alpha=0.5)  # 设置网格线


def draw_city_sale(ax: Axes, data):
    """需求二：统计对比不同城市的累计销售数量。（柱状图）"""
    # 1. 获取x,y轴数据
    cum_sale = data.groupby('客户所在城市')['销售数量'].sum()

    x_data = cum_sale.index.tolist()
    y_data = cum_sale.values.tolist()

    # 2. 绘制柱状图 & 设置图表参数
    ax.bar(x_data, y_data, color='green', width=0.3)  # 绘制子图二
    ax.set_title('不同城市累计销售数量对比图', fontsize=18, y=1.02)  # 添加子图标题
    ax.set_xlabel('客户所在城市', fontsize=14)  # 添加x轴标签
    ax.set_ylabel('销售数量', fontsize=14)  # 添加y轴标签
    ax.tick_params(axis='x', rotation=0, labelsize=10)  # x轴刻度参数调整
    ax.tick_params(axis='y', rotation=0, labelsize=10)  # y轴刻度参数调整
    ax.set_yticks([i for i in range(0, 401, 50)])  # 设置y轴刻度间隔
    ax.grid(linestyle='--', alpha=0.5)  # 设置网格线


def draw_category_ratio(ax: Axes, data):
    """需求三：统计不同产品类型对应的订单比例。（饼状图）"""
    # 1. 获取x,y轴数据（这里x,y数据分别代表饼状图数据以及数据对应的标签）
    cum_sale = data.groupby('产品类别')['销售数量'].sum()
    x_data = cum_sale.values.tolist()  # 订单数量列表
    y_data = cum_sale.index.tolist()  # 产品类别列表

    # 2. 绘制饼状图 & 设置图表参数
    ax.pie(x_data, labels=y_data, autopct='%1.1f%%', startangle=90, radius=1)
    ax.set_title('不同产品类型对应的订单比例图', fontsize=18, y=1.05)
    ax.legend(loc='lower center', ncols=3, bbox_to_anchor=(0.5, -0.35))


def draw_payment_ratio(ax: Axes, data):
    """需求四：统计不同支付方式对应的订单比例。（饼状图）"""
    # 1. 获取x,y轴数据（这里x,y数据分别代表饼状图数据以及数据对应的标签）
    cum_sale = data.groupby('支付方式')['销售数量'].sum()
    x_data = cum_sale.values.tolist()  # 订单数量列表
    y_data = cum_sale.index.tolist()  # 支付方式列表

    # 2. 绘制饼状图 & 设置图表参数
    ax.pie(x_data, labels=y_data, autopct='%1.1f%%', startangle=90, radius=1)
    ax.set_title('不同支付方式对应的订单比例图', fontsize=18, y=1.05)
    ax.legend(loc='lower center', ncols=2, bbox_to_anchor=(0.5, -0.35))


def main():
    # 一、读取数据并清洗
    data = load_data()
    data = clean_data(data)

    # 二、准备工作：创建画布并获取子图
    fig, axes = setup_canvas()
    axes1: Axes = axes[0]
    axes2: Axes = axes[1]
    axes3: Axes = axes[2]
    axes4: Axes = axes[3]

    # 三、需求一：每天销售额变化（折线图）
    draw_daily_sale(axes1, data)

    # 四、需求二：不同城市累计销售数量对比（柱状图）
    draw_city_sale(axes2, data)

    # 五、需求三：不同产品类型订单比例（饼状图）
    draw_category_ratio(axes3, data)

    # 六、需求四：不同支付方式订单比例（饼状图）
    draw_payment_ratio(axes4, data)

    # 保存图片
    plt.savefig('data/某连锁店销售订单统计分析图.png')

    # 展示画布
    plt.show()


if __name__ == '__main__':
    main()
