import os
from utils import *
from imitate_ui import *

import dist.calculate_score as calculate_score


openpose_dir='<PATH TO OPENPOSE>'


class FFmpegCapturer(object):
    def __init__(self, camera_device="None"):
        self.camera_device = camera_device

    def start_capture(self, output_file):
        command = "ffmpeg -f dshow -i video=\"%s\" -qscale:v 2 -vframes 1 -s 1920x1080 -y %s"%(self.camera_device, output_file)
        os.system(command)

class OpenPosePic():
    def openposedemo_pic(self,input_pic,output_pic,face=False,hand=False):
        cwd=os.getcwd()
        print(cwd)
        os.chdir(openpose_dir)
        command='OpenPoseDemo --image_dir '+input_pic+' --write_images '+output_pic
        if face:
            command+=' --face'
        if hand:
            command+=' --hand'
        os.system(command)
        os.chdir(cwd)
    def openposedemo_json(self,input_pic,output_json,face=False,hand=False):
        cwd=os.getcwd()
        print(cwd)
        os.chdir(openpose_dir)
        command='OpenPoseDemo --image_dir '+input_pic+' --write_json '+output_json
        if face:
            command+=' --face'
        if hand:
            command+=' --hand'
        os.system(command)
        os.chdir(cwd)

def photo_score(ns,camera=True,num=5,del_all=True,pose=True):
    ##CAMERA_DEVICE = "USB Camera"
    CAMERA_DEVICE='HP Wide Vision HD Camera'#设备管理器查看
    f_obj = FFmpegCapturer(CAMERA_DEVICE)
    pose_obj=OpenPosePic()
    origin_pic_path=rootpath+'\\origin_pics'
    origin_json_path=rootpath+'\\origin_jsons'
    imitate_pic_path=rootpath+'\\imitate_pics'
    imitate_json_path=rootpath+'\\imitate_jsons'
    #ns='3'
    if camera:
        if del_all:
            del_file(imitate_pic_path)
            del_file(imitate_json_path)
        for i in range(num):
            print("摄像头正在进行第%s次拍照"%i)
            f_obj.start_capture(imitate_pic_path+'\\'+get_pic_name(ns))
    if pose:
        pose_obj.openposedemo_json(input_pic=imitate_pic_path,output_json=imitate_json_path)
    return calculate_score.score_print(ns,origin_json_path,imitate_json_path)

def main():
    pygame.init()

    ScreenSize=(1200+300,800)#屏幕大小

    #bgColor=(255, 204, 255)#背景颜色
    bgColor=(255,255,220)#背景颜色
    btColor=(215, 252, 252)

    screen = pygame.display.set_mode(ScreenSize, pygame.RESIZABLE)
    screen.fill(bgColor)

    namelist=os.listdir(rootpath+'\\origin_pics\\')

    records=draw_bg(screen,namelist=namelist,rankboard=True)#绘制界面

    #等待鼠标操作
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y=event.pos[0],event.pos[1]
                    if 150<x<295 and 10<y<60:#点击输入照片名称
                        pygame.draw.rect(screen, btColor,((150,10),(145, 50)))
                        reset_ui(screen)
                        pygame.display.flip()

                        #输入照片名称
                        flg=1
                        while(flg):#控制输入合法
                            name=input_str(screen,1)
                            name+='.jpg'
                            if name not in namelist:
                                fontch = pygame.font.SysFont('simHei',15)
                                txt = fontch.render('输入名称非法，请重新输入', True, (255,0,0))
                                screen.blit(txt, (5,140))
                                pygame.display.flip()
                                pygame.time.delay(500)
                                pygame.draw.rect(screen, bgColor,((0,135),(290, 45)))
                                pygame.display.flip()
                            else:
                                flg=0

                        insert_picture(screen,name)
                        pygame.display.flip()
                    elif 515<x<660 and 10<y<60:#点击输入照片数
                        pygame.draw.rect(screen, btColor,((515,10),(145, 50)))
                        pygame.display.flip()

                        #输入照片数
                        flg=1
                        while(flg):#控制输入合法
                            num=input_str(screen,2)
                            try:
                                num=int(num)
                                flg=0
                            except:
                                fontch = pygame.font.SysFont('simHei',15)
                                txt = fontch.render('输入数目非法，请重新输入', True, (255,0,0))
                                screen.blit(txt, (5,140))
                                pygame.display.flip()
                                pygame.time.delay(500)
                                pygame.draw.rect(screen, bgColor,((0,135),(290, 45)))
                                pygame.display.flip()
                    elif 5<x<140 and 70<y<120:#拍照
                        score,name_score=photo_score(ns=name[:-4],num=num,camera=True,pose=True,del_all=True) # set as False to use cached json files to score
                    elif 370<x<505 and 70<y<120:#分数
                        print_score(screen,score=score,name_score=name_score)

                        #print(score,name)
                        if score>records[name][0]:
                            records[name]=score

                            fontch = pygame.font.SysFont('simHei',20)
                            txt = fontch.render(name+'图片新纪录!', True, (255,0,0))
                            screen.blit(txt, (965,415))
                            pygame.display.flip()
                            pygame.time.delay(1500)
                            pygame.draw.rect(screen, bgColor,((965,415),(200, 30)))
                            pygame.display.flip()
                            print_records(screen,namelist,records)

main()