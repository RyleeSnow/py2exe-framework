# Py2exe Framework

> **Language**: [English](README.md) | [中文](README.zh.md)

![Python](https://img.shields.io/badge/python-3.9.12-blue.svg)
![PyInstaller](https://img.shields.io/badge/PyInstaller-6.14.1-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)


利用 PyInstaller 帮助你将自己的 Python 项目快速打包成独立的 `.exe` 可执行文件。支持 GUI 界面版本和后台运行版本。

<br>

## 📚 目录

- [框架特性](#-框架特性)
- [项目结构](#-项目结构)
- [快速开始](#-快速开始)
- [集成自己的代码](#%EF%B8%8F-集成自己的代码)
- [打包代码到EXE](#-打包代码到exe)
- [常见问题](#-常见问题)
- [许可证](#-许可证)

<br>

## ✨ 框架特性

- 🖥️ **GUI 界面支持**：提供友好的图形化界面，支持修改参数、保存配置和实时日志输出
- 🔧 **后台运行模式**：静默后台运行，通过 JSON 文件配置参数，运行完成后弹窗提示
- 📝 **完善日志系统**：集成日志模块，便于调试和问题排查
- 🎨 **自定义字体**：支持加载自定义字体文件，提升界面美观度
- 🛡️ **异常处理**：完善的异常处理和进程管理

<br>

## 📁 项目结构

```
py2exe-framework/
├── src/                         # 源代码文件夹
│   ├── gui/                     # GUI 界面版本
│   │   ├── main.py              # 你的主要业务逻辑代码
│   │   ├── run_gui.py           # GUI 界面入口
│   │   ├── my_logger.py         # 日志模块
│   │   ├── config.json          # 配置文件
│   │   ├── icon.ico             # 应用图标
│   │   └── generate_exe.sh      # GUI版打包脚本
│   └── background/              # 后台运行版本
│       ├── main.py              # 你的主要业务逻辑代码
│       ├── run_background.py    # 后台运行入口
│       ├── my_logger.py         # 日志模块
│       ├── config.json          # 配置文件
│       ├── icon.ico             # 应用图标
│       └── generate_exe.sh      # 后台版打包脚本
├── fonts/                       # 字体文件夹
│   ├── README.md                # 字体使用说明
│   └── SarasaMonoSC-Regular.ttf # 示例字体文件
├── examples/                    # 测试数据文件夹
│   └── sample_data.csv          # 测试数据文件
└── LICENSE                      # 许可证文件
```

<br>

## 🚀 快速开始

### 1. 环境准备

```bash
# 确保已安装 Python (推荐 3.9 或更高版本)
python --version

# 安装 PyInstaller
pip install pyinstaller

# 安装其他依赖（根据你的代码需求，如果直接使用测试案例的话仅需安装 pandas）
pip install pandas
```


### 2. 下载 REPO

```bash
git clone <repo-url>
cd py2exe-framework
```

### 3. 快速测试
**(1) <u>GUI 界面版本</u>**
- 特点：图形化界面操作，用户友好
- 功能：可在界面上直接修改参数、保存配置、查看实时日志输出
```bash
cd src/gui
python run_gui.py
```
- 启动后会打开图形界面
- 可以在界面上修改参数并保存
- 点击运行按钮查看实时输出

**(2) <u>后台运行版本</u>**
- 特点：静默后台运行，无界面干扰
- 功能：通过修改 JSON 配置文件设置参数，运行完成后会弹窗提示结果
```bash
cd src/background
python run_background.py
```
- 程序会在后台静默运行
- 运行完成后弹窗提示结果
- 查看日志文件了解详细运行情况

<br>

## 🛠️ 集成自己的代码
选择你想用的模式：
- GUI 界面版本，进入 `src/gui` 文件夹
- 后台运行版本，进入 `src/background` 文件夹
### 1. 配置参数

修改 `config.json` 文件：目前内容仅为示例，可根据实际情况进行参数设置。

```json
{
  "logs_folder": "",
  "custom_param_1": "...",
  "custom_param_2": "...",
  "custom_param_3": "..."
}
```

**注意：**
- 请把所有需要用户设置的参数填入，如果不提供默认值，可以先填入空字符串占位符。
- 支持字符串、数字、布尔值等基本数据类型；Windows 路径请使用双反斜杠 `\\` 或正斜杠 `/`。
- `logs_folder` 为固定参数：
  - 如果不需要 log 文件，可删除此参数，程序仍正常运行；
  - 如果希望生成 log 文件，可保留此参数，日志文件将保存至指定文件夹，文件名格式：`logger_YYYYMMDD_HHMMSS.log`。在代码中的使用示例如下：

    ```python
    from my_logger import logger

    def some_function():
        logger.info("程序开始执行")
        logger.warning("这是一个警告")
        logger.error("这是一个错误")
        logger.debug("调试信息")
    ```


### 2. 放入自己的代码到文件夹
将自己的代码放入文件夹中（`src/gui` 或者 `src/background`），如有层级关系可保留，只要保证以 `main.py` 为主入口即可。编辑 `main_process` 函数，保证以此函数调用你代码的主流程。

**注意：** 所有 `config.json` 中设置的参数或用户在 GUI 界面填入的参数，都将以 `dict` 格式传入 `main_process` 函数。

```python
def main_process(args_dict: dict) -> None:
    """
    你的主要业务逻辑函数
    """    
```

### 3. 界面自定义 (仅针对 GUI 界面版本)

- 自定义应用名称

    在 `src/gui/run_gui.py` 中修改：

    ```python
    application_name = "你的应用程序名称"  # 修改这里
    ```

- 添加自定义字体
  - 将字体文件（`.ttf` 或 `.otf`）放入 `fonts/` 文件夹
  - 在 `run_gui.py` 中的 `preferred_fonts` 配置中使用：

    ```python
    preferred_fonts = {
        'default': [
            ("你的字体名称", 10),
            ("Microsoft YaHei", 10)  # 备用字体
        ],
    }
    ```

### 4. 运行
**(1) <u>GUI 界面版本</u>**
```bash
python run_gui.py
```
启动 GUI 界面后，你将看到：

- **配置参数区域**：显示当前 `config.json` 中的所有参数
   - 可以直接在界面上修改参数值
   
- **操作按钮**：
   - `Load Config`：再次从 `config.json` 文件加载配置参数
   - `Save Config`：将当前界面上的参数保存到 `config.json` 文件
   - `Run Program`：执行主程序逻辑

- **程序输出区域**：实时显示程序运行过程
   - 显示日志信息（info、warning、error等）
   - 显示程序的print输出
   - 支持滚动查看历史输出

**(2) <u>后台运行版本</u>**
```bash
python run_background.py
```
- 程序启动后会读取 `config.json` 配置文件
- 静默执行 `main_process` 函数中的业务逻辑
- 程序执行完成后会弹出提示窗口告知运行结果
- **注意**：在运行前手动编辑 `src/background/config.json` 文件，修改所需的参数值，保存文件后再运行程序

<br>


## 📦 打包代码到 EXE

### 1. 准备工作

- 确保程序能正常运行
- 检查所有依赖是否已安装
- 确认配置文件路径正确

### 2. Windows 系统打包

**(1) <u>GUI 界面版本</u>**

```bash
cd src/gui

# 方式一：使用提供的脚本
generate_exe.sh

# 方式二：手动执行
pyinstaller --onefile --noconsole --icon=icon.ico run_gui.py
```

**(2) <u>后台运行版本</u>**

```bash
cd src/background

# 方式一：使用提供的脚本
generate_exe.sh

# 方式二：手动执行
pyinstaller --onefile --noconsole --icon=icon.ico run_background.py
```

**(3) 打包参数说明**

- `--onefile`：打包成单个exe文件
- `--noconsole`：不显示控制台窗口（适合GUI版本和后台静默运行）
- `--icon=icon.ico`：设置exe文件图标

**(4) 打包后处理**

- 打包完成后，在 `dist/` 文件夹中找到生成的 `.exe` 文件
- 将 `.exe` 文件复制到目标位置
  - **GUI版本**：复制 `config.json` 到exe同目录（用户可在界面修改参数）
  - **后台版本**：确保 `config.json` 配置正确后复制到exe同目录
- 删除不需要的 `build/` 和 `dist/` 文件夹以及 `.spec` 文件

### 3. Linux 系统打包（测试中）

- 如果需要在 Linux 上打包 Windows exe：

    ```bash
    # 安装 wine
    sudo apt update
    sudo apt install wine

    # 使用 wine 运行 PyInstaller
    wine C:/Python38/Scripts/pyinstaller.exe run_background.py --icon="icon.ico" --onefile
    ```
- `.spec` 文件
    ```
    a = Analysis(
        ['objdictedit.py'],    # 主程序或脚本文件的列表。这里只有一个文件 'objdictedit.py'。
        pathex=[],             # 指定 Python 解释器的搜索路径。这里为空列表，表示使用默认的搜索路径。
        binaries=[],           # 包含在打包文件中的二进制文件列表。这里没有指定任何二进制文件。
        datas=[
        ('config/DS-302.prf', 'config'),
        ('config/DS-401.prf', 'config'),
        ],
        hiddenimports=[],      # 需要明确指定的隐藏导入模块列表。这里没有指定任何隐藏导入模块。
        hookspath=[],          # 钩子文件的路径列表，用于处理特定模块的导入问题。这里为空列表，表示没有额外的钩子路径。
        hooksconfig={},        # 钩子配置选项的字典，用于定制导入钩子的行为。这里为空字典，表示没有特定的钩子配置。
        runtime_hooks=[],      # 运行时钩子列表，这些钩子在运行时修改导入行为。这里为空列表，表示没有运行时钩子。
        excludes=[],           # 被排除在打包之外的模块列表。这里为空列表，表示没有需要排除的模块。
        noarchive=False,       # 控制是否将 Python 源代码打包到归档中。这里设置为 False，表示允许将 Python 源代码打包到归档中。
        optimize=0,            # 优化级别，控制生成的字节码的优化等级。这里设置为 0，表示没有进行任何优化。
    )
    ```

<br>

## 🐛 常见问题

### 1. 打包后exe无法运行

**解决方法**：
- 检查是否遗漏了依赖文件
- 确保所有路径使用绝对路径
- 确保 Python 可以顺利运行程序

### 2. 找不到配置文件

**解决方法**：
- 确保 `config.json` 与 exe 文件在同一目录
  - GUI版本：可在界面重新加载配置文件
  - 后台版本：必须与 exe 文件在同一目录

### 3. 后台版本运行后没有弹窗

**解决方法**：
- 检查程序是否正常执行完成
- 查看日志文件确认程序状态
- 确保程序没有卡在某个步骤

### 4. 程序崩溃

**解决方法**：
- 确保主入口有完善的异常处理：
```python
if __name__ == '__main__':
    try:
        # 你的代码
        pass
    except Exception as e:
        logger.error(f"程序异常：{e}")
        input("按回车键退出...")
```
### 5. 其他注意事项
- `main.py` 所在的文件夹里面不要有 `__init__.py`，否则路径会出问题

<br>

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。


