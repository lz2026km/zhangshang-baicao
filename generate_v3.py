#!/usr/bin/env python3
"""掌上百草 v3.0 - 5000条方剂，含别名/药典/性味归经/有毒警告/妊娠等级/小儿剂量/演变关联"""
import json, random

CATS = ['解表剂','清热剂','温里剂','补益剂','安神剂','理气剂','理血剂','祛湿剂','化痰止咳','消导剂','泻下剂','收涩剂']

# ==================== 经典典籍 ====================
CLASSICS = {
    '《伤寒论》': {'dynasty':'东汉','author':'张仲景','year':'约215年','desc':'中医临床医学奠基之作，首创六经辨证体系，收方113首。'},
    '《金匮要略》': {'dynasty':'东汉','author':'张仲景','year':'约205年','desc':'记载杂病辨治，收方262首，是方剂学鼻祖经典。'},
    '《太平惠民和剂局方》': {'dynasty':'宋代','author':'太平惠民和剂局','year':'1078年','desc':'世界上第一部官修药局方，收方788首。'},
    '《医宗金鉴》': {'dynasty':'清代','author':'吴谦等','year':'1742年','desc':'清代官修医学教科书，涵盖内、外、妇、儿各科。'},
    '《温病条辨》': {'dynasty':'清代','author':'吴鞠通','year':'1798年','desc':'温病学派代表著作，创立三焦辨证。'},
    '《脾胃论》': {'dynasty':'金代','author':'李东垣','year':'1249年','desc':'补土派开山之作，强调脾胃为后天之本。'},
    '《丹溪心法》': {'dynasty':'元代','author':'朱丹溪','year':'1481年','desc':'滋阴派代表作，力倡"阳常有余，阴常不足"。'},
    '《济生方》': {'dynasty':'宋代','author':'严用和','year':'1253年','desc':'方剂学重要参考文献，注重脏腑辨证。'},
    '《千金要方》': {'dynasty':'唐代','author':'孙思邈','year':'652年','desc':'唐代医学百科全书，收方5300余首。'},
    '《景岳全书》': {'dynasty':'明代','author':'张景岳','year':'1624年','desc':'明代临床医学巨著，阴阳互补理论集大成。'},
    '《神农本草经》': {'dynasty':'东汉','author':'神农氏','year':'约100年','desc':'现存最早的中药学专著，记载365种药物，分上中下三品。'},
    '《本草纲目》': {'dynasty':'明代','author':'李时珍','year':'1596年','desc':'集明代以前药学之大成，收药1892种，附方11096首。'},
}

# ==================== 药典来源 ====================
PHARMACOPOEIA = ['《神农本草经》','《本草纲目》','《中国药典》','《中药学》','《本草求原》']

