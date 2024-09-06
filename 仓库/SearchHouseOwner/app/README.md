# 房东直租

一个简单的使用 Flask 的 Python 应用。
可以运行在 LeanEngine Python 运行时环境。

# 安装依赖
```
pip install -Ur requirements.txt 
```

将 app id 等信息更新到 `start.sh` 文件中：

```
export LC_APP_ID=<your app id>
export LC_APP_KEY=<your app key>
export LC_APP_MASTER_KEY=<your master key>
```

启动项目：

```
$ ./start.sh
```

应用即可启动运行：[localhost:3000](http://localhost:3000)



##提取图片数子步骤

1. 下载cuneiform或者tesseract-ocr ,这两个是提取器
```
sudo apt-get install tesseract-ocr cuneiform
```

2. 下载python图片处理类库
```
pip install Pillow
```

3. 下载python的ocr处理类库
```
pip install pyocr
```