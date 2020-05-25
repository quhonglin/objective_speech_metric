import os
import argparse
import copy

from parse import list_parse, directory_parse
from comp import compute
from save import save_result


def calculate():
    """解析命令行参数和选项并进行计算

    Notes:
        结果保存到output_path中，默认为"./output.xls"

    """
    # 添加参数
    parser = argparse.ArgumentParser(description="Speech Enhancement Evaluation Metrics")
    parser.add_argument("--path_file", required=False, type=str, help="包含两组语音文件路径的列表")
    parser.add_argument("--clean_dir", required=False, type=str, help="纯净语音文件目录")
    parser.add_argument("--noisy_dir", required=False, type=str, help="带噪语音文件目录")
    parser.add_argument("--denoisy_dir", required=False, type=str, help="降噪语音文件目录")
    parser.add_argument("--output_path", default="./output.xls", type=str, help="评价指标存储的全路径，必须以拓展名 .xls 结尾")
    parser.add_argument("--limit", default=0, type=int, help="被测试语音的数量。默认为0，表示不限制数量")
    parser.add_argument("--offset", default=0, type=int, help="从某个索引位置开始计算评价指标，默认为0，表示从索引为 0 的语音开始计算")
    parser.add_argument("--sr", default=16000, type=int, help="语音文件的采样率")
    args = parser.parse_args()

    # 测试参数
    # args.path_file = "../data/path_two.txt"
    args.path_file = "../data/path_three.txt"
    # args.clean_dir = "data/Clean"
    # args.noisy_dir = "data/Noisy"
    # args.denoisy_dir = "data/DeNoisy"
    # args.clean_dir = "data/Clean_normal"
    # args.noisy_dir = "data/Noisy_normal"
    # args.denoisy_dir = "data/DeNoisy_normal"

    if args.path_file:
        assert os.path.exists(args.path_file), "列表不存在！"
        assert (args.clean_dir is None) and (args.noisy_dir is None) and (args.denoisy_dir is None), "不可同时输入列表和目录！"
    elif args.clean_dir and args.noisy_dir:
        assert os.path.exists(args.clean_dir), "纯净语音文件不存在！"
        assert os.path.exists(args.noisy_dir), "带噪语音文件不存在！"
    else:
        raise NotImplementedError("请至少输入一个列表文件或两组目录！")

    # 解析
    if args.path_file:
        print(f"音频列表文件路径为：{args.path_file}")
        path_arr = list_parse(args.path_file)
    else:
        print(f"纯净语音目录路径为：{args.clean_dir}")
        print(f"带噪语音目录路径为：{args.noisy_dir}")
        if args.denoisy_dir:
            print(f"降噪语音目录路径为：{args.denoisy_dir}")
        path_arr = directory_parse(args.clean_dir, args.noisy_dir, args.denoisy_dir, args.limit, args.offset)

    """计算"""
    result_arr_c_n, result_arr_c_d = compute(path_arr=path_arr, sr=args.sr)

    """保存"""
    headers = ("语音编号", "噪声类型", "信噪比")
    metrics_seq = copy.deepcopy(result_arr_c_n)
    denoisy_paths = path_arr[2]
    stoi = 3
    pesq = 4
    if len(metrics_seq[0]) == 3:
        headers = headers[0:1]
        stoi = 1
        pesq = 2
    if denoisy_paths:
        headers += (
            "STOI 纯净与带噪",
            "STOI 纯净与降噪 ",
            "PESQ 纯净与带噪",
            "PESQ 纯净与降噪",
            "STOI 提升",
            "PESQ 提升",
        )

        for i, arr in enumerate(metrics_seq):
            arr.append(result_arr_c_d[i][stoi])        # STOI_c_d
            arr.append(result_arr_c_d[i][pesq])        # PESQ_c_d
            arr.append((result_arr_c_d[i][stoi] - result_arr_c_n[i][stoi]) / result_arr_c_n[i][stoi])    # STOI:(c_d - c_n) / c_n
            arr.append((result_arr_c_d[i][pesq] - result_arr_c_n[i][pesq]) / result_arr_c_n[i][pesq])    # PESQ:(c_d - c_n) / c_n

    else:
        headers += (
            "STOI",
            "PESQ",
        )

    save_result(metrics_seq, headers, output_path=args.output_path)


# 测试运行
calculate()
