# -*- coding: utf-8 -*-
"""精准营养技术网 —— 原型站生成脚本

用法（在 prototype 目录下执行）：
    python build.py

生成：
    index.html            首页
    pages/<slug>.html     40 个栏目详情页 + 导航页
    assets/style.css      样式
    assets/site.js        交互脚本（咨询框 / 回到顶部）
    README.md             结构与占位清单说明
"""

import os
import hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = "精准营养技术网"
ORG_NAME = "北京市身心智医学研究所"
UPDATED = "2026-09-14"

# --------------------------------------------------------------------------
# 1. 栏目线框图标（48x48，线性描边，跟随 currentColor）
# --------------------------------------------------------------------------
ICONS = {
    "unit-intro": '<rect x="13" y="11" width="22" height="28" rx="1.5"/><path d="M8 39h32"/><path d="M19 18h4M25 18h4M19 25h4M25 25h4M19 32h4M25 32h4"/>',
    "precision-tech": '<circle cx="24" cy="24" r="13"/><circle cx="24" cy="24" r="5.5"/><path d="M24 5v6M24 37v6M5 24h6M37 24h6"/>',
    "cases": '<path d="M9 15.5A2.5 2.5 0 0 1 11.5 13h7l4 4H36.5A2.5 2.5 0 0 1 39 19.5v16A2.5 2.5 0 0 1 36.5 38h-25A2.5 2.5 0 0 1 9 35.5z"/><path d="M16 26h16M16 32h10"/>',
    "personal-recipe": '<circle cx="24" cy="15" r="6"/><path d="M11 41c0-7.2 5.8-12 13-12s13 4.8 13 12"/><path d="M17 24h14"/>',
    "family-recipe": '<path d="M8 23 24 10l16 13"/><path d="M13 22v17h22V22"/><path d="M18.5 32h11"/><path d="M24 32v7"/>',
    "canteen-recipe": '<path d="M9 31h30"/><path d="M13 31a11 11 0 0 1 22 0"/><path d="M24 20v-4"/><path d="M11 37h26"/>',
    "restaurant-recipe": '<path d="M17 8v13a4 4 0 0 0 8 0V8"/><path d="M21 25v15"/><path d="M33 8c2.6 1.4 4 4.6 4 8.6 0 3.2-1 5.6-3 6.9V40"/>',
    "smart-method": '<path d="M24 8a10 10 0 0 1 6.2 17.8V30H17.8v-4.2A10 10 0 0 1 24 8z"/><path d="M19.5 34h9M21 38.5h6"/>',
    "health-method": '<path d="M24 40C15 34 8 28.5 8 20.6A7.6 7.6 0 0 1 24 16a7.6 7.6 0 0 1 16 4.6C40 28.5 33 34 24 40z"/><path d="M13 24h6l2.5-4 3.5 8 3-4h7"/>',
    "longevity": '<path d="M14 9h20M14 39h20"/><path d="M16.5 9c0 7.5 7.5 10 7.5 15s-7.5 7.5-7.5 15"/><path d="M31.5 9c0 7.5-7.5 10-7.5 15s7.5 7.5 7.5 15"/>',
    "anti-cancer": '<path d="M24 7l14 5v12.5C38 33 32 38.5 24 42c-8-3.5-14-9-14-17.5V12z"/><path d="M17.5 24.5l4.5 4.5 8.5-9"/>',
    "recovery": '<circle cx="24" cy="24" r="15"/><path d="M24 16.5v15M16.5 24h15"/>',
    "immunity": '<circle cx="24" cy="24" r="8.5"/><path d="M24 8v5.5M24 34.5V40M8 24h5.5M34.5 24H40M12.7 12.7l3.9 3.9M31.4 31.4l3.9 3.9M35.3 12.7l-3.9 3.9M16.6 31.4l-3.9 3.9"/>',
    "disease-prevention": '<path d="M16 9v11a8 8 0 0 0 16 0V9"/><path d="M16 9h-3M32 9h3"/><path d="M24 28v5a6 6 0 0 0 12 0v-3.5"/><circle cx="36" cy="27.5" r="2.5"/>',
    "body-mind": '<path d="M21.5 9.5a7.5 7.5 0 0 0-7.3 9.2 6.5 6.5 0 0 0-1.1 12.4 6 6 0 0 0 8.4 7.4V9.5z"/><path d="M26.5 9.5a7.5 7.5 0 0 1 7.3 9.2 6.5 6.5 0 0 1 1.1 12.4 6 6 0 0 1-8.4 7.4V9.5z"/>',
    "mood": '<path d="M37 11C21 11 12 21.5 12 34.5 25 34.5 35 24 37 11z"/><path d="M14 34.5C20 27 26.5 22.5 33 19.5"/>',
    "health-manage": '<rect x="12" y="10" width="24" height="30" rx="2"/><path d="M20 7.5h8v5h-8z"/><path d="M18 25h3v9h-3zM23.5 20h3v14h-3zM29 28h3v6h-3z"/>',
    "beauty": '<path d="M24 7.5l4.2 12.3L40.5 24l-12.3 4.2L24 40.5l-4.2-12.3L7.5 24l12.3-4.2z"/>',
    "happy": '<circle cx="24" cy="24" r="15"/><path d="M18.5 20h.01M29.5 20h.01"/><path d="M16.5 28c2 3.2 4.6 4.8 7.5 4.8s5.5-1.6 7.5-4.8"/>',
    "happiness": '<circle cx="24" cy="19" r="6.5"/><path d="M24 5.5v3.5M24 29v3.5M10.5 19H14M34 19h3.5M14.5 9.5l2.5 2.5M31 12l2.5-2.5"/><path d="M12 41c0-5 5.4-8 12-8s12 3 12 8"/>',
    "nanny": '<circle cx="24" cy="14" r="5.5"/><path d="M13 41c0-7 5-11.5 11-11.5S35 34 35 41"/><path d="M18 30l-3 11M30 30l3 11"/>',
    "nutritionist-hr": '<circle cx="18" cy="16" r="5.5"/><circle cx="33" cy="18.5" r="4.5"/><path d="M7.5 39c0-6.3 4.7-10.5 10.5-10.5S28.5 32.7 28.5 39"/><path d="M30 39c0-4.8 2.8-7.8 6.5-7.8S43 34.2 43 39"/>',
    "charity": '<path d="M24 35S9.5 26.5 9.5 18.6A6.6 6.6 0 0 1 24 15.4a6.6 6.6 0 0 1 14.5 3.2C38.5 26.5 24 35 24 35z"/><path d="M8 41h32"/>',
    "articles": '<path d="M13.5 8H27L35 15.5V40H13.5z"/><path d="M27 8v8h8"/><path d="M19 23h14M19 29h14M19 35h8"/>',
    "health-catalog": '<rect x="12" y="8" width="24" height="32" rx="2"/><path d="M18 16h3.5M25.5 16h5.5M18 23h3.5M25.5 23h5.5M18 30h3.5M25.5 30h5.5"/>',
    "certificate": '<circle cx="24" cy="19" r="10"/><path d="M24 13.5l1.8 3.6 4 .6-2.9 2.8.7 4-3.6-1.9-3.6 1.9.7-4-2.9-2.8 4-.6z"/><path d="M17.5 27.5L14.5 41l9.5-5 9.5 5-3-13.5"/>',
    "books": '<path d="M10 12.5A2.5 2.5 0 0 1 12.5 10H23v30H12.5A2.5 2.5 0 0 0 10 42.5z"/><path d="M38 12.5A2.5 2.5 0 0 0 35.5 10H25v30h10.5A2.5 2.5 0 0 1 38 42.5z"/>',
    # --- 新增栏目图标（第二批 40 栏目） ---
    "nutrition-medicine": '<circle cx="24" cy="24" r="13"/><path d="M24 17v14M17 24h14"/>',
    "nature-medicine": '<path d="M24 41V23"/><path d="M24 25c-8 0-12.5-5-12.5-13 8 0 12.5 5 12.5 13z"/><path d="M24 27c8 0 12.5-5 12.5-13-8 0-12.5 5-12.5 13z"/>',
    "functional-medicine": '<circle cx="15" cy="16" r="4"/><circle cx="33" cy="16" r="4"/><circle cx="24" cy="34" r="4"/><path d="M18.5 18.5 21.5 30M29.5 18.5 26.5 30M19 16h10"/>',
    "evidence-medicine": '<circle cx="21" cy="21" r="10.5"/><path d="M29 29 38 38"/><path d="M17 21h8M21 17v8"/>',
    "brain-science": '<path d="M22 11c-3.8 0-6.5 2.6-6.5 6.2-2.7.6-4.5 2.8-4.5 5.4 0 2.7 1.7 4.9 4.4 5.5.4 3.4 3 5.9 6.6 5.9h1V11z"/><path d="M26 11c3.8 0 6.5 2.6 6.5 6.2 2.7.6 4.5 2.8 4.5 5.4 0 2.7-1.7 4.9-4.4 5.5-.4 3.4-3 5.9-6.6 5.9h-1V11z"/><path d="M24 11v22"/>',
    "longevity-medicine": '<path d="M24 8l12 4.2v10.2c0 8-5 13.2-12 16.1-7-2.9-12-8.1-12-16.1V12.2z"/><path d="M17.5 24.5h4l2.4-4.2 3 8 2.4-3.8h3.2"/>',
    "human-quality": '<circle cx="20" cy="16" r="6"/><path d="M8 40c0-7 5.5-12 12-12 3.2 0 6.1 1.1 8.3 3"/><path d="M34 39V23M28.5 28.5 34 23l5.5 5.5"/>',
    "eugenics-recipe": '<path d="M24 38C15 32 8 27 8 19.5A7 7 0 0 1 24 15a7 7 0 0 1 16 4.5C40 27 33 32 24 38z"/><path d="M24 19.5v9M19.5 24h9"/>',
    "maternal-recipe": '<circle cx="18" cy="14" r="5"/><path d="M8 38c0-6 4.5-10 10-10s10 4 10 10"/><circle cx="33" cy="19" r="3.5"/><path d="M26.5 36c0-4 2.9-6.5 6.5-6.5s6.5 2.5 6.5 6.5"/>',
    "children-recipe": '<circle cx="18" cy="15" r="5"/><path d="M8 38c0-6 4.4-10 10-10 2.6 0 4.9.8 6.7 2.3"/><rect x="27" y="21" width="13" height="17" rx="1.5"/><path d="M30.5 27h6M30.5 31h4"/>',
    "women-recipe": '<circle cx="24" cy="21" r="3.6"/><circle cx="24" cy="12" r="3.6"/><circle cx="32.6" cy="17" r="3.6"/><circle cx="15.4" cy="17" r="3.6"/><circle cx="30" cy="28" r="3.6"/><circle cx="18" cy="28" r="3.6"/><path d="M24 31.5V41"/>',
    "elderly-recipe": '<circle cx="21" cy="13" r="5.5"/><path d="M12 39c0-6.6 4-11 9-11s9 4.4 9 11"/><path d="M36 15v23a3 3 0 0 1-6 0"/>',
    "kindergarten-recipe": '<rect x="11" y="26" width="11.5" height="11.5" rx="1.6"/><rect x="25.5" y="26" width="11.5" height="11.5" rx="1.6"/><rect x="18" y="13" width="11.5" height="11.5" rx="1.6"/>',
    "group-meal-recipe": '<circle cx="16" cy="15" r="4.5"/><circle cx="32" cy="15" r="4.5"/><path d="M7 37c0-5.2 4-8.8 9-8.8s9 3.6 9 8.8"/><path d="M23 37c0-5.2 4-8.8 9-8.8s9 3.6 9 8.8"/>',
    "wellness-base": '<path d="M9 22 24 10l15 12"/><path d="M13 21v18h22V21"/><path d="M24 39V28"/><path d="M24 30c-4 0-6-2.6-6-6 4 0 6 2 6 6zM24 31c4 0 6-2.6 6-6-4 0-6 2-6 6z"/>',
    "feedback": '<path d="M10 11h28v19H21l-8 7v-7h-3z"/><path d="M17 19h14M17 24h9"/>',
    "cooperation": '<circle cx="16" cy="16" r="4.5"/><path d="M7 38c0-5.5 4-9 9-9s9 3.5 9 9"/><path d="M34 12v11M28.5 17.5h11"/>',
}

