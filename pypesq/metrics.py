from pypesq import pesq
from pystoi.stoi import stoi


def compute_STOI(clean_signal, noisy_signal, sr=16000):
    """计算 STOI

    Args:
        clean_signal:纯净语音信号
        noisy_signal:带噪语音信号
        sr:采样率
    """
    return stoi(clean_signal, noisy_signal, sr, extended=False)


def compute_PESQ(clean_signal, noisy_signal, sr=16000):
    """计算PESQ

    Args:
        clean_signal:纯净语音信号
        noisy_signal:带噪语音信号
        sr: 采样率
    """
    return pesq(clean_signal, noisy_signal, sr)