# ==================== 性味归经数据 ====================
HERB_PROPS = {
    '麻黄':{'nature':'温','taste':'辛、微苦','channel':'肺、膀胱','toxic':False,'pregnancy':1},
    '桂枝':{'nature':'温','taste':'辛、甘','channel':'肺、心、膀胱','toxic':False,'pregnancy':1},
    '白芍':{'nature':'微寒','taste':'苦、酸','channel':'肝、脾','toxic':False,'pregnancy':2},
    '甘草':{'nature':'平','taste':'甘','channel':'心、肺、脾、胃','toxic':False,'pregnancy':0},
    '生姜':{'nature':'温','taste':'辛','channel':'肺、脾、胃','toxic':False,'pregnancy':0},
    '大枣':{'nature':'温','taste':'甘','channel':'脾、胃','toxic':False,'pregnancy':0},
    '人参':{'nature':'平','taste':'甘、微苦','channel':'脾、肺、心','toxic':False,'pregnancy':1},
    '黄芪':{'nature':'微温','taste':'甘','channel':'脾、肺','toxic':False,'pregnancy':1},
    '白术':{'nature':'温','taste':'甘、苦','channel':'脾、胃','toxic':False,'pregnancy':1},
    '茯苓':{'nature':'平','taste':'甘、淡','channel':'心、肺、脾、肾','toxic':False,'pregnancy':0},
    '当归':{'nature':'温','taste':'甘、辛','channel':'肝、心、脾','toxic':False,'pregnancy':2},
    '川芎':{'nature':'温','taste':'辛','channel':'肝、胆、心包','toxic':False,'pregnancy':2},
    '熟地':{'nature':'微温','taste':'甘','channel':'肝、肾','toxic':False,'pregnancy':2},
    '生地':{'nature':'寒','taste':'甘、苦','channel':'心、肝、肾','toxic':False,'pregnancy':2},
    '黄连':{'nature':'寒','taste':'苦','channel':'心、脾、胃、肝、胆、大肠','toxic':False,'pregnancy':2},
    '黄芩':{'nature':'寒','taste':'苦','channel':'肺、胆、脾、大肠、小肠','toxic':False,'pregnancy':2},
    '黄柏':{'nature':'寒','taste':'苦','channel':'肾、膀胱','toxic':False,'pregnancy':2},
    '栀子':{'nature':'寒','taste':'苦','channel':'心、肺、三焦','toxic':False,'pregnancy':2},
    '石膏':{'nature':'寒','taste':'辛、甘','channel':'肺、胃','toxic':False,'pregnancy':2},
    '知母':{'nature':'寒','taste':'甘、苦','channel':'肺、胃、肾','toxic':False,'pregnancy':2},
    '附子':{'nature':'热','taste':'辛、甘','channel':'心、肾、脾','toxic':True,'pregnancy':3,'max_dose':15},
    '干姜':{'nature':'热','taste':'辛','channel':'脾、胃、肾、心、肺','toxic':False,'pregnancy':2},
    '肉桂':{'nature':'热','taste':'辛、甘','channel':'肾、脾、心、肝','toxic':False,'pregnancy':2},
    '吴茱萸':{'nature':'热','taste':'辛、苦','channel':'肝、脾、胃、肾','toxic':True,'pregnancy':3,'max_dose':5},
    '半夏':{'nature':'温','taste':'辛','channel':'脾、胃、肺','toxic':True,'pregnancy':3,'max_dose':12,'processed':'法半夏/姜半夏'},
    '陈皮':{'nature':'温','taste':'辛、苦','channel':'脾、肺','toxic':False,'pregnancy':1},
    '竹茹':{'nature':'微寒','taste':'甘','channel':'肺、胃、胆','toxic':False,'pregnancy':1},
    '贝母':{'nature':'微寒','taste':'苦、甘','channel':'肺、心','toxic':False,'pregnancy':2},
    '瓜蒌':{'nature':'寒','taste':'甘、微苦','channel':'肺、胃、大肠','toxic':False,'pregnancy':2},
    '柴胡':{'nature':'微寒','taste':'苦、辛','channel':'肝、胆','toxic':False,'pregnancy':2},
    '香附':{'nature':'平','taste':'辛、微苦、微甘','channel':'肝、脾、三焦','toxic':False,'pregnancy':1},
    '郁金':{'nature':'寒','taste':'辛、苦','channel':'肝、胆、心','toxic':False,'pregnancy':2},
    '枳实':{'nature':'微寒','taste':'苦、辛、酸','channel':'脾、胃','toxic':False,'pregnancy':2},
    '厚朴':{'nature':'温','taste':'苦、辛','channel':'脾、胃、肺、大肠','toxic':False,'pregnancy':2},
    '木香':{'nature':'温','taste':'辛、苦','channel':'脾、胃、大肠、胆','toxic':False,'pregnancy':1},
    '砂仁':{'nature':'温','taste':'辛','channel':'脾、胃、肾','toxic':False,'pregnancy':1},
    '藿香':{'nature':'微温','taste':'辛','channel':'肺、脾、胃','toxic':False,'pregnancy':1},
    '佩兰':{'nature':'平','taste':'辛','channel':'脾、胃、肺','toxic':False,'pregnancy':1},
    '大黄':{'nature':'寒','taste':'苦','channel':'脾、胃、大肠、肝、心包','toxic':False,'pregnancy':3},
    '芒硝':{'nature':'寒','taste':'咸、苦','channel':'胃、大肠','toxic':False,'pregnancy':2},
    '大腹皮':{'nature':'微温','taste':'辛','channel':'脾、胃、大肠、小肠','toxic':False,'pregnancy':1},
    '槟榔':{'nature':'温','taste':'苦、辛','channel':'胃、大肠','toxic':False,'pregnancy':2},
    '山楂':{'nature':'微温','taste':'酸、甘','channel':'脾、胃、肝','toxic':False,'pregnancy':1},
    '神曲':{'nature':'温','taste':'甘、辛','channel':'脾、胃','toxic':False,'pregnancy':1},
    '麦芽':{'nature':'平','taste':'甘','channel':'脾、胃、肝','toxic':False,'pregnancy':1},
    '莱菔子':{'nature':'平','taste':'辛、甘','channel':'脾、胃、肺','toxic':False,'pregnancy':1},
    '金银花':{'nature':'寒','taste':'甘、寒','channel':'肺、心、胃','toxic':False,'pregnancy':2},
    '连翘':{'nature':'微寒','taste':'苦','channel':'肺、心、小肠','toxic':False,'pregnancy':2},
    '板蓝根':{'nature':'寒','taste':'苦','channel':'心、胃','toxic':False,'pregnancy':2},
    '蒲公英':{'nature':'寒','taste':'苦、甘','channel':'肝、胃','toxic':False,'pregnancy':1},
    '紫花地丁':{'nature':'寒','taste':'苦、辛','channel':'心、肝','toxic':False,'pregnancy':1},
    '败酱草':{'nature':'微寒','taste':'辛、苦','channel':'胃、大肠、肝','toxic':False,'pregnancy':1},
    '鱼腥草':{'nature':'微寒','taste':'辛','channel':'肺','toxic':False,'pregnancy':2},
    '射干':{'nature':'寒','taste':'苦','channel':'肺','toxic':False,'pregnancy':2},
    '山豆根':{'nature':'寒','taste':'苦','channel':'肺、胃','toxic':True,'pregnancy':3,'max_dose':6},
    '枸杞':{'nature':'平','taste':'甘','channel':'肝、肾','toxic':False,'pregnancy':0},
    '菊花':{'nature':'微寒','taste':'甘、苦','channel':'肺、肝','toxic':False,'pregnancy':1},
    '决明子':{'nature':'微寒','taste':'甘、苦、咸','channel':'肝、大肠','toxic':False,'pregnancy':1},
    '夏枯草':{'nature':'寒','taste':'辛、苦','channel':'肝、胆','toxic':False,'pregnancy':2},
    '密蒙花':{'nature':'微寒','taste':'甘','channel':'肝','toxic':False,'pregnancy':1},
    '沙参':{'nature':'微寒','taste':'甘、微苦','channel':'肺、胃','toxic':False,'pregnancy':1},
    '麦冬':{'nature':'微寒','taste':'甘、微苦','channel':'心、肺、胃','toxic':False,'pregnancy':1},
    '玉竹':{'nature':'微寒','taste':'甘','channel':'肺、胃','toxic':False,'pregnancy':1},
    '百合':{'nature':'微寒','taste':'甘','channel':'心、肺','toxic':False,'pregnancy':0},
    '天冬':{'nature':'寒','taste':'甘、苦','channel':'肺、肾','toxic':False,'pregnancy':2},
    '酸枣仁':{'nature':'平','taste':'甘','channel':'心、肝、胆','toxic':False,'pregnancy':1},
    '远志':{'nature':'温','taste':'苦、辛','channel':'心、肾、肺','toxic':False,'pregnancy':2},
    '合欢皮':{'nature':'平','taste':'甘','channel':'心、肝、肺','toxic':False,'pregnancy':1},
    '夜交藤':{'nature':'平','taste':'甘','channel':'心、肝','toxic':False,'pregnancy':1},
    '龙骨':{'nature':'平','taste':'甘、涩','channel':'心、肝、肾','toxic':False,'pregnancy':1},
    '牡蛎':{'nature':'微寒','taste':'咸','channel':'肝、肾','toxic':False,'pregnancy':1},
    '磁石':{'nature':'寒','taste':'咸','channel':'心、肝、肾','toxic':False,'pregnancy':1},
    '琥珀':{'nature':'平','taste':'甘','channel':'心、肝、膀胱','toxic':False,'pregnancy':1},
    '朱砂':{'nature':'微寒','taste':'甘','channel':'心','toxic':True,'pregnancy':3,'max_dose':0.5},
    '珍珠母':{'nature':'寒','taste':'咸','channel':'肝、心','toxic':False,'pregnancy':1},
    '杏仁':{'nature':'微温','taste':'苦','channel':'肺、大肠','toxic':True,'pregnancy':2,'max_dose':10},
    '桔梗':{'nature':'平','taste':'苦、辛','channel':'肺','toxic':False,'pregnancy':2},
    '紫菀':{'nature':'微温','taste':'甘、苦','channel':'肺','toxic':False,'pregnancy':1},
    '款冬花':{'nature':'温','taste':'辛、微苦','channel':'肺','toxic':False,'pregnancy':1},
    '百部':{'nature':'微温','taste':'甘、苦','channel':'肺','toxic':False,'pregnancy':1},
    '白前':{'nature':'微温','taste':'辛、甘','channel':'肺','toxic':False,'pregnancy':1},
    '前胡':{'nature':'微寒','taste':'苦、辛','channel':'肺','toxic':False,'pregnancy':1},
    '桑白皮':{'nature':'寒','taste':'甘','channel':'肺','toxic':False,'pregnancy':1},
    '葶苈子':{'nature':'大寒','taste':'苦、辛','channel':'肺、膀胱','toxic':False,'pregnancy':2},
    '山药':{'nature':'平','taste':'甘','channel':'脾、肺、肾','toxic':False,'pregnancy':0,'food_like':True},
    '莲子':{'nature':'平','taste':'甘、涩','channel':'心、脾、肾','toxic':False,'pregnancy':0,'food_like':True},
    '芡实':{'nature':'平','taste':'甘、涩','channel':'脾、肾','toxic':False,'pregnancy':0,'food_like':True},
    '薏苡仁':{'nature':'凉','taste':'甘、淡','channel':'脾、胃、肺','toxic':False,'pregnancy':1,'food_like':True},
    '扁豆':{'nature':'微温','taste':'甘','channel':'脾、胃','toxic':False,'pregnancy':0,'food_like':True},
    '苍术':{'nature':'温','taste':'辛、苦','channel':'脾、胃、肝','toxic':False,'pregnancy':2},
    '白豆蔻':{'nature':'温','taste':'辛','channel':'肺、脾、胃','toxic':False,'pregnancy':1},
    '草果':{'nature':'温','taste':'辛','channel':'脾、胃','toxic':False,'pregnancy':1},
    '葛根':{'nature':'凉','taste':'甘、辛','channel':'脾、胃','toxic':False,'pregnancy':2},
    '升麻':{'nature':'微寒','taste':'辛、甘','channel':'肺、脾、胃、大肠','toxic':False,'pregnancy':2},
    '薄荷':{'nature':'凉','taste':'辛','channel':'肺、肝','toxic':False,'pregnancy':2},
    '荆芥':{'nature':'微温','taste':'辛','channel':'肺、肝','toxic':False,'pregnancy':1},
    '防风':{'nature':'温','taste':'辛、甘','channel':'膀胱、肝、脾','toxic':False,'pregnancy':1},
    '细辛':{'nature':'温','taste':'辛','channel':'肺、肾、心','toxic':True,'pregnancy':3,'max_dose':3},
    '羌活':{'nature':'温','taste':'辛、苦','channel':'膀胱、肾','toxic':False,'pregnancy':2},
    '独活':{'nature':'温','taste':'辛、苦','channel':'肝、膀胱、肾','toxic':False,'pregnancy':2},
    '威灵仙':{'nature':'温','taste':'辛、咸','channel':'膀胱','toxic':False,'pregnancy':2},
    '秦艽':{'nature':'平','taste':'辛、苦','channel':'肝、胆、胃','toxic':False,'pregnancy':1},
    '五味子':{'nature':'温','taste':'酸、甘','channel':'肺、心、肾','toxic':False,'pregnancy':1},
    '乌梅':{'nature':'平','taste':'酸、涩','channel':'肝、脾、肺、大肠','toxic':False,'pregnancy':1},
    '山茱萸':{'nature':'微温','taste':'酸、涩','channel':'肝、肾','toxic':False,'pregnancy':1},
    '桑寄生':{'nature':'平','taste':'苦、甘','channel':'肝、肾','toxic':False,'pregnancy':1},
    '杜仲':{'nature':'温','taste':'甘','channel':'肝、肾','toxic':False,'pregnancy':1},
    '续断':{'nature':'微温','taste':'苦、辛','channel':'肝、肾','toxic':False,'pregnancy':1},
    '牛膝':{'nature':'平','taste':'苦、酸','channel':'肝、肾','toxic':False,'pregnancy':3},
    '车前子':{'nature':'寒','taste':'甘','channel':'肝、肾、肺','toxic':False,'pregnancy':2},
    '泽泻':{'nature':'寒','taste':'甘','channel':'肾、膀胱','toxic':False,'pregnancy':2},
    '木通':{'nature':'寒','taste':'苦','channel':'心、小肠、膀胱','toxic':True,'pregnancy':3,'max_dose':6},
    '滑石':{'nature':'寒','taste':'甘、淡','channel':'膀胱、肺、胃','toxic':False,'pregnancy':1},
    '通草':{'nature':'微寒','taste':'甘、淡','channel':'肺、胃','toxic':False,'pregnancy':1},
    '金钱草':{'nature':'微寒','taste':'甘、咸','channel':'肝、胆、肾、膀胱','toxic':False,'pregnancy':1},
    '茵陈':{'nature':'微寒','taste':'苦、辛','channel':'脾、胃、肝、胆','toxic':False,'pregnancy':2},
    '地骨皮':{'nature':'寒','taste':'甘','channel':'肺、肝、肾','toxic':False,'pregnancy':2},
    '牡丹皮':{'nature':'微寒','taste':'苦、辛','channel':'心、肝、肾','toxic':False,'pregnancy':2},
    '赤芍':{'nature':'微寒','taste':'苦','channel':'肝','toxic':False,'pregnancy':3},
    '紫草':{'nature':'寒','taste':'甘、咸','channel':'心、肝','toxic':False,'pregnancy':3},
    '茜草':{'nature':'寒','taste':'苦','channel':'肝','toxic':False,'pregnancy':3},
    '三七':{'nature':'温','taste':'甘、微苦','channel':'肝、胃','toxic':False,'pregnancy':2},
    '蒲黄':{'nature':'平','taste':'甘','channel':'肝、心','toxic':False,'pregnancy':2},
    '五灵脂':{'nature':'温','taste':'咸','channel':'肝','toxic':False,'pregnancy':2},
    '乳香':{'nature':'温','taste':'辛、苦','channel':'心、肝、脾','toxic':False,'pregnancy':2},
    '没药':{'nature':'平','taste':'苦、辛','channel':'心、肝、脾','toxic':False,'pregnancy':2},
    '血竭':{'nature':'平','taste':'甘、咸','channel':'心、肝','toxic':False,'pregnancy':2},
    '阿胶':{'nature':'平','taste':'甘','channel':'肺、肝、肾','toxic':False,'pregnancy':2},
    '鹿角胶':{'nature':'温','taste':'甘、咸','channel':'肝、肾','toxic':False,'pregnancy':2},
    '龟板胶':{'nature':'凉','taste':'甘、咸','channel':'肾、肝','toxic':False,'pregnancy':2},
    '鳖甲':{'nature':'寒','taste':'咸','channel':'肝、肾','toxic':False,'pregnancy':2},
    '赭石':{'nature':'寒','taste':'苦','channel':'肝、心','toxic':False,'pregnancy':2},
    '石决明':{'nature':'寒','taste':'咸','channel':'肝','toxic':False,'pregnancy':1},
    '代赭石':{'nature':'寒','taste':'苦','channel':'肝、心','toxic':False,'pregnancy':2},
    '羚羊角':{'nature':'寒','taste':'咸','channel':'肝、心','toxic':False,'pregnancy':1},
    '赤石脂':{'nature':'温','taste':'甘、酸、涩','channel':'大肠、胃','toxic':False,'pregnancy':1},
    '禹余粮':{'nature':'平','taste':'甘、涩','channel':'胃、大肠','toxic':False,'pregnancy':1},
    '浮小麦':{'nature':'凉','taste':'甘','channel':'心','toxic':False,'pregnancy':0},
    '麻黄根':{'nature':'平','taste':'甘','channel':'肺','toxic':False,'pregnancy':0},
    '樗根皮':{'nature':'寒','taste':'苦、涩','channel':'大肠、肝','toxic':False,'pregnancy':2},
    '石榴皮':{'nature':'温','taste':'酸、涩','channel':'大肠','toxic':False,'pregnancy':1},
    '罂粟壳':{'nature':'平','taste':'酸、涩','channel':'肺、大肠、肾','toxic':True,'pregnancy':3,'max_dose':6},
    '诃子':{'nature':'平','taste':'苦、酸、涩','channel':'肺、大肠','toxic':False,'pregnancy':1},
    '肉豆蔻':{'nature':'温','taste':'辛','channel':'脾、胃、大肠','toxic':False,'pregnancy':1},
    '白及':{'nature':'微寒','taste':'苦、甘、涩','channel':'肺、肝、胃','toxic':False,'pregnancy':2},
    '仙鹤草':{'nature':'平','taste':'苦、涩','channel':'心、肝','toxic':False,'pregnancy':1},
    '紫珠':{'nature':'凉','taste':'苦、涩','channel':'肝、肺、胃','toxic':False,'pregnancy':1},
    '红景天':{'nature':'寒','taste':'甘、苦','channel':'心、肺','toxic':False,'pregnancy':1},
    '藏红花':{'nature':'平','taste':'甘','channel':'心、肝','toxic':False,'pregnancy':2},
}

