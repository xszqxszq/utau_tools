UTAU、人力Vocaloid相关脚本与工具的存放处。不定期更新。

## process_ibm_json.py
根据[IBM Watson Speech to Text](https://www.ibm.com/watson/services/speech-to-text/)返回的json与原始音频文件，将整段音频分割为单音节发音，供UTAU等软件使用。目前仅支持中文音频。

使用例：
`python process_ibm_json.py [JSON文件] [原始WAV音频] [置信度阈值(0~1)] [音节时长阈值(秒)]`

## process_ibm_json_jpn.py
与 `process_ibm_json.py` 使用方法类似，但此程序仅支持日语(罗马音)。

为确保效果，在使用`process_ibm_json_jpn.py`推荐使用以下命令获取语音识别结果：

`curl -X POST -u "apikey:你的API密钥" --header "Content-Type: audio/wav" --data-binary @文件名.wav "你的URL/v1/recognize?model=ja-JP_BroadbandModel&profanity_filter=false&redaction=false&timestamps=true&word_confidence=true" --output 识别结果文件名.json`

API密钥和URL可以在IBM Cloud控制台查看。

Watson Speech to Text的使用教程：
https://cloud.ibm.com/docs/services/speech-to-text?topic=speech-to-text-gettingStarted#getting-started-tutorial
