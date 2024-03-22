import sys
import os
from datetime import datetime
import time
sys.path.append('./')
sys.path.append('./root')
sys.path.append('./script')
sys.path.append('./img')


from script.scriptBot import ScriptBot
from img.img_audio import ImgBot
from img.img_audio import AudioBot
from video.videoBot import VideoBot
def main():
    #requirement = "Giới thiệu về dự án Datalace, mục tiêu là tạo ra một ứng dụng giúp người dụng nhập file dữ liệu và yêu cầu vẽ đồ thị, ứng dụng sẽ cho ra những đồ thị đẹp dựa vào yêu cầu của người dùng."
    #requirement = "Giới thiệu về cờ tướng và cách chơi"
    #requirement = "Giới thiệu về Cha Co Chi (Chả có chi), đây là một fanpage chuyên với ba lĩnh vực chính là blogger, sách và chuyện học đại học. Được thành lập bởi 3 thành viên là các sinh viên đại học. Nhóm tác giả sử dụng hình ảnh con sứa làm biểu tượng cho fanpage. Fanpage có mục tiêu là tạo ra những bài viết chất lượng, những câu chuyện thú vị qua giọng văn mộc mạc, tình cảm."
    requirement = "Giới thiệu về cách làm bánh mì chảo, nguyên liệu gồm có bánh mì, trứng, thịt, rau cải và gia vị."
    time = datetime.now()
    #time_str = '16:53,2024_03_13'
    time_str = time.strftime("%H:%M,%Y_%m_%d")
    os.makedirs(f"result/{time_str}", exist_ok=True)
    bot = ScriptBot(time_str)
    bot.execute(requirement)
    i, v =bot.seperate()

    imgBot = ImgBot(time_str)
    imgBot.execute(i)
    print(v)
    audioBot = AudioBot(time_str)
    audioBot.execute(v)

    videoBot1 = VideoBot(time_str)
    videoBot1.merge()

    videoBot1.gen_subtitle()
    videoBot1.create_srt_file()
    videoBot1.add_subtitle()
    print("Done")

if __name__ == "__main__":
    main()
