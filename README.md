# AWG4100 Python API

Awg4100-Python.7z 包含了 `awg4100`模块与示例。
AWG4100用户手册.docx 是用户手册，包含接口说明。

## 使用说明

脚本运行环境为Python3(建议版本 > 3.6) 。为了方便各个版本使用，我们不提供需要安装的版本，使用时需要与 模块 `awg4100` 在同一目录下，如下所示，目录`awg4100`中的内容缺一不可。**使用前请确保Demo能够正确运行**
![avatar](./python使用目录.png)

## 常见问题
### OSError: [WinError 126]
可能是由于缺失 VC运行时造成的，请安装msvc2013运行时环境。https://www.microsoft.com/zh-cn/download/details.aspx?id=40784  和  msvc2015 运行时环境 https://www.microsoft.com/en-us/download/details.aspx?id=48145 建议x86版本与x64版本都要安装。为了方便，我们在`VC运行时`放了一份。

如果安装之后依旧报错。请将 msvcp120.dll、msvcr120.dll、msvcp140.dll vcruntime140.dll 放到 `awg4100` 目录下。**请注意这几个 dll 是 32 位的还是 64 位的**如果使用 32 位 Python 则复制 32 位的，如果使用 64 位 Python 则复制 64 位的。