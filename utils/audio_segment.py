"""
dependecies:
  conda install ffmpeg
  pip install pydub
"""

from pydub import AudioSegment
from pydub.silence import split_on_silence

# 读取wav文件
sound_file = AudioSegment.from_wav("test.wav")
audio_chunks = split_on_silence(sound_file, 
    # 静默部分的阈值，小于该值的部分会被认为是静默
    min_silence_len=500,
    # 静默部分的最小长度
    silence_thresh=-50
)

# 遍历每个语音片段并输出
for i, chunk in enumerate(audio_chunks):
    out_file = f"chunk{i}.wav"
    chunk.export(out_file, format="wav")
    print(f"Saved chunk {i}. Length: {len(chunk)}ms")
