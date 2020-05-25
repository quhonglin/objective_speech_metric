import os
import librosa
import copy
from tqdm import tqdm
from metrics import compute_STOI, compute_PESQ


# 默认参数：定义默认参数要写在最右边
def compute(path_arr, sr=16000):
    """分别计算clean与noise、clean与denoisy的STOI、PESQ值

    Args:
        path_arr: 包含clean、noisy（denoisy）文件路径的数组
        sr: 采样率

    Returns:
        result_arr_c_n:包含clean与noisy计算结果的列表
        result_arr_c_d:包含clean与denoisy计算结果的列表。若无denoisy，则该项为空
    """
    file_num = 1
    result_arr_c_n = []
    result_arr_c_d = []
    clean_wavs_paths = path_arr[0]
    noisy_wavs_paths = path_arr[1]
    denoisy_wavs_paths = path_arr[2]

    # load()：以浮点时间序列的形式加载音频文件,将音频格式转化为Numpy格式存储
    clean_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(clean_wavs_paths, desc="Loading clean wavs")]
    noisy_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(noisy_wavs_paths, desc="Loading noisy wavs")]
    assert (len(clean_wavs) == len(noisy_wavs)), "clean与noisy文件数量不一致"

    if denoisy_wavs_paths:
        denoisy_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(denoisy_wavs_paths, desc="Loading denoisy wavs")]
        assert (len(clean_wavs) == len(denoisy_wavs)), "clean与denoisy文件数量不一致"
    else:
        denoisy_wavs = copy.deepcopy(noisy_wavs)

    for i, (noisy_wav, clean_wav, denoisy_wav) in tqdm(
            # enumerate()：将参数与索引号连接为一个enumerate(枚举)对象
            enumerate(zip(noisy_wavs, clean_wavs, denoisy_wavs)), desc="正在计算评价指标"
    ):
        lengths = [len(noisy_wav), len(clean_wav), len(denoisy_wav)]
        lengths.sort()
        shorter_length = lengths[0]

        stoi_c_n = compute_STOI(clean_wav[:shorter_length], noisy_wav[:shorter_length])
        pesq_c_n = compute_PESQ(clean_wav[:shorter_length], noisy_wav[:shorter_length])
        if denoisy_wavs_paths:
            stoi_c_d = compute_STOI(clean_wav[:shorter_length], denoisy_wav[:shorter_length])
            pesq_c_d = compute_PESQ(clean_wav[:shorter_length], denoisy_wav[:shorter_length])
        else:
            stoi_c_d = 0
            pesq_c_d = 0

        """
        解析路径：
            D:/数据集/Clean/0001_bus_0dB.wav --> basename()：0001_bus_0dB.wav
            --> splitext()：("0001_bus_0dB", ".wav") --> [0]：0001_bus_0dB
            --> split()：["0001", "bus", "0dB"]
        """
        file_name = os.path.splitext(os.path.basename(clean_wavs_paths[i]))[0].split("_")

        result_arr_c_n.append(
            [
                file_num,
                stoi_c_n,
                pesq_c_n,
            ]
        )
        if denoisy_wavs_paths:
            result_arr_c_d.append(
                [
                    file_num,
                    stoi_c_d,
                    pesq_c_d,
                ]
            )

        if len(file_name) == 3:
            num, noise, snr = file_name
            c_n_item = result_arr_c_n[-1]
            c_n_item[0] = num
            c_n_item.insert(1, noise)
            c_n_item.insert(2, snr)
            if denoisy_wavs_paths:
                c_d_item = result_arr_c_d[-1]
                c_d_item[0] = num
                c_d_item.insert(1, noise)
                c_d_item.insert(2, snr)

        file_num += 1

    return result_arr_c_n, result_arr_c_d