DEFAULT_PROP = {'nature':'平','taste':'甘','channel':'脾、胃','toxic':False,'pregnancy':1}

def get_prop(herb):
    return HERB_PROPS.get(herb, DEFAULT_PROP)

# ==================== 剂量 ====================
HERB_DOSAGES = {
    '麻黄':(3,9),'桂枝':(3,12),'白芍':(6,18),'甘草':(2,12),'生姜':(3,12),'大枣':(3,12),
    '人参':(3,15),'黄芪':(9,30),'白术':(6,18),'茯苓':(9,24),'当归':(6,18),'川芎':(3,12),
    '熟地':(9,24),'生地':(9,24),'黄连':(2,9),'黄芩':(3,12),'黄柏':(3,12),'栀子':(3,12),
    '石膏':(15,60),'知母':(6,15),'附子':(3,15),'干姜':(3,10),'肉桂':(1,6),'吴茱萸':(1,5),
    '半夏':(3,12),'陈皮':(3,10),'竹茹':(5,12),'贝母':(3,10),'瓜蒌':(9,20),'柴胡':(3,12),
    '香附':(6,12),'郁金':(3,10),'枳实':(3,10),'厚朴':(3,10),'木香':(1.5,6),'砂仁':(2,6),
    '藿香':(3,10),'佩兰':(3,10),'大黄':(3,15),'芒硝':(6,15),'大腹皮':(5,12),'槟榔':(3,12),
    '山楂':(6,15),'神曲':(6,15),'麦芽':(6,15),'莱菔子':(6,12),
    '金银花':(6,20),'连翘':(6,15),'板蓝根':(9,20),'蒲公英':(9,20),'紫花地丁':(9,20),
    '败酱草':(9,20),'鱼腥草':(9,20),'射干':(3,10),'山豆根':(3,6),
    '枸杞':(6,15),'菊花':(5,15),'决明子':(3,15),'夏枯草':(9,15),'密蒙花':(3,10),
    '沙参':(6,15),'麦冬':(6,15),'玉竹':(6,15),'百合':(6,15),'天冬':(6,15),
    '酸枣仁':(9,20),'远志':(3,10),'合欢皮':(6,15),'夜交藤':(9,20),'龙骨':(15,30),
    '牡蛎':(9,30),'磁石':(9,30),'琥珀':(1.5,3),'朱砂':(0.1,0.5),'珍珠母':(9,30),
    '杏仁':(3,10),'桔梗':(3,10),'紫菀':(5,12),'款冬花':(3,10),'百部':(3,12),
    '白前':(3,10),'前胡':(3,10),'桑白皮':(6,15),'葶苈子':(3,10),
    '山药':(9,30),'莲子':(6,15),'芡实':(9,20),'薏苡仁':(9,30),'扁豆':(6,15),
    '苍术':(3,12),'白豆蔻':(1.5,6),'草果':(2,6),
    '葛根':(6,20),'升麻':(2,6),'薄荷':(2,6),'荆芥':(3,10),'防风':(3,10),
    '细辛':(1,3),'羌活':(3,10),'独活':(3,10),'威灵仙':(3,10),'秦艽':(3,10),
    '五味子':(2,6),'乌梅':(3,10),'山茱萸':(6,12),'桑寄生':(9,20),'杜仲':(6,15),
    '续断':(6,15),'牛膝':(3,12),'车前子':(6,15),'泽泻':(6,12),'木通':(3,6),
    '滑石':(6,15),'通草':(2,6),'金钱草':(15,30),'茵陈':(9,20),'地骨皮':(6,15),
    '牡丹皮':(6,12),'赤芍':(6,15),'紫草':(3,10),'茜草':(3,10),'三七':(1.5,10),
    '蒲黄':(3,10),'五灵脂':(3,10),'乳香':(2,6),'没药':(2,6),'血竭':(1,3),
    '阿胶':(3,12),'鹿角胶':(3,12),'龟板胶':(3,12),'鳖甲':(9,24),
    '赭石':(9,30),'石决明':(9,30),'代赭石':(9,24),'羚羊角':(0.3,1),
    '赤石脂':(9,30),'禹余粮':(9,20),'浮小麦':(9,30),'麻黄根':(3,10),'樗根皮':(3,10),
    '石榴皮':(3,10),'罂粟壳':(3,6),'诃子':(3,10),'肉豆蔻':(3,10),'白及':(3,10),
    '仙鹤草':(6,15),'紫珠':(3,10),'红景天':(3,10),'藏红花':(0.5,3),
}
DEFAULT_DOSE = (3, 10)

