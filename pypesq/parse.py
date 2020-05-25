import os
from utils import find_aligned_wav_files


def list_parse(path_file):
    """解析出clean、noisy（denoisy）文件路径

    Args:
        path_file: 文件路径列表

    Returns:
        包含clean、noisy（denoisy）文件路径的数组
    """
    clean_wavs_paths = []
    noisy_wavs_paths = []
    denoisy_wavs_paths = []

    assert os.path.exists(path_file), "列表不存在！"

    with open(path_file, "r", newline="\n") as f:
        for line in f.readlines():
            # 去掉行末的换行符
            if line[-1:] == "\n":
                line = line[:-2]
            # 解析每行有几个路径字符串
            line_str = line.split(",")
            line_str_len = len(line_str)
            if (line_str[-1] == "") or (line_str[-1] == " "):
                line_str_len -= 1
            if (line_str_len != 2) and (line_str_len != 3):
                print("列表无法读取！")
            # strip():去除首尾空格
            clean_wavs_paths.append(line_str[0].strip())
            noisy_wavs_paths.append(line_str[1].strip())
            if line_str_len == 3:
                denoisy_wavs_paths.append(line_str[2].strip())

    return [clean_wavs_paths, noisy_wavs_paths, denoisy_wavs_paths]


def directory_parse(clean_dir, noisy_dir, denoisy_dir="", limit=0, offset=0):
    """解析出clean、noisy（denoisy）文件路径

    Args:
        clean_dir: 纯净语音目录
        noisy_dir: 带噪语音目录
        denoisy_dir: 降噪语音目录。默认为空，表示可选
        limit: 被测试语音的数量。默认为0，表示不限制数量
        offset: 从某个索引位置开始计算评价指标，默认为0，表示从索引为 0 的语音开始计算

    Returns:
        包含clean、noisy（denoisy）文件路径的数组
    """
    denoisy_wavs_paths = []

    noisy_wavs_paths, clean_wavs_paths, shorter_length = find_aligned_wav_files(
        noisy_dir, clean_dir, limit=limit, offset=offset
    )

    if denoisy_dir:
        denoisy_wavs_paths, _, shorter_length = find_aligned_wav_files(
            denoisy_dir, clean_dir, limit=limit, offset=offset
        )

    return [clean_wavs_paths, noisy_wavs_paths, denoisy_wavs_paths]
