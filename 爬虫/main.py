import os
import time
import random
import platform
import requests
import pandas as pd
import jieba
import matplotlib.pyplot as plt
from lxml import etree
from snownlp import SnowNLP
from wordcloud import WordCloud

# 如果没有 fake_useragent 报错，可以删除这行引用，直接用下面写死的 Header
# from fake_useragent import UserAgent

# ================= ⚠️ 配置区域 (必改) ⚠️ =================

# 1. 电影ID (只填数字！不要填网址！)
# 例如：《肖申克的救赎》ID是 1292052
MOVIE_ID = '1292052'

# 2. 豆瓣Cookie (必填！否则无法爬取，甚至直接 403)
# 获取方法：浏览器登录豆瓣 -> F12 -> Console -> 输入 document.cookie -> 复制结果
COOKIE = 'bid=lf7Bck0ksNo; ll="118337"; _gid=GA1.2.419664119.1770037444; _ga=GA1.1.1539301421.1770037444; _ga_Y4GN1R87RG=GS2.1.s1770037443$o1$g0$t1770037448$j55$l0$h0; dbcl2="285319578:wKGoR+2Zj/I"; ck=7ibz; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; frodotk_db="a5101fafc1d2c9b1ef305f0f45785d13"; __utma=30149280.1539301421.1770037444.1770037478.1770037478.1; __utmc=30149280; __utmz=30149280.1770037478.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.28531; __utma=223695111.1539301421.1770037444.1770037975.1770037975.1; __utmb=223695111.0.10.1770037975; __utmc=223695111; __utmz=223695111.1770037975.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/gallery/topic/3666789/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1770037975%2C%22https%3A%2F%2Fwww.douban.com%2Fgallery%2Ftopic%2F3666789%2F%22%5D; _pk_id.100001.4cf6=8cf1ca59b4c1cd8e.1770037975.; _pk_ses.100001.4cf6=1; __yadk_uid=f4ZqNHPORbX1sqbg9OfXkmJURPUnbiV4; _vwo_uuid_v2=D61CC81D8B5F69405EC404CB35C4C2B3A|24ad3fe3d78e9fb3077f815835b4cd27; __utmt=1; __utmb=30149280.20.6.1770037963031'

# 3. 字体设置 (建议下载 SimHei.ttf 放在代码同目录下)
LOCAL_FONT_NAME = 'SimHei.ttf'


# ========================================================

class FontManager:
    """自动解决中文字体路径，防止乱码"""

    @staticmethod
    def get_font_path():
        # 1. 优先检测本地同级目录
        if os.path.exists(LOCAL_FONT_NAME):
            return LOCAL_FONT_NAME

        system = platform.system()
        # 2. 根据系统尝试调用内置字体
        if system == 'Windows':
            paths = ['C:/Windows/Fonts/simhei.ttf', 'C:/Windows/Fonts/msyh.ttc']
            for p in paths:
                if os.path.exists(p): return p
        elif system == 'Darwin':  # Mac
            paths = ['/System/Library/Fonts/Supplemental/Arial Unicode.ttf', '/System/Library/Fonts/PingFang.ttc']
            for p in paths:
                if os.path.exists(p): return p

        print("⚠️ 未找到合适的中文字体，图表中文可能显示为方框。建议下载 SimHei.ttf")
        return 'arial.ttf'  # 英文默认字体