# --------------------------------------------------------------------------
# 2. 分组（首页分区顺序 = 栏目编号顺序）
# --------------------------------------------------------------------------
SECTIONS = [
    ("sec-1", "医学视角正解", "MEDICINE PERSPECTIVES",
     ["nutrition-medicine", "nature-medicine", "functional-medicine", "evidence-medicine", "brain-science", "longevity-medicine"]),
    ("sec-2", "精准营养与人的质量", "PRECISION NUTRITION &amp; HUMAN QUALITY",
     ["precision-tech", "human-quality", "smart-method", "longevity"]),
    ("sec-3", "真实案例与人群食谱设计", "CASES &amp; GROUP RECIPES",
     ["cases", "personal-recipe", "family-recipe", "eugenics-recipe", "maternal-recipe",
      "children-recipe", "women-recipe", "elderly-recipe", "kindergarten-recipe"]),
    ("sec-4", "集体供餐食谱设计", "COLLECTIVE CATERING RECIPES",
     ["group-meal-recipe", "canteen-recipe", "restaurant-recipe"]),
    ("sec-5", "健康新方法", "NEW WAYS TO HEALTH",
     ["health-method", "anti-cancer", "recovery", "immunity", "disease-prevention",
      "body-mind", "mood", "health-manage"]),
    ("sec-6", "养生 · 身心", "WELLNESS &amp; BODY-MIND",
     ["wellness-base", "beauty", "happy"]),
    ("sec-7", "服务 · 资料 · 文献", "SERVICES &amp; ARCHIVES",
     ["nanny", "nutritionist-hr", "charity", "articles", "health-catalog", "certificate", "books"]),
]

