# openvasTranslate

本程序使用的是有道翻译API，故需要在translate.py文件中输入自己的ID和秘钥
```
# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''
```

由于openvas无法输出中文报告，但可以输出一个英文的xml报告文件，故使用此程序从输出的xml报告中提取需要的数据，然后调用API进行翻译，翻译后的数据存储到translate.json文件中，然后再根据自己需要的报告模板(reportdemo.html)输出目标中文报告
