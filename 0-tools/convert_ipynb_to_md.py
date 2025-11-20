import nbconvert
import sys
from pathlib import Path
import logging
import argparse

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def convert_single_notebook(ipynb_path: Path, output_dir: Path):
    """
    将单个 .ipynb 文件转换为 .md 文件，并保持原有的目录结构。

    Args:
        ipynb_path (Path): 源 .ipynb 文件的路径对象。
        output_dir (Path): 保存 .md 文件的目标根目录。
    """
    try:
        # 确保输出文件的父目录存在
        output_md_path = output_dir / (ipynb_path.stem + ".md")
        output_md_path.parent.mkdir(parents=True, exist_ok=True)

        logging.info(f"正在转换: {ipynb_path} -> {output_md_path}")

        # 1. 初始化 Markdown 转换器
        exporter = nbconvert.MarkdownExporter()

        # 2. 读取 ipynb 文件内容
        #    nbformat.read 会验证 notebook 格式
        (body, resources) = exporter.from_filename(str(ipynb_path))

        # 3. 将转换后的内容写入新的 .md 文件
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(body)

        logging.info(f"成功转换: {output_md_path}")

    except Exception as e:
        logging.error(f"转换失败: {ipynb_path}. 错误: {e}")


def main():
    """
    主函数，用于解析命令行参数并启动转换过程。
    """
    # --- 创建命令行参数解析器 ---
    # 这是构建 CLI 工具的标准方式
    parser = argparse.ArgumentParser(
        description="一个将 .ipynb 文件递归转换为 .md 格式的命令行工具。"
    )

    # 添加 "输入路径" 参数，可以是文件或目录
    parser.add_argument(
        "input_path",
        type=str,
        help="源文件 (.ipynb) 或源目录的路径。"
    )

    # 添加一个可选的 "输出目录" 参数
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="converted_markdown",
        help="保存转换后 .md 文件的目录 (默认为: converted_markdown)。"
    )

    args = parser.parse_args()

    # --- 将字符串路径转换为更易于操作的 Path 对象 ---
    input_path = Path(args.input_path)
    output_path = Path(args.output)

    # --- 校验输入路径是否存在 ---
    if not input_path.exists():
        logging.error(f"错误: 输入路径 '{input_path}' 不存在。")
        sys.exit(1)  # 退出程序并返回一个错误码

    # --- 判断输入是文件还是目录，并执行相应操作 ---
    if input_path.is_file():
        if input_path.suffix == '.ipynb':
            convert_single_notebook(input_path, output_path)
        else:
            logging.warning(f"输入文件 '{input_path}' 不是 .ipynb 文件，已跳过。")

    elif input_path.is_dir():
        logging.info(f"开始递归扫描目录: {input_path}")
        # 使用 .rglob('*.ipynb') 递归查找所有 .ipynb 文件
        notebooks_found = list(input_path.rglob('*.ipynb'))

        if not notebooks_found:
            logging.warning(f"在目录 '{input_path}' 中没有找到任何 .ipynb 文件。")
            return

        logging.info(f"找到了 {len(notebooks_found)} 个 .ipynb 文件，准备转换...")

        for notebook in notebooks_found:
            # 计算相对于原始输入目录的路径，以便在输出目录中重建结构
            relative_path = notebook.relative_to(input_path)
            # 组合成最终的输出目录
            final_output_dir = output_path / relative_path.parent
            convert_single_notebook(notebook, final_output_dir)

    logging.info("所有转换任务已完成！")


# --- Python 脚本的入口点 ---
# 确保只有当这个文件被直接执行时，main() 函数才会被调用
if __name__ == "__main__":
    main()