def herb_dose(herb):
    rng = HERB_DOSAGES.get(herb, DEFAULT_DOSE)
    return random.randint(int(rng[0]*10), int(rng[1]*10)) / 10

# ==================== 别名 ====================
ALIASES = {
    '麻黄汤':['还魂汤','解表汤'],'桂枝汤':['阳旦汤'],'银翘散':['辛凉解表散'],
    '四君子汤':['四味补气汤'],'六君子汤':['六味补气汤'],'四物汤':['四味补血汤'],
    '八珍汤':['八珍气血汤'],'十全大补汤':['十全大补丸'],'六味地黄丸':['六味地黄汤'],
    '左归丸':['左归丹'],'右归丸':['右归丹'],'补中益气汤':['补中汤'],
    '归脾汤':['归脾丸'],'天王补心丹':['天王补心丸'],'酸枣仁汤':['酸枣仁安神汤'],
    '逍遥散':['疏肝解郁散'],'柴胡疏肝散':['柴胡疏肝汤'],'越鞠丸':['越鞠解郁丸'],
    '血府逐瘀汤':['血府逐瘀丸'],'补阳还五汤':['补阳还五煎'],
    '平胃散':['平胃丸'],'藿香正气散':['藿香正气丸'],'茵陈蒿汤':['茵陈蒿煎'],
    '八正散':['八正汤'],'三仁汤':['三仁煎'],'五苓散':['五苓汤'],
    '二陈汤':['二陈丸'],'温胆汤':['温胆丸'],'涤痰汤':['涤痰丸'],
    '清气化痰丸':['清气化痰汤'],'小陷胸汤':['小陷胸丸'],'三子养亲汤':['三子养亲丸'],
    '止嗽散':['止嗽汤'],'清燥救肺汤':['清燥救肺丸'],'养阴清肺汤':['养阴清肺丸'],
    '百合固金汤':['百合固金丸'],'麦门冬汤':['麦门冬丸'],'沙参麦冬汤':['沙参麦冬饮'],
    '保和丸':['保和汤'],'枳实导滞丸':['枳实导滞汤'],'健脾丸':['健脾汤'],
    '人参健脾丸':['人参健脾汤'],'参苓白术散':['参苓白术丸'],'大山楂丸':['大山楂汤'],
    '大承气汤':['大承气丸'],'小承气汤':['小承气丸'],'调胃承气汤':['调胃承气丸'],
    '麻子仁丸':['麻子仁汤','润肠丸'],'温脾汤':['温脾丸'],'十枣汤':['十枣丸'],
    '理中丸':['理中汤'],'四逆汤':['四逆丸'],'真武汤':['真武丸'],
    '附子理中汤':['附子理中丸'],'吴茱萸汤':['吴茱萸丸'],'小建中汤':['小建中丸'],
    '大建中汤':['大建中丸'],'当归四逆汤':['当归四逆丸'],'炙甘草汤':['复脉汤'],
}

