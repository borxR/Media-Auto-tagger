import subprocess
import json
import os
from imdb import IMDb
ia = IMDb()

mediainfo="binaries\\mediainfo.exe"
mkvpropedit="binaries\\mkvpropedit.exe"


file=input("Enter Filepath: ")



grp="" #Enter Your group name here

mimdb=input("Enter IMDB LINK: ")
newid=(mimdb.replace("https://www.imdb.com/title/","").replace("/"," ")).split()

for ids in newid:
    if ids.find("tt")!=-1:
        imbdbid=ids.replace("tt","").replace("/","").replace(" ","")

    
new=ia.get_movie(imbdbid)
mname=new['title'].replace("'","").replace(",","").replace(" ",".")
myear="."+str(new['year'])
finname=mname+myear




jsonname=file.replace(".mkv","")+".json"

mediainfo_output = subprocess.Popen([mediainfo, '--Output=JSON', '-f', file], stdout=subprocess.PIPE)
mediainfo_json = json.load(mediainfo_output.stdout)




mediainfo = mediainfo_json


for v in mediainfo['media']['track']: # mediainfo do video
    if v['@type'] == 'Video':
        video_format = v['Format']
        

video_codec = ''
if video_format == "AVC":
    video_codec = 'H.264'
elif video_format == "HEVC":
    video_codec = 'HEVC'


for v in mediainfo['media']['track']: # mediainfo do video
    if v['@type'] == 'Video':  
        video_res= v['Height']
        video_resw= v['Width']


if video_res=="2160" or video_resw=="3840":
    vid_res="2160p"
elif video_res=="1080" or video_resw=="1920":
    vid_res="1080p"
elif video_res=="720" or video_resw=="1280":
    vid_res="720p"

for m in mediainfo['media']['track']: # mediainfo do audio
    if m['@type'] == 'Audio' and m['ID']=='2' :
        codec_name = m['Format']
        channels_number = m['Channels']
        atmos_chk=m['Format_Commercial_IfAny']

audio_codec = ''
audio_channels = ''
if codec_name == "AAC":
    audio_codec = 'AAC'
elif codec_name == "AC-3":
    audio_codec = "DD"
elif codec_name == "E-AC-3":
    audio_codec = "DDP"
elif codec_name == "E-AC-3 JOC":
    audio_codec = "Atmos"
elif codec_name == "MLP FBA":
    audio_codec = "TrueHD"
    
if channels_number == "2":
    audio_channels = "2.0"
elif channels_number == "6":
    audio_channels = "5.1"
elif channels_number == "8":
    audio_channels = "7.1"

# print(atmos_chk)

if str(atmos_chk).find("Atmos")!=-1:
    srrnd=".Atmos"
else:
    srrnd=""
for v in mediainfo['media']['track']: # check bluray
    if v['@type'] == 'Video':
        vid_src = v
        r = v.get('extra', None)
if r!=None:
    if r["OriginalSourceMedium"]=="Blu-ray":
        vid_type="Bluray.Remux"
else:
    pltname=input("Enter Platform Name Abbreviation: ")
    vid_type=pltname+".WEB-DL"


audio_ = audio_codec + audio_channels + srrnd


output_name = '{}.{}.{}.{}.{}-{}'.format(finname,vid_res, vid_type,video_codec, audio_,grp)


tagname=('{} {} {} {} {}-{}'.format(finname,vid_res, vid_type,video_codec, audio_,grp)).replace(".Atmos"," Atmos").replace(".WEB-DL"," WEB-DL")
os.system(f'{mkvpropedit} "{file}" --edit info --set "title={tagname}"')
print("File Tagged:",tagname)
os.rename(file,os.path.dirname(file)+output_name+".mkv")
print("\n")

print(output_name)