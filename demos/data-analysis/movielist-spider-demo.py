# 案例：获取高分电影榜单（Top100）数据，并保存在csv文件中
# 数据包括：电影名、年份、上映时间、类型、时长、评分、语言、导演、作者、主演、Slogan（宣传标语）、简介
# 步骤：
# 一、明确网站（https://www.themoviedb.org/）的robots.txt中的抓取规则
# 二、查看页面结构、拆解具体的操作步骤、按步骤开发
# 1. 获取高分电影列表数据
# 2. 遍历电影列表，获取每一部电影的详情信息，并提取电影数据信息
# 3. 将电影详情信息保存到csv文件

import requests
import csv
from lxml import html
import re

# 常量（一般全称不变的变量通常认为是常量，定义的时候全程大写，不强制）
MOVIE_LIST_FILE = '06.resources/movie_list_02.csv'
TMDB_BASE_URL = 'https://www.themoviedb.org'
TMDB_TOP_URL_1 = 'https://www.themoviedb.org/movie/top-rated'  # 高分电影榜单的url，默认访问第一页的数据
TMDB_TOP_URL_2 = 'https://www.themoviedb.org/discover/movie/items'  # 高分电影榜单url，第二页之后的url

# 保存电影数据，保存为csv文件
def save_all_movies(all_movies):
    with open(MOVIE_LIST_FILE, 'w', encoding='utf-8', newline='') as csvfile:  #newline=''避免每次生成空行
        writer = csv.DictWriter(csvfile,fieldnames=['电影名', '年份', '上映时间', '类型', '时长', '评分', '语言', '导演', '作者', '宣传语', '简介'])
        writer.writeheader()  # 写入表头
        writer.writerows(all_movies)  # writerow一次写一行内容，writerows一次写入所有内容

# 获取电影年份
def get_movie_year(movie_years):
    movie_year = movie_years[0].strip() if movie_years else ''   #strip()函数：去除左右两端的空白字符
    return movie_year.replace('(', '').replace(')', '')

# 获取电影上映时间
def get_movie_publish_date(movie_dates):
    movie_date = movie_dates[0].strip() if movie_dates else ''
    return re.search(r'\d{4}-\d{2}-\d{2}', movie_date).group()

# 获取电影时长（统一用分钟表示）
def get_movie_cost_time(movie_cost_times):
    movie_cost_time = movie_cost_times[0].strip() if movie_cost_times else ''
    h_res = re.search(r'(\d+)h', movie_cost_time)
    m_res = re.search(r'(\d+)m', movie_cost_time)
    h = int(h_res.group(1)) if h_res else 0
    m = int(m_res.group(1)) if m_res else 0
    return h * 60 + m


# 获取电影详情
def get_movie_info(movie_info_url):
    # 1. 发送请求，获取电影详情数据
    movie_response = requests.get(movie_info_url, timeout=60)
    print(f'发送请求{movie_info_url}，获取电影详情数据...')

    # 2. 解析数据，获取电影详情
    movie_doc = html.fromstring(movie_response.text)

    movie_names = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")  # 电影名称
    movie_years = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")  # 上映年份
    movie_dates = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='release']/text()")  # 上映时间
    movie_tags = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='genres']/a/text()")  # 类型
    movie_cost_times = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='runtime']/text()")  # 时长
    movie_scores = movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")  # 评分
    movie_languages = movie_doc.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")  # 语言
    movie_directors = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")  # 导演
    movie_authors = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")  # 作者
    movie_slogans = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")  # 宣传语
    movie_descriptions = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")  # 简介

    # 3. 返回电影详情
    movie_info = {
        '电影名': movie_names[0].strip() if movie_names else '',  # 使用三元运算符，如果电影名数据不存在那么返回空值，避免报错
        '年份': get_movie_year(movie_years),
        '上映时间': get_movie_publish_date(movie_dates),
        '类型': ','.join(movie_tags) if movie_tags else '',  # 字符串方法，使用''中的分隔符连接列表中多个元素
        '时长': get_movie_cost_time(movie_cost_times),
        '评分': movie_scores[0].strip() if movie_scores else '',
        '语言': movie_languages[0].strip() if movie_languages else '',
        '导演': ','.join(movie_directors) if movie_directors else '',
        '作者': ','.join(movie_authors) if movie_authors else '',
        '宣传语': movie_slogans[0].strip() if movie_slogans else '',
        '简介': movie_descriptions[0].strip() if movie_descriptions else '',
    }
    return movie_info


# 主函数，定义核心逻辑
def main():
    all_movies = []  # 保存所有的电影数据

    # 循环获取电影列表，从第一页到第五页
    for page_num in range(1,6):
        # 1. 发送请求，获取高分电影榜单数据
        if page_num == 1:
            response = requests.get(TMDB_TOP_URL_1, timeout=60)  # TMDB是外网网速较慢，timeout表示超时时间，避免服务器没返回数据而一直卡住；60表示连接时间+读取时间合计最多60s
        else:
            response = requests.post(TMDB_TOP_URL_2,
                f'air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-03-10&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400',
                timeout=60)


        print(f'发送请求，访问第{page_num}页的数据，获取TMDB电影榜单数据...')

        # 2. 解析数据，获取电影列表
        document = html.fromstring(response.text)
        movie_list = document.xpath(
            "//div[@class='w-full overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-colors hover:border-gray-300']")

        # 3. 遍历电影列表，获取电影详情
        for movie in movie_list:
            movie_urls = movie.xpath("./div/div/a/@href")
            if movie_urls:
                # 电影详情的url地址
                movie_info_url = TMDB_BASE_URL + movie_urls[
                    0]  # movie_urls[0]为所有提取出来的电影地址列表里的第一项（在浏览器中href后的地址），本身不带完整域名，前面加TMDB_BASE_URL
                # 发送请求，获取电影详情数据
                movie_info = get_movie_info(movie_info_url)
                all_movies.append(movie_info)

    # 4. 保存数据，保存为csv文件
    print('获取到所有的电影详情，保存电影详情到CSV文件...')
    save_all_movies(all_movies)

if __name__ == '__main__':
    main()