class DoubanSpider:
    def __init__(self, movie_id, max_pages=3, cookie=''):
        self.movie_id = movie_id
        self.max_pages = max_pages
        # 构造 URL
        self.base_url = f'https://movie.douban.com/subject/{movie_id}/comments'

        # 使用固定的 Header，模拟真实浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Cookie': cookie,
            'Host': 'movie.douban.com',
            'Connection': 'keep-alive'
        }
        self.data_list = []

    def fetch_page(self, start=0):
        params = {'start': start, 'limit': 20, 'status': 'P', 'sort': 'new_score'}
        try:
            # 随机休眠
            time.sleep(random.uniform(1.5, 3.0))

            # --- 调试打印：确认网址是否正确 ---
            if start == 0:
                print(f"   [Debug] 正在请求网址: {self.base_url}")
            # --------------------------------

            response = requests.get(self.base_url, headers=self.headers, params=params, timeout=10)

            if response.status_code == 200:
                return response.text
            elif response.status_code == 404:
                print(f"❌ 错误：404 Not Found。")
                print(f"   原因：电影ID [{self.movie_id}] 错误，或者该电影不存在。")
                print("   检查：请确保 MOVIE_ID 变量只包含数字！")
                return None
            elif response.status_code == 403:
                print("❌ 错误：403 Forbidden。")
                print("   原因：Cookie失效 或 IP被封。请更新 Cookie！")
                return None
            else:
                print(f"⚠️ 请求状态码异常: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ 请求发生异常: {e}")
            return None

    def parse_html(self, html):
        if not html: return

        # --- 🛠️ 调试核心代码：保存网页看看到底是啥 ---
        with open("debug_douban.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("   [调试] 已将下载的网页保存为 'debug_douban.html'，请在文件夹中双击打开它！")
        # ----------------------------------------------

        tree = etree.HTML(html)

        # 1. 检查标题
        title = tree.xpath('//title/text()')
        print(f"   [调试] 网页标题是: {title}")

        # 2. 尝试更宽松的匹配规则 (关键修改！！！)
        # 原来的写法：[@class="comment-item "] (必须带空格，太死板)
        # 现在的写法：[contains(@class, "comment-item")] (只要包含这个词就行)
        items = tree.xpath('//div[contains(@class, "comment-item")]')

        if not items:
            print("   ⚠️ 依然没有找到评论条目。请检查 debug_douban.html 是否显示了登录页面。")
            return

        for item in items:
            try:
                # 兼容不同情况的用户名提取
                user_try = item.xpath('.//span[@class="comment-info"]/a/text()')
                username = user_try[0] if user_try else "未知用户"

                rating_class = item.xpath('.//span[@class="comment-info"]/span[2]/@class')
                rating = int(rating_class[0].split('allstar')[1].split()[0]) // 10 if rating_class else 0

                content_list = item.xpath('.//span[@class="short"]/text()')
                content = content_list[0].strip() if content_list else ""

                if content:
                    self.data_list.append({
                        'user': username,
                        'rating': rating,
                        'content': content
                    })
            except Exception as e:
                # print(f"解析单条出错: {e}") # 只有调试时才打开，避免刷屏
                continue

    def run(self):
        print(f"🕷️ 开始采集电影ID: [{self.movie_id}]")
        for page in range(self.max_pages):
            print(f"   正在爬取第 {page + 1}/{self.max_pages} 页...")
            html = self.fetch_page(start=page * 20)
            if not html: break  # 如果请求失败直接退出

            start_len = len(self.data_list)
            self.parse_html(html)
            end_len = len(self.data_list)

            if end_len == start_len:
                print("   ⚠️ 本页没有提取到新数据，停止翻页。")
                break

        if not self.data_list:
            return pd.DataFrame()  # 返回空表

        df = pd.DataFrame(self.data_list)
        df.drop_duplicates(subset=['content'], inplace=True)
        df.to_csv('douban_comments.csv', index=False, encoding='utf-8-sig')
        print(f"✅ 采集完成，共获取 {len(df)} 条有效数据，已保存到 CSV。")
        return df


class NLPProcessor:
    def __init__(self, filepath='douban_comments.csv'):
        self.df = pd.read_csv(filepath)
        self.stopwords = {'的', '了', '是', '我', '在', '也', '都', '和', '就', '人', '看', '电影', '觉得', '就是',
                          '真的'}

    def process(self):
        print("🧠 开始 NLP 分析...")
        # 1. 情感打分
        self.df['content'] = self.df['content'].astype(str)
        self.df['sentiment_score'] = self.df['content'].apply(lambda x: SnowNLP(x).sentiments if len(x) > 1 else 0.5)

        # 2. 打标签
        self.df['sentiment_label'] = self.df['sentiment_score'].apply(
            lambda x: '积极' if x >= 0.6 else ('消极' if x <= 0.4 else '中性')
        )

        # 3. 分词
        def seg_words(text):
            return [w for w in jieba.cut(text) if w not in self.stopwords and len(w) > 1]

        self.df['words'] = self.df['content'].apply(seg_words)

        self.df.to_csv('douban_processed.csv', index=False, encoding='utf-8-sig')
        print("✅ 分析完成，结果已保存。")
        return self.df


class Visualizer:
    def __init__(self, filepath='douban_processed.csv'):
        self.df = pd.read_csv(filepath)
        self.font_path = FontManager.get_font_path()
        # Matplotlib 字体设置
        try:
            from matplotlib import font_manager
            self.prop = font_manager.FontProperties(fname=self.font_path)
        except:
            self.prop = None

    def run_all(self):
        print("📊 开始绘图...")

        # 图1：评分分布
        plt.figure(figsize=(7, 5))
        counts = self.df['rating'].value_counts().sort_index()
        plt.bar(counts.index, counts.values, color='#3498DB')
        plt.title('用户评分分布', fontproperties=self.prop, fontsize=14)
        plt.xlabel('星级', fontproperties=self.prop)
        plt.savefig('rating_dist.png')
        print("   -> 已生成 rating_dist.png")

        # 图2：情感占比
        plt.figure(figsize=(6, 6))
        sentiment_counts = self.df['sentiment_label'].value_counts()
        plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
                colors=['#58D68D', '#EC7063', '#F5CBA7'],
                textprops={'fontproperties': self.prop})
        plt.title('情感倾向占比', fontproperties=self.prop, fontsize=14)
        plt.savefig('sentiment_pie.png')
        print("   -> 已生成 sentiment_pie.png")

        # 图3：词云
        # 数据处理：将字符串格式的列表转回列表
        all_words = []
        for w_list in self.df['words']:
            # CSV读取后可能是字符串 "['a', 'b']"
            if isinstance(w_list, str):
                import ast
                try:
                    w_list = ast.literal_eval(w_list)
                except:
                    w_list = []
            if isinstance(w_list, list):
                all_words.extend(w_list)

        text = " ".join(all_words)
        if not text.strip():
            print("⚠️ 警告：没有提取到关键词，跳过词云生成。")
            return

        wc = WordCloud(
            font_path=self.font_path,
            background_color='white',
            width=800, height=600,
            max_words=80
        )
        wc.generate(text)
        plt.figure(figsize=(8, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title('高频关键词', fontproperties=self.prop, fontsize=14)
        plt.savefig('wordcloud.png')
        print("   -> 已生成 wordcloud.png")


if __name__ == "__main__":
    # --- 1. 爬虫部分 ---
    spider = DoubanSpider(movie_id=MOVIE_ID, max_pages=3, cookie=COOKIE)
    df = spider.run()

    # --- 2. 安全检查 ---
    if df.empty:
        print("\n" + "=" * 50)
        print("❌ 严重错误：未能获取任何数据！")
        print("可能原因：")
        print("1. MOVIE_ID 填错了 (是否填了网址而非数字？)")
        print("2. Cookie 过期或未填写 (是否看到了 '登录' 提示？)")
        print("3. IP 被封 (是否看到了 403 Forbidden？)")
        print("=" * 50)
        # 强制结束，防止后面报错
        exit()

        # --- 3. 分析与展示 ---
    try:
        nlp = NLPProcessor('douban_comments.csv')
        nlp.process()

        viz = Visualizer('douban_processed.csv')
        viz.run_all()

        print("\n🎉 恭喜！系统运行成功，请在当前文件夹查看生成的图片。")
    except Exception as e:
        print(f"运行分析时出错: {e}")