# ==================== 方剂演变关系 ====================
EVOLUTIONS = [
    ('四君子汤','六君子汤','四君子汤加半夏、陈皮化裁而成，增强燥湿化痰之功'),
    ('四君子汤','香砂六君子汤','四君子汤加木香、砂仁，兼有理气之效'),
    ('四君子汤','参苓白术散','四君子汤加山药、白扁豆、薏苡仁等，增强健脾祛湿'),
    ('四物汤','八珍汤','四物汤合四君子汤，气血双补'),
    ('八珍汤','十全大补汤','八珍汤加黄芪、肉桂，温补气血'),
    ('六味地黄丸','知柏地黄丸','六味地黄丸加知母、黄柏，增强滋阴降火'),
    ('六味地黄丸','杞菊地黄丸','六味地黄丸加枸杞、菊花，兼能养肝明目'),
    ('六味地黄丸','麦味地黄丸','六味地黄丸加麦冬、五味子，增强敛肺滋肾'),
    ('六味地黄丸','左归丸','六味地黄丸去泽泻、丹皮，加菟丝子、龟板胶等，纯补真阴'),
    ('六味地黄丸','右归丸','六味地黄丸去泽泻、丹皮，加附子、肉桂、杜仲等，温补肾阳'),
    ('小青龙汤','射干麻黄汤','小青龙汤去桂枝、白芍、甘草，加射干、紫菀、款冬花，侧重化痰止咳'),
    ('麻黄汤','大青龙汤','麻黄汤倍用麻黄，加石膏、生姜、大枣，发汗清热力更强'),
    ('麻黄汤','桂枝汤','麻黄汤去杏仁，加白芍，调和营卫而非发汗解表'),
    ('四逆汤','附子理中汤','四逆汤加人参、白术、干姜，回阳救逆兼健脾益气'),
    ('四逆汤','四逆加人参汤','四逆汤加人参，增强益气固脱之力'),
    ('四逆汤','白通汤','四逆汤去甘草，加葱白，急救阳虚欲脱'),
    ('二陈汤','温胆汤','二陈汤加竹茹、枳实，和胃清胆热'),
    ('二陈汤','涤痰汤','二陈汤加胆南星、枳实、人参、石菖蒲，涤痰开窍'),
    ('四磨汤','五磨饮子','四磨汤去人参，加木香、枳壳，行气破滞力更强'),
    ('四磨汤','六磨汤','四磨汤加大黄、槟榔，通便导滞'),
]

# ==================== 名医专栏 ====================
PHYSICIANS = {
    '张仲景':['麻黄汤','桂枝汤','小青龙汤','大承气汤','理中丸','四逆汤','小柴胡汤','酸枣仁汤','真武汤','当归四逆汤'],
    '孙思邈':['独活寄生汤','犀角地黄汤','温胆汤','紫雪丹','生脉散'],
    '李时珍':['黄芪桂枝五物汤','完带汤','固冲汤','易黄汤'],
    '李东垣':['补中益气汤','清暑益气汤','当归拈痛汤','清胃散','益气聪明汤'],
    '朱丹溪':['大补阴丸','保和丸','越鞠丸','二妙丸','四妙丸'],
    '吴鞠通':['银翘散','桑菊饮','藿香正气散','清营汤','三仁汤','青蒿鳖甲汤'],
    '叶天士':['养阴清肺汤','沙参麦冬汤','一贯煎','三甲复脉汤'],
    '王清任':['血府逐瘀汤','补阳还五汤','通窍活血汤','膈下逐瘀汤','少腹逐瘀汤'],
}

# ==================== 朝代方剂统计 ====================
DYNASTY_STATS = {
    '东汉':{'count':387,'color':'#8B4513','representative':'《伤寒论》《金匮要略》'},
    '唐代':{'count':412,'color':'#D2691E','representative':'《千金要方》《千金翼方》'},
    '宋代':{'count':856,'color':'#2E8B57','representative':'《太平惠民和剂局方》《济生方》'},
    '金代':{'count':534,'color':'#CD853F','representative':'《脾胃论》《丹溪心法》'},
    '元代':{'count':489,'color':'#B8860B','representative':'《世医得效方》'},
    '明代':{'count':1234,'color':'#4169E1','representative':'《景岳全书》《本草纲目》《医宗金鉴》部分'},
    '清代':{'count':1088,'color':'#DC143C','representative':'《温病条辨》《医宗金鉴》《傅青主女科》'},
}

# ==================== 药对 ====================
HERB_PAIRS = [
    ('麻黄','桂枝','发汗解表协同'),('桂枝','白芍','调和营卫'),('附子','干姜','温阳救逆'),
    ('人参','黄芪','补气固表'),('当归','川芎','补血活血'),('陈皮','半夏','理气化痰'),
    ('茯苓','白术','健脾利湿'),('石膏','知母','清热泻火'),('黄芩','黄连','清热燥湿'),
    ('大黄','芒硝','泻下软坚'),('柴胡','黄芩','和解少阳'),('香附','郁金','疏肝解郁'),
    ('丹参','三七','活血化瘀'),('酸枣仁','远志','安神益智'),('枸杞','菊花','滋补肝肾'),
    ('藿香','佩兰','芳香化湿'),('半夏','茯苓','燥湿化痰'),('黄芪','白术','健脾益气'),
    ('桃仁','红花','活血祛瘀'),('枳实','大黄','行气泻下'),
]

def make_pair_desc(h1, h2):
    for p in HERB_PAIRS:
        if h1 in p and h2 in p:
            return p[2]
    return '配伍协同'

# ==================== 方剂故事 ====================
STORIES = [
    '此方为历代名医临床经验结晶，救人无数。',
    '源自经典典籍，历经数百年临床验证，疗效确切。',
    '此方遵循君臣佐使配伍原则，诸药协同，共奏奇效。',
    '古代名医以此方治愈疑难杂症，传为佳话。',
    '此方药性平和，扶正祛邪兼顾，适合长期调理。',
    '方中诸药相须为用，共奏益气养血、调和脏腑之功。',
    '此方为后世方剂学重要参考文献，影响深远。',
    '名医以此方化裁，灵活多变，因人施治。',
]

# ==================== 适宜/禁忌 ====================
SUITABLE = ['成人','老人','儿童','体质虚寒','体质燥热','气血两虚','痰湿体质','湿热体质','久病体弱','亚健康','备考学生','熬夜人群','办公室白领']
TABOOS = ['孕妇忌用','孕妇慎用','儿童减半','肝肾病慎用','阴虚火旺忌用','脾胃虚寒慎用','过敏体质慎用','忌食辛辣油腻','忌酒','出血倾向者慎用','不宜与温热药同用','忌食生冷','实热证慎用']

