import tablib


def save_result(metrics_seq, headers, output_path="./output.xls"):
    """设计输出表格

    Args:
        metrics_seq: 表格数据
        headers: 表格头部
        output_path: 保存路径

    """
    data = tablib.Dataset(*metrics_seq, headers=headers)
    print(f"测试过程结束，结果将存储至 {output_path}.")
    with open(output_path, "wb") as f:
        f.write(data.export("xls"))
