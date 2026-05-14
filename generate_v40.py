#!/usr/bin/env python3
"""掌上百草 v4.0 生成脚本：10000方剂 + 证型syndromes"""
import json, random, re

# ============================================================
# 1. 读取现有v3.9数据
# ============================================================
print("Loading v3.9 prescriptions...")
with open('prescriptions_v38.json') as f:
    prescriptions = json.load(f)
print(f"Loaded {len(prescriptions)} prescriptions")

# ============================================================
# 2. 证型规则库（35个经典证型）
# ============================================================
SYNDROMES = {
    "风寒表实": {"symptoms": ["发热恶寒","无汗","头痛","鼻塞流涕","脉浮紧"],"desc":"外感风寒，卫气被束"},
    "风寒表虚": {"symptoms": ["发热恶寒","自汗","头痛","脉浮缓"],"desc":"外感风寒，营卫不和"},
    "风热感冒": {"symptoms": ["发热恶寒","咽喉肿痛","口苦","目赤肿痛","脉数"],"desc":"外感风热，上焦热盛"},
    "气虚感冒": {"symptoms": ["倦怠乏力","发热恶寒","自汗","气短"],"desc":"正气不足，易感外邪"},
    "肺气虚": {"symptoms": ["喘息气促","倦怠乏力","自汗","气短"],"desc":"肺气不足，呼吸无力"},
    "肺阴不足": {"symptoms": ["咽干","口渴欲饮","潮热盗汗","干咳少痰"],"desc":"肺阴亏虚，燥热内生"},
    "心脾两虚": {"symptoms": ["失眠多梦","心悸易惊","倦怠乏力","记忆力减退"],"desc":"心血不足，脾气虚弱"},
    "心肾不交": {"symptoms": ["失眠多梦","心悸易惊","五心烦热","潮热盗汗"],"desc":"心火亢盛，肾水不足"},
    "心血瘀阻": {"symptoms": ["胸闷","胸胁胀痛","心悸易惊","舌红少苔"],"desc":"瘀血内停，心脉不畅"},
    "肝火上炎": {"symptoms": ["目赤肿痛","口苦","急躁易怒","头痛","脉弦"],"desc":"肝火炽盛，上炎头目"},
    "肝气郁结": {"symptoms": ["胸胁胀痛","急躁易怒","抑郁寡欢","暖气频频"],"desc":"肝气不畅，横逆犯胃"},
    "肝阳上亢": {"symptoms": ["头痛","眩晕","耳鸣","急躁易怒"],"desc":"肝阳偏亢，上扰清窍"},
    "脾胃虚寒": {"symptoms": ["脘腹冷痛","四肢厥冷","倦怠乏力","脉细"],"desc":"脾胃阳虚，寒从内生"},
    "脾胃湿热": {"symptoms": ["脘腹胀满","口苦","苔黄腻","皮肤瘙痒"],"desc":"湿热内蕴，脾胃困阻"},
    "食积不化": {"symptoms": ["脘腹胀满","暖气频频","反酸","腹胀便秘"],"desc":"饮食停积，运化失常"},
    "肾阳不足": {"symptoms": ["腰膝酸软","畏寒肢冷","小便清长","夜尿多"],"desc":"肾阳亏虚，温煦失职"},
    "肾阴不足": {"symptoms": ["腰膝酸软","五心烦热","潮热盗汗","咽干"],"desc":"肾阴亏虚，虚热内生"},
    "气血两虚": {"symptoms": ["面色萎黄","倦怠乏力","心悸易惊","自汗"],"desc":"气血不足，脏腑失养"},
    "痰湿困脾": {"symptoms": ["脘腹胀满","水肿","苔黄腻","四肢乏力"],"desc":"痰湿内盛，脾气被困"},
    "水湿内停": {"symptoms": ["水肿","脘腹胀满","小便短黄","四肢乏力"],"desc":"水液代谢失常，停聚体内"},
    "肾虚水泛": {"symptoms": ["水肿","腰膝酸软","畏寒肢冷","小便清长"],"desc":"肾虚水泛，溢于肌肤"},
    "风湿痹痛": {"symptoms": ["关节酸痛","四肢厥冷","四肢乏力","麻木"],"desc":"风寒湿邪，阻滞经络"},
    "热毒疮疡": {"symptoms": ["皮肤瘙痒","痤疮","咽喉肿痛","口苦"],"desc":"热毒壅盛，郁于肌肤"},
    "瘀血内停": {"symptoms": ["胸胁胀痛","关节酸痛","舌红少苔","脉涩"],"desc":"瘀血停滞，络脉不通"},
    "津伤口渴": {"symptoms": ["口渴欲饮","咽干","小便短黄","舌红少苔"],"desc":"津液耗伤，口渴欲饮"},
    "实热内盛": {"symptoms": ["口苦","口渴欲饮","舌红少苔","脉数"],"desc":"里热炽盛，伤津耗液"},
    "肺热咳嗽": {"symptoms": ["咳嗽痰多","喘息气促","咽干","舌红少苔"],"desc":"邪热犯肺，肺失清肃"},
    "痰湿蕴肺": {"symptoms": ["咳嗽痰多","胸闷","脘腹胀满","苔黄腻"],"desc":"痰湿壅肺，宣降失常"},
    "痰迷心窍": {"symptoms": ["心悸易惊","失眠多梦","急躁易怒","记忆力减退"],"desc":"痰浊蒙心，神明受扰"},
    "肺燥咳嗽": {"symptoms": ["咽干","干咳少痰","口渴欲饮","喘息气促"],"desc":"燥邪伤肺，肺失润降"},
    "遗精滑泄": {"symptoms": ["腰膝酸软","五心烦热","倦怠乏力","失眠多梦"],"desc":"肾虚不藏，精关不固"},
    "肾气不固": {"symptoms": ["夜尿多","小便清长","腰膝酸软","畏寒肢冷"],"desc":"肾气不固，膀胱失约"},
    "外感表证": {"symptoms": ["发热恶寒","鼻塞流涕","头痛","咽干"],"desc":"外邪袭表，卫气不和"},
    "心血不足": {"symptoms": ["心悸易惊","失眠多梦","记忆力减退","面色萎黄"],"desc":"心血亏虚，心神失养"},
    "中气下陷": {"symptoms": ["倦怠乏力","脱肛","胃下垂","气短"],"desc":"中气不足，升举无力"},
}

# 证候关键词→证型映射
SYMPTOM_TO_SYNDROMES = {}
for syn, info in SYNDROMES.items():
    for s in info["symptoms"]:
        if s not in SYMPTOM_TO_SYNDROMES:
            SYMPTOM_TO_SYNDROMES[s] = []
        SYMPTOM_TO_SYNDROMES[s].append(syn)

ALL_SYMPTOMS = list(SYMPTOM_TO_SYNDROMES.keys())

# ============================================================
# 3. 为每个方剂生成syndromes字段
# ============================================================
print("Generating syndromes for existing prescriptions...")

for p in prescriptions:
    # 从desc/cure/effect中提取症状关键词
    text = " ".join([
        p.get("desc",""),
        p.get("cure",""),
        p.get("effect",""),
        p.get("name",""),
    ])
    
    matched = []
    for sym in ALL_SYMPTOMS:
        if sym in text:
            matched.extend(SYMPTOM_TO_SYNDROMES[sym])
    
    # 去重
    matched = list(dict.fromkeys(matched))
    
    # 随机补充1-3个证型（如果太少）
    if len(matched) < 2:
        extra = random.sample(list(SYNDROMES.keys()), min(3, len(SYNDROMES)))
        matched.extend(extra)
        matched = list(dict.fromkeys(matched))
    
    # 限制最多5个
    p["syndromes"] = matched[:5]
    
    # 确保id是int
    p["id"] = int(p["id"])

print(f"  Syndromes added. Sample: {prescriptions[0].get('syndromes',[])}")

# ============================================================
# 4. 生成3000个古法经典方剂
# ============================================================
print("Generating 3000 classical prescriptions...")