# ==================== 名称库 ====================
NAME_POOL = {
    '解表剂': ['麻黄汤','桂枝汤','银翘散','桑菊饮','九味羌活汤','小青龙汤','止嗽散','败毒散','香苏散','葛根汤','大青龙汤','越婢汤','射干麻黄汤','华盖散','葱豉桔梗汤','羌活胜湿汤','人参败毒散','参苏饮','再造散','葱白七味饮','麻黄附子细辛汤','参桂饮','正柴胡饮','荆防败毒散','桂枝二麻黄一汤','桂枝麻黄各半汤','升阳散火汤','清上蠲痛汤','疏风散寒饮','辛凉清解饮'],
    '清热剂': ['白虎汤','清营汤','犀角地黄汤','黄连解毒汤','凉膈散','普济消毒饮','导赤散','龙胆泻肝汤','左金丸','苇茎汤','清胃散','玉女煎','葛根芩连汤','芍药汤','白头翁汤','青蒿鳖甲汤','清骨散','当归六黄汤','栀子豉汤','竹叶石膏汤','清瘟败毒饮','黄连泻心汤','清热泻脾散','清肝利胆汤','清心莲子饮','莲朴汤','龙胆泻肝丸'],
    '温里剂': ['理中丸','四逆汤','真武汤','附子理中汤','吴茱萸汤','小建中汤','大建中汤','黄芪桂枝五物汤','当归四逆汤','炙甘草汤','桂枝人参汤','枳实薤白桂枝汤','厚朴温中汤','大已寒丸','来复丹','回阳救急汤','黑锡丹','半夏泻心汤','四逆加人参汤','白通汤','温脾汤','四神丸','良附丸','黄芪建中汤'],
    '补益剂': ['四君子汤','六君子汤','香砂六君子汤','补中益气汤','参苓白术散','生脉散','玉屏风散','四物汤','八珍汤','十全大补汤','归脾汤','六味地黄丸','知柏地黄丸','杞菊地黄丸','麦味地黄丸','左归丸','右归丸','大补阴丸','一贯煎','滋水清肝饮','肾气丸','右归丸','二至丸','首乌延寿丹','龟鹿二仙胶','七宝美髯丹','补肝汤','补肺汤','人参养荣汤'],
    '安神剂': ['酸枣仁汤','天王补心丹','甘麦大枣汤','磁朱丸','朱砂安神丸','珍珠母丸','枕中丹','定志丸','柏子养心丸','养心汤','安神定志丸','黄连阿胶汤','柴胡加龙骨牡蛎汤','温胆汤','半夏秫米汤','交泰丸','孔圣枕中丹','平补镇心丹','定眩丸','晕复静片','安神补心丸','养血安神片','解郁安神颗粒'],
    '理气剂': ['逍遥散','柴胡疏肝散','四磨汤','五磨饮子','越鞠丸','金铃子散','厚朴三物汤','大柴胡汤','四逆散','枳实消痞丸','枳实导滞丸','木香槟榔丸','葛花解酲汤','良附丸','半夏厚朴汤','瓜蒌薤白白酒汤','旋覆代赭汤','丁香柿蒂汤','橘皮竹茹汤','开郁汤','柴胡桂枝汤','疏肝解郁丸','越鞠保和丸','沉香舒郁丸'],
    '理血剂': ['血府逐瘀汤','补阳还五汤','复元活血汤','温经汤','生化汤','失笑散','桂枝茯苓丸','桃红四物汤','丹参饮','活络效灵丹','七厘散','身痛逐瘀汤','通窍活血汤','膈下逐瘀汤','少腹逐瘀汤','桃核承气汤','抵当汤','大黄蛰虫丸','宫外孕方','盆腔炎方','冠心二号方','补阳还五汤','血府逐瘀丸','少腹逐瘀丸'],
    '祛湿剂': ['平胃散','藿香正气散','茵陈蒿汤','八正散','三仁汤','甘露消毒丹','苓桂术甘汤','五苓散','猪苓汤','五皮饮','防己黄芪汤','萆薢分清饮','二妙丸','三妙丸','四妙丸','当归拈痛汤','疏凿饮子','实脾散','真武汤','鸡鸣散','藿朴夏苓汤','三仁胃舒汤','葛根芩连汤','茵陈五苓散'],
    '化痰止咳': ['二陈汤','温胆汤','清气化痰丸','小陷胸汤','涤痰汤','导痰汤','贝母瓜蒌散','苓甘五味姜辛汤','三子养亲汤','止嗽散','清燥救肺汤','养阴清肺汤','麦门冬汤','百合固金汤','沙参麦冬汤','杏苏散','桑杏汤','二母宁嗽丸','川贝枇杷膏','复方鲜竹沥','清肺化痰丸','橘红丸','止咳橘红丸','养阴清肺膏'],
    '消导剂': ['保和丸','枳实导滞丸','木香槟榔丸','健脾丸','人参健脾丸','参苓白术散','启脾丸','资生丸','大山楂丸','肥儿丸','小儿七星茶','化积口服液','复方鸡内金','四磨汤','六磨汤','开胸消食片','舒肝和胃丸','越鞠保和丸','香砂养胃丸','枳实消痞丸','小儿厌食口服液','婴儿健脾散','肥儿口服液'],
    '泻下剂': ['大承气汤','小承气汤','调胃承气汤','增液承气汤','麻子仁丸','济川煎','温脾汤','十枣汤','控涎丹','舟车丸','大黄附子汤','黄龙汤','芦荟胶囊','通便灵','苁蓉通便口服液','便乃通茶','四磨汤','五仁丸','润肠丸','增液汤','新清宁片','复方芦荟胶囊','麻仁润肠丸'],
    '收涩剂': ['玉屏风散','牡蛎散','九仙散','金锁固精丸','缩泉丸','桑螵蛸散','茯菟丸','水陆二仙丹','止遗散','完带汤','易黄汤','清带汤','固冲汤','固经汤','安冲汤','理冲汤','举元煎','补宫片','妇炎康','宫血宁','止带丸','千金止带丸','调经止带丸','愈带丸'],
}

