import pandas as pd
import matplotlib.pyplot as plt


def initPlt():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.dpi'] = 300  # 扩大分辨率 防止生成的图片太小
    plt.rcParams['savefig.dpi'] = 800  # 图片像素


filePath = 'E:/理工/课程/数据挖掘/课程结业论文/课程结业论文/题B-新冠疫情数据分析/data.xlsx'
# 读入省份对照数据
data_sf = pd.read_excel(filePath, sheet_name='城市省份对照表')
# 读入疫情数据
data_yq_chinese = pd.read_excel(filePath, sheet_name='城市疫情')
data_yq_out = pd.read_excel(filePath, sheet_name='国际疫情')

# 进行对应省份的序列化
citys = {data_sf['城市'].array[i]: data_sf['省份'].array[i] for i in range(data_sf['城市'].array.size)}


# print(citys)
# print(citys.get('安庆'))


def chinese_status():
    # 初始化图表设置
    initPlt()
    plt.title('国内疫情总概况')
    # 求取疫情感染总人数
    coronavirusCount = data_yq_chinese.pivot_table(index='日期', columns='城市', values='新增确诊', aggfunc='sum', fill_value=0,
                                                   dropna=False).sum().sum()
    # 求取疫情死亡总人数
    deathCount = data_yq_chinese.pivot_table(index='日期', columns='城市', values='新增死亡', aggfunc='sum', fill_value=0,
                                             dropna=False).sum().sum()
    # 求取疫情治愈总人数
    cureCount = data_yq_chinese.pivot_table(index='日期', columns='城市', values='新增治愈', aggfunc='sum', fill_value=0,
                                            dropna=False).sum().sum()

    print("国内->", '死亡总人数', deathCount, '感染总人数', coronavirusCount, '治愈总人数', cureCount)
    # 绘图
    plt.barh(range(3), [coronavirusCount, deathCount, cureCount], align='center', color='steelblue', alpha=0.8)
    # 添加轴标签
    plt.xlabel('人数')
    plt.yticks(range(3), ['感染总人数', '死亡总人数', '治愈总人数'])
    for x, y in enumerate([coronavirusCount, deathCount, cureCount]):
        plt.text(y + 0.1, x, '%s' % y, va='center')
    # 保存图像
    plt.savefig('dist/chinese_coronavirus_status.png')
    plt.show()  # 调试查看


def outCountry_status():
    # 初始化图表设置
    initPlt()
    plt.title('国外疫情总概况')
    # 求取疫情感染总人数
    coronavirusCount = data_yq_out.pivot_table(index='日期', columns='国家', values='累计死亡', aggfunc='sum', fill_value=0,
                                               dropna=False).sum().sum()
    # 求取疫情死亡总人数
    deathCount = data_yq_out.pivot_table(index='日期', columns='国家', values='累计死亡', aggfunc='sum', fill_value=0,
                                         dropna=False).sum().sum()
    # 求取疫情治愈总人数
    cureCount = data_yq_out.pivot_table(index='日期', columns='国家', values='累计治愈', aggfunc='sum', fill_value=0,
                                        dropna=False).sum().sum()

    print("国外->", '死亡总人数', deathCount, '感染总人数', coronavirusCount, '治愈总人数', cureCount)
    # 绘图
    plt.barh(range(3), [coronavirusCount, deathCount, cureCount], align='center', color='steelblue', alpha=0.8)
    # 添加轴标签
    plt.xlabel('人数')
    plt.yticks(range(3), ['感染总人数', '死亡总人数', '治愈总人数'])
    for x, y in enumerate([coronavirusCount, deathCount, cureCount]):
        plt.text(y + 0.1, x, '%s' % y, va='center')
    # 保存图像
    plt.savefig('dist/out_coronavirus_status.png')
    plt.show()  # 调试查看


# 映射城市到省份至表格中
def mapCityToTable(df):
    table_map = df.copy()
    for i in range(len(df)):
        table_map.loc[i, '城市'] = citys.get(df['城市'].loc[i])

    return table_map



def outSpaceAndTimeChangesStatus():
    # 初始化
    initPlt()
    plt.title('疫情时空变化情况')
    # 对城市进行分类
    cate = list(pd.Categorical(data_yq_chinese['城市']).categories)
    for i in range(len(cate)):
        if cate[i] == '湖北':
            # 对湖北进行特殊处理
            plt.plot(data_yq_chinese[data_yq_chinese['城市'].isin([cate[i]])].loc[:, '日期'],
                     data_yq_chinese[data_yq_chinese['城市'].isin([cate[i]])].loc[:, '累计确诊'],
                     label=cate[i],
                     ls='-.',
                     color='red')
            continue
        plt.plot(data_yq_chinese[data_yq_chinese['城市'].isin([cate[i]])].loc[:, '日期'],
                 data_yq_chinese[data_yq_chinese['城市'].isin([cate[i]])].loc[:, '累计确诊'],
                 label=cate[i])
    plt.xlabel('时间')
    plt.ylabel('累计确诊人数')
    plt.legend(loc='lower left', prop={'size': 6})
    plt.savefig('dist/疫情时空变化情况.png')
    plt.show()

'''
    计算各个城市的对应累计确诊、累计死亡、累计治愈
'''
def calcAccumulateCount(df):
    # 计算各个城市的对应累积确诊
    accumulate = df.groupby('城市').cumsum()
    # 修改列名
    accumulate.columns = ['累计确诊', '累计治愈', '累计死亡']
    # 新增列
    df.loc[:, '累计确诊'] = accumulate.loc[:, '累计确诊']
    df.loc[:, '累计治愈'] = accumulate.loc[:, '累计治愈']
    df.loc[:, '累计死亡'] = accumulate.loc[:, '累计死亡']

    return df


if __name__ == '__main__':
    # 输出国内疫情总概况
    chinese_status()
    # 输出国外疫情总概览
    outCountry_status()
    data_yq_chinese = mapCityToTable(data_yq_chinese)

    # 计算累计
    data_yq_chinese = calcAccumulateCount(data_yq_chinese)
    print(data_yq_chinese)
    # 输出疫情时空变化图
    outSpaceAndTimeChangesStatus()
