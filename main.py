# -*- coding: utf-8 -*-
import struct
import wave

from pydub import AudioSegment


def cross_sound():
    a1 = wave.open(f1)
    a2 = wave.open(f2)
    output = wave.open('cross_sound.wav', 'w')
    output.setnchannels(1)  # 音频文件只有一个声道
    output.setsampwidth(2)  # 音频文件采样位宽为 2 Bytes
    output.setframerate(sampleRate * 2)  # 设置输出音频的采样率16000*2，即为原音频的两倍，这样音频时长就不变

    for i in range(min(a1.getnframes(), a2.getnframes())):
        # 依次读取两个文件的音频帧并顺序写入至输出文件
        output.writeframes(a1.readframes(1))
        output.writeframes(a2.readframes(1))
    output.close()


def combine_sound():
    """
    手动合并两个音轨成一个音频
    :return:
    """
    # 使用Python内置的wave库来打开wav音频文件
    a1 = wave.open(f1)
    a2 = wave.open(f2)
    output = wave.open('combine_sound.wav', 'w')
    output.setnchannels(1)  # 音频文件只有一个声道
    output.setsampwidth(2)  # 音频文件采样位宽为 2 Bytes
    output.setframerate(sampleRate)  # 采样率16000

    for i in range(min(a1.getnframes(), a2.getnframes())):
        frame1 = a1.readframes(1)
        frame2 = a2.readframes(1)
        # 每个采样点的能量值相加除以2.
        # 16000采样率、单声道、16bits位宽的音频，每帧是两个字节
        # 读出来的bytes，使用struct.unpack('<h', )转成有符号short integer后进行相加
        # Ref: https://docs.python.org/3.6/library/struct.html
        frame = (struct.unpack('<h', frame1)[0] + struct.unpack('<h', frame2)[0]) // 2
        # 有符号short integer使用struct.pack('<h', )转为bytes后再写入帧序列中
        output.writeframes(struct.pack('<h', frame))
    output.close()


def combine2():
    """
    使用pydub库来合并两个音轨成一个音频
    :return:
    """
    sound1 = AudioSegment.from_file(f1)
    sound2 = AudioSegment.from_file(f2)
    # pydub合并的声音会比手动合并的声音更大
    combined = sound1.overlay(sound2)
    combined.export("combined.wav", format='wav')


if __name__ == '__main__':
    f1 = 'bensound-creativeminds_10s.wav'
    f2 = 'bensound-summer_10s.wav'
    sampleRate = 16000.0  # hertz

    cross_sound()
    combine_sound()
    combine2()
