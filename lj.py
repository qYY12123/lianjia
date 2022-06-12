f = open('房源.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '上次交易',
    '交易权属',
    '产权所属',
    '单价',
    '售价',
    '套内面积',
    '建筑类型',
    '建筑结构',
    '建筑面积',
    '户型结构',
    '房屋年限',
    '房屋户型',
    '房屋朝向',
    '房屋用途',
    '房本备件',
    '房源核验码',
    '所在楼层',
    '抵押信息',
    '挂牌时间',
    '标题',
    '梯户比例',
    '装修情况',
    '详情页',
    '配备电梯',
    '别墅类型'
])
csv_writer.writeheader()  # 写入表头
for page in range(1, 11):
    print(f'===================正在爬取第{page}页数据内容===================')
    url = f'https://su.lianjia.com/ershoufang/pg2/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
        # 解析数据 解析方式: css xpath re
    # css选择器: 根据标签属性内容提取数据
    selector = parsel.Selector(response.text)  # 返回对象
    # attr 属性选择器 getall() 获取所有 返回数据列表 
    href = selector.css('.sellListContent li .title a::attr(href)').getall()
    # print(href)
    # 列表 数据容器(一个箱子) 元素(箱子里面东西)
    # for 循环 遍历就是从这个箱子里面一个一个拿东西出来
    for link in href:
        response_1 = requests.get(url=link, headers=headers)
        #解析数据提取我们想要数据
        # print(response_1.text)
        selector_1 = parsel.Selector(response_1.text)  # 返回对象
        # get() 取一个
        title = selector_1.css('.title .main::text').get()  # 标题
        price = selector_1.css('.price .total::text').get()  # 售价
        price_1 = selector_1.css('.unitPriceValue::text').get()  # 单价
        attr_list = selector_1.css('.base .content li .label::text').getall()
        attr_list_1 = selector_1.css('.transaction .content li .label::text').getall()
        content_list = selector_1.css('.base .content li::text').getall()
        content_list_1 = selector_1.css('.transaction .content li span::text').getall()
        # 两个列表 如何创建成一个字典 attr_list 做键 content_list 做值
        # print(attr_list)
        # print(content_list)
        # 保存csv文件表格
        # 需要创建一个字典
        dit = {
            "详情页": link,
            "标题": title,
            "售价": price,
            "单价": price_1,
            # "区域": price_1,
        }
        dit_1 = dict(zip(attr_list, content_list))
        dit_2 = dict(zip(attr_list_1, content_list_1))
        dit.update(dit_1)
        dit.update(dit_2)
        # print(title, price, price_1)
        csv_writer.writerow(dit) # 写入数据
        pprint.pprint(dit) # 格式化输出模块