# --------------------------------------------------------------------------
# 3. 栏目内容
#    blocks: ("h2", 文本) / ("p", 文本) / ("ul", [条目]) / ("note", 文本)
#            ("table", (表头列表, [行列表]))
# --------------------------------------------------------------------------
CONTENT = {
"unit-intro": ("单位简介", "以\u201c身心智一体\u201d为核心理念的营养健康研究与应用机构", [
 ("h2", "我们是谁"),
 ("p", "北京市身心智医学研究所长期从事身心智健康与营养关系的研究与应用，提出并实践\u201c精准营养技术\u201d体系。研究所主张：人的身体状况、情绪状态与思维能力是一个整体，而日常饮食结构是影响这个整体最持续、也最可控的变量。"),
 ("h2", "我们做什么"),
 ("ul", [
   "研究食物营养成分与人体常见表现之间的对应关系，形成可落地的分析方法；",
   "为个人、家庭、食堂、餐厅设计科学营养食谱；",
   "面向营养师、家政与照护人员、健康管理者开展技术培训与交流；",
   "整理并发布面向大众的身心智健康科普内容。",
 ]),
 ("h2", "我们的主张"),
 ("p", "人类常见病的主因，往往是\u201c稀里糊涂吃\u201d——不清楚吃什么、吃多少、怎么搭配。饮食越科学，身心智越健康。我们希望把\u201c怎么吃才对\u201d这件事，从一句口号变成一份看得懂、买得到、做得出、坚持得住的日常方案。"),
 ("note", "本页为机构介绍。文中营养相关内容均为健康科普性质，不能替代医疗诊断与治疗。"),
]),

"precision-tech": ("精准营养技术新方法", "知道您体内问题由哪些食物营养丰歉引起——技术原理与方法", [
 ("h2", "一句话说清"),
 ("p", "精准营养技术要回答一个问题：您身上的不适与问题，究竟与哪几类食物的营养\u201c丰\u201d或\u201c歉\u201d有关？先找到答案，才能设计出真正适合您的食谱，而不是照搬一张人人通用的清单。"),
 ("h2", "与\u201c通用营养建议\u201d的区别"),
 ("table", (["对比项", "通用营养建议", "精准营养技术"], [
   ["出发点", "面向所有人", "面向具体的您"],
   ["结论形态", "原则性口号", "具体食物类别与分量"],
   ["落地方式", "自行理解", "三餐与采购清单"],
   ["反馈机制", "无", "按周期复盘调整"],
 ])),
 ("h2", "技术路径：四步"),
 ("ul", [
   "① 信息采集：饮食习惯、进食节律、身体常见表现、既往体检数据；",
   "② 营养归因：判断哪些营养素可能长期\u201c丰\u201d、哪些长期\u201c歉\u201d；",
   "③ 食谱设计：把结论翻译成具体的三餐、食材与分量；",
   "④ 跟踪反馈：按 2 至 4 周为周期复盘，逐步微调。",
 ]),
 ("h2", "核心概念：结构偏差"),
 ("p", "多数人的问题不是\u201c缺某一种补品\u201d，而是长期的结构偏差：主食过于精细、油脂与盐分偏高、蔬菜占比偏低、进食时间越来越晚。精准营养技术优先修正结构，再考虑局部补充。"),
 ("note", "本技术用于日常膳食结构的改善与健康管理，属于健康科普与生活方式干预范畴，不用于疾病诊断，不替代医院治疗。"),
]),

"cases": ("真实独特案例", "真实、去标识、完整记录的实践案例与思路复盘", [
 ("p", "案例栏目遵循三条原则：真实（来自实际服务记录）、去标识（隐去姓名与可识别信息）、完整（记录前后变化与跟踪周期）。案例用于理解思路，不作为疗效承诺。"),
 ("h2", "案例类型"),
 ("ul", [
   "长期疲劳、精力不济者的饮食结构重建；",
   "儿童与青少年食欲差、注意力不集中的膳食调整（先行排除疾病因素）；",
   "情绪急躁、睡眠不稳者的饮食与作息同步调整；",
   "体重与体脂管理者的长期食谱执行；",
   "术后与病后康复期的营养支持配合。",
 ]),
 ("h2", "每个案例包含五个部分"),
 ("ul", [
   "基本情况：年龄、职业、作息、主要困扰；",
   "膳食调查：一周真实进食记录；",
   "营养归因：结构偏差与可能的营养素丰歉判断；",
   "食谱设计：可执行的三餐与采购清单；",
   "跟踪结果：周期内的体感与指标变化。",
 ]),
 ("h2", "如何阅读案例"),
 ("p", "个体差异极大，同样的问题在不同人身上可能对应完全不同的饮食原因。请把案例当作\u201c分析思路的示范\u201d，不要直接照搬食谱。"),
 ("note", "案例中的效果描述为个体经验，不代表普遍结论，也不构成医疗建议。"),
]),

"personal-recipe": ("个人营养食谱设计新方法", "一人一谱：按身体情况与作息定制的三餐方案", [
 ("h2", "服务内容"),
 ("ul", [
   "膳食结构评估：现有饮食的问题定位；",
   "7 日或 14 日食谱：含食材、分量与做法要点；",
   "外食与应酬场景的替代方案；",
   "跟踪调整建议：每 2 至 4 周复盘一次。",
 ]),
 ("h2", "设计流程"),
 ("ul", [
   "填写信息 → 营养归因 → 出食谱 → 试执行 1 周 → 复盘微调。",
 ]),
 ("h2", "适用人群"),
 ("ul", [
   "长期外食的上班族；",
   "精力差、易疲劳、饭后困倦明显的人；",
   "体重与体脂需要管理的人；",
   "备孕、产后、康复期需要特别照顾的人（需与医生方案配合）。",
 ]),
 ("h2", "落地要点"),
 ("p", "食谱只解决\u201c吃什么\u201d，还要同时说明\u201c什么时候吃、吃多少、怎么吃\u201d。我们会把这三件事一起写进方案，避免出现\u201c看着合理、执行不了\u201d的情况。"),
 ("note", "本方案为膳食结构改善建议，属健康科普范畴，不构成医疗建议；患病期间请遵医嘱。"),
]),

"family-recipe": ("家庭营养食谱设计新方法", "一家一谱：兼顾老人、孩子与成人的家庭餐桌方案", [
 ("h2", "为什么家庭需要单独设计"),
 ("p", "同一个锅里吃饭，需求却不一样：老人需要易消化、钙与优质蛋白；孩子需要充足能量与生长所需营养素；成年人则要控油控糖。家庭食谱的核心是\u201c一餐多配\u201d——同一批食材，通过搭配与做法的差异，满足全家。"),
 ("h2", "服务内容"),
 ("ul", [
   "家庭膳食结构评估；",
   "一周家庭菜单（含采购清单）；",
   "老人 / 儿童 / 成人分档搭配说明；",
   "厨房备餐、储存与二次加工建议；",
   "月度复盘与菜单轮换。",
 ]),
 ("h2", "采购与成本"),
 ("p", "我们按\u201c主食 + 蛋白 + 蔬果 + 油脂 + 调味\u201d五类给出采购表，优先使用当季食材，在控制成本的同时提高营养密度。"),
 ("h2", "共餐本身就是健康管理"),
 ("p", "一家人规律、适量、有交流地吃饭，比任何补品都更稳。餐桌秩序理顺了，孩子的挑食对抗、家里的晚饭争吵，往往也会跟着减少。"),
 ("note", "本方案为家庭膳食改善建议，属健康科普范畴，不构成医疗建议。"),
]),

"canteen-recipe": ("食堂营养食谱设计新方法", "面向学校、幼儿园与单位的批量食谱与营养公示", [
 ("h2", "服务对象"),
 ("ul", ["中小学与高校食堂；", "幼儿园与托育机构；", "企事业单位职工食堂；", "养老机构。"]),
 ("h2", "设计要点"),
 ("ul", [
   "按人数与年龄段计算营养素供给量；",
   "菜品组合避免\u201c高油高盐叠加\u201d；",
   "周期轮换菜单，降低重复感；",
   "兼顾成本与出餐效率；",
   "给出留样、出品与公示建议。",
 ]),
 ("h2", "交付内容"),
 ("ul", [
   "周期轮换食谱（周 / 双周）；",
   "主辅料用量与采购量估算；",
   "菜品标准做法卡；",
   "营养公示牌文案（供食堂张贴）。",
 ]),
 ("h2", "常见误区"),
 ("p", "很多食堂的问题不是\u201c没菜\u201d，而是结构失衡：主食精细、荤菜集中、蔬菜变成点缀。通过结构调整，通常可以在不增加预算的前提下改善整体营养水平。"),
 ("note", "涉及食品安全与从业人员资质的事项，按当地监管部门要求执行。"),
]),

"restaurant-recipe": ("餐厅营养食谱设计新方法", "为餐厅设计有营养卖点的菜单、套餐与出品标准", [
 ("h2", "服务内容"),
 ("ul", [
   "现有菜单营养结构诊断；",
   "健康套餐设计（控糖、轻负担、家庭套餐等）；",
   "菜品营养标识与菜单呈现建议；",
   "后厨出品标准与操作培训要点；",
   "菜单文案与卖点包装。",
 ]),
 ("h2", "商业价值"),
 ("ul", [
   "差异化定位，不比拼低价；",
   "提升客单与复购；",
   "对接企业团餐、健身人群与家庭客群；",
   "为健康主题宣传与相关认证做准备。",
 ]),
 ("h2", "落地方式"),
 ("p", "建议从 3 到 5 道招牌健康菜开始试点，跑通出品、成本与顾客反馈后，再逐步扩展到整本菜单，避免一次性推翻造成经营波动。"),
 ("note", "菜单营养标识的表述需符合相关法规要求，宣传中不得使用疾病治疗类用语。"),
]),

"smart-method": ("提高智力新方法", "认知、注意力与学习效率的营养基础与改善方法", [
 ("h2", "基本思路"),
 ("p", "大脑对营养供应非常敏感：血糖是否稳定、优质蛋白与脂肪是否充足、铁锌碘与 B 族维生素水平如何，都会直接体现在专注力、记忆和反应速度上。"),
 ("h2", "重点人群"),
 ("ul", ["学生与备考人群；", "脑力工作者；", "长期熬夜、用脑过度者；", "注意力容易涣散、上课走神的儿童（先排除疾病因素）。"]),
 ("h2", "方法要点"),
 ("ul", [
   "早餐给足优质蛋白与适量脂肪，避免纯碳水\u201c顶上去又掉下来\u201d；",
   "午晚餐控制精制糖与高升糖主食的集中摄入；",
   "保证铁、锌、碘、B 族等与认知相关营养素的稳定来源；",
   "饮食规律，不用零食替代正餐。",
 ]),
 ("note", "若孩子存在明显的注意力与学习困难，应先到医院评估，营养调整作为配合手段。"),
]),

"health-method": ("健康新方法", "把饮食结构当作第一道健康防线：结构、节律、分量", [
 ("h2", "观念转变"),
 ("p", "多数人关注健康的方式是\u201c体检出问题 → 去医院\u201d。精准营养技术主张把干预前移：在指标还没严重异常时，先把长期偏离的膳食结构拨回来。"),
 ("h2", "三个抓手"),
 ("ul", [
   "结构：主食、蛋白、蔬果、油脂的比例关系；",
   "节律：什么时候吃、一天吃几顿、晚上吃多少；",
   "分量：每餐实际摄入量，而不是\u201c感觉差不多\u201d。",
 ]),
 ("h2", "怎样判断吃对了"),
 ("ul", [
   "精力是否稳定，不靠咖啡硬撑；",
   "睡眠与排便是否规律；",
   "体重与腰围是否平稳；",
   "情绪波动是否可控；",
   "体检关键指标是否逐年改善。",
 ]),
 ("p", "这些指标比\u201c吃了什么补品\u201d更能说明饮食是否科学。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议。"),
]),

"longevity": ("促进长寿新方法", "少犯错比多进补更重要：衰老与膳食结构的关系", [
 ("h2", "被反复观察到的几件事"),
 ("p", "关于长寿地区与人群的研究，结论相当朴素：食物以天然形态为主、植物性食物占比高、总热量不过剩、蛋白质来源多样、很少依赖深加工食品。难的不是道理，而是长期做到。"),
 ("h2", "精准营养的做法"),
 ("ul", [
   "先评估当前膳食结构的偏离程度；",
   "逐步减少高糖、高精制碳水与深加工食品；",
   "保证优质蛋白与膳食纤维的稳定供给；",
   "控制总热量，但不制造强烈的饥饿感；",
   "按季度跟踪体重、腰围与精力水平。",
 ]),
 ("h2", "节律与心态"),
 ("p", "规律三餐、不过饱、不宵夜，是被反复验证的简单原则。情绪长期紧绷的人，很难长期吃对；饮食理顺之后，情绪往往也会跟着稳下来。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议。"),
]),

"anti-cancer": ("防癌新方法", "膳食结构与癌症风险：日常防线该怎么做", [
 ("h2", "先说清定位"),
 ("p", "饮食不能\u201c治癌\u201d，也不能保证\u201c不得癌\u201d。但大量流行病学研究显示，膳食结构与部分癌症的发生风险存在关联，因此调整饮食结构具有现实意义。"),
 ("h2", "值得做的方向"),
 ("ul", [
   "提高蔬菜、水果、全谷物与豆类的摄入比例；",
   "减少加工肉制品、腌制与烧烤类食物的频率；",
   "控制酒精与含糖饮料；",
   "避免长期高热量摄入与超重状态；",
   "保证膳食纤维与多种抗氧化营养素的来源。",
 ]),
 ("h2", "必须同时做好的事"),
 ("ul", [
   "按年龄与风险因素定期筛查；",
   "戒烟；",
   "按医嘱接种相关疫苗；",
   "出现异常症状及时就医。",
 ]),
 ("p", "饮食调整是\u201c日常防线\u201d，筛查与治疗是\u201c专业防线\u201d，两者不可互相替代。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议，不能替代筛查与治疗。"),
]),

"recovery": ("康复新方法", "修复需要材料：术后与病后康复期营养支持", [
 ("h2", "康复营养的核心问题"),
 ("p", "术后、病后以及长期慢性消耗状态下，身体对蛋白质、能量、维生素与矿物质的需求往往高于平时，而食欲与消化能力却在下降——供需错位是康复变慢的重要原因。"),
 ("h2", "介入原则"),
 ("ul", [
   "在主治医生方案基础上做营养支持，不擅自更改治疗；",
   "优先保证优质蛋白与总能量；",
   "少量多餐，减轻消化负担；",
   "按病情调整食物性状（软食、半流、流质）；",
   "关注水分与电解质补充。",
 ]),
 ("h2", "交付内容"),
 ("ul", [
   "康复期分阶段食谱（急性期 / 恢复期 / 巩固期）；",
   "可执行的高蛋白点心与饮品方案；",
   "家属照护与进食要点说明。",
 ]),
 ("note", "康复期营养方案必须与主治医生及临床营养科配合，本栏目内容不构成医疗建议。"),
]),

"immunity": ("提高免疫力新方法", "免疫力是守出来的：蛋白、黏膜与微量营养素", [
 ("h2", "常见误区"),
 ("ul", [
   "把免疫等同于进补，认为越贵越好；",
   "长期大量服用单一营养素；",
   "三餐不规律，靠保健品\u201c补回来\u201d；",
   "熬夜与饮食失衡同时存在。",
 ]),
 ("h2", "更有效的做法"),
 ("ul", [
   "保证优质蛋白：免疫细胞与抗体的原料；",
   "充足蔬果：提供维生素 C、A 与多种植物化学物；",
   "保证锌、硒、铁等微量元素的来源；",
   "保护肠道与呼吸道黏膜：膳食纤维、充足水分、规律进食；",
   "睡眠与适度运动同步改善。",
 ]),
 ("h2", "关于补充剂"),
 ("p", "优先从食物中获得。确需补充时，应在明确缺乏的前提下，按建议剂量与周期使用，避免长期大剂量自行服用。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议。"),
]),

"disease-prevention": ("常见病预防新方法", "三高、脂肪肝、痛风、胃病的饮食结构调整要点", [
 ("h2", "共同点"),
 ("p", "这些问题往往经历多年形成：主食越来越精细、油盐越来越多、蔬菜占比越来越低、进食时间越来越晚。指标异常是结果，不是起点。"),
 ("h2", "分项要点"),
 ("ul", [
   "血压：控盐并识别隐形盐（加工食品、调味料），提高钾的摄入来源；",
   "血糖：控制精制碳水与含糖饮料，增加全谷物与膳食纤维，规律进餐；",
   "血脂与脂肪肝：减少油炸与反式脂肪，控制总热量与酒精，合理安排鱼与坚果；",
   "痛风：限制高嘌呤食物与酒精，保证饮水与体重管理；",
   "胃病：规律进食，避免过烫、过硬与过度刺激。",
 ]),
 ("h2", "关键提醒"),
 ("p", "已有明确诊断并正在用药的人，饮食调整需与医生方案同步，不可自行停药或改药。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议。"),
]),

"body-mind": ("身心智德健康促进新方法", "身体、情绪、思维一体：一套食谱同时影响三件事", [
 ("h2", "一个整体观"),
 ("p", "我们习惯把身体问题、情绪问题、思维问题分开处理：身体看内科，情绪看心理，思维看教育。但三者的物质基础是共享的——血糖、蛋白质、脂肪、微量元素与肠道状态，会同时作用于身体感受、情绪稳定与认知效率。"),
 ("h2", "精准营养如何介入"),
 ("ul", [
   "从膳食调查出发，找出长期偏离的结构性问题；",
   "优先修正能量供给节律（忽高忽低最伤状态）；",
   "补齐与神经递质、激素合成相关的营养素来源；",
   "把情绪与精力的变化，作为结构调整的反馈指标。",
 ]),
 ("h2", "可观察的改善方向"),
 ("ul", [
   "精力更平稳，不再依赖咖啡因；",
   "情绪波动减少，急躁与低落减轻；",
   "睡眠与食欲更规律；",
   "注意力与工作效率改善。",
 ]),
 ("note", "明显的情绪障碍与心理疾病需要专业诊疗，营养调整作为配合手段。"),
]),

"mood": ("心理疾病营养食谱设计新方法", "情绪有物质基础：饮食与急躁、低落的辅助管理", [
 ("h2", "先说清边界"),
 ("p", "抑郁与焦虑障碍属于疾病范畴，需要专业诊断与治疗。本栏目讨论的是：日常饮食结构如何影响情绪稳定性，以及如何把饮食作为辅助的自我管理手段。"),
 ("h2", "优先修正的四件事"),
 ("ul", [
   "早餐不足或不吃，上午血糖骤降，情绪最先失控；",
   "精制糖与含糖饮料的反复刺激，造成情绪\u201c过山车\u201d；",
   "长期缺乏优质蛋白与 B 族维生素、铁、镁等来源；",
   "晚间进食过量或吃宵夜，影响睡眠——睡眠差，情绪必然差。",
 ]),
 ("h2", "辅助调整建议"),
 ("ul", [
   "三餐定时，先保证早餐；",
   "用全谷物、豆类、蔬菜替代部分精制主食与甜食；",
   "晚餐清淡且不过晚；",
   "减少酒精与咖啡因的过量摄入；",
   "规律作息与适度运动同步进行。",
 ]),
 ("note", "如出现持续两周以上的情绪低落、兴趣丧失、睡眠障碍，请及时就医。本栏目内容不构成医疗建议。"),
]),

"health-manage": ("健康管理新方法", "建立个人膳食档案，让健康管理有据可依", [
 ("h2", "从\u201c感觉\u201d到\u201c记录\u201d"),
 ("p", "多数人对自己的饮食只有模糊印象：\u201c吃得还行\u201d。健康管理的第一步就是把模糊变具体——记录一周真实进食，才会看到问题在哪里。"),
 ("h2", "个人膳食档案包含"),
 ("ul", [
   "基础信息：年龄、身高体重、腰围、既往指标；",
   "膳食记录：一周进食清单与时间；",
   "评估结论：结构偏差与营养素丰歉判断；",
   "干预方案：食谱与执行要点；",
   "跟踪数据：体重、腰围、精力、睡眠与体检关键指标。",
 ]),
 ("h2", "跟踪节奏"),
 ("ul", [
   "月度复盘：执行情况与体感变化；",
   "季度评估：体重腰围与关键指标变化；",
   "年度总结：体检数据对比与方案迭代。",
 ]),
 ("p", "档案的价值在于连续性——单次评估只能发现问题，长期跟踪才能真正改变结果。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议。"),
]),

"beauty": ("漂亮新方法", "皮肤、气色、体态首先是吃出来的", [
 ("h2", "基本认识"),
 ("p", "皮肤与毛发是身体营养状况的\u201c外显指标\u201d：蛋白质不足则松弛无光，铁与维生素 C 不足则面色暗淡，必需脂肪酸缺乏则干燥敏感，糖与油脂过量则容易出油长痘。"),
 ("h2", "重点营养方向"),
 ("ul", [
   "优质蛋白：皮肤与毛发的基础材料；",
   "维生素 C 与多种抗氧化营养素：帮助抵抗氧化损伤；",
   "必需脂肪酸：维持皮肤屏障；",
   "B 族维生素：参与代谢与修复；",
   "充足水分与膳食纤维：改善整体状态。",
 ]),
 ("h2", "同时要减少的"),
 ("ul", ["高糖与含糖饮料；", "油炸与深加工食品；", "长期熬夜——任何营养方案都补不回睡眠债。"]),
 ("h2", "体态与体重"),
 ("p", "漂亮是\u201c紧致、有精神、体态好\u201d，而不是单纯的体重数字。通过结构化的食谱与规律进食，体重与体态的变化会更稳定、更可持续。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议。"),
]),

"happy": ("快乐新方法", "快乐也有物质基础：稳定血糖与规律进餐", [
 ("h2", "快乐从哪里来"),
 ("p", "情绪的物质基础包括神经递质的合成原料、稳定的血糖供应、良好的睡眠与肠道状态。饮食结构直接参与其中，所以\u201c吃得对\u201d常常表现为\u201c心情稳\u201d。"),
 ("h2", "具体做法"),
 ("ul", [
   "三餐规律，避免长时间空腹后暴食高糖食物；",
   "保证优质蛋白与 B 族维生素来源；",
   "增加富含色氨酸、镁、铁的食物；",
   "控制咖啡因与酒精；",
   "把吃饭时间变成真正放松的时间，而不是刷手机的间隙。",
 ]),
 ("h2", "与家人一起"),
 ("p", "一起做饭、一起吃饭，是最低成本的情绪改善方式。共餐带来的交流与陪伴，对情绪的作用不亚于营养成分本身。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议。"),
]),

"happiness": ("幸福方法", "从一张全家都吃得好的餐桌开始经营幸福", [
 ("h2", "一个不太浪漫但靠谱的入口"),
 ("p", "家庭矛盾常常在餐桌上爆发：\u201c随便吃\u201d\u201c你又不好好吃饭\u201d\u201c天天点外卖\u201d。饮食失序往往是生活失序的外在表现，先把餐桌理顺，是经营幸福最具体的抓手。"),
 ("h2", "具体方法"),
 ("ul", [
   "建立家庭固定的共餐时间；",
   "设计全家都能接受的一周菜单：有人吃得不勉強，有人吃得够营养；",
   "让孩子参与备餐，减少挑食对抗；",
   "把\u201c吃什么\u201d从争吵话题变成共同决策；",
   "用节律代替意志力——规律比自律更容易坚持。",
 ]),
 ("h2", "与健康的关系"),
 ("p", "稳定的家庭膳食结构与情绪状态相互促进：吃得规律，情绪稳定；情绪稳定，才愿意继续好好吃。"),
 ("note", "本栏目为健康科普内容，不构成医疗建议。"),
]),

"nanny": ("高级保姆", "懂精准营养的照护人员：培训、推荐与上门指导", [
 ("h2", "需求从哪来"),
 ("p", "月子照护、婴幼儿喂养、老人饮食、病后康复，这些场景的日常执行者往往是家里的保姆或照护人员。她们懂不懂营养，直接决定老人和孩子每天实际吃到了什么。"),
 ("h2", "服务内容"),
 ("ul", [
   "营养知识培训：基础营养素、常见误区、特殊人群要点；",
   "食谱执行培训：按方案备餐、分量控制、做法与口感调整；",
   "照护要点：进食安全、吞咽困难应对、食欲不佳的应对；",
   "结业考核与持续指导。",
 ]),
 ("h2", "服务方式"),
 ("ul", [
   "家里已有保姆：培训 + 上门指导；",
   "需要人员的家庭：根据需求推荐并匹配；",
   "正在找工作的照护人员：参加培训，纳入人才库。",
 ]),
 ("note", "涉及医疗护理的部分需具备相应资质，本栏目服务为营养与生活照护范畴。"),
]),

"nutritionist-hr": ("供求专兼职营养师", "营养师人才供需对接，专职兼职均可", [
 ("h2", "面向机构"),
 ("ul", [
   "食堂、餐厅、幼儿园、学校、养老机构；",
   "健康管理公司、月子中心、健身机构；",
   "需要兼职营养顾问的中小企业。",
 ]),
 ("h2", "面向营养师"),
 ("ul", [
   "提供兼职与专职岗位信息；",
   "提供精准营养技术方向的培训与案例实践机会；",
   "支持远程咨询与食谱设计类工作。",
 ]),
 ("h2", "怎样加入"),
 ("ul", [
   "提交基本信息与专业背景；",
   "沟通确认方向与时间安排；",
   "签署合作说明，进入推荐名单或人才库。",
 ]),
 ("note", "本栏目为人才信息对接，具体合作与报酬以双方约定为准。请勿提交他人隐私信息。"),
]),

"charity": ("慈善新方法", "把精准营养做成公益：儿童、老人与乡村食堂", [
 ("h2", "我们相信"),
 ("p", "慈善不只是捐钱捐物，也可以是\u201c把正确的方法教给需要的人\u201d。一次系统的膳食指导，可能比一批短期物资更能改变一个家庭的长期状态。"),
 ("h2", "公益方向"),
 ("ul", [
   "面向困难家庭儿童提供膳食结构评估与改善方案；",
   "面向养老机构与社区老人开展营养科普与食谱支持；",
   "面向乡村学校食堂提供食谱设计支持；",
   "为公益机构提供营养知识培训。",
 ]),
 ("h2", "如何参与"),
 ("ul", [
   "个人：申请公益服务名额，或作为志愿者参与科普；",
   "机构：提供场地、物资或服务对象对接；",
   "专业人员：加入公益营养师队伍。",
 ]),
 ("note", "公益服务名额与服务方式以实际公布为准。"),
]),

"articles": ("重要原创文章", "技术原理、专题分析与案例复盘的精选阅读", [
 ("p", "本栏目收录研究所在营养与身心智健康方向的重要文章、科普长文与专题分析，按主题分类，便于查阅。"),
 ("h2", "主题分类"),
 ("ul", [
   "技术原理：精准营养技术的逻辑与方法；",
   "常见病与饮食结构：三高、脂肪肝、痛风、胃病；",
   "人群专题：儿童、学生、女性、老人、康复期；",
   "误区辨析：保健品、补钙、无糖食品、轻食外卖；",
   "案例复盘：真实案例的完整思路。",
 ]),
 ("h2", "阅读建议"),
 ("p", "建议先读\u201c技术原理\u201d，理解\u201c营养丰歉\u201d与\u201c结构偏差\u201d这两个核心概念，再按自身关注的问题选择专题。"),
 ("note", "文章均为健康科普内容，不能替代医疗诊断。本页为栏目框架原型，文章列表待填充。"),
]),

"health-catalog": ("重要原创健康书稿目录、研讨会、研学游主题", "本站原创内容总目录，按主题检索", [
 ("p", "本栏目是网站原创内容的总索引。目录按主题树编排，每条包含标题、所属栏目与简要说明，便于快速定位。"),
 ("h2", "目录结构"),
 ("ul", [
   "一、技术体系：精准营养技术原理 / 评估方法 / 食谱设计规范；",
   "二、人群方案：个人 / 家庭 / 食堂 / 餐厅 / 特殊人群；",
   "三、健康专题：聪明、健康、长寿、防癌、康复、免疫力、常见病预防；",
   "四、身心智专题：情绪、睡眠、认知、健康管理；",
   "五、资料文献：重要文章、获奖证书、图书与资料。",
 ]),
 ("h2", "使用说明"),
 ("ul", [
   "目录随内容更新，标注更新日期；",
   "如需纸质目录或资料索取，可通过页脚联系方式或右侧咨询框留言。",
 ]),
 ("note", "目录中的全部内容为健康科普性质，不构成医疗建议。"),
]),

"certificate": ("重要获奖证书", "资质认定、荣誉奖项与合作证明", [
 ("p", "本栏目展示研究所及相关技术成果获得的资质认定、荣誉证书与合作证明，供查阅与验证。"),
 ("h2", "展示内容"),
 ("ul", [
   "机构资质与登记信息；",
   "技术成果鉴定与认定文件；",
   "荣誉奖项与表彰证书；",
   "合作单位与项目证明。",
 ]),
 ("h2", "证书列表（占位）"),
 ("ul", [
   "【占位】证书名称一 · 颁发机构 · 年份；",
   "【占位】证书名称二 · 颁发机构 · 年份；",
   "【占位】证书名称三 · 颁发机构 · 年份。",
 ]),
 ("h2", "说明"),
 ("p", "证书以扫描件形式展示，涉及他人信息的部分做遮挡处理。如需核验原件，请联系我们。"),
 ("note", "本页图框为版式占位，上线前请替换为真实证书扫描件。"),
]),

"books": ("原创图书简介", "图书与资料：把技术体系写成可以照着做的读物", [
 ("p", "本栏目介绍研究所编写与推荐的图书、手册与内部资料，覆盖技术原理、人群方案与实操食谱。"),
 ("h2", "图书列表（占位）"),
 ("ul", [
   "【占位】《图书名称一》· 精准营养技术原理与实操 · 出版年份；",
   "【占位】《图书名称二》· 家庭营养食谱设计手册 · 出版年份；",
   "【占位】《图书名称三》· 常见病饮食结构调整指南 · 出版年份。",
 ]),
 ("h2", "内部资料"),
 ("ul", [
   "膳食调查表模板；",
   "个人 / 家庭食谱设计模板；",
   "食堂周期菜单模板；",
   "营养师培训讲义。",
 ]),
 ("h2", "获取方式"),
 ("p", "图书可通过正规渠道购买；内部资料面向培训学员与合作机构提供。如需咨询，请通过右侧咨询框留言。"),
 ("note", "图书与资料均为健康科普性质，不构成医疗建议。"),
]),

"nutrition-medicine": ("营养医学正解", "把营养当作医学的基础变量：常见病先从饮食结构找原因", [
 ("p", "营养医学正解主张：营养不是可有可无的保健品，而是影响身体状态最持续的基础变量。很多常见问题的背后，长期饮食结构偏差比偶然因素更值得优先排查。"),
 ("h2", "核心观点"),
 ("ul", [
   "食物提供身体运转所需的原料，原料结构长期失衡，身体迟早会以某种方式表现出来；",
   "同一种表现，可能由不同的营养结构造成，需要先归因、再调整；",
   "营养干预针对的是结构与节律，不替代医院诊断与治疗。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议，不用于疾病诊断。"),
]),

"nature-medicine": ("自然医学正解", "顺应自然：用食物、节律与生活方式修复身体", [
 ("p", "自然医学正解强调顺应身体的自然规律：充足睡眠、规律进餐、适度运动、亲近自然，再配合食物结构的改善，让身体的自愈能力有条件发挥作用。"),
 ("h2", "四条基本原则"),
 ("ul", [
   "先去除干扰：减少高糖、高油、过度加工食品与熬夜；",
   "再补足原料：保证优质蛋白、蔬菜、全谷与水分；",
   "尊重节律：进食时间与睡眠时间尽量规律；",
   "循序渐进：以可长期坚持为先，不追求短期猛改。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"functional-medicine": ("功能医学正解", "先看功能失衡，再谈指标：找原因而不是只压数字", [
 ("p", "功能医学正解的思路是：指标异常往往是功能长期失衡的结果。与其只盯着数字，不如回溯饮食、作息、压力与消化吸收等环节，找到可以调整的源头。"),
 ("h2", "与“只看指标”的区别"),
 ("table", (["对比项", "只看指标", "功能医学视角"], [
   ["关注点", "数字是否超标", "功能为何失衡"],
   ["处理方式", "对症压制", "查找并调整原因"],
   ["时间尺度", "短期", "中长期的饮食与生活调整"],
 ])),
 ("note", "本栏目为健康科普，不构成医疗建议，具体问题请就医。"),
]),

"evidence-medicine": ("循证医学正解", "以证据说话：哪些说法可信，哪些只是经验之谈", [
 ("p", "循证医学正解提醒我们：面对铺天盖地的健康信息，要区分“有证据支持的结论”和“个人经验或商业话术”。判断一个说法是否可信，要看证据的等级与来源。"),
 ("h2", "判断三步"),
 ("ul", [
   "看证据来源：是系统研究、临床观察，还是个人体验？",
   "看人群范围：结论来自多少人、什么人群、观察多久？",
   "看利益关系：发布者是否在推销某种产品或服务？",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"brain-science": ("脑科学正解", "大脑也靠吃：情绪、记忆与专注的物质基础", [
 ("p", "脑科学正解关注的是：情绪、记忆、专注力这些“看不见”的能力，同样依赖稳定的营养供给与血糖节律。大脑对能量与原料的变化十分敏感。"),
 ("h2", "影响大脑的三个饮食要点"),
 ("ul", [
   "稳定血糖：避免长时间空腹与高糖冲击，让大脑有平稳的能量供应；",
   "优质脂肪：深海鱼、坚果、植物油等为神经细胞提供结构材料；",
   "充足蛋白与微量元素：与神经递质的合成密切相关。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"longevity-medicine": ("长寿医学正解", "长寿是长期结构的结果，不是单一因素", [
 ("p", "长寿医学正解认为：长寿不是靠某一种“神奇食物”或补品，而是几十年饮食结构、生活方式与情绪状态共同累积的结果。少犯错，比多进补更重要。"),
 ("h2", "长期主义的三件事"),
 ("ul", [
   "把结构调对：主食粗细搭配、蔬菜占比提高、油盐适度；",
   "把节律稳住：三餐规律、睡眠充足、体重平稳；",
   "把习惯留住：能坚持几十年的，才是真正有效的方法。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"human-quality": ("提高人的质量新方法", "体质、智力、情绪三位一体的人的质量提升", [
 ("p", "提高人的质量新方法，关注的是把“体质、智力、情绪”作为整体来改善——身体结实、头脑清楚、情绪稳定，三者互相支撑。饮食结构是同时作用于三者的抓手。"),
 ("h2", "三个维度"),
 ("ul", [
   "体质：肌肉、耐力、免疫与恢复能力；",
   "智力：注意力、记忆与学习效率的营养基础；",
   "情绪：稳定血糖与规律进餐对情绪的帮助。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"eugenics-recipe": ("优生优育营养食谱设计新方法", "备孕与孕前：先把营养结构调整好", [
 ("p", "优生优育营养食谱设计新方法强调：新生命的质量，很大程度上取决于父母在孕前的身体状态。备孕阶段就应把营养结构调整到位，而不是等怀孕后再补救。"),
 ("h2", "备孕期要点"),
 ("ul", [
   "男女双方同步调整，保证优质蛋白、蔬菜与全谷的摄入；",
   "减少烟酒、高糖与过度加工食品；",
   "规律作息，配合适量运动与体重管理。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议，具体请遵医嘱。"),
]),

"maternal-recipe": ("母婴营养食谱设计新方法", "孕产与哺乳期分阶段的食谱设计", [
 ("p", "母婴营养食谱设计新方法按孕早期、孕中期、孕晚期、哺乳期分阶段设计，兼顾母亲的营养需求与胎儿、婴儿的发育需要，同时照顾口味与可执行性。"),
 ("h2", "分阶段思路"),
 ("ul", [
   "孕早期：缓解孕吐，保证基础营养与水分；",
   "孕中晚期：增加优质蛋白、钙、铁与叶酸的来源；",
   "哺乳期：保证能量与水分，支持泌乳与恢复。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议，请遵医嘱。"),
]),

"children-recipe": ("儿童学生营养食谱设计新方法", "长身体、用脑多：儿童与学生阶段的食谱要点", [
 ("p", "儿童学生营养食谱设计新方法面向正在长身体、用脑强度大的孩子，重点是保证优质蛋白、蔬菜、全谷与适量脂肪，同时减少含糖饮料与油炸零食。"),
 ("h2", "三个关注点"),
 ("ul", [
   "早餐要吃好：为上午的学习提供稳定能量；",
   "控糖控油：减少甜饮料与油炸零食；",
   "规律三餐：避免以零食代替正餐。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议；孩子如有疾病请及时就医。"),
]),

"women-recipe": ("女士营养食谱设计新方法", "不同生理阶段的女性营养结构方案", [
 ("p", "女士营养食谱设计新方法考虑女性在不同生理阶段的营养特点，围绕气血、皮肤状态、体态与情绪，设计适合长期坚持的日常食谱。"),
 ("h2", "常见关注方向"),
 ("ul", [
   "保证优质蛋白与铁的来源，支持气血与精力；",
   "增加蔬菜与抗氧化食物，帮助皮肤状态；",
   "控制精制糖与油炸，兼顾体态管理。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"elderly-recipe": ("中老年人营养食谱设计新方法", "中老年：控结构、保肌肉、护心脑", [
 ("p", "中老年人营养食谱设计新方法针对中老年的生理变化，重点是控制总结构与盐油，保证优质蛋白以维持肌肉，并照顾心脑血管与消化吸收。"),
 ("h2", "三个要点"),
 ("ul", [
   "优质蛋白要够，帮助维持肌肉与体力；",
   "控盐控油，减轻心脑血管负担；",
   "食物做得软烂易嚼，照顾消化与牙口。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议，慢性病请遵医嘱。"),
]),

"kindergarten-recipe": ("幼儿园营养食谱设计新方法+智力、智慧提升", "幼儿园集体供餐与智力、智慧提升", [
 ("p", "幼儿园营养食谱设计新方法面向幼儿园集体供餐场景，在保证食品安全与营养均衡的前提下，兼顾口味与成本，并通过食谱结构支持孩子的智力与智慧发展。"),
 ("h2", "设计要点"),
 ("ul", [
   "一周食谱轮换，主食粗细搭配、蔬菜品种多样；",
   "保证奶、蛋、豆、肉的优质蛋白来源；",
   "控糖控油，少用油炸与含糖饮料。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"group-meal-recipe": ("团餐营养食谱设计新方法", "面向企业、机构的团餐营养结构设计", [
 ("p", "团餐营养食谱设计新方法面向企业食堂、机构与大型供餐场景，在有限的成本与出餐条件下，把营养结构做合理：主食、蛋白、蔬菜的比例与轮换节奏都纳入设计。"),
 ("h2", "落地抓手"),
 ("ul", [
   "建立每周轮换食谱，避免长期单一；",
   "把蔬菜与全谷的占比写进出餐标准；",
   "结合就餐人群特点调整（体力型 / 脑力型 / 老龄型）。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"wellness-base": ("综合科学养生基地", "把精准营养落到实处的综合养生空间", [
 ("p", "综合科学养生基地是把精准营养技术落到实处的线下空间：集膳食调查、食谱设计、食材供应、健康科普与研学于一体，让“怎么吃才对”变成可以体验和长期执行的日常。"),
 ("h2", "基地功能"),
 ("ul", [
   "膳食调查与个人、家庭食谱设计服务；",
   "营养食材与科学配餐的展示与供应；",
   "健康科普、研讨会与研学游活动。",
 ]),
 ("note", "本栏目为健康科普，不构成医疗建议。"),
]),

"feedback": ("意见建议", "对本网站、栏目与内容提出您的意见建议", [
 ("p", "欢迎您对本网站提出意见建议。无论是栏目设置、内容表述、使用体验，还是您希望增加的专题，都可以通过页脚联系方式或右侧咨询框告诉我们。"),
 ("h2", "您可以反馈"),
 ("ul", [
   "栏目与导航的设置是否清晰、好用；",
   "内容是否有表述不清、需要补充或更正之处；",
   "您希望新增的专题与问题。",
 ]),
 ("h2", "联系方式"),
 ("p", "邮箱：810476008@qq.com　电话：16710241939。也可直接使用页面右侧的顾客咨询框留言。"),
 ("note", "本页为意见建议入口，您的信息仅用于本次反馈处理。"),
]),

"cooperation": ("合作加盟", "合作与加盟方式说明", [
 ("p", "精准营养技术面向有意向的机构与个人开放合作，包括营养食谱设计、技术培训、团餐与食堂改造、养生基地共建等方向。欢迎洽谈合作与加盟。"),
 ("h2", "合作方向"),
 ("ul", [
   "食堂、餐厅、团餐机构：食谱设计与出餐标准改造；",
   "幼儿园、学校、养老机构：集体供餐营养方案；",
   "健康管理机构与养生空间：技术与内容合作；",
   "营养师与从业者：培训、认证与人才对接。",
 ]),
 ("h2", "联系方式"),
 ("p", "邮箱：810476008@qq.com　电话：16710241939。请说明您的机构名称、所在地区与合作意向，我们会尽快与您联系。"),
 ("note", "本页为合作加盟说明，具体合作条款以双方正式协议为准。"),
]),
}

# --------------------------------------------------------------------------
# 4. 顺序索引
# --------------------------------------------------------------------------
ORDER = []
for _sid, _tcn, _ten, _slugs in SECTIONS:
    for _s in _slugs:
        ORDER.append(_s)
assert len(ORDER) == 40, "栏目数量应为 40，实际 %d" % len(ORDER)
NO = {slug: i + 1 for i, slug in enumerate(ORDER)}
SECTION_OF = {}
SECTION_TITLE = {}
for _sid, _tcn, _ten, _slugs in SECTIONS:
    for _s in _slugs:
        SECTION_OF[_s] = _sid
        SECTION_TITLE[_s] = _tcn

NAV = [
    ("单位简介", "pages/unit-intro.html", False, "unit-intro"),
    ("合作加盟", "pages/cooperation.html", False, "cooperation"),
    ("意见建议", "pages/feedback.html", False, "feedback"),
    ("联系我们", "index.html#contact", False, None),
]

# --------------------------------------------------------------------------
# 5. 样式 / 脚本
# --------------------------------------------------------------------------
CSS = r"""
:root{
  --red:#d81e06; --red-dark:#b31605; --ink:#1f1f1f; --gray:#666;
  --gray-2:#8c8c8c; --line:#e6e6e6; --soft:#f7f7f8; --nav:#262626;
  --wrap:1160px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:#fff;color:var(--ink);font-size:15px;line-height:1.8;
  font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB","Source Han Sans SC","Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 24px}

/* ---------- 顶部导航 ---------- */
.topbar{background:var(--nav);position:sticky;top:0;z-index:100;box-shadow:0 1px 0 rgba(0,0,0,.15)}
.topbar-inner{display:flex;align-items:center;justify-content:space-between;min-height:68px;gap:20px}
.brand{display:flex;align-items:center;gap:11px;flex:none}
.brand-mark{
  width:38px;height:38px;border-radius:3px;background:var(--red);color:#fff;
  display:grid;place-items:center;font-size:19px;font-weight:700;letter-spacing:0;flex:none;
}
.brand-text{display:flex;flex-direction:column;line-height:1.25}
.brand-text strong{color:#fff;font-size:17px;letter-spacing:2px;font-weight:600}
.brand-text em{font-style:normal;color:#8d8d8d;font-size:10.5px;letter-spacing:1.4px;text-transform:uppercase}
.mainnav{display:flex;align-items:center}
.mainnav a{
  color:#c9c9c9;font-size:14.5px;padding:0 15px;line-height:68px;display:block;
  position:relative;white-space:nowrap;transition:.2s;
}
.mainnav a:hover{color:#fff}
.mainnav a.active{color:#fff;background:rgba(255,255,255,.09)}
.mainnav a .hot{
  position:absolute;top:9px;right:3px;background:var(--red);color:#fff;font-size:9.5px;
  line-height:1;padding:3px 4px;border-radius:2px;letter-spacing:.5px;font-style:normal;
}

/* ---------- 首页 Hero ---------- */
.hero{padding:54px 0 10px;text-align:center;background:linear-gradient(180deg,#fafafa 0%,#fff 78%)}
.hero-org{color:var(--gray-2);font-size:13px;letter-spacing:2px}
.hero-title{font-size:44px;letter-spacing:4px;margin:12px 0 6px;font-weight:700}
.hero-rule{width:52px;height:3px;background:var(--red);margin:20px auto 0}
.intro{
  max-width:900px;margin:26px auto 0;background:#fff;border:1px solid var(--line);
  border-top:3px solid var(--red);border-radius:2px;box-shadow:0 8px 30px rgba(0,0,0,.05);
  padding:30px 34px 32px;text-align:center;
}
.intro .il{font-size:17.5px;font-weight:600;color:#2b2b2b;margin:0 0 12px;line-height:1.9;letter-spacing:.3px}
.intro .il:last-child{margin-bottom:0}
.intro .il .hl{color:var(--red)}
.intro .il.hl{color:var(--red);font-weight:700}

/* ---------- 四步流程：已移除（首页直接展示全部栏目） ---------- */

/* ---------- 分区标题 ---------- */
.sec{padding:42px 0 6px;scroll-margin-top:84px}
.sec-head{text-align:center;margin-bottom:32px}
.sec-title{font-size:28px;letter-spacing:1.5px;margin:0;font-weight:700}
.sec-en{color:var(--red);font-size:12px;letter-spacing:2.6px;margin-top:8px;text-transform:uppercase}
.sec-en::after{content:"";display:block;width:40px;height:2px;background:var(--line);margin:14px auto 0}

/* ---------- 栏目卡片 ---------- */
.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:15px}
.card{
  position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;
  padding:24px 15px 20px;background:#fff;border:1px solid var(--line);border-radius:2px;
  transition:border-color .22s,box-shadow .22s,transform .22s;
}
.card:hover{border-color:var(--red);box-shadow:0 12px 28px rgba(216,30,6,.10);transform:translateY(-3px)}
.card-no{
  position:absolute;top:9px;left:12px;font-size:11.5px;color:#c6c6c6;
  letter-spacing:1px;font-family:Consolas,Menlo,monospace;
}
.card-icon{color:#4c4c4c;transition:color .22s;line-height:0}
.card:hover .card-icon{color:var(--red)}
.card-icon svg{width:42px;height:42px}
.card h3{
  font-size:15px;margin:14px 0 9px;padding:4px 10px;border:1px solid var(--line);
  border-radius:2px;font-weight:600;letter-spacing:.4px;transition:.22s;
}
.card:hover h3{border-color:var(--red);color:var(--red);background:rgba(216,30,6,.04)}
.card p{margin:0;font-size:12.5px;color:#7d7d7d;line-height:1.7}

/* ---------- 快捷索引条 ---------- */
.chipbar{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:6px 0 4px}
.chipbar a{
  border:1px solid var(--line);padding:6px 14px;font-size:13px;color:#666;border-radius:2px;transition:.2s;
}
.chipbar a:hover{border-color:var(--red);color:var(--red)}
.chipbar .chip-count{color:#aaa;font-size:12.5px;padding:6px 2px}

/* ---------- 右侧悬浮咨询 ---------- */
.consult{position:fixed;right:0;top:50%;transform:translateY(-50%);z-index:300;font-size:14px}
.consult-tab{
  writing-mode:vertical-rl;background:var(--red);color:#fff;border:0;cursor:pointer;
  padding:20px 10px;font-size:13.5px;letter-spacing:4px;border-radius:4px 0 0 4px;
  box-shadow:-2px 2px 12px rgba(0,0,0,.18);font-family:inherit;
}
.consult-tab:hover{background:var(--red-dark)}
.consult-panel{
  position:absolute;right:46px;top:50%;transform:translate(12px,-50%);
  width:340px;background:#fff;border:1px solid var(--line);border-radius:4px;
  box-shadow:0 16px 44px rgba(0,0,0,.16);padding:20px 22px 22px;
  opacity:0;visibility:hidden;transition:.25s ease;
  max-height:calc(100vh - 32px);overflow-y:auto;
}
.consult.open .consult-panel{opacity:1;visibility:visible;transform:translate(0,-50%)}
.cp-head{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:11px}
.cp-head strong{font-size:16px;letter-spacing:1px}
.cp-close{background:none;border:0;font-size:22px;line-height:1;color:#aaa;cursor:pointer;padding:0 2px}
.cp-close:hover{color:var(--red)}
.cp-sub{margin:11px 0 15px;font-size:12.5px;color:#999;line-height:1.7}
#consultForm label{display:block;font-size:13px;color:#555;margin-bottom:11px}
#consultForm input,#consultForm select,#consultForm textarea{
  width:100%;margin-top:5px;border:1px solid var(--line);border-radius:2px;padding:9px 10px;
  font-size:14px;font-family:inherit;color:var(--ink);background:#fff;
}
#consultForm input:focus,#consultForm select:focus,#consultForm textarea:focus{
  outline:none;border-color:var(--red);box-shadow:0 0 0 2px rgba(216,30,6,.08);
}
#consultForm textarea{resize:vertical;line-height:1.7}
.btn-primary{
  width:100%;background:var(--red);color:#fff;border:0;padding:11px;font-size:15px;
  letter-spacing:3px;border-radius:2px;cursor:pointer;font-family:inherit;transition:.2s;
}
.btn-primary:hover{background:var(--red-dark)}
.form-tip{margin:11px 0 0;font-size:11.5px;color:#a5a5a5;line-height:1.65}
.cp-ok{display:none;padding:14px 0 6px;text-align:center}
.cp-ok strong{display:block;font-size:15px;color:var(--red);margin-bottom:8px}
.cp-ok p{margin:0;font-size:13px;color:#777;line-height:1.8}

/* ---------- 右下工具组 ---------- */
.side-tools{position:fixed;right:12px;bottom:34px;z-index:280;display:flex;flex-direction:column;gap:8px}
.tool{
  width:40px;height:40px;border:1px solid var(--line);background:#fff;border-radius:3px;
  display:grid;place-items:center;color:#5a5a5a;cursor:pointer;transition:.2s;
  box-shadow:0 2px 8px rgba(0,0,0,.07);padding:0;font-family:inherit;
}
.tool:hover{background:var(--red);color:#fff;border-color:var(--red)}
.tool svg{width:20px;height:20px}
.tool-tip{position:absolute;right:48px;background:#333;color:#fff;font-size:12px;padding:4px 9px;border-radius:2px;white-space:nowrap;opacity:0;pointer-events:none;transition:.2s}
.tool-wrap{position:relative;display:block}
.tool-wrap:hover .tool-tip{opacity:1}

/* ---------- 页脚 ---------- */
.footer{background:var(--soft);border-top:1px solid var(--line);margin-top:52px;padding-top:38px}
.footer-grid{display:grid;grid-template-columns:1.35fr 1.25fr .75fr;gap:34px}
.footer h4{
  font-size:16px;margin:0 0 14px;padding-left:11px;border-left:3px solid var(--red);
  line-height:1.3;letter-spacing:.5px;
}
.footer p{margin:0 0 8px;font-size:13.5px;color:#6a6a6a;line-height:1.95}
.footer p b{color:#3d3d3d;font-weight:600}
.foot-qr{text-align:center}
.qr-box{
  width:132px;height:132px;margin:0 auto 8px;background:#fff;border:1px solid var(--line);
  padding:7px;border-radius:3px;
}
.qr-svg{width:100%;height:100%;display:block}
.qr-img{width:100%;height:100%;display:block;object-fit:contain}
.qr-cap{margin:0;font-size:12.5px;color:#7a7a7a;line-height:1.6}
.foot-bar{background:var(--nav);color:#9a9a9a;font-size:12.5px;margin-top:32px;padding:15px 0}
.foot-bar .wrap{display:flex;flex-wrap:wrap;gap:6px 22px;justify-content:space-between;align-items:center}
.foot-bar span{line-height:1.7}
.foot-bar a{color:#c2c2c2}
.foot-bar a:hover{color:#fff}

/* ---------- 内页 ---------- */
.crumb{background:var(--soft);border-bottom:1px solid var(--line);font-size:13px;color:#8b8b8b}
.crumb .wrap{padding:14px 24px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.crumb a:hover{color:var(--red)}
.crumb .sep{color:#c9c9c9}
.crumb .cur{color:#3d3d3d}
.article-wrap{display:grid;grid-template-columns:minmax(0,1fr) 286px;gap:44px;padding:38px 0 10px}
.article h1{font-size:30px;margin:0 0 10px;letter-spacing:1.5px;font-weight:700;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.draft-badge{
  font-size:11px;color:var(--red);border:1px solid currentColor;padding:2px 7px;
  border-radius:2px;font-weight:400;letter-spacing:1px;font-style:normal;
}
.article-en{color:var(--red);font-size:11.5px;letter-spacing:2.4px;text-transform:uppercase}
.article-meta{
  margin:16px 0 28px;padding-bottom:16px;border-bottom:1px solid var(--line);
  font-size:13px;color:#9a9a9a;display:flex;gap:18px;flex-wrap:wrap;
}
.article h2{
  font-size:19px;margin:32px 0 13px;padding-left:12px;border-left:3px solid var(--red);
  line-height:1.45;letter-spacing:.5px;
}
.article p{margin:0 0 15px;font-size:15.5px;line-height:2.05;color:#333}
.article ul{list-style:none;margin:0 0 16px;padding:0}
.article ul li{position:relative;padding-left:20px;margin-bottom:10px;font-size:15.5px;line-height:1.95;color:#3d3d3d}
.article ul li::before{content:"";position:absolute;left:4px;top:13px;width:6px;height:6px;border-radius:50%;background:var(--red);opacity:.75}
.article ul li.nobullet{padding-left:0}
.article ul li.nobullet::before{display:none}
.article table{width:100%;border-collapse:collapse;margin:18px 0 22px;font-size:14px}
.article th,.article td{border:1px solid var(--line);padding:10px 12px;text-align:left;line-height:1.8}
.article th{background:var(--soft);font-weight:600;color:#3d3d3d}
.article td{color:#555}
.article .note{
  background:#fff8f6;border:1px solid #f7ded8;border-left:3px solid var(--red);
  padding:14px 16px;font-size:13.5px;color:#8a5b52;line-height:1.95;margin:24px 0 8px;border-radius:2px;
}
.article-nav{
  display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
  margin-top:38px;padding-top:20px;border-top:1px solid var(--line);font-size:14px;color:#8b8b8b;
}
.article-nav a{color:#4a4a4a}
.article-nav a:hover{color:var(--red)}
.aside-card{border:1px solid var(--line);border-radius:2px;padding:18px;margin-bottom:20px;background:#fff}
.aside-card h4{
  font-size:15px;margin:0 0 12px;padding-left:10px;border-left:3px solid var(--red);line-height:1.3;
}
.aside-list a{
  display:flex;justify-content:space-between;gap:10px;font-size:13.5px;color:#6b6b6b;
  padding:9px 0;border-bottom:1px dashed var(--line);transition:.2s;
}
.aside-list a:last-child{border-bottom:0}
.aside-list a:hover{color:var(--red)}
.aside-list a span.no{color:#c6c6c6;font-family:Consolas,Menlo,monospace;font-size:12px}
.aside-cta{background:var(--soft)}
.aside-cta p{margin:0 0 12px;font-size:13px;color:#777;line-height:1.85}
.aside-cta button{width:100%}

/* ---------- 响应式 ---------- */
@media (max-width:1100px){
  .grid{grid-template-columns:repeat(4,1fr)}
  .article-wrap{grid-template-columns:1fr;gap:30px}
}
@media (max-width:900px){
  .topbar-inner{flex-wrap:wrap;padding:12px 0;min-height:0}
  .mainnav{width:100%;overflow-x:auto;border-top:1px solid rgba(255,255,255,.08);padding-top:2px}
  .mainnav a{line-height:46px;padding:0 13px;font-size:14px}
  .mainnav a .hot{top:4px}
  .grid{grid-template-columns:repeat(3,1fr)}
  .footer-grid{grid-template-columns:1fr;gap:26px}
  .foot-qr{text-align:left}
  .qr-box{margin:0 0 8px}
}
@media (max-width:720px){
  .grid{grid-template-columns:repeat(2,1fr)}
  .hero{padding:34px 0 6px}
  .hero-title{font-size:30px;letter-spacing:2px}
  .intro{padding:22px 18px 24px;margin-top:20px}
  .intro .il{font-size:15.5px}
  .sec-title{font-size:23px}
  .consult-panel{right:44px;width:min(320px,calc(100vw - 58px));padding:16px 16px 18px}
  .side-tools{right:8px;bottom:22px}
  .article h1{font-size:23px}
  .article p,.article ul li{font-size:15px}
  .foot-bar .wrap{justify-content:flex-start}
}
@media (max-width:430px){
  .grid{grid-template-columns:1fr}
  .card{padding:22px 16px 20px}
}

/* ---------- Hero 简介（简洁·窄） ---------- */
.hero-inner{max-width:820px;margin:0 auto;text-align:center}
.hero-text{text-align:center}
.hero-text .hero-org{margin-left:auto;margin-right:auto}
.hero-text .hero-rule{margin:18px auto 0}
.hero-text .intro{margin:22px auto 0;max-width:640px}
@media (max-width:760px){
  .hero-inner{max-width:100%}
}
"""

JS = r"""
(function () {
  /* 右侧顾客咨询：展开 / 收起 */
  var box = document.getElementById('consult');
  var tab = document.getElementById('consultTab');
  var closeBtn = document.getElementById('consultClose');
  function openBox() { box && box.classList.add('open'); }
  function closeBox() { box && box.classList.remove('open'); }
  if (tab) {
    tab.addEventListener('click', function (e) {
      e.stopPropagation();
      box.classList.contains('open') ? closeBox() : openBox();
    });
  }
  if (closeBtn) closeBtn.addEventListener('click', closeBox);
  document.addEventListener('click', function (e) {
    if (box && box.classList.contains('open') && !box.contains(e.target)) closeBox();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeBox();
  });

  /* 任意"咨询"触发按钮 */
  Array.prototype.forEach.call(document.querySelectorAll('[data-open-consult]'), function (el) {
    el.addEventListener('click', function (e) { e.preventDefault(); openBox(); });
  });

  /* 表单：原型不提交，仅本地反馈 */
  var form = document.getElementById('consultForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = document.getElementById('consultOk');
      if (ok) ok.style.display = 'block';
      form.style.display = 'none';
    });
  }

  /* 回到顶部 */
  var toTop = document.getElementById('toTop');
  function syncTop() {
    if (!toTop) return;
    toTop.style.display = window.scrollY > 300 ? '' : 'none';
  }
  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    window.addEventListener('scroll', syncTop);
    syncTop();
  }
})();
"""

# --------------------------------------------------------------------------
# 6. HTML 片段
# --------------------------------------------------------------------------
def nav_html(prefix, active_key):
    parts = []
    for label, href, hot, key in NAV:
        cls = "navlink"
        if key and key == active_key:
            cls += " active"
        badge = '<i class="hot">HOT</i>' if hot else ""
        parts.append('<a class="%s" href="%s%s">%s%s</a>' % (cls, prefix, href, label, badge))
    return "\n      ".join(parts)

CONSULT_HTML = """
<div class="consult" id="consult">
  <button class="consult-tab" id="consultTab" type="button" aria-label="打开顾客咨询">顾客咨询</button>
  <div class="consult-panel" id="consultPanel">
    <div class="cp-head">
      <strong>顾客咨询</strong>
      <button type="button" class="cp-close" id="consultClose" aria-label="关闭">&times;</button>
    </div>
    <p class="cp-sub">留下您的情况，我们按具体问题给建议。</p>
    <form id="consultForm">
      <label>称呼<input type="text" name="name" placeholder="怎么称呼您"></label>
      <label>手机号<input type="tel" name="phone" placeholder="方便联系的手机号"></label>
      <label>咨询方向
        <select name="topic">
          <option>个人营养食谱设计</option>
          <option>家庭营养食谱设计</option>
          <option>食堂 / 餐厅食谱设计</option>
          <option>健康问题咨询</option>
          <option>培训与营养师合作</option>
          <option>公益服务申请</option>
          <option>其他</option>
        </select>
      </label>
      <label>您的具体情况<textarea name="content" rows="3" placeholder="例如：常年在外吃饭，容易疲劳，想调整饮食结构"></textarea></label>
      <button type="submit" class="btn-primary">提交咨询</button>
      <p class="form-tip">提交后我们会在 1 个工作日内与您联系。您的信息仅用于本次咨询。</p>
    </form>
    <div class="cp-ok" id="consultOk">
      <strong>已收到您的咨询</strong>
      <p>我们会尽快与您联系。若需即时沟通，可拨打页脚电话。</p>
    </div>
  </div>
</div>
"""

SIDE_TOOLS_HTML = """
<div class="side-tools">
  <span class="tool-wrap">
    <a class="tool" href="tel:16710241939" title="电话咨询">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h3l2 5-2.5 1.5a11 11 0 0 0 5 5L15 12l5 2v3a2 2 0 0 1-2.2 2A15 15 0 0 1 4 5.2A2 2 0 0 1 6 3z"/></svg>
    </a>
    <span class="tool-tip">电话咨询</span>
  </span>
  <span class="tool-wrap">
    <button class="tool" type="button" title="微信咨询">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 4C5 4 2 6.7 2 10c0 1.9 1 3.5 2.7 4.6L4 17.5l3-1.6c.6.1 1.3.2 2 .2"/><path d="M15 9c-3.9 0-7 2.5-7 5.6s3.1 5.6 7 5.6c.8 0 1.5-.1 2.2-.3l2.8 1.5-.7-2.5c1.6-1 2.7-2.6 2.7-4.3C22 11.5 18.9 9 15 9z"/></svg>
    </button>
    <span class="tool-tip">微信咨询</span>
  </span>
  <span class="tool-wrap">
    <button class="tool" id="toTop" type="button" title="回到顶部">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20V5"/><path d="M5.5 11.5 12 5l6.5 6.5"/></svg>
    </button>
    <span class="tool-tip">回到顶部</span>
  </span>
</div>
"""

def qr_svg(seed="precision-nutrition-site", n=25, size=140):
    """生成一个视觉上像二维码的占位图形（非可扫描二维码）。"""
    h = hashlib.md5(seed.encode("utf-8")).digest()
    finders = [(0, 0), (0, n - 7), (n - 7, 0)]

    def finder_state(i, j):
        for fi, fj in finders:
            if fi <= i < fi + 7 and fj <= j < fj + 7:
                di, dj = i - fi, j - fj
                ring = (di in (0, 6) or dj in (0, 6) or (2 <= di <= 4 and 2 <= dj <= 4))
                return True, ring
        return False, False

    def inside_quiet(i, j):
        for fi, fj in finders:
            if fi - 1 <= i < fi + 8 and fj - 1 <= j < fj + 8:
                return True
        return False

    m = size / float(n)
    rects = []
    for i in range(n):
        for j in range(n):
            is_finder, ring = finder_state(i, j)
            if is_finder:
                on = ring
            elif inside_quiet(i, j):
                on = False
            else:
                b = h[(i * 7 + j * 13) % len(h)]
                on = ((b >> ((i * 3 + j) % 8)) & 1) == 1
            if on:
                rects.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>' % (j * m, i * m, m, m))
    return ('<svg class="qr-svg" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
            'fill="#1f1f1f" shape-rendering="crispEdges">%s</svg>' % (size, size, "".join(rects)))

QR_IMG_PATH = os.path.join(ROOT, "assets", "wechat-qr.png")
QR_IMG_EXISTS = os.path.isfile(QR_IMG_PATH)

def footer_html(prefix):
    if QR_IMG_EXISTS:
        qr = '<img class="qr-img" src="%sassets/wechat-qr.png" alt="微信二维码">' % prefix
        cap = "扫码加微信咨询"
    else:
        qr = qr_svg()
        cap = "扫码加微信咨询<br>（二维码为占位图，待替换）"
    return """
<footer class="footer" id="contact">
  <div class="wrap footer-grid">
    <div>
      <h4>%s</h4>
      <p><b>主办单位：</b>%s</p>
      <p>%s致力于身心智健康与营养关系的研究与应用，以\u201c精准营养技术\u201d为方法，为个人、家庭、食堂、餐厅设计科学营养食谱。</p>
      <p><b>服务方向：</b>营养食谱设计 · 健康科普 · 技术培训 · 人才对接 · 公益服务</p>
    </div>
    <div>
      <h4>联系我们</h4>
      <p><b>地址：</b>北京海淀区中关村善缘街1号<br>深圳宝安区沙井荣泰园1106号<br>北海市银海区杭州路金癸领海郡2501号</p>
      <p><b>电话：</b>16710241939</p>
      <p><b>邮箱：</b>810476008@qq.com</p>
    </div>
    <div class="foot-qr">
      <div class="qr-box">%s</div>
      <p class="qr-cap">%s</p>
    </div>
  </div>
  <div class="foot-bar">
    <div class="wrap">
      <span>&copy; 2026 %s · %s</span>
      <span>京ICP备2026056507号</span>
      <span>本站内容为健康科普参考，不构成医疗建议，不作为诊疗依据</span>
    </div>
  </div>
</footer>
""" % (ORG_NAME, ORG_NAME, ORG_NAME, qr, cap, ORG_NAME, SITE_NAME)

# 首页简介四行文案已直接内联在 build_index()；四步流程区已移除。

# --------------------------------------------------------------------------
# 7. 页面组装
# --------------------------------------------------------------------------
def page_shell(prefix, active_key, title, desc, body, extra_head=""):
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="keywords" content="精准营养技术,营养食谱设计,身心智健康,%s">
<link rel="stylesheet" href="%sassets/style.css">
</head>
<body>
<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="brand" href="%sindex.html">
      <span class="brand-mark">营</span>
      <span class="brand-text">
        <strong>%s</strong>
        <em>%s</em>
      </span>
    </a>
    <nav class="mainnav">
      %s
    </nav>
  </div>
</header>
%s
%s
%s
%s
<script src="%sassets/site.js"></script>
</body>
</html>
""" % (title, desc, ORG_NAME, prefix, prefix, SITE_NAME,
       "PRECISION NUTRITION TECHNOLOGY", nav_html(prefix, active_key),
       body, CONSULT_HTML, SIDE_TOOLS_HTML, footer_html(prefix), prefix)


def render_blocks(blocks):
    out = []
    for kind, payload in blocks:
        if kind == "h2":
            out.append("<h2>%s</h2>" % payload)
        elif kind == "p":
            out.append("<p>%s</p>" % payload)
        elif kind == "ul":
            items = []
            for x in payload:
                cls = " class=\"nobullet\"" if x[:1] in "①②③④⑤⑥⑦⑧⑨⑩" else ""
                items.append("<li%s>%s</li>" % (cls, x))
            out.append("<ul>%s</ul>" % "".join(items))
        elif kind == "note":
            out.append('<div class="note">%s</div>' % payload)
        elif kind == "table":
            head, rows = payload
            th = "".join("<th>%s</th>" % h for h in head)
            trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (th, trs))
    return "\n".join(out)


def card_html(slug):
    title, brief, _ = CONTENT[slug]
    icon = ICONS[slug]
    return """<a class="card" href="pages/%s.html">
  <span class="card-no">%02d</span>
  <span class="card-icon"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">%s</svg></span>
  <h3>%s</h3>
  <p>%s</p>
</a>""" % (slug, NO[slug], icon, title, brief)


# 首页：四行居中简介 + 40 栏目网格（已移除 Hero 插画、信任背书区与四步流程区）。

def build_index():
    cards = "\n".join(card_html(s) for s in ORDER)
    secs_html = """
<section class="sec" id="all-sections" style="padding-top:26px">
  <div class="wrap">
    <div class="grid">
%s
    </div>
  </div>
</section>""" % cards

    body = """
<section class="hero">
  <div class="wrap hero-inner">
    <div class="hero-text">
      <div class="hero-org">%s &nbsp;主办</div>
      <h1 class="hero-title">%s</h1>
      <div class="hero-rule"></div>
      <div class="intro">
        <p class="il">人类常见病主因：<span class="hl">稀里糊涂吃，糊里糊涂病！</span></p>
        <p class="il">精准营养技术可预测常见病，也知道您体内食物营养丰歉，</p>
        <p class="il">设计个人、家庭、团餐、食堂、餐厅科学营养食谱！</p>
        <p class="il hl">饮食越科学，身心智越健康！</p>
      </div>
    </div>
  </div>
</section>
%s
""" % (ORG_NAME, SITE_NAME, secs_html)

    return page_shell(
        "", None,
        "%s — %s" % (SITE_NAME, ORG_NAME),
        "精准营养技术网：人类常见病主因是稀里糊涂吃。由%s主办，提供个人、家庭、团餐、食堂、餐厅科学营养食谱设计与身心智健康科普。" % ORG_NAME,
        body,
    )


def build_detail(slug):
    title, brief, blocks = CONTENT[slug]
    idx = NO[slug]
    prev_slug = ORDER[idx - 2] if idx > 1 else None
    next_slug = ORDER[idx] if idx < len(ORDER) else None

    related = [s for s in SECTIONS_BY_SLUG[slug][3] if s != slug]
    for s in ORDER:
        if s not in related and s != slug and len(related) < 6:
            related.append(s)

    rel_html = "".join(
        '<a href="%s.html"><span>%s</span><span class="no">%02d</span></a>' % (s, CONTENT[s][0], NO[s])
        for s in related[:6]
    )

    nav_html_ = ""
    if prev_slug:
        nav_html_ += '<a href="%s.html">&larr; 上一栏目：%s</a>' % (prev_slug, CONTENT[prev_slug][0])
    else:
        nav_html_ += '<a href="../index.html">&larr; 返回首页</a>'
    if next_slug:
        nav_html_ += '<a href="%s.html">下一栏目：%s &rarr;</a>' % (next_slug, CONTENT[next_slug][0])

    body = """
<div class="crumb">
  <div class="wrap">
    <a href="../index.html">首页</a>
    <span class="sep">/</span>
    <a href="../index.html#all-sections">全部栏目</a>
    <span class="sep">/</span>
    <span class="cur">%s</span>
  </div>
</div>

<div class="wrap article-wrap">
  <article class="article">
    <h1>%s <em class="draft-badge">原型稿</em></h1>
    <div class="article-en">%s</div>
    <div class="article-meta">
      <span>栏目 %02d / 40</span>
      <span>分类：%s</span>
      <span>更新：%s</span>
    </div>
    %s
    <div class="article-nav">%s</div>
  </article>

  <aside>
    <div class="aside-card">
      <h4>相关栏目</h4>
      <div class="aside-list">%s</div>
    </div>
    <div class="aside-card aside-cta">
      <h4>需要具体方案？</h4>
      <p>个人 / 家庭 / 食堂 / 餐厅的营养食谱设计，可按您的实际情况定制。</p>
      <button class="btn-primary" type="button" data-open-consult>立即咨询</button>
    </div>
  </aside>
</div>
""" % (title,
       title, "CN-%02d" % idx, idx, SECTION_TITLE[slug], UPDATED,
       render_blocks(blocks), nav_html_, rel_html)

    return page_shell(
        "../", "all-sections",
        "%s — %s" % (title, SITE_NAME),
        "%s：%s" % (title, brief),
        body,
    )


NAV_PAGES = ("unit-intro", "feedback", "cooperation")


def build_nav_page(slug):
    """导航型页面（单位简介 / 意见建议 / 合作加盟）：不在 40 栏目网格内。"""
    title, brief, blocks = CONTENT[slug]
    body = """
<div class="crumb">
  <div class="wrap">
    <a href="../index.html">首页</a>
    <span class="sep">/</span>
    <span class="cur">%s</span>
  </div>
</div>

<div class="wrap article-wrap">
  <article class="article">
    <h1>%s</h1>
    <div class="article-meta">
      <span>更新：%s</span>
    </div>
    %s
    <div class="article-nav"><a href="../index.html">&larr; 返回首页</a></div>
  </article>

  <aside>
    <div class="aside-card aside-cta">
      <h4>需要具体方案？</h4>
      <p>个人 / 家庭 / 团餐 / 食堂 / 餐厅的营养食谱设计，可按您的实际情况定制。</p>
      <button class="btn-primary" type="button" data-open-consult>立即咨询</button>
    </div>
  </aside>
</div>
""" % (title, title, UPDATED, render_blocks(blocks))

    return page_shell(
        "../", slug,
        "%s — %s" % (title, SITE_NAME),
        "%s：%s" % (title, brief),
        body,
    )


SECTIONS_BY_SLUG = {}
for _sid, _tcn, _ten, _slugs in SECTIONS:
    for _s in _slugs:
        SECTIONS_BY_SLUG[_s] = (_sid, _tcn, _ten, _slugs)


def write(path, text):
    full = os.path.join(ROOT, path)
    d = os.path.dirname(full)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    return full


README = """# 精准营养技术网 · 原型站

静态原型，双击 `index.html` 即可在浏览器打开；也可用任意静态服务器托管。

## 目录结构

```
index.html            首页（网站简介 + 40 栏目网格 + 页脚）
pages/*.html          40 个栏目详情页 + 3 个导航页（单位简介 / 意见建议 / 合作加盟）
assets/style.css      全站样式
assets/site.js        右侧咨询框 / 回到顶部等交互
build.py              生成脚本（改内容后重新运行 python build.py 即可重建全站）
README.md             本说明
```

## 布局要点

- 顶部深色导航（单位简介 / 合作加盟 / 意见建议 / 联系我们），首页正文居中标题 + 红色分隔线。
- 首页上方为网站简介（四行居中，口号标红），下方直接平铺 40 个栏目，每排 5 个，点击卡片进入详情页。
- 右侧边缘悬浮"顾客咨询"竖标签，点击展开表单（原型不提交，仅本地提示）。
- 右下角三个圆形工具按钮：电话、微信、回到顶部。
- 页脚：主办单位、地址、电话、邮箱、二维码、备案号、科普免责声明。

## 待替换的占位内容（上线前必改）

| 位置 | 当前占位 | 说明 |
| --- | --- | --- |
| 页脚 地址 | 已填写（北京 / 深圳 / 北海三地） | 如需调整请改 build.py 的 footer_html() |
| 页脚 电话 | 已填写（16710241939） | — |
| 页脚 邮箱 | 已填写（810476008@qq.com） | — |
| 页脚 备案号 | 已填写（京ICP备2026056507号） | — |
| 页脚 二维码 | 已接入（assets/wechat-qr.png） | 更换该图片后重跑 build.py 即可 |
| 证书页 | 【占位】证书名称一/二/三 | 替换为真实证书扫描件 |
| 图书页 | 【占位】《图书名称一/二/三》 | 替换为真实书名与封面 |
| 文章页 | 主题分类框架 | 待填充真实文章列表 |
| 咨询表单 | 前端演示，无后端 | 上线需接后端接口或表单服务 |

## 内容说明

- 40 个栏目的详情文字为原型示例文案，用于确认信息层级与阅读节奏，正式上线前需由业务方定稿。
- 全站健康类内容均标注"不构成医疗建议"，正式上线请保留该免责声明。
"""


def main():
    write("assets/style.css", CSS.strip() + "\n")
    write("assets/site.js", JS.strip() + "\n")
    write("index.html", build_index())
    for s in ORDER:
        write("pages/%s.html" % s, build_detail(s))
    for s in NAV_PAGES:
        write("pages/%s.html" % s, build_nav_page(s))
    write("README.md", README)
    print("built: index.html + %d detail pages + %d nav pages" % (len(ORDER), len(NAV_PAGES)))
    for s in ORDER:
        print("  %02d %s -> pages/%s.html" % (NO[s], CONTENT[s][0], s))


if __name__ == "__main__":
    main()
