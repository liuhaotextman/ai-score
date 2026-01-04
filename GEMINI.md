项目的规划是这样的，完成一个在线考试阅卷评分系统(后续顺利的话，就做线下阅卷评分)。技术方案：导入知识库(或者添加知识库的时候)
使用google的文本模型把文本解析成向量，再把向量和文本存入pgsql17。
阅卷评分的时候，通过试题获取知识库向量，然后传给gemini大模型，让他打分。
api方面通过fast api提供接口给前端使用。暂时不考虑前端的开发。
关于pgsql和redis的配置放在config.ymal中了，gemini api key放在环境变量中，获取方式：os.environ.get("GEMINI_API_KEY", "")
<br>
你帮我快速的构建产品，并提供产品建议。
<br>
这里用的是虚拟环境，python版本和安装包以及包安装工具pip都在.venv中。
上一级目录的cookbook文件夹
是一个google开源的一个项目，帮助开发者快速入门和了解他们的大模型产品gemini及其相关的大模型产品。因为现在是用gemini做大语言模型，所以如果你使用gemini api的时候可以参考他们的例子。
他们的代码例子在quickstarts和examples当中，请忽略他们提供的js代码
<br>