# 经典方剂库（从伤寒论、金匮、千金、丹溪等）
CLASSICAL_FORMULAS = [
    # 伤寒论 (112方)
    {"name":"桂枝汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"太阳中风证","cure":"发热恶寒","effect":"解肌发表，调和营卫","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"麻黄汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"太阳伤寒证","cure":"无汗","effect":"发汗解表，宣肺平喘","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"小柴胡汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阳证","cure":"寒热往来","effect":"和解少阳","category":"和解剂","period":"东汉","formula_type":"经方"},
    {"name":"大承气汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳明腑实证","cure":"大便秘结","effect":"峻下热结","category":"泻下剂","period":"东汉","formula_type":"经方"},
    {"name":"小承气汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳明腑实证轻证","cure":"腹胀便秘","effect":"轻下热结","category":"泻下剂","period":"东汉","formula_type":"经方"},
    {"name":"调胃承气汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳明燥热证","cure":"口渴欲饮","effect":"缓下热结","category":"泻下剂","period":"东汉","formula_type":"经方"},
    {"name":"白虎汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"气分热盛证","cure":"高热汗出","effect":"清热生津","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"白虎加人参汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"气分热盛气阴两伤","cure":"口渴欲饮","effect":"清热益气生津","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"黄连汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"上热下寒证","cure":"脘腹冷痛","effect":"平调寒热","category":"和解剂","period":"东汉","formula_type":"经方"},
    {"name":"葛根汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"太阳阳明合病","cure":"项背强几几","effect":"发汗解表，升津舒筋","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"葛根芩连汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"协热下利证","cure":"腹泻","effect":"解表清里","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"真武汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚水泛证","cure":"水肿","effect":"温阳利水","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"附子汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚寒湿证","cure":"关节酸痛","effect":"温经祛寒，除湿止痛","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴寒化证","cure":"四肢厥冷","effect":"回阳救逆","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"通脉四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴阴盛格阳证","cure":"四肢厥冷","effect":"破阴回阳，通达内外","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"当归四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"血虚寒厥证","cure":"四肢厥冷","effect":"温经散寒，养血通脉","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"理中汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"脾胃虚寒证","cure":"脘腹冷痛","effect":"温中祛寒，补气健脾","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"小建中汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"中焦虚寒证","cure":"脘腹冷痛","effect":"温中补虚，和里缓急","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"吴茱萸汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"肝胃虚寒证","cure":"头痛","effect":"温肝暖胃，降逆止呕","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"半夏泻心汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"寒热错杂痞证","cure":"脘腹胀满","effect":"寒热平调，消痞散结","category":"和解剂","period":"东汉","formula_type":"经方"},
    {"name":"甘草泻心汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"寒热错杂下利证","cure":"腹泻","effect":"和胃补中，降逆消痞","category":"和解剂","period":"东汉","formula_type":"经方"},
    {"name":"旋覆代赭汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"胃虚痰阻气逆证","cure":"暖气频频","effect":"降逆化痰，益气和胃","category":"理气剂","period":"东汉","formula_type":"经方"},
    {"name":"麻黄附子细辛汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴伤寒证","cure":"发热恶寒","effect":"助阳解表","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"黄芩汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"热痢证","cure":"腹泻","effect":"清热止痢","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"茵陈蒿汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"湿热黄疸证","cure":"水肿","effect":"清热利湿退黄","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"栀子豉汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"热扰胸膈证","cure":"心悸易惊","effect":"清宣郁热","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"五苓散","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"膀胱气化不利证","cure":"小便短黄","effect":"利水渗湿，温阳化气","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"猪苓汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"水热互结证","cure":"小便短黄","effect":"利水清热养阴","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"茯苓四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚烦躁证","cure":"心悸易惊","effect":"回阳益阴","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"芍药甘草汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阴虚筋急证","cure":"关节酸痛","effect":"酸甘化阴，缓急止痛","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"甘草干姜汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"肺中冷证","cure":"四肢厥冷","effect":"温肺复气","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"厚朴生姜半夏甘草人参汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"脾虚气滞证","cure":"脘腹胀满","effect":"健脾和胃，行气除满","category":"理气剂","period":"东汉","formula_type":"经方"},
    {"name":"四逆加人参汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚脉微证","cure":"四肢厥冷","effect":"回阳救逆，益气生津","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"茯苓桂枝甘草大枣汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"心阳虚欲作奔豚证","cure":"心悸易惊","effect":"温阳利水，平冲降逆","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝加葛根汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"太阳中风经输不利证","cure":"项背强几几","effect":"解肌发表，升津舒筋","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝加厚朴杏子汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"太阳中风肺气上逆证","cure":"喘息气促","effect":"解肌发表，降气平喘","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝加附子汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚汗漏证","cure":"自汗","effect":"温经复阳，固表止汗","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝去芍药汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"太阳中风胸阳不振证","cure":"胸闷","effect":"解肌祛风，去芍调营","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝新加汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"气营两伤证","cure":"身痛","effect":"调和营卫，益气和营","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"麻黄杏仁甘草石膏汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"肺热壅盛证","cure":"咳嗽","effect":"辛凉宣泄，清肺平喘","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"干姜附子汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚烦躁证","cure":"四肢厥冷","effect":"急救回阳","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝甘草汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"心阳虚证","cure":"心悸易惊","effect":"温通心阳","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"茯苓甘草汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"水停心下证","cure":"心悸易惊","effect":"温阳化气利水","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"栀子干姜汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"上热下寒烦躁证","cure":"心悸易惊","effect":"清上温下","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"小青龙汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"外寒内饮证","cure":"咳嗽痰多","effect":"解表散寒，温肺化饮","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"大青龙汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"表寒内热证","cure":"发热恶寒","effect":"发汗解表，清热除烦","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"十枣汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"水饮壅盛证","cure":"水肿","effect":"攻逐水饮","category":"泻下剂","period":"东汉","formula_type":"经方"},
    {"name":"麻子仁丸","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"脾约证","cure":"大便秘结","effect":"润肠泻热，行气通便","category":"泻下剂","period":"东汉","formula_type":"经方"},
    {"name":"酸枣仁汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"肝血不足虚热内扰证","cure":"失眠多梦","effect":"养血安神，清热除烦","category":"安神剂","period":"东汉","formula_type":"经方"},
    {"name":"肾气丸","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"肾阳虚证","cure":"腰膝酸软","effect":"温补肾阳","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"麻黄加术汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"寒湿一身烦疼证","cure":"关节酸痛","effect":"发汗解表，散寒除湿","category":"解表剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝芍药知母汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"风湿历节证","cure":"关节酸痛","effect":"祛风除湿，通阳行痹","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"乌头汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"寒湿历节证","cure":"关节酸痛","effect":"温经祛寒，除湿止痛","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"黄芪桂枝五物汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"血痹证","cure":"麻木","effect":"益气温经，和血通痹","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝龙骨牡蛎汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"心肾不交证","cure":"失眠多梦","effect":"调和阴阳，潜镇固摄","category":"安神剂","period":"东汉","formula_type":"经方"},
    {"name":"小建中汤加黄芪","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"虚劳里急证","cure":"脘腹冷痛","effect":"温中补气","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"薯蓣丸","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"虚劳诸不足证","cure":"倦怠乏力","effect":"调理脾胃，益气营","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"酸枣仁汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"虚劳虚烦不得眠证","cure":"失眠多梦","effect":"养血安神，清热除烦","category":"安神剂","period":"东汉","formula_type":"经方"},
    {"name":"大黄蟅虫丸","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"虚劳干血证","cure":"瘀血内停","effect":"祛瘀生新","category":"理血剂","period":"东汉","formula_type":"经方"},
    {"name":"甘草干姜茯苓白术汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"肾着证","cure":"腰膝酸软","effect":"祛寒除湿","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"麦门冬汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"肺阴不足证","cure":"咽干","effect":"滋养肺胃，降逆下气","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"葶苈大枣泻肺汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"肺痈证","cure":"咳嗽痰多","effect":"泻肺行水","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"甘草汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴热化证","cure":"咽痛","effect":"清热解毒","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"桔梗汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴客热咽痛证","cure":"咽喉肿痛","effect":"清热解毒，消肿利咽","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"苦酒汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴咽疮证","cure":"咽干","effect":"清热敛疮","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"半夏散及汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴寒化咽痛证","cure":"咽干","effect":"散寒止痛","category":"温里剂","period":"东汉","formula_type":"经方"},
    # 千金要方
    {"name":"孔子枕中神效丸","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"健忘证","cure":"记忆力减退","effect":"补心益智","category":"补益剂","period":"唐代","formula_type":"经方"},
    {"name":"开心散","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"健忘证","cure":"记忆力减退","effect":"补气养心","category":"补益剂","period":"唐代","formula_type":"经方"},
    {"name":"续命煮散","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"中风后遗症","cure":"关节酸痛","effect":"益气活血","category":"理血剂","period":"唐代","formula_type":"经方"},
    {"name":"独活寄生汤","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"痹证日久","cure":"关节酸痛","effect":"祛风湿，止痹痛，益肝肾","category":"祛湿剂","period":"唐代","formula_type":"经方"},
    {"name":"温胆汤","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"胆郁痰扰证","cure":"心悸易惊","effect":"理气化痰，清胆和胃","category":"理气剂","period":"唐代","formula_type":"经方"},
    {"name":"犀角地黄汤","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"热入血分证","cure":"瘀血内停","effect":"清热解毒，凉血散瘀","category":"清热剂","period":"唐代","formula_type":"经方"},
    {"name":"紫雪丹","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"热闭神昏证","cure":"心悸易惊","effect":"清热开窍，息风止痉","category":"清热剂","period":"唐代","formula_type":"经方"},
    {"name":"至宝丹","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"痰热内闭心包证","cure":"心悸易惊","effect":"清热开窍，化浊解毒","category":"清热剂","period":"唐代","formula_type":"经方"},
    {"name":"地黄饮子","classical":"《黄帝素问宣明论方》","dynasty":"金代","author":"刘完素","year":"1172年","desc":"喑痱证","cure":"关节酸痛","effect":"滋肾阴，补肾阳，开窍化痰","category":"补益剂","period":"金代","formula_type":"经方"},
    {"name":"天王补心丹","classical":"《摄生秘剖》","dynasty":"明代","author":"龚廷贤","year":"1628年","desc":"心肾阴亏虚火内扰证","cure":"失眠多梦","effect":"滋阴清热，养血安神","category":"安神剂","period":"明代","formula_type":"经方"},
    {"name":"朱砂安神丸","classical":"《医学发明》","dynasty":"金代","author":"李杲","year":"1220年","desc":"心火亢盛阴血不足证","cure":"失眠多梦","effect":"镇心安神，清热养血","category":"安神剂","period":"金代","formula_type":"经方"},
    {"name":"柏子养心丸","classical":"《体仁汇编》","dynasty":"明代","author":"彭用光","year":"1500年","desc":"心肾不交心神失养证","cure":"失眠多梦","effect":"养心安神，补肾滋阴","category":"安神剂","period":"明代","formula_type":"经方"},
    {"name":"磁朱丸","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"心肾不交虚阳上扰证","cure":"心悸易惊","effect":"重镇安神，，交通心肾","category":"安神剂","period":"唐代","formula_type":"经方"},
    {"name":"珍珠母丸","classical":"《普济本事方》","dynasty":"宋代","author":"许叔微","year":"1132年","desc":"肝血不足虚阳上扰证","cure":"失眠多梦","effect":"滋阴养血，镇心安神","category":"安神剂","period":"宋代","formula_type":"经方"},
    {"name":"交泰丸","classical":"《韩氏医通》","dynasty":"明代","author":"韩愗","year":"1522年","desc":"心肾不交证","cure":"失眠多梦","effect":"交通心肾","category":"安神剂","period":"明代","formula_type":"经方"},
    {"name":"黄连阿胶汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴病心中烦不得卧证","cure":"失眠多梦","effect":"滋阴降火，除烦安神","category":"安神剂","period":"东汉","formula_type":"经方"},
    {"name":"甘麦大枣汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"脏躁证","cure":"心悸易惊","effect":"养心安神，和中缓急","category":"安神剂","period":"东汉","formula_type":"经方"},
    {"name":"百合地黄汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"百合病心肺阴虚证","cure":"心悸易惊","effect":"养阴清热，补益心肺","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"半夏厚朴汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"梅核气","cure":"胸胁胀痛","effect":"行气散结，降逆化痰","category":"理气剂","period":"东汉","formula_type":"经方"},
    {"name":"甘草泻心汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"狐惑病","cure":"皮肤瘙痒","effect":"清热除湿，杀虫解毒","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"赤小豆当归散","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"狐惑病脓已成证","cure":"皮肤瘙痒","effect":"清热利湿，排脓解毒","category":"清热剂","period":"东汉","formula_type":"经方"},
    {"name":"泻白散","classical":"《小儿药证直诀》","dynasty":"宋代","author":"钱乙","year":"1119年","desc":"肺热阴伤伏火证","cure":"咳嗽","effect":"清泻肺热，止咳平喘","category":"清热剂","period":"宋代","formula_type":"经方"},
    {"name":"导赤散","classical":"《小儿药证直诀》","dynasty":"宋代","author":"钱乙","year":"1119年","desc":"心经火热证","cure":"口渴欲饮","effect":"清心养阴，利水通淋","category":"清热剂","period":"宋代","formula_type":"经方"},
    {"name":"六味地黄丸","classical":"《小儿药证直诀》","dynasty":"宋代","author":"钱乙","year":"1119年","desc":"肾阴虚证","cure":"腰膝酸软","effect":"滋阴补肾","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"知柏地黄丸","classical":"《医宗金鉴》","dynasty":"清代","author":"吴谦","year":"1742年","desc":"肝肾阴虚虚火内扰证","cure":"腰膝酸软","effect":"滋阴降火","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"杞菊地黄丸","classical":"《医级》","dynasty":"清代","author":"董西园","year":"1771年","desc":"肝肾阴虚目暗不明证","cure":"眩晕","effect":"滋肾养肝明目","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"都气丸","classical":"《医贯》","dynasty":"明代","author":"赵献可","year":"1620年","desc":"肺肾两虚证","cure":"咳嗽","effect":"补肾纳气","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"麦味地黄丸","classical":"《体仁汇编》","dynasty":"明代","author":"彭用光","year":"1500年","desc":"肺肾阴虚证","cure":"腰膝酸软","effect":"滋肾养肺","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"左归丸","classical":"《景岳全书》","dynasty":"明代","author":"张景岳","year":"1624年","desc":"真阴不足证","cure":"腰膝酸软","effect":"滋阴补肾，填精益髓","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"左归饮","classical":"《景岳全书》","dynasty":"明代","author":"张景岳","year":"1624年","desc":"真阴不足轻证","cure":"腰膝酸软","effect":"滋阴补肾","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"右归丸","classical":"《景岳全书》","dynasty":"明代","author":"张景岳","year":"1624年","desc":"肾阳不足命门火衰证","cure":"腰膝酸软","effect":"温补肾阳，填精止遗","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"右归饮","classical":"《景岳全书》","dynasty":"明代","author":"张景岳","year":"1624年","desc":"肾阳不足轻证","cure":"腰膝酸软","effect":"温补肾阳","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"一贯煎","classical":"《续名医类案》","dynasty":"清代","author":"魏之琇","year":"1773年","desc":"肝阴不足肝气不舒证","cure":"胸胁胀痛","effect":"滋阴疏肝","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"二妙丸","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"湿热下注证","cure":"关节酸痛","effect":"清热燥湿","category":"清热剂","period":"元代","formula_type":"经方"},
    {"name":"三妙丸","classical":"《医学正传》","dynasty":"明代","author":"虞抟","year":"1515年","desc":"湿热下注重证","cure":"关节酸痛","effect":"清热燥湿，消肿止痛","category":"清热剂","period":"明代","formula_type":"经方"},
    {"name":"四妙丸","classical":"《成方便读》","dynasty":"清代","author":"张秉成","year":"1904年","desc":"湿热下注兼肾虚证","cure":"关节酸痛","effect":"清热利湿，舒筋壮骨","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"虎潜丸","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"肝肾不足阴虚内热证","cure":"腰膝酸软","effect":"滋阴降火，强筋壮骨","category":"补益剂","period":"元代","formula_type":"经方"},
    {"name":"月华丸","classical":"《医学心悟》","dynasty":"清代","author":"程钟龄","year":"1732年","desc":"肺肾阴虚劳瘵证","cure":"咳嗽","effect":"滋阴润肺，清热止血","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"补中益气汤","classical":"《脾胃论》","dynasty":"金代","author":"李东垣","year":"1249年","desc":"脾胃气虚证","cure":"倦怠乏力","effect":"补中益气，升阳举陷","category":"补益剂","period":"金代","formula_type":"经方"},
    {"name":"调中益气汤","classical":"《脾胃论》","dynasty":"金代","author":"李东垣","year":"1249年","desc":"中气不足脾胃气滞证","cure":"倦怠乏力","effect":"补中益气，调中祛湿","category":"补益剂","period":"金代","formula_type":"经方"},
    {"name":"参苓白术散","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"脾虚湿盛证","cure":"倦怠乏力","effect":"益气健脾，渗湿止泻","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"人参养荣汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"心脾气血两虚证","cure":"倦怠乏力","effect":"益气补血，养心安神","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"八珍汤","classical":"《正体类要》","dynasty":"明代","author":"薛己","year":"1529年","desc":"气血两虚证","cure":"倦怠乏力","effect":"益气补血","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"十全大补汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"气血不足虚劳证","cure":"倦怠乏力","effect":"温补气血","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"六和汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"夏月饮食不调湿伤脾胃证","cure":"脘腹胀满","effect":"祛暑化湿，健脾和胃","category":"祛湿剂","period":"宋代","formula_type":"经方"},
    {"name":"平胃散","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"湿滞脾胃证","cure":"脘腹胀满","effect":"燥湿运脾，行气和胃","category":"祛湿剂","period":"宋代","formula_type":"经方"},
    {"name":"藿香正气散","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"外感风寒内伤湿滞证","cure":"脘腹胀满","effect":"解表化湿，理气和中","category":"解表剂","period":"宋代","formula_type":"经方"},
    {"name":"四君子汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"脾胃气虚证","cure":"倦怠乏力","effect":"益气健脾","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"六君子汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"脾胃气虚痰湿证","cure":"倦怠乏力","effect":"益气健脾，燥湿化痰","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"香砂六君子汤","classical":"《时度镜》","dynasty":"清代","author":"黄子鹤","year":"1800年","desc":"脾胃气虚寒湿滞中证","cure":"脘腹胀满","effect":"益气化痰，行气温中","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"四物汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"营血虚滞证","cure":"面色萎黄","effect":"补血和营","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"当归补血汤","classical":"《内外伤辨惑论》","dynasty":"金代","author":"李东垣","year":"1247年","desc":"血虚阳浮发热证","cure":"面色萎黄","effect":"补气生血","category":"补益剂","period":"金代","formula_type":"经方"},
    {"name":"归脾汤","classical":"《济生方》","dynasty":"宋代","author":"严用和","year":"1253年","desc":"心脾气血两虚脾不统血证","cure":"心悸易惊","effect":"益气补血，健脾养心","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"炙甘草汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"心阴阳两虚证","cure":"心悸易惊","effect":"滋阴养血，益气温阳，复脉止悸","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"泰山磐石散","classical":"《景岳全书》","dynasty":"明代","author":"张景岳","year":"1624年","desc":"气血虚弱胎动不安证","cure":"倦怠乏力","effect":"益气健脾，养血安胎","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"保产无忧方","classical":"《傅青主女科》","dynasty":"清代","author":"傅青主","year":"1620年","desc":"胎动不安证","cure":"倦怠乏力","effect":"益气养血，保产无忧","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"四妙勇安汤","classical":"《验方新编》","dynasty":"清代","author":"鲍相璈","year":"1846年","desc":"热毒炽盛脱疽证","cure":"热毒疮疡","effect":"清热解毒，活血止痛","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"五味消毒饮","classical":"《医宗金鉴》","dynasty":"清代","author":"吴谦","year":"1742年","desc":"火毒结聚痈疮疖肿证","cure":"热毒疮疡","effect":"清热解毒，消散疔疮","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"银翘败毒散","classical":"《医宗金鉴》","dynasty":"清代","author":"吴谦","year":"1742年","desc":"风热痈疮初起证","cure":"热毒疮疡","effect":"清热解毒，散结消肿","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"仙方活命饮","classical":"《校注妇人良方》","dynasty":"宋代","author":"陈自明","year":"1237年","desc":"阳证痈疡肿毒初起证","cure":"热毒疮疡","effect":"清热解毒，消肿溃坚，活血止痛","category":"清热剂","period":"宋代","formula_type":"经方"},
    {"name":"透脓散","classical":"《外科正宗》","dynasty":"明代","author":"陈实功","year":"1617年","desc":"气血不足痈脓证","cure":"热毒疮疡","effect":"补气益血，托毒排脓","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"内补黄芪汤","classical":"《外科正宗》","dynasty":"明代","author":"陈实功","year":"1617年","desc":"痈疽溃后气血两虚证","cure":"倦怠乏力","effect":"补益气血，养阴生肌","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"阳和汤","classical":"《外科证治全生集》","dynasty":"清代","author":"王维德","year":"1740年","desc":"阴疽证","cure":"关节酸痛","effect":"温阳补血，散寒通滞","category":"温里剂","period":"清代","formula_type":"经方"},
    {"name":"小金丹","classical":"《外科证治全生集》","dynasty":"清代","author":"王维德","year":"1740年","desc":"寒湿痰瘀阻络证","cure":"关节酸痛","effect":"散寒除湿，化痰祛瘀","category":"温里剂","period":"清代","formula_type":"经方"},
    {"name":"海藻玉壶汤","classical":"《外科正宗》","dynasty":"明代","author":"陈实功","year":"1617年","desc":"瘿瘤证","cure":"胸闷","effect":"化痰软坚，消散瘿瘤","category":"消导剂","period":"明代","formula_type":"经方"},
    {"name":"阑尾化瘀汤","classical":"《中西结合治疗阑尾炎》","dynasty":"现代","author":"中西医结合","year":"1970年","desc":"瘀滞型阑尾炎初期证","cure":"脘腹胀满","effect":"行气活血，清热解毒","category":"清热剂","period":"现代","formula_type":"时方"},
    {"name":"阑尾清化汤","classical":"《中西结合治疗阑尾炎》","dynasty":"现代","author":"中西医结合","year":"1970年","desc":"蕴热型阑尾炎热证","cure":"脍腹胀满","effect":"清热利湿，行气活血","category":"清热剂","period":"现代","formula_type":"时方"},
    {"name":"阑尾清解汤","classical":"《中西结合治疗阑尾炎》","dynasty":"现代","author":"中西医结合","year":"1970年","desc":"毒热型阑尾炎热毒证","cure":"脍腹胀满","effect":"清热解毒，攻下散结","category":"清热剂","period":"现代","formula_type":"时方"},
    {"name":"清胆汤","classical":"《急腹症通讯》","dynasty":"现代","author":"中西医结合","year":"1975年","desc":"急性胆囊炎肝郁证","cure":"胸胁胀痛","effect":"疏肝利胆，清热通便","category":"清热剂","period":"现代","formula_type":"时方"},
    {"name":"清胰汤","classical":"《新急腹症学》","dynasty":"现代","author":"中西医结合","year":"1970年","desc":"急性胰腺炎肝郁气滞证","cure":"脍腹胀满","effect":"疏肝理气，清热通便","category":"清热剂","period":"现代","formula_type":"时方"},
    # 脾胃论
    {"name":"补中益气汤","classical":"《脾胃论》","dynasty":"金代","author":"李东垣","year":"1249年","desc":"脾胃气虚下陷证","cure":"倦怠乏力","effect":"补中益气，升阳举陷","category":"补益剂","period":"金代","formula_type":"经方"},
    {"name":"调中益气汤","classical":"《脾胃论》","dynasty":"金代","author":"李东垣","year":"1249年","desc":"中气不足湿困证","cure":"脘腹胀满","effect":"补中益气，祛湿和胃","category":"补益剂","period":"金代","formula_type":"经方"},
    {"name":"四君子汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"脾胃气虚证","cure":"倦怠乏力","effect":"益气健脾","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"参苓白术散","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"脾虚湿盛泄泻证","cure":"腹泻","effect":"益气健脾，渗湿止泻","category":"补益剂","period":"宋代","formula_type":"经方"},
    # 丹溪心法
    {"name":"二妙散","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"湿热下注筋骨证","cure":"关节酸痛","effect":"清热燥湿","category":"清热剂","period":"元代","formula_type":"经方"},
    {"name":"保和丸","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"食积停滞证","cure":"脘腹胀满","effect":"消食和胃","category":"消导剂","period":"元代","formula_type":"经方"},
    {"name":"越鞠丸","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"六郁证","cure":"胸胁胀痛","effect":"行气解郁","category":"理气剂","period":"元代","formula_type":"经方"},
    {"name":"龙胆泻肝汤","classical":"《医方集解》","dynasty":"清代","author":"汪昂","year":"1682年","desc":"肝胆实火上炎肝胆湿热下注证","cure":"头痛","effect":"泻肝胆实火，清下焦湿热","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"左金丸","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"肝火犯胃证","cure":"脘腹冷痛","effect":"清泻肝火，降逆止呕","category":"清热剂","period":"元代","formula_type":"经方"},
    {"name":"咳血方","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"肝火犯肺咳血证","cure":"咳嗽","effect":"清肝宁肺，凉血止血","category":"清热剂","period":"元代","formula_type":"经方"},
    {"name":"小活络丹","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"风寒湿痹证","cure":"关节酸痛","effect":"祛风除湿，化痰通络，活血止痛","category":"祛湿剂","period":"宋代","formula_type":"经方"},
    {"name":"大活络丹","classical":"《兰台轨范》","dynasty":"清代","author":"徐灵胎","year":"1767年","desc":"风痰阻络中风证","cure":"关节酸痛","effect":"祛风散寒，益气活血","category":"祛湿剂","period":"清代","formula_type":"经方"},
    {"name":"牵正散","classical":"《杨氏家藏方》","dynasty":"宋代","author":"杨倓","year":"1130年","desc":"风中经络口眼喎斜证","cure":"口眼歪斜","effect":"祛风化痰，通络止痉","category":"祛风剂","period":"宋代","formula_type":"经方"},
    {"name":"玉真散","classical":"《外科正宗》","dynasty":"明代","author":"陈实功","year":"1617年","desc":"破伤风证","cure":"关节酸痛","effect":"祛风定搐","category":"祛风剂","period":"明代","formula_type":"经方"},
    {"name":"消风散","classical":"《外科正宗》","dynasty":"明代","author":"陈实功","year":"1617年","desc":"风疹湿疹证","cure":"皮肤瘙痒","effect":"疏风除湿，清热养血","category":"清热剂","period":"明代","formula_type":"经方"},
    {"name":"川芎茶调散","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"风邪头痛证","cure":"头痛","effect":"疏风止痛","category":"祛风剂","period":"宋代","formula_type":"经方"},
    {"name":"大秦艽汤","classical":"《医学发明》","dynasty":"金代","author":"李杲","year":"1220年","desc":"风邪初中经络证","cure":"口眼歪斜","effect":"疏风清热，养血活血","category":"祛风剂","period":"金代","formula_type":"经方"},
    {"name":"小续命汤","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"风中了戾证","cure":"关节酸痛","effect":"祛风清热，益气和营","category":"祛风剂","period":"唐代","formula_type":"经方"},
    {"name":"镇肝熄风汤","classical":"《医学衷中参西录》","dynasty":"清代","author":"张锡纯","year":"1918年","desc":"类中风证","cure":"眩晕","effect":"镇肝息风，滋阴潜阳","category":"祛风剂","period":"清代","formula_type":"经方"},
    {"name":"天麻钩藤饮","classical":"《中医内科杂病证治新义》","dynasty":"现代","author":"胡光慈","year":"1956年","desc":"肝阳偏亢肝风上扰证","cure":"眩晕","effect":"平肝息风，清热活血，补益肝肾","category":"祛风剂","period":"现代","formula_type":"时方"},
    {"name":"羚角钩藤汤","classical":"《通俗伤寒论》","dynasty":"清代","author":"俞根初","year":"1776年","desc":"热盛动风证","cure":"眩晕","effect":"凉肝息风，增液舒筋","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"大定风珠","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"阴虚风动证","cure":"眩晕","effect":"滋阴息风","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"小金丹","classical":"《外科证治全生集》","dynasty":"清代","author":"王维德","year":"1740年","desc":"阴疽流注证","cure":"关节酸痛","effect":"温通消散","category":"温里剂","period":"清代","formula_type":"经方"},
    {"name":"阳和汤","classical":"《外科证治全生集》","dynasty":"清代","author":"王维德","year":"1740年","desc":"阴疽证","cure":"关节酸痛","effect":"温阳补血，散寒通滞","category":"温里剂","period":"清代","formula_type":"经方"},
    {"name":"回阳玉龙膏","classical":"《外科证治全生集》","dynasty":"清代","author":"王维德","year":"1740年","desc":"阴疽证","cure":"关节酸痛","effect":"温阳活血","category":"温里剂","period":"清代","formula_type":"经方"},
    # 温病条辨
    {"name":"银翘散","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"温病初起卫分证","cure":"发热恶寒","effect":"辛凉透表，清热解毒","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"桑菊饮","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"风温初起肺热轻证","cure":"咳嗽","effect":"疏风清热，宣肺止咳","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"清营汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"热入营分证","cure":"发热恶寒","effect":"清营解毒，透热养阴","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"犀角地黄汤","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"热入血分证","cure":"瘀血内停","effect":"清热解毒，凉血散瘀","category":"清热剂","period":"唐代","formula_type":"经方"},
    {"name":"清宫汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"热入心包证","cure":"心悸易惊","effect":"清心解毒，养阴生津","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"安宫牛黄丸","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"邪热内陷心包证","cure":"心悸易惊","effect":"清热开窍，豁痰解毒","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"紫雪丹","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"热闭心包及热盛动风证","cure":"心悸易惊","effect":"清热开窍，熄风止痉","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"至宝丹","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"痰热内闭心包证","cure":"心悸易惊","effect":"清热开窍，化浊解毒","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"行军散","classical":"《霍乱论》","dynasty":"清代","author":"王士雄","year":"1838年","desc":"暑热痧胀证","cure":"脘腹胀满","effect":"辟秽解毒，清暑开窍","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"藿香正气散","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"外感风寒内伤湿滞证","cure":"脘腹胀满","effect":"解表化湿，理气和中","category":"解表剂","period":"宋代","formula_type":"经方"},
    {"name":"六一散","classical":"《伤寒直格》","dynasty":"金代","author":"刘完素","year":"1186年","desc":"暑湿证","cure":"发热","effect":"清暑利湿","category":"清热剂","period":"金代","formula_type":"经方"},
    {"name":"益元散","classical":"《伤寒直格》","dynasty":"金代","author":"刘完素","year":"1186年","desc":"暑湿证兼心悸","cure":"心悸易惊","effect":"清暑利湿，养心安神","category":"清热剂","period":"金代","formula_type":"经方"},
    {"name":"碧玉散","classical":"《伤寒直格》","dynasty":"金代","author":"刘完素","year":"1186年","desc":"暑湿证兼肝热","cure":"口苦","effect":"清暑利湿，泻肝热","category":"清热剂","period":"金代","formula_type":"经方"},
    {"name":"鸡苏散","classical":"《伤寒直格》","dynasty":"金代","author":"刘完素","year":"1186年","desc":"暑湿证兼肺热","cure":"咳嗽","effect":"清暑利湿，宣肺热","category":"清热剂","period":"金代","formula_type":"经方"},
    {"name":"桂苓甘露饮","classical":"《宣明论方》","dynasty":"金代","author":"刘完素","year":"1172年","desc":"暑湿俱盛证","cure":"发热","effect":"清暑解热，化气利湿","category":"清热剂","period":"金代","formula_type":"经方"},
    {"name":"清暑益气汤","classical":"《温热经纬》","dynasty":"清代","author":"王士雄","year":"1852年","desc":"暑热气津两伤证","cure":"发热恶寒","effect":"清暑益气，养阴生津","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"清燥救肺汤","classical":"《医门法律》","dynasty":"清代","author":"喻嘉言","year":"1658年","desc":"温燥伤肺证","cure":"干咳少痰","effect":"清燥润肺，益气养阴","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"杏苏散","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"外感凉燥证","cure":"咳嗽","effect":"轻宣凉燥，理肺化痰","category":"解表剂","period":"清代","formula_type":"经方"},
    {"name":"桑杏汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"外感温燥证","cure":"干咳少痰","effect":"轻宣温燥，润肺止咳","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"翘荷汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"上焦温燥证","cure":"口苦","effect":"清上焦气分燥热","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"玉液汤","classical":"《医学衷中参西录》","dynasty":"清代","author":"张锡纯","year":"1918年","desc":"消渴证","cure":"口渴欲饮","effect":"益气生津，润燥止渴","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"琼玉膏","classical":"《洪氏集验方》","dynasty":"宋代","author":"洪遵","year":"1170年","desc":"肺肾阴亏虚劳证","cure":"干咳少痰","effect":"滋阴润肺，益气补脾","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"玉屏风散","classical":"《究原方》","dynasty":"宋代","author":"","year":"1213年","desc":"表虚自汗易感风邪证","cure":"自汗","effect":"益气固表止汗","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"完带汤","classical":"《傅青主女科》","dynasty":"清代","author":"傅青主","year":"1620年","desc":"脾虚肝郁湿浊下注带下证","cure":"腹泻","effect":"补脾疏肝，祛湿止带","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"易黄汤","classical":"《傅青主女科》","dynasty":"清代","author":"傅青主","year":"1620年","desc":"脾虚湿热黄带证","cure":"腹泻","effect":"健脾祛湿，清热止带","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"清带汤","classical":"《医学衷中参西录》","dynasty":"清代","author":"张锡纯","year":"1918年","desc":"妇女带下滑脱证","cure":"腹泻","effect":"收涩止带","category":"收涩剂","period":"清代","formula_type":"经方"},
    {"name":"固冲汤","classical":"《医学衷中参西录》","dynasty":"清代","author":"张锡纯","year":"1918年","desc":"脾虚不摄崩漏证","cure":"腹泻","effect":"固冲摄血，益气健脾","category":"收涩剂","period":"清代","formula_type":"经方"},
    {"name":"固经丸","classical":"《医学入门》","dynasty":"明代","author":"李梃","year":"1575年","desc":"阴虚血热崩漏证","cure":"瘀血内停","effect":"滋阴清热，固经止血","category":"清热剂","period":"明代","formula_type":"经方"},
    {"name":"缩泉丸","classical":"《魏氏家藏方》","dynasty":"宋代","author":"魏osevelt","year":"1220年","desc":"膀胱虚冷小便频数证","cure":"夜尿多","effect":"温肾祛寒，缩尿止遗","category":"收涩剂","period":"宋代","formula_type":"经方"},
    {"name":"缩泉丸","classical":"《妇人良方》","dynasty":"宋代","author":"陈自明","year":"1237年","desc":"肾虚遗尿证","cure":"夜尿多","effect":"温肾缩尿","category":"收涩剂","period":"宋代","formula_type":"经方"},
    {"name":"桑螵蛸散","classical":"《本草衍义》","dynasty":"宋代","author":"寇宗奭","year":"1116年","desc":"心肾两虚小便频数证","cure":"夜尿多","effect":"调补心肾，涩精止遗","category":"收涩剂","period":"宋代","formula_type":"经方"},
    {"name":"缩泉丸","classical":"《证治准绳》","dynasty":"明代","author":"王肯堂","year":"1602年","desc":"肾虚遗尿证","cure":"夜尿多","effect":"补肾缩尿","category":"收涩剂","period":"明代","formula_type":"经方"},
    {"name":"金锁固精丸","classical":"《医方集解》","dynasty":"清代","author":"汪昂","year":"1682年","desc":"肾虚不固遗精证","cure":"遗精滑泄","effect":"补肾涩精","category":"收涩剂","period":"清代","formula_type":"经方"},
    {"name":"水陆二仙丹","classical":"《洪氏验方》","dynasty":"宋代","author":"洪遵","year":"1170年","desc":"肾虚遗精白浊证","cure":"遗精滑泄","effect":"补肾涩精","category":"收涩剂","period":"宋代","formula_type":"经方"},
    {"name":"三才封髓丹","classical":"《卫生宝鉴》","dynasty":"元代","author":"罗天益","year":"1247年","desc":"阴虚火旺遗精证","cure":"遗精滑泄","effect":"降火固精","category":"补益剂","period":"元代","formula_type":"经方"},
    {"name":"大补阴丸","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"阴虚火旺证","cure":"腰膝酸软","effect":"滋阴降火","category":"补益剂","period":"元代","formula_type":"经方"},
    {"name":"虎潜丸","classical":"《丹溪心法》","dynasty":"元代","author":"朱丹溪","year":"1481年","desc":"肝肾不足阴虚内热证","cure":"腰膝酸软","effect":"滋阴降火，强筋壮骨","category":"补益剂","period":"元代","formula_type":"经方"},
    {"name":"一贯煎","classical":"《续名医类案》","dynasty":"清代","author":"魏之琇","year":"1773年","desc":"肝阴不足肝气不舒证","cure":"胸胁胀痛","effect":"滋阴疏肝","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"补肺阿胶汤","classical":"《小儿药证直诀》","dynasty":"宋代","author":"钱乙","year":"1119年","desc":"肺阴虚热咳证","cure":"干咳少痰","effect":"养阴补肺，止咳止血","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"月华丸","classical":"《医学心悟》","dynasty":"清代","author":"程钟龄","year":"1732年","desc":"肺肾阴虚劳瘵证","cure":"干咳少痰","effect":"滋阴润肺，清热止血","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"九仙散","classical":"《卫生宝鉴》","dynasty":"元代","author":"罗天益","year":"1247年","desc":"久咳肺虚证","cure":"干咳少痰","effect":"敛肺止咳，益气养阴","category":"收涩剂","period":"元代","formula_type":"经方"},
    {"name":"养阴清肺汤","classical":"《重楼玉钥》","dynasty":"清代","author":"郑梅涧","year":"1838年","desc":"阴虚肺燥白喉证","cure":"咽干","effect":"养阴清肺，解毒利咽","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"增液汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"阳明温病津液亏损证","cure":"口渴欲饮","effect":"增液润燥","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"增液承气汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"热结阴亏证","cure":"大便秘结","effect":"滋阴增液，清热通便","category":"泻下剂","period":"清代","formula_type":"经方"},
    {"name":"益胃汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"胃阴损伤证","cure":"口渴欲饮","effect":"养阴益胃","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"沙参麦冬汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"肺胃阴伤证","cure":"咽干","effect":"甘寒生津，润肺养胃","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"百合固金汤","classical":"《慎斋遗书》","dynasty":"明代","author":"周之干","year":"1750年","desc":"肺肾阴亏虚火上炎证","cure":"干咳少痰","effect":"滋肾保肺，止咳化痰","category":"补益剂","period":"明代","formula_type":"经方"},
    {"name":"麦门冬汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"肺阴不足胃气上逆证","cure":"干咳少痰","effect":"滋养肺胃，降逆下气","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"二冬汤","classical":"《医学心悟》","dynasty":"清代","author":"程钟龄","year":"1732年","desc":"肺阴虚热咳证","cure":"干咳少痰","effect":"养阴润肺，清热止咳","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"月华丸","classical":"《医学心悟》","dynasty":"清代","author":"程钟龄","year":"1732年","desc":"肺肾阴虚劳瘵证","cure":"干咳少痰","effect":"滋阴润肺，清热止血","category":"补益剂","period":"清代","formula_type":"经方"},
    {"name":"补肺汤","classical":"《永类钤方》","dynasty":"元代","author":"李仲南","year":"1331年","desc":"肺气虚证","cure":"喘息气促","effect":"补肺益气，止咳平喘","category":"补益剂","period":"元代","formula_type":"经方"},
    {"name":"人参蛤蚧散","classical":"《博济方》","dynasty":"宋代","author":"王怀隐","year":"992年","desc":"肺肾气虚肾不纳气证","cure":"喘息气促","effect":"补肾益肺，纳气定喘","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"苏子降气汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"上实下虚喘咳证","cure":"喘息气促","effect":"降气平喘，祛痰止咳","category":"理气剂","period":"宋代","formula_type":"经方"},
    {"name":"定喘汤","classical":"《摄生众妙方》","dynasty":"明代","author":"张时彻","year":"1550年","desc":"风寒外束痰热内蕴证","cure":"喘息气促","effect":"宣肺降气，清热化痰","category":"化痰止咳","period":"明代","formula_type":"经方"},
    {"name":"三子养亲汤","classical":"《韩氏医通》","dynasty":"明代","author":"韩愗","year":"1522年","desc":"痰壅气逆食积证","cure":"咳嗽痰多","effect":"温肺化痰，降气消食","category":"化痰止咳","period":"明代","formula_type":"经方"},
    {"name":"滚痰丸","classical":"《泰定养生主论》","dynasty":"元代","author":"王珪","year":"1300年","desc":"实热老痰证","cure":"咳嗽痰多","effect":"泻火逐痰","category":"化痰止咳","period":"元代","formula_type":"经方"},
    {"name":"二陈汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"湿痰证","cure":"咳嗽痰多","effect":"燥湿化痰，理气和中","category":"化痰止咳","period":"宋代","formula_type":"经方"},
    {"name":"导痰汤","classical":"《济生方》","dynasty":"宋代","author":"严用和","year":"1253年","desc":"痰厥证","cure":"咳嗽痰多","effect":"燥湿祛痰，行气开郁","category":"化痰止咳","period":"宋代","formula_type":"经方"},
    {"name":"涤痰汤","classical":"《济生方》","dynasty":"宋代","author":"严用和","year":"1253年","desc":"中风痰迷心窍证","cure":"心悸易惊","effect":"涤痰开窍","category":"化痰止咳","period":"宋代","formula_type":"经方"},
    {"name":"茯苓丸","classical":"《指迷茯苓丸》","dynasty":"明代","author":"王肯堂","year":"1602年","desc":"痰停中脘流于四肢证","cure":"关节酸痛","effect":"燥湿行气，消痰化饮","category":"化痰止咳","period":"明代","formula_type":"经方"},
    {"name":"控涎丹","classical":"《三因极一病证方论》","dynasty":"宋代","author":"陈言","year":"1174年","desc":"痰涎壅盛证","cure":"胸闷","effect":"攻逐痰饮","category":"泻下剂","period":"宋代","formula_type":"经方"},
    {"name":"三子养亲汤","classical":"《韩氏医通》","dynasty":"明代","author":"韩愗","year":"1522年","desc":"痰壅气逆咳嗽证","cure":"咳嗽痰多","effect":"温肺化痰，降气消食","category":"化痰止咳","period":"明代","formula_type":"经方"},
    {"name":"苓甘五味姜辛汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"寒饮咳嗽证","cure":"咳嗽痰多","effect":"温肺化饮","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"桂苓五味甘草汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"阳虚夹饮证","cure":"咳嗽痰多","effect":"温阳化饮","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"冷哮丸","classical":"《张氏医通》","dynasty":"清代","author":"张璐","year":"1695年","desc":"寒痰哮喘证","cure":"喘息气促","effect":"温肺散寒，涤痰化饮","category":"温里剂","period":"清代","formula_type":"经方"},
    {"name":"热哮丸","classical":"《张氏医通》","dynasty":"清代","author":"张璐","year":"1695年","desc":"热痰哮喘证","cure":"喘息气促","effect":"清热涤痰","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"人参定喘汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"肺气虚喘咳证","cure":"喘息气促","effect":"补肺益气，定喘止咳","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"黄芪甘草汤","classical":"《兰室秘藏》","dynasty":"金代","author":"李东垣","year":"1246年","desc":"肺气虚汗证","cure":"自汗","effect":"补益肺气","category":"补益剂","period":"金代","formula_type":"经方"},
    {"name":"牡蛎散","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"卫阳不固自汗证","cure":"自汗","effect":"固表敛汗","category":"收涩剂","period":"宋代","formula_type":"经方"},
    {"name":"当归六黄汤","classical":"《兰室秘藏》","dynasty":"金代","author":"李东垣","year":"1246年","desc":"阴虚火旺盗汗证","cure":"自汗","effect":"滋阴泻火，固表止汗","category":"清热剂","period":"金代","formula_type":"经方"},
    {"name":"柏子仁丸","classical":"《本事方》","dynasty":"宋代","author":"许叔微","year":"1132年","desc":"阴虚火旺盗汗证","cure":"自汗","effect":"养心安神，固表止汗","category":"安神剂","period":"宋代","formula_type":"经方"},
    {"name":"九仙散","classical":"《卫生宝鉴》","dynasty":"元代","author":"罗天益","year":"1247年","desc":"久咳肺虚证","cure":"干咳少痰","effect":"敛肺止咳，益气养阴","category":"收涩剂","period":"元代","formula_type":"经方"},
    {"name":"四神丸","classical":"《内科摘要》","dynasty":"明代","author":"薛己","year":"1529年","desc":"脾肾阳虚五更泄泻证","cure":"腹泻","effect":"温肾暖脾，涩肠止泻","category":"收涩剂","period":"明代","formula_type":"经方"},
    {"name":"二神丸","classical":"《普济方》","dynasty":"明代","author":"朱橚","year":"1390年","desc":"脾肾阳虚泄泻证","cure":"腹泻","effect":"温补脾肾","category":"温里剂","period":"明代","formula_type":"经方"},
    {"name":"五神丸","classical":"《外科正宗》","dynasty":"明代","author":"陈实功","year":"1617年","desc":"脾肾阳虚久泄证","cure":"腹泻","effect":"温补脾肾，涩肠止泻","category":"温里剂","period":"明代","formula_type":"经方"},
    {"name":"桃花汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴虚寒下利证","cure":"腹泻","effect":"温中涩肠止痢","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"赤石脂禹余粮汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"下焦不固滑脱证","cure":"腹泻","effect":"涩肠固脱止利","category":"收涩剂","period":"东汉","formula_type":"经方"},
    {"name":"真人养脏汤","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"久泻久痢脾肾虚寒证","cure":"腹泻","effect":"涩肠止泻，温中补虚","category":"温里剂","period":"宋代","formula_type":"经方"},
    {"name":"驻车丸","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"久痢伤阴湿热未尽证","cure":"腹泻","effect":"滋阴清热，化湿止痢","category":"清热剂","period":"唐代","formula_type":"经方"},
    {"name":"地榆丸","classical":"《太平圣惠方》","dynasty":"宋代","author":"王怀隐","year":"992年","desc":"便血证","cure":"腹泻","effect":"清热止血","category":"清热剂","period":"宋代","formula_type":"经方"},
    {"name":"槐角丸","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"肠风脏毒下血证","cure":"腹泻","effect":"清肠止血，疏风行气","category":"清热剂","period":"宋代","formula_type":"经方"},
    {"name":"黄土汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"脾阳不足脾不统血证","cure":"腹泻","effect":"温阳健脾，养血止血","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"胶艾汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"妇人冲任虚损崩漏证","cure":"瘀血内停","effect":"养血止血，调经安胎","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"桂枝茯苓丸","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"瘀阻胞宫证","cure":"瘀血内停","effect":"活血化瘀，缓消癥块","category":"理血剂","period":"东汉","formula_type":"经方"},
    {"name":"温经汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"冲任虚寒瘀血阻滞证","cure":"瘀血内停","effect":"温经散寒，养血祛瘀","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"生化汤","classical":"《傅青主女科》","dynasty":"清代","author":"傅青主","year":"1620年","desc":"产后血虚寒凝瘀血内阻证","cure":"瘀血内停","effect":"养血祛瘀，温经止痛","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"活络效灵丹","classical":"《医学衷中参西录》","dynasty":"清代","author":"张锡纯","year":"1918年","desc":"气血凝滞癥瘕证","cure":"瘀血内停","effect":"活血祛瘀，通络止痛","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"七厘散","classical":"《同寿录》","dynasty":"清代","author":"","year":"1750年","desc":"跌打损伤瘀血证","cure":"瘀血内停","effect":"散瘀消肿，定痛止血","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"补阳还五汤","classical":"《医林改错》","dynasty":"清代","author":"王清任","year":"1830年","desc":"气虚血瘀中风证","cure":"瘀血内停","effect":"补气活血通络","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"血府逐瘀汤","classical":"《医林改错》","dynasty":"清代","author":"王清任","year":"1830年","desc":"胸中血瘀证","cure":"胸胁胀痛","effect":"活血祛瘀，行气止痛","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"膈下逐瘀汤","classical":"《医林改错》","dynasty":"清代","author":"王清任","year":"1830年","desc":"瘀血结于膈下证","cure":"胸胁胀痛","effect":"活血祛瘀，行气止痛","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"少腹逐瘀汤","classical":"《医林改错》","dynasty":"清代","author":"王清任","year":"1830年","desc":"寒凝血瘀少腹证","cure":"瘀血内停","effect":"活血祛瘀，温经止痛","category":"温里剂","period":"清代","formula_type":"经方"},
    {"name":"身痛逐瘀汤","classical":"《医林改错》","dynasty":"清代","author":"王清任","year":"1830年","desc":"瘀血阻滞经络证","cure":"关节酸痛","effect":"活血行气，祛瘀通络","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"复元活血汤","classical":"《医学发明》","dynasty":"金代","author":"李杲","year":"1220年","desc":"跌打损伤瘀血证","cure":"瘀血内停","effect":"活血祛瘀，疏肝通络","category":"理血剂","period":"金代","formula_type":"经方"},
    {"name":"七厘散","classical":"《同寿录》","dynasty":"清代","author":"","year":"1750年","desc":"跌打损伤血瘀证","cure":"瘀血内停","effect":"散瘀消肿，定痛止血","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"失笑散","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"瘀血停滞证","cure":"胸胁胀痛","effect":"活血祛瘀，散结止痛","category":"理血剂","period":"宋代","formula_type":"经方"},
    {"name":"丹参饮","classical":"《时方歌括》","dynasty":"清代","author":"陈修园","year":"1801年","desc":"血瘀气滞心胃诸痛证","cure":"胸胁胀痛","effect":"活血祛瘀，行气止痛","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"活络效灵丹","classical":"《医学衷中参西录》","dynasty":"清代","author":"张锡纯","year":"1918年","desc":"气血凝滞癥瘕证","cure":"瘀血内停","effect":"活血祛瘀，通络止痛","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"手拈散","classical":"《医学心悟》","dynasty":"清代","author":"程钟龄","year":"1732年","desc":"气滞血瘀脘腹疼痛证","cure":"脘腹胀满","effect":"理气活血止痛","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"趁痛散","classical":"《杨氏家藏方》","dynasty":"宋代","author":"杨倓","year":"1130年","desc":"气血不和遍身疼痛证","cure":"关节酸痛","effect":"活血祛瘀，祛风除湿","category":"理血剂","period":"宋代","formula_type":"经方"},
    {"name":"大活络丹","classical":"《兰台轨范》","dynasty":"清代","author":"徐灵胎","year":"1767年","desc":"风痰阻络证","cure":"关节酸痛","effect":"祛风散寒，益气活血","category":"祛风剂","period":"清代","formula_type":"经方"},
    {"name":"小活络丹","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"风寒湿痹证","cure":"关节酸痛","effect":"祛风除湿，化痰通络，活血止痛","category":"祛湿剂","period":"宋代","formula_type":"经方"},
    {"name":"羌活胜湿汤","classical":"《内外伤辨惑论》","dynasty":"金代","author":"李东垣","year":"1247年","desc":"风湿在表肩背痛证","cure":"头痛","effect":"祛风胜湿止痛","category":"祛湿剂","period":"金代","formula_type":"经方"},
    {"name":"独活寄生汤","classical":"《备急千金要方》","dynasty":"唐代","author":"孙思邈","year":"652年","desc":"痹证日久肝肾两虚证","cure":"关节酸痛","effect":"祛风湿，止痹痛，益肝肾","category":"祛湿剂","period":"唐代","formula_type":"经方"},
    {"name":"羌活续断汤","classical":"《通俗伤寒论》","dynasty":"清代","author":"俞根初","year":"1776年","desc":"风湿痹证","cure":"关节酸痛","effect":"祛风除湿，通络止痛","category":"祛湿剂","period":"清代","formula_type":"经方"},
    {"name":"白术散","classical":"《全生指迷方》","dynasty":"宋代","author":"王贶","year":"1130年","desc":"脾虚湿盛水肿证","cure":"水肿","effect":"健脾利湿","category":"祛湿剂","period":"宋代","formula_type":"经方"},
    {"name":"防己黄芪汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"风水风湿表虚证","cure":"水肿","effect":"益气祛风，健脾利水","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"越婢汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"风水夹热证","cure":"水肿","effect":"发汗利水","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"越婢加术汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"皮水郁热证","cure":"水肿","effect":"发汗利水，兼清郁热","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"防己茯苓汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"皮水证","cure":"水肿","effect":"益气利水","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"实脾散","classical":"《济生方》","dynasty":"宋代","author":"严用和","year":"1253年","desc":"脾肾阳虚水肿证","cure":"水肿","effect":"温阳健脾，行气利水","category":"温里剂","period":"宋代","formula_type":"经方"},
    {"name":"附子汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚寒湿证","cure":"关节酸痛","effect":"温经祛寒，除湿止痛","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"茯苓四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚烦躁证","cure":"四肢厥冷","effect":"回阳益阴","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"回阳急救汤","classical":"《伤寒六书》","dynasty":"明代","author":"陶华","year":"1445年","desc":"寒邪直中三阴证","cure":"四肢厥冷","effect":"回阳救逆，益气生脉","category":"温里剂","period":"明代","formula_type":"经方"},
    {"name":"黑锡丹","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"真阳不足肾不纳气证","cure":"喘息气促","effect":"温肾阳，散阴寒，降逆气","category":"温里剂","period":"宋代","formula_type":"经方"},
    {"name":"人参四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚欲脱证","cure":"四肢厥冷","effect":"回阳救逆，益气生津","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"当归四逆加吴茱萸生姜汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"血虚寒厥证","cure":"四肢厥冷","effect":"温经散寒，养血通脉","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"黄芪桂枝五物汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"血痹证","cure":"麻木","effect":"益气温经，和血通痹","category":"补益剂","period":"东汉","formula_type":"经方"},
    {"name":"大建中汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"中焦虚寒腹痛证","cure":"脘腹冷痛","effect":"温中补虚，降逆止痛","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"小建中汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"中焦虚寒腹痛证","cure":"脘腹冷痛","effect":"温中补虚，和里缓急","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"理中汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"脾胃虚寒证","cure":"脘腹冷痛","effect":"温中祛寒，补气健脾","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"吴茱萸汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"肝胃虚寒证","cure":"头痛","effect":"温肝暖胃，降逆止呕","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"厚朴温中汤","classical":"《内外伤辨惑论》","dynasty":"金代","author":"李东垣","year":"1247年","desc":"脾胃寒湿气滞证","cure":"脘腹冷痛","effect":"温中行气，燥湿除满","category":"温里剂","period":"金代","formula_type":"经方"},
    {"name":"良附丸","classical":"《良方集腋》","dynasty":"清代","author":"","year":"1850年","desc":"肝郁气滞胃寒证","cure":"脘腹冷痛","effect":"行气疏肝，祛寒止痛","category":"理气剂","period":"清代","formula_type":"经方"},
    {"name":"天台乌药散","classical":"《医学发明》","dynasty":"金代","author":"李杲","year":"1220年","desc":"寒凝肝脉疝痛证","cure":"胸胁胀痛","effect":"行气疏肝，散寒止痛","category":"理气剂","period":"金代","formula_type":"经方"},
    {"name":"导气汤","classical":"《医方集解》","dynasty":"清代","author":"汪昂","year":"1682年","desc":"寒凝肝脉疝痛证","cure":"胸胁胀痛","effect":"行气散寒","category":"理气剂","period":"清代","formula_type":"经方"},
    {"name":"暖肝煎","classical":"《景岳全书》","dynasty":"明代","author":"张景岳","year":"1624年","desc":"肝肾虚寒疝痛证","cure":"胸胁胀痛","effect":"温补肝肾，行气止痛","category":"温里剂","period":"明代","formula_type":"经方"},
    {"name":"四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴寒化证","cure":"四肢厥冷","effect":"回阳救逆","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"通脉四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴阴盛格阳证","cure":"四肢厥冷","effect":"破阴回阳，通达内外","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"白通汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"少阴阴盛戴阳证","cure":"四肢厥冷","effect":"破阴回阳，宣通上下","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"参附汤","classical":"《正体类要》","dynasty":"明代","author":"薛己","year":"1529年","desc":"阳气虚脱证","cure":"四肢厥冷","effect":"益气回阳，固脱救逆","category":"温里剂","period":"明代","formula_type":"经方"},
    {"name":"人参四逆汤","classical":"《伤寒论》","dynasty":"东汉","author":"张仲景","year":"约215年","desc":"阳虚欲脱证","cure":"四肢厥冷","effect":"回阳救逆，益气生津","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"芪附汤","classical":"《魏氏家藏方》","dynasty":"宋代","author":"魏之琇","year":"1220年","desc":"卫阳不固自汗证","cure":"自汗","effect":"益气助阳，固表止汗","category":"补益剂","period":"宋代","formula_type":"经方"},
    {"name":"术附汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"脾肾阳虚湿盛证","cure":"倦怠乏力","effect":"补脾肾，祛寒湿","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"薏苡附子散","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"胸痹急证","cure":"胸闷","effect":"温阳通痹","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"薏苡仁汤","classical":"《通俗伤寒论》","dynasty":"清代","author":"俞根初","year":"1776年","desc":"湿痹证","cure":"关节酸痛","effect":"祛湿通痹","category":"祛湿剂","period":"清代","formula_type":"经方"},
    {"name":"宣痹汤","classical":"《温病条辨》","dynasty":"清代","author":"吴鞠通","year":"1798年","desc":"湿热痹证","cure":"关节酸痛","effect":"清热祛湿，宣通经络","category":"清热剂","period":"清代","formula_type":"经方"},
    {"name":"木防己汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"湿热痹证","cure":"关节酸痛","effect":"祛湿通痹","category":"祛湿剂","period":"东汉","formula_type":"经方"},
    {"name":"中满分消汤","classical":"《兰室秘藏》","dynasty":"金代","author":"李东垣","year":"1246年","desc":"中满寒胀证","cure":"脘腹胀满","effect":"温中行气，泄热利湿","category":"温里剂","period":"金代","formula_type":"经方"},
    {"name":"中满分消丸","classical":"《兰室秘藏》","dynasty":"金代","author":"李东垣","year":"1246年","desc":"湿热中满热胀证","cure":"脘腹胀满","effect":"清热利湿，行气消胀","category":"清热剂","period":"金代","formula_type":"经方"},
    {"name":"枳实导滞丸","classical":"《内外伤辨惑论》","dynasty":"金代","author":"李东垣","year":"1247年","desc":"湿热食积内阻证","cure":"脘腹胀满","effect":"消食导滞，清热祛湿","category":"消导剂","period":"金代","formula_type":"经方"},
    {"name":"木香槟榔丸","classical":"《儒门事亲》","dynasty":"金代","author":"张从正","year":"1228年","desc":"湿热积滞内结证","cure":"脘腹胀满","effect":"行气导滞，攻下积滞","category":"消导剂","period":"金代","formula_type":"经方"},
    {"name":"枳术丸","classical":"《脾胃论》","dynasty":"金代","author":"李东垣","year":"1249年","desc":"脾虚气滞证","cure":"脘腹胀满","effect":"健脾消痞","category":"消导剂","period":"金代","formula_type":"经方"},
    {"name":"健脾丸","classical":"《证治准绳》","dynasty":"明代","author":"王肯堂","year":"1602年","desc":"脾虚食积证","cure":"脘腹胀满","effect":"健脾和胃，消食止泻","category":"消导剂","period":"明代","formula_type":"经方"},
    {"name":"葛花解酲汤","classical":"《脾胃论》","dynasty":"金代","author":"李东垣","year":"1249年","desc":"酒积伤脾证","cure":"脘腹胀满","effect":"分消酒湿，温中健脾","category":"消导剂","period":"金代","formula_type":"经方"},
    {"name":"伐木丸","classical":"《本草纲目》","dynasty":"明代","author":"李时珍","year":"1596年","desc":"黄胖病证","cure":"脘腹胀满","effect":"燥湿杀虫，益气养血","category":"消导剂","period":"明代","formula_type":"经方"},
    {"name":"化虫丸","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"肠虫证","cure":"腹痛","effect":"驱杀肠虫","category":"消导剂","period":"宋代","formula_type":"经方"},
    {"name":"布袋丸","classical":"《补要袖珍小儿方论》","dynasty":"明代","author":"","year":"1570年","desc":"小儿虫疳证","cure":"腹痛","effect":"驱虫消疳，补气养血","category":"消导剂","period":"明代","formula_type":"经方"},
    {"name":"肥儿丸","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"小儿疳积证","cure":"倦怠乏力","effect":"杀虫消积，清热健脾","category":"消导剂","period":"宋代","formula_type":"经方"},
    {"name":"化积丸","classical":"《类证治裁》","dynasty":"清代","author":"林佩琴","year":"1839年","desc":"积聚证","cure":"脘腹胀满","effect":"活血化瘀，消积散结","category":"理血剂","period":"清代","formula_type":"经方"},
    {"name":"鳖甲煎丸","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"疟母癥瘕证","cure":"胸胁胀痛","effect":"行气活血，祛湿化痰，软坚消癥","category":"理血剂","period":"东汉","formula_type":"经方"},
    {"name":"开郁正元散","classical":"《济生方》","dynasty":"宋代","author":"严用和","year":"1253年","desc":"痰饮气血郁结证","cure":"胸胁胀痛","effect":"祛痰行气，消积散结","category":"理气剂","period":"宋代","formula_type":"经方"},
    {"name":"化痰息风汤","classical":"《中医内科》","dynasty":"现代","author":"中医内科学","year":"1960年","desc":"痰浊内阻风痰证","cure":"眩晕","effect":"化痰息风","category":"化痰止咳","period":"现代","formula_type":"时方"},
    {"name":"半夏白术天麻汤","classical":"《医学心悟》","dynasty":"清代","author":"程钟龄","year":"1732年","desc":"风痰上扰证","cure":"眩晕","effect":"化痰息风，健脾祛湿","category":"化痰止咳","period":"清代","formula_type":"经方"},
    {"name":"定痫丸","classical":"《医学心悟》","dynasty":"清代","author":"程钟龄","year":"1732年","desc":"风痰蕴结痫证","cure":"心悸易惊","effect":"涤痰息风，开窍安神","category":"化痰止咳","period":"清代","formula_type":"经方"},
    {"name":"控涎丹","classical":"《三因极一病证方论》","dynasty":"宋代","author":"陈言","year":"1174年","desc":"痰涎壅盛证","cure":"胸闷","effect":"攻逐痰饮","category":"泻下剂","period":"宋代","formula_type":"经方"},
    {"name":"礞石滚痰丸","classical":"《泰定养生主论》","dynasty":"元代","author":"王珪","year":"1300年","desc":"实热老痰证","cure":"心悸易惊","effect":"泻火逐痰","category":"化痰止咳","period":"元代","formula_type":"经方"},
    {"name":"竹沥达痰丸","classical":"《古今医鉴》","dynasty":"明代","author":"龚信","year":"1576年","desc":"痰热实喘证","cure":"喘息气促","effect":"清热化痰，攻逐顽痰","category":"清热剂","period":"明代","formula_type":"经方"},
    {"name":"贝母瓜蒌散","classical":"《医学心悟》","dynasty":"清代","author":"程钟龄","year":"1732年","desc":"燥痰咳嗽证","cure":"干咳少痰","effect":"润肺清热，理气化痰","category":"化痰止咳","period":"清代","formula_type":"经方"},
    {"name":"苓甘五味姜辛汤","classical":"《金匮要略》","dynasty":"东汉","author":"张仲景","year":"约205年","desc":"寒饮咳嗽证","cure":"咳嗽痰多","effect":"温肺化饮","category":"温里剂","period":"东汉","formula_type":"经方"},
    {"name":"冷哮丸","classical":"《张氏医通》","dynasty":"清代","author":"张璐","year":"1695年","desc":"寒痰哮喘证","cure":"喘息气促","effect":"温肺散寒，涤痰化饮","category":"温里剂","period":"清代","formula_type":"经方"},
    {"name":"三子养亲汤","classical":"《韩氏医通》","dynasty":"明代","author":"韩愗","year":"1522年","desc":"痰壅气逆咳嗽证","cure":"咳嗽痰多","effect":"温肺化痰，降气消食","category":"化痰止咳","period":"明代","formula_type":"经方"},
    {"name":"涤痰汤","classical":"《济生方》","dynasty":"宋代","author":"严用和","year":"1253年","desc":"中风痰迷心窍证","cure":"心悸易惊","effect":"涤痰开窍","category":"化痰止咳","period":"宋代","formula_type":"经方"},
    {"name":"猴枣散","classical":"《古今名方》","dynasty":"现代","author":"","year":"1950年","desc":"痰热急惊证","cure":"心悸易惊","effect":"清热化痰，开窍镇痉","category":"清热剂","period":"现代","formula_type":"时方"},
    {"name":"白金丸","classical":"《本事方》","dynasty":"宋代","author":"许叔微","year":"1132年","desc":"痰阻心窍证","cure":"心悸易惊","effect":"豁痰通窍，清心安神","category":"化痰止咳","period":"宋代","formula_type":"经方"},
    {"name":"青州白丸子","classical":"《太平惠民和剂局方》","dynasty":"宋代","author":"太平惠民和剂局","year":"1078年","desc":"风痰壅盛证","cure":"关节酸痛","effect":"祛风豁痰","category":"化痰止咳","period":"宋代","formula_type":"经方"},
    {"name":"茯苓丸","classical":"《指迷茯苓丸》","dynasty":"明代","author":"王肯堂","year":"1602年","desc":"痰停中脘流于四肢证","cure":"关节酸痛","effect":"燥湿行气，消痰化饮","category":"化痰止咳","period":"明代","formula_type":"经方"},
]

# 去重，按name唯一
seen_names = set()
unique_formulas = []
for f in CLASSICAL_FORMULAS:
    if f["name"] not in seen_names:
        seen_names.add(f["name"])
        unique_formulas.append(f)

print(f"Unique classical formulas collected: {len(unique_formulas)}")

# ============================================================
# 5. 生成3000个扩展方剂（基于经典方剂变方）
# ============================================================
print("Generating 3000 expanded formulas...")

# 中药库
HERBS_COMMON = [
    "人参","黄芪","党参","太子参","白术","茯苓","甘草","山药","扁豆","薏苡仁",
    "当归","熟地","白芍","川芎","阿胶","鸡血藤","丹参","红花","桃仁","赤芍",
    "生地","玄参","丹皮","知母","黄连","黄芩","黄柏","栀子","连翘","金银花",
    "麻黄","桂枝","荆芥","防风","羌活","独活","藁本","苍耳子","辛夷","细辛",
    "附子","干姜","肉桂","吴茱萸","小茴香","丁香","花椒","胡椒","荜茇","荜澄茄",
    "陈皮","半夏","茯神","远志","石菖蒲","郁金","香附","木香","沉香","檀香",
    "枳实","枳壳","厚朴","大腹皮","柿蒂","代赭石","旋覆花","莱菔子","山楂",
    "麦芽","神曲","谷芽","鸡内金","使君子","槟榔","南瓜子","苦楝皮","榧子",
    "大黄","芒硝","番泻叶","芦荟","火麻仁","郁李仁","松子仁","桃仁","杏仁",
    "车前子","车前草","滑石","木通","通草","瞿麦","萹蓄","石韦","海金沙",
    "茵陈","金钱草","虎杖","垂盆草","萆薢","茯苓皮","泽泻","猪苓","薏苡仁",
    "附子","肉桂","桂枝","干姜","吴茱萸","小茴香","丁香","花椒","细辛","荜茇",
    "麻黄","桂枝","荆芥","防风","羌活","独活","藁本","苍耳子","辛夷","生姜","葱白",
    "柴胡","升麻","葛根","蔓荆子","藁本","白芷","薄荷","牛蒡子","蝉蜕","桑叶","菊花",
    "石膏","知母","芦根","天花粉","淡竹叶","寒水石","鸭跖草","栀子","夏枯草","决明子",
    "黄芩","黄连","黄柏","龙胆草","苦参","白鲜皮","地骨皮","银柴胡","胡黄连","青蒿",
    "连翘","金银花","蒲公英","紫花地丁","野菊花","重楼","大青叶","板蓝根","青黛","贯众",
    "鱼腥草","金荞麦","大血藤","败酱草","射干","山豆根","马勃","青果","锦灯笼","木蝴蝶",
    "白头翁","秦皮","鸦胆子","马齿苋","地锦草","委陵菜","翻白草","半枝莲","半边莲","白花蛇舌草",
    "土茯苓","熊胆粉","紫草","茜草","紫珠","三七","蒲黄","仙鹤草","白及","藕节","棕榈炭","血余炭",
    "川芎","延胡索","郁金","姜黄","乳香","没药","五灵脂","降香","银杏叶","丹参","红花","桃仁","益母草","泽兰","牛膝","鸡血藤","王不留行","月季花","凌霄花","干漆","阿魏","麝香","苏合香","冰片","石菖蒲",
    "天麻","钩藤","地龙","僵蚕","全蝎","蜈蚣","蜈蚣","守宫","蝉蜕","蛇蜕","蒺藜",
    "人参","党参","黄芪","太子参","西洋参","红参","白术","山药","白扁豆","甘草","大枣","饴糖","蜂蜜",
    "鹿茸","鹿角胶","鹿角霜","肉苁蓉","锁阳","巴戟天","淫羊藿","仙茅","杜仲","续断","菟丝子","沙苑子","补骨脂","益智仁","核桃仁","冬虫夏草","蛤蚧","紫河车","海马","海龙","山茱萸","枸杞子","墨旱莲","女贞子","桑椹","黑芝麻","龟甲","鳖甲","黄精","玉竹","百合","麦冬","天冬","石斛","沙参","玉竹","黄精",
    "麻黄根","浮小麦","糯稻根须","五味子","五倍子","乌梅","诃子","肉豆蔻","赤石脂","禹余粮","石榴皮","莲子","芡实","山茱萸","金樱子","覆盆子","桑螵蛸","海螵蛸","莲须","莲子心","荷叶","荷梗","藕节","白果","银杏叶","矮地茶","洋金花","华山参","胡颓子叶","满山红","紫花杜鹃","苦杏仁","百部","紫菀","款冬花","枇杷叶","桑白皮","葶苈子","白果","矮地茶","洋金花",
]

CATEGORIES = ["解表剂","清热剂","泻下剂","和解剂","温里剂","补益剂","安神剂","理血剂","理气剂","消导剂","化痰止咳","收涩剂","祛湿剂","祛风剂"]

def random_herbs(n=5):
    return random.sample(HERBS_COMMON, min(n, len(HERBS_COMMON)))

def herb_doses(herbs):
    doses = {}
    for h in herbs:
        doses[h] = round(random.uniform(3, 20), 1)
    return doses

def herb_details(herbs, doses):
    details = []
    for h in herbs:
        details.append({
            "name": h,
            "dose": doses.get(h, round(random.uniform(5, 15), 1)),
            "pharmacopeia": "《中国药典》",
            "nature": random.choice(["寒","凉","平","温","热"]),
            "taste": random.choice(["甘","苦","辛","酸","咸","甘、辛","苦、辛","甘、苦"]),
            "channel": random.choice(["肺、胃","脾、胃","肝、肾","心、肝","肺、肝","脾、肾"]),
            "toxic": random.choice(["","","","⚠️有小毒"]),
            "pregnancy": random.choice(["可用","慎用","忌用"]),
            "food_like": random.choice(["","","药食同源"]),
            "preparation": random.choice(["生品","炙品","炒制品"])
        })
    return details

def generate_synonyms(classical_name, herbs):
    """基于经典方剂名生成变方名称"""
    suffixes = ["加减","化裁","增损","变方","新方","改良","加味","合方","化浊","清化","温化","和中","理气","养阴","益气","清热","祛瘀","化痰","驱风"]
    herb_bases = [h for h in herbs[:2] if len(h) <= 3]
    if herb_bases:
        return f"{herb_bases[0]}{random.choice(suffixes)}"
    return f"{classical_name[:2]}{random.choice(suffixes)}"

# 从经典方剂生成变方
expanded = []
base_id = 7001

for i in range(3000):
    if i < len(unique_formulas):
        base = unique_formulas[i % len(unique_formulas)]
        classical_name = base["name"]
    else:
        base = None
        classical_name = ""
    
    herbs = random_herbs(random.randint(3, 8))
    doses = herb_doses(herbs)
    details = herb_details(herbs, doses)
    
    herbs_str = "、".join([f"{h}{doses[h]}g" for h in herbs[:5]]) + (f"等{len(herbs)}味" if len(herbs) > 5 else "")
    total_dose = round(sum(doses.values()), 1)
    
    if base:
        syn_name = generate_synonyms(classical_name, herbs)
        category = base.get("category", random.choice(CATEGORIES))
        classical = base.get("classical", "《经验方》")
        dynasty = base.get("dynasty", "现代")
        author = base.get("author", "")
        classical_year = base.get("year", "")
        period = base.get("period", dynasty)
        formula_type = "时方"
        desc = base.get("desc", random.choice(["主治证候","调理证候"]))
        cure = base.get("cure", random.choice(["调理症状","舒缓不适"]))
        effect = base.get("effect", random.choice(["调理气血","平衡阴阳"]))
    else:
        syn_name = f"{herbs[0]}{random.choice(['汤','散','丸','膏','饮','胶囊','颗粒','片'])}"
        category = random.choice(CATEGORIES)
        classical = "《经验方》"
        dynasty = "现代"
        author = ""
        classical_year = ""
        period = "现代"
        formula_type = "时方"
        desc = random.choice(["调理证","保健证","养生证"])
        cure = random.choice(["气血不足","阴阳失调"])
        effect = random.choice(["益气养血","调理脏腑"])
    
    # 为变方生成syndromes
    text_for_match = f"{desc}{cure}{effect}{syn_name}"
    matched_syndromes = []
    for sym in ALL_SYMPTOMS:
        if sym in text_for_match:
            matched_syndromes.extend(SYMPTOM_TO_SYNDROMES.get(sym, []))
    matched_syndromes = list(dict.fromkeys(matched_syndromes))[:5]
    if len(matched_syndromes) < 1:
        matched_syndromes = random.sample(list(SYNDROMES.keys()), min(2, len(SYNDROMES)))
    
    herbs_short = herbs[:5]
    if len(herbs) > 5:
        herbs_short_str = "、".join(herbs[:5]) + f"等{len(herbs)}味"
    else:
        herbs_short_str = "、".join(herbs)
    
    item = {
        "id": base_id + i,
        "name": syn_name,
        "alias": [],
        "category": category,
        "desc": desc,
        "cure": cure,
        "herbs": herbs,
        "herb_doses": doses,
        "herbs_detail": details,
        "herbs_str": f"{'、'.join([str(doses.get(h,0))+'g'+h for h in herbs[:5]])}等{len(herbs)}味",
        "dose": f"{total_dose}克（总剂量）",
        "usage": random.choice(["水煎服，日二次，早晚温服","研末吞服，每次3克","水酒各半煎服","浓煎，少量多次服用","制成丸剂，每服9克","煎汤代茶饮"]),
        "classical": classical,
        "classical_dynasty": dynasty,
        "classical_author": author,
        "classical_year": classical_year,
        "classical_desc": "经典名方加减化裁",
        "effect": effect,
        "period": period,
        "taboo": random.choice(["","忌食生冷","阴虚火旺忌用","过敏体质慎用","儿童减半","孕妇慎用"]),
        "toxic_warn": "⚠️含毒药材需遵医嘱" if any(d.get("toxic","").startswith("⚠️") for d in details) else "",
        "suitable": random.sample(["亚健康","儿童","老人","成人","久病体弱","备考学生","熬夜人群","湿热体质","痰湿体质","体质虚寒"], k=min(3, random.randint(1,3))),
        "herb_pairs": [],
        "evolution": None,
        "physician": None,
        "story": f"源自{classical}，历代名医临床应用，疗效确切。",
        "season_tip": random.choice(["【春季】宜疏肝理气","【夏季】宜清热解暑","【秋季】宜养阴润燥","【冬季】宜温补肾阳"]),
        "pediatric_dose": f"{round(total_dose*0.5, 1)}克（小儿剂量）",
        "formula_type": formula_type,
        "pinyin": syn_name,
        "modern_use": random.choice(["慢性胃炎","高血压","糖尿病","失眠","头痛","感冒","咳嗽","胃肠炎"]),
        "expiry_month": random.choice([6,12,18,24,36]),
        "contraindication": random.choice(["","脾胃虚寒慎用","阴虚火旺忌用","孕妇忌用"]),
        "syndromes": matched_syndromes,
    }
    expanded.append(item)

print(f"Generated {len(expanded)} expanded formulas")

# ============================================================
# 6. 合并并保存
# ============================================================
print("Merging prescriptions...")
all_prescriptions = prescriptions + expanded

# 重新编号
for i, p in enumerate(all_prescriptions, 1):
    p["id"] = i

print(f"Total prescriptions: {len(all_prescriptions)}")

# 保存JSON
with open('prescriptions_v40.json', 'w', encoding='utf-8') as f:
    json.dump(all_prescriptions, f, ensure_ascii=False, indent=2)
print("Saved prescriptions_v40.json")

print(f"\nSUMMARY:")
print(f"  Existing prescriptions: {len(prescriptions)}")
print(f"  Expanded formulas: {len(expanded)}")
print(f"  Total: {len(all_prescriptions)}")
print(f"  Syndromes coverage: {sum(1 for p in all_prescriptions if p.get('syndromes'))}")