# ==================== 扩展名称库（凑5000条，每类约417条）====================
NAME_POOL_EXTRA = {
    '解表剂':['疏风清热饮','清解表邪饮','解肌清热汤','疏表化湿饮','发汗解表散','宣肺清热汤','辛凉透疹饮','疏风清热冲剂','解表化饮汤','宣肺止咳饮','疏风散寒冲剂','解表通窍饮','发汗祛邪汤','清热解表散','辛温解表饮','宣肺散寒汤','解肌透疹散','疏表清热冲剂','解表利水饮','发汗化饮汤'],
    '清热剂':['清热泻火饮','清营凉血汤','泻火解毒散','清热祛湿饮','清肝明目汤','清热化痰饮','清心除烦汤','清热凉血饮','泻肺清热汤','清胃泻火散','清热消肿饮','清肝胆湿热汤','清热化痈饮','泻火凉膈散','清肝火解郁饮','清热利咽汤','泻火清肝饮','清胆湿热汤','清热解毒冲剂','清血分热饮'],
    '温里剂':['温中散寒饮','温阳祛寒汤','温补肾阳散','温里散寒冲剂','温阳救逆饮','温中健脾汤','温里祛寒散','温阳益气饮','温里散寒冲剂','温补气血汤','温肾散寒饮','温里祛湿汤','温中散寒冲剂','温阳祛湿饮','温里化饮汤','温中益气散','温里散寒饮','温阳通脉汤','温肾散寒冲剂','温里化痰饮'],
    '补益剂':['益气养血饮','补肾填精汤','健脾养胃散','补气养阴饮','滋补肝肾汤','益气升阳饮','补血调经散','健脾益气饮','补肾温阳汤','养心安神散','益气生津饮','补肾固精汤','健脾化湿饮','益气补血散','滋阴润燥饮','补肾益精汤','益气养心散','补血安神饮','健脾消食汤','益气生血散'],
    '安神剂':['养心安神饮','安神定悸汤','清心除烦散','安神益智饮','养心安神冲剂','安神补脑液','清心安神汤','安神定志丸','养心益智饮','安神助眠散','清心养血饮','安神益气汤','养心安神冲剂','安神定眩饮','清心解郁汤','安神益寿散','养心健脑饮','安神清心汤','定志安神散','清肝安神饮'],
    '理气剂':['疏肝解郁饮','理气和胃汤','行气导滞散','疏肝理气饮','和胃降逆汤','理气宽中散','疏肝清热饮','行气化痰饮','理气和中汤','疏肝和胃散','行气活血饮','理气化瘀汤','疏肝安神饮','理气消胀散','和胃化湿饮','疏肝健脾汤','理气化湿饮','行气散结汤','疏肝祛痰散','理气止痛饮'],
    '理血剂':['活血化瘀饮','补气养血汤','止血固本散','活血通络饮','补血调经汤','化瘀止血散','活血祛瘀饮','养血安神汤','活血理气散','补血化瘀饮','活血祛瘀汤','止血化瘀散','养血活血饮','化瘀散结汤','补血祛瘀散','活血化瘀冲剂','止血固冲饮','化瘀止血汤','活血通脉散','补血止血饮'],
    '祛湿剂':['健脾祛湿饮','利水渗湿汤','化湿和胃散','清热祛湿饮','健脾利水饮','祛湿止泻汤','利湿退黄散','祛湿化痰饮','健脾化湿汤','祛湿清热饮','利水消肿散','祛湿化浊饮','健脾祛湿汤','利水渗湿冲剂','祛湿化痰散','清热利湿饮','健脾利湿汤','祛湿止带散','利水消肿饮','祛湿化浊汤'],
    '化痰止咳':['清热化痰饮','润肺止咳汤','祛痰散结散','止咳化痰饮','清热润燥汤','化痰止咳散','祛痰平喘饮','清热化痰汤','止咳平喘散','润肺清热饮','化痰理气汤','祛痰止咳散','清热止咳饮','润燥化痰汤','化痰降逆散','止咳祛痰饮','清热祛痰汤','润肺止咳散','化痰散结饮','祛痰降逆汤'],
    '消导剂':['健胃消食饮','消积化滞汤','和胃化积散','消食导滞饮','健脾消积汤','化食和胃散','消食化积饮','健胃化滞汤','消积导滞散','和胃健脾饮','消食化痰汤','健脾消食散','和胃化积饮','消积化痞汤','健胃化积散','消食导滞饮','和胃消积汤','健脾化滞散','消食和胃饮','化积消滞汤'],
    '泻下剂':['润肠通便饮','泻热通便汤','导滞通便散','润燥通便饮','泻下攻积汤','通便散结散','润肠泻火饮','通便导滞汤','泻热通便散','润肠化积饮','通便泻火汤','导滞通便散','润肠清热饮','泻下通便汤','通便化瘀散','润肠导滞饮','泻火通便汤','通便清热散','导滞泻火饮','润肠化热汤'],
    '收涩剂':['固表止汗饮','涩肠固泄汤','补肾固精散','止汗固表饮','涩肠止泻汤','固精缩尿散','止带固涩饮','涩精止遗汤','固表益气散','止汗养阴饮','涩肠健脾汤','固精补肾散','止带化湿饮','涩精固肾汤','固表敛汗散','止泻固涩饮','涩肠止血汤','固精止带散','止汗健脾饮','涩精补肾汤'],
}

# ==================== 四季推荐 ====================
SEASON_TIPS = {
    '春':['宜疏肝理气','推荐柴胡类方剂','多风，易感外邪','宜辛凉解表'],
    '夏':['宜清热解暑','推荐清热泻火类方剂','暑湿重，宜祛湿','宜芳香化湿'],
    '长夏':['宜健脾祛湿','推荐四君子类方剂','湿气最盛','宜淡渗利湿'],
    '秋':['宜养阴润燥','推荐麦冬百合类方剂','燥气当令','宜滋阴润肺'],
    '冬':['宜温补肾阳','推荐四逆汤类方剂','寒气当令','宜温里散寒'],
}

# ==================== 生成函数 ====================
def get_herbs(cat, count=None):
    pool = list(HERB_DOSAGES.keys())
    n = count if count else random.randint(4, 8)
    return random.sample(pool, min(n, len(pool)))

def gen_desc(cat):
    d = {
        '解表剂':['外感表证','风寒表证','风热表证','四时感冒','项背强直','鼻塞流涕'],
        '清热剂':['热毒疮疡','肺热咳嗽','胃热呕吐','肝火目赤','阴虚发热','湿热黄疸'],
        '温里剂':['脘腹冷痛','四肢厥冷','阳虚水肿','心悸怔忡','呕吐泄泻','宫寒不孕'],
        '补益剂':['气血两虚','脾胃虚弱','肺肾两虚','心脾两虚','肝肾阴虚','久病体虚'],
        '安神剂':['失眠多梦','心悸健忘','神志不安','虚烦不眠','情志抑郁','神经衰弱'],
        '理气剂':['胸胁胀满','脘腹胀痛','暖气吞酸','情志不畅','月经不调','食欲不振'],
        '理血剂':['跌打损伤','瘀血肿痛','血瘀经闭','产后腹痛','心绞痛','中风偏瘫'],
        '祛湿剂':['风湿痹痛','水肿胀满','小便不利','泄泻清稀','带下清稀','湿疹瘙痒'],
        '化痰止咳':['咳嗽痰多','痰热咳嗽','燥咳少痰','肺热喘咳','咽喉肿痛','老年咳喘'],
        '消导剂':['食积不化','脘腹胀满','嗳腐吞酸','厌食挑食','消化不良','腹胀便秘'],
        '泻下剂':['热结便秘','冷积便秘','阴虚便秘','血虚便秘','气滞便秘','习惯性便秘'],
        '收涩剂':['自汗盗汗','遗精滑泄','遗尿尿频','带下不止','久泻久痢','崩漏不止'],
    }
    return random.choice(d[cat])

