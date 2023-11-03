
import requests
import json
import jieba  
from collections import Counter  
from wordcloud import WordCloud  
import matplotlib.pyplot as plt  
import os

def get_word_cloud(text):
    # 给定的文段  
    # text = "探寻文化与自然：一段穿越时空的旅行。您曾踏足布达拉宫，感受那神圣而庄重的氛围，仿佛置身于藏传佛教文化的中心。又曾游览武汉大学，沐浴在学府的气息中，感受历史的流转和知识的沉淀。大雁塔下，您领略了古代中国的艺术和文化，每一块石头、每一道刻痕都在诉说着过去的故事。而当您登上北京长城，又仿佛穿越时空，体验了历史的厚重和民族的自豪。这些旅程带给您不仅是视觉的享受，更是心灵的洗礼。在布达拉宫，您体验到了信仰的力量；在武汉大学，您感受到了知识的魅力；大雁塔让您对古人的智慧赞叹不已；而北京长城则让您对中华民族的坚韧精神有了更深的理解。您的旅行偏好明显倾向于具有深厚文化底蕴和自然风光的地方。这些地方既能让您领略到人类文明的瑰宝，又能感受大自然的壮丽景色。您的旅行不仅是为了欣赏美景，更是为了寻求文化的熏陶和自然的启示。这场穿越时空的旅行，让您对文化与自然有了更深的理解和感悟。旅行不仅是为了放松身心，更是为了丰富内心，拓宽视野。您将继续在未来的旅行中，探寻更多文化与自然的奇迹，让每一次旅程都成为一次生命的精彩体验。"
    # 使用jieba进行分词  
    words = jieba.lcut(text)  
    
    # 使用collections的Counter来统计词频  
    word_counts = Counter(words)  
    
    # 移除停用词或不重要的词，这个取决于你的需求  
    stopwords = set()
    content1 = [line.strip() for line in open('assets/stopwords/cn_stopwords.txt','r',encoding='utf-8').readlines()] 
    content2 = ["明显","既能","则","更是","而","又","与","不仅","对","旅行","让","每","为了","您","的", "了", "在", "是", "我", "有","和","，","。","我们","大家","了解","一","一下","而且","了解","这里","有着","！","？","：","、","中国","湖北省","共产党","台湾"]
    stopwords.update(content1 + content2)
    word_counts = {word: count for word, count in word_counts.items() if word not in stopwords}  
    
    # 生成词云  
    wc = WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体路径，这里假设我们使用了黑体字体  
                background_color="white",  # 设置背景颜色  
                max_words=100,  # 最多显示的词汇量  
                width=3200,  # 图片的宽度  
                height=2400,  # 图片的高度  
                random_state=42  # 随机状态，用于确保颜色的一致性  
                )  
    wordcloud = wc.generate_from_frequencies(word_counts)  
    
    # 使用matplotlib来显示词云图片  
    # plt.figure(figsize=(10, 8))  
    # plt.imshow(wordcloud, interpolation='bilinear')  
    # plt.axis("off")  
    # plt.show()
    return wordcloud
    
def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=C5fadikFYXTYi1sOUq3GSPAO&client_secret=udY6zhfeDvNMmpiEOck3V6fBLrnCBnzv"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def main():
    a = get_access_token()
    print(a)
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + a
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "简要介绍一下北京大学"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

if __name__ == '__main__':
    main()