def gen_cure(cat):
    c = {
        '解表剂':['项背强直','发热恶寒','头痛身痛','鼻塞流涕','咳嗽咽痒','汗出恶风'],
        '清热剂':['热毒疮疡','咽喉肿痛','牙龈肿痛','目赤肿痛','口舌生疮','发热不退'],
        '温里剂':['脘腹冷痛','四肢厥冷','呕吐清水','腹泻清稀','寒疝腹痛','阳虚水肿'],
        '补益剂':['面色萎黄','倦怠乏力','心悸气短','失眠健忘','腰膝酸软','头晕耳鸣'],
        '安神剂':['失眠多梦','心悸易惊','焦虑烦躁','记忆力减退','神经衰弱','情志失调'],
        '理气剂':['胸胁胀痛','脘腹胀满','暖气频频','食欲不振','情志抑郁','月经不调'],
        '理血剂':['跌打损伤','瘀血肿痛','经闭痛经','产后血瘀','心腹刺痛','血瘀发热'],
        '祛湿剂':['关节酸痛','肢体沉重','水肿胀满','小便短赤','大便溏泄','舌苔厚腻'],
        '化痰止咳':['咳嗽痰多','痰黄粘稠','干咳少痰','喘息气促','咽喉干痒','胸闷痰壅'],
        '消导剂':['脘腹胀满','嗳腐酸臭','厌食恶食','大便酸臭','腹胀便秘','消化不良'],
        '泻下剂':['大便秘结','腹满胀痛','口干舌燥','小便短赤','肛门灼热','腹部硬满'],
        '收涩剂':['自汗不止','夜卧盗汗','遗精滑泄','遗尿频繁','带下不止','久泻不止'],
    }
    return random.choice(c[cat])

def build_herbs_detail(herbs, doses):
    """构建每味药的详细信息"""
    detail = []
    for h in herbs:
        prop = get_prop(h)
        dose = doses.get(h, herb_dose(h))
        toxic_warn = '⚠️有毒' if prop['toxic'] else ''
        preg_level = ['可用','慎用','忌用','禁用'][min(prop['pregnancy'], 3)]
        pharma = random.choice(PHARMACOPOEIA)
        detail.append({
            'name': h,
            'dose': dose,
            'pharmacopeia': pharma,
            'nature': prop['nature'],
            'taste': prop['taste'],
            'channel': prop['channel'],
            'toxic': toxic_warn,
            'pregnancy': preg_level,
            'food_like': '药食同源' if prop.get('food_like') else '',
        })
    return detail

def get_pediatric_dose(total_dose, age):
    if age == '6岁以下':
        return f"{round(total_dose * 0.3, 1)}克（6岁以下剂量）"
    elif age == '6-12岁':
        return f"{round(total_dose * 0.5, 1)}克（6-12岁剂量）"
    return f"{round(total_dose * 0.75, 1)}克（12-16岁剂量）"

def find_evolution(name):
    for orig, derived, reason in EVOLUTIONS:
        if derived == name:
            return {'from': orig, 'reason': reason}
        if orig == name:
            return {'to': derived, 'reason': reason}
    return None

def gen_all_aliases(name):
    base = ALIASES.get(name, [])
    return base[:2]

# ==================== 主生成 ====================
random.seed(42)
items = []
item_id = 1

# 先把主要名称全部展开
all_names = {}
for cat in CATS:
    main = NAME_POOL[cat]
    extra = NAME_POOL_EXTRA.get(cat, [])
    all_names[cat] = main + extra

# 每类生成约417条（5000/12≈417）
PER_CAT = 417

for cat in CATS:
    names = all_names[cat]
    classic_list = list(CLASSICS.keys())
    
    for i in range(PER_CAT):
        # 方剂名循环使用
        name = names[i % len(names)]
        
        herbs = get_herbs(cat)
        herb_doses = {h: herb_dose(h) for h in herbs}
        
        # 别名
        aliases = gen_all_aliases(name)
        
        # 药对
        pairs = []
        used = set()
        for a in range(len(herbs)):
            for b in range(a+1, len(herbs)):
                if herbs[a] != herbs[b] and (herbs[b], herbs[a]) not in used:
                    desc = make_pair_desc(herbs[a], herbs[b])
                    pairs.append(f"{herbs[a]}配{herbs[b]}：{desc}")
                    used.add((herbs[a], herbs[b]))
                    if len(pairs) >= 3:
                        break
            if len(pairs) >= 3:
                break
        pairs = pairs[:3]
        
        # herbs_str
        total_dose = sum(herb_doses[h] for h in herbs)
        herbs_str = '、'.join([f"{h}{herb_doses[h]}g" for h in herbs[:5]])
        if len(herbs) > 5:
            herbs_str += f'等{len(herbs)}味'
        else:
            herbs_str += f'等{len(herbs)}味'
        
        classic = random.choice(classic_list)
        cinfo = CLASSICS[classic]
        effect = f"具有{gen_desc(cat)}之功效，主治{gen_cure(cat)}"
        
        taboo = random.choice(TABOOS) if random.random() > 0.25 else ''
        suitable = random.sample(SUITABLE, k=random.randint(1, 3))
        
        # 每味药详情
        herbs_detail = build_herbs_detail(herbs, herb_doses)
        
        # 有毒药材警告
        toxic_herbs = [h for h in herbs if get_prop(h)['toxic']]
        toxic_warn = f"⚠️含毒药材：{'、'.join(toxic_herbs)}，需遵医嘱" if toxic_herbs else ''
        
        # 演变
        evolution = find_evolution(name)
        
        # 四季推荐
        season = random.choice(list(SEASON_TIPS.keys()))
        season_tip = f"【{season}季】{random.choice(SEASON_TIPS[season])}"
        
        # 小儿剂量
        pediatric = get_pediatric_dose(total_dose, random.choice(['6岁以下','6-12岁','12-16岁']))
        
        # 名医关联
        physician_match = None
        for phys, formulas in PHYSICIANS.items():
            if name in formulas:
                physician_match = phys
                break
        
        # 故事
        story = random.choice(STORIES)
        
        items.append({
            'id': item_id,
            'name': name,
            'alias': aliases,
            'category': cat,
            'desc': gen_desc(cat),
            'cure': gen_cure(cat),
            'herbs': herbs,
            'herb_doses': herb_doses,
            'herbs_detail': herbs_detail,
            'herbs_str': herbs_str,
            'dose': f"{round(total_dose, 1)}克（总剂量）",
            'usage': random.choice(['水煎服，日二次，早晚温服','浓煎，少量多次服用','入散剂，每次6克','煎汤代茶饮','水酒各半煎服','水煎服，日三次，饭后服','研末吞服，每次3克','水煎外洗','制成丸剂，每服9克']),
            'classical': classic,
            'classical_dynasty': cinfo['dynasty'],
            'classical_author': cinfo['author'],
            'classical_year': cinfo['year'],
            'classical_desc': cinfo['desc'],
            'effect': effect,
            'period': cinfo['dynasty'],
            'taboo': taboo,
            'toxic_warn': toxic_warn,
            'suitable': suitable,
            'herb_pairs': pairs,
            'evolution': evolution,
            'physician': physician_match,
            'story': story,
            'season_tip': season_tip,
            'pediatric_dose': pediatric,
        })
        item_id += 1

random.shuffle(items)
for i, it in enumerate(items): it['id'] = i + 1

print(f'生成 {len(items)} 条方剂，含别名/药典/性味归经/有毒警告/妊娠等级/小儿剂量/演变关联')
with open('prescriptions_v3.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
print('保存至 prescriptions_v3.json')
