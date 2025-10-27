import face_recognition
import os
import cv2
import pygame,sys
import PIL
from PIL import Image
from tkinter.filedialog import askdirectory
import pygame.camera
import shutil
clock = pygame.time.Clock()
pygame.init()
KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'
TOLERANCE = 0.5
FRAME_THICKNESS = 4
FONT_THICKNESS = 2
MODEL = 'hog'  
run=True
pygame.camera.init()
cameranotfound=False
try:
        ok=pygame.camera.list_cameras()
        webcam=pygame.camera.Camera(ok[0])
except:
        cameranotfound=True
        

class Button:
        def __init__(self,text,width,height,pos,elevation,top_color,bottom_color,ct):
                #Core attributes 
                self.pressed = False
                self.elevation = elevation
                self.dynamic_elecation = elevation
                self.original_y_pos = pos[1]
                self.ct=ct
                self.tp_color=top_color
                # top rectangle 
                self.top_rect = pygame.Rect(pos,(width,height))
                #self.top_color = '#475F77'

                # bottom rectangle 
                self.bottom_rect = pygame.Rect(pos,(width,height))
                #self.bottom_color = '#354B5E'
                #text
                self.text_surf = gui_font.render(text,True,'#FFFFFF')
                self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
                self.top_color=top_color
                self.bottom_color=bottom_color                              

        def draw1(self):
                # elevation logic 
                self.top_rect.y = self.original_y_pos - self.dynamic_elecation
                self.text_rect.center = self.top_rect.center 

                self.bottom_rect.midtop = self.top_rect.midtop
                self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

                pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
                pygame.draw.rect(screen,self.tp_color, self.top_rect,border_radius = 12)
                screen.blit(self.text_surf, self.text_rect)
                self.check_click()

        def check_click(self):
                mouse_pos = pygame.mouse.get_pos()
                if self.top_rect.collidepoint(mouse_pos):
                        self.tp_color = self.ct
                        if pygame.mouse.get_pressed()[0]:
                                self.dynamic_elecation = 0
                                self.pressed = True
                        else:
                                self.dynamic_elecation = self.elevation
                                if self.pressed == True:
                                        
                                        self.pressed = False
                else:
                        self.dynamic_elecation = self.elevation
                        self.tp_color = self.top_color

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Gui Menu')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None,30)


def name_to_color(name):
        pass 
# Returns (R, G, B) from name
def name_to_color(name):
    # Take 3 first letters, tolower()
    # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color
def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1],
                                   "BGR")

print('Loading known faces...')
known_faces = []
known_names = []

# We oranize known faces as subfolders of KNOWN_FACES_DIR
# Each subfolder's name becomes our label (name)


d={}
d1=[]
st=""
i=0
print('Processing unknown faces...')

l=0
button_width, button_height = 200, 50
button_x, button_y = (700 - button_width) // 2, (1500 - 700) // 2
button_rect = pygame.Rect(650, 550, button_width, button_height)
loading_bar_x, loading_bar_y = 479, 460
loading_bar_width, loading_bar_height = 510, 26
x=0
loading_bar_rect = pygame.Rect(loading_bar_x, loading_bar_y, x, loading_bar_height)
loading_bar_rect1 = pygame.Rect(loading_bar_x, loading_bar_y, 600, loading_bar_height)
loading_duration = 5 * 10  
loading_start_time = 0
start =False
bp=True
bbl=0
xx=2
win = pygame.display.set_mode((1500,700))
but=pygame.image.load("assets/button.png").convert_alpha()
b1=pygame.transform.scale(but,(50,50))
b2=pygame.transform.flip(b1,True,False)
s=pygame.image.load("assets/1.png").convert_alpha()
s1=pygame.transform.scale(s,(1500,700))
ss=pygame.image.load("assets/2.png").convert_alpha()
s2=pygame.transform.scale(ss,(1500,700))
sss=pygame.image.load("assets/3.png").convert_alpha()
s3=pygame.transform.scale(sss,(1500,700))
ssss=pygame.image.load("assets/4.png").convert_alpha()
s4=pygame.transform.scale(ssss,(1500,700))
sssss=pygame.image.load("assets/5.png").convert_alpha()
s5=pygame.transform.scale(sssss,(1500,700))
ssssss=pygame.image.load("assets/6.png").convert_alpha()
s6=pygame.transform.scale(ssssss,(1500,700))
sssssss=pygame.image.load("assets/7.png").convert_alpha()
s7=pygame.transform.scale(sssssss,(1500,700))
ssssssss=pygame.image.load("assets/8.png").convert_alpha()
s8=pygame.transform.scale(ssssssss,(1500,700))
sssssssss=pygame.image.load("assets/9.png").convert_alpha()
s9=pygame.transform.scale(sssssssss,(1500,700))
ssssssssss=pygame.image.load("assets/10.png").convert_alpha()
s10=pygame.transform.scale(ssssssssss,(1500,700))
load=pygame.transform.scale(pygame.image.load("assets/loading.png"),(550,150))
t1=[s1,s2,s3,s4,s6,s7,s8,s9,s10]
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
arrow_width = 80
arrow_height = 40
once=True
ddl=0
pygame.display.set_caption("FACIAL RECOGNITION")
ti=pygame.image.load("assets/logo.jpeg")
pygame.display.set_icon(ti)
once1=False
kekw=False
pog=False
img1=None
clicked=False
show=False
def blurSurf(surface, amt):

    scale = 5.0/float(amt)

    surf_size = surface.get_size()

    scale_size = (float(surf_size[0]*scale), float(surf_size[1]*scale))

    surf = pygame.transform.smoothscale(surface, scale_size)

    surf = pygame.transform.smoothscale(surf, surf_size)

    return surf
def modify_image_pixel(wi,ht):
    width, height = wi, ht
    aspect_ratio = width / height
    if aspect_ratio>1:
        new_width = int(aspect_ratio * 400)
        new_pixel = (new_width, 400)
        return new_pixel
    else:    
        new_width = int(aspect_ratio * 500)
        new_pixel = (new_width, 500)
        return new_pixel

def draw(im,bp):
    
    win.fill((0,255,255))
    fontsss=pygame.font.SysFont('comicsans', 30,True)
    fonts = pygame.font.SysFont('Cyborg Punk', 33, True)
    if  bp :
        win.blit(t1[bbl],(0,0))
    if not bp:
        win.blit(blurSurf(t1[bbl],xx),(0,0))
    if not start and known_uploaded and unknown_uploaded and kekw:
        if not lulw:    
                button4.draw1()
        else:
              texterror1=fontsss.render("Uploaded Folder For Known Faces Does Not Contain Proper Format Of Files or pictures are ",1, (255,255,255))
              texterror2=fontsss.render("blurry in it Please Go Back and Reupload Files There is How to Upload Files on Top Left",1, (255,255,255))
              win.blit(texterror1,(100,200))
              win.blit(texterror2,(100,250))
              button6.draw1()  
    text1 = fonts.render("Face Detection Using Neural Network" , 1, (204, 255, 13))    
    win.blit(text1,(230,30))
    if rstart:
            button3.draw1()
    if (not start and not rstart and not kekw):
            if howto:
                    textinf1=fontsss.render("For Known Faces Upload the Folder Which Contains one or More Folder named by  ",1, (255,255,255))
                    textinf2=fontsss.render("the person name that has to be identified in Unkown Faces and all thos folder ",1, (255,255,255))
                    textinf3=fontsss.render("should contain multiple angles of one person only and For ",1, (255,255,255))
                    textinf4=fontsss.render("Unkown Faces Folder Upload the Folder which contains all the images in which ",1, (255,255,255))
                    textinf5=fontsss.render("Known Faces person is to be identified if its present in those pictures or not ",1, (255,255,255))

                    win.blit(textinf1,(100,150))
                    win.blit(textinf2,(100,200))
                    win.blit(textinf3,(100,250))
                    win.blit(textinf4,(100,300))
                    win.blit(textinf5,(100,350))
                    button6.draw1()
                    #button7.pressed=False
            elif takepic:
                    webcam.start()
                    im=webcam.get_image();
                    img=pygame.transform.scale(im,(500,400))
                    
                            
                            
                    if show:
                            
                            img1=pygame.transform.scale(pygame.image.load(noom),(500,400))
                            
                            if goingtoknown:
                                    textsavedknown=fontsss.render("Person's Name(This will be folder name)",1, (255,255,255))
                                    win.blit(textsavedknown,(900,520))
                                    pygame.draw.rect(win,color1,input_rect1,3)
                                    base_font = pygame.font.SysFont(None, 30, True)
                                    text_surface1=base_font.render(lc,True,(255, 255, 0))
                                    input_rect1.w=max(150,text_surface1.get_width()+10)
                                    screen.blit(text_surface1,(input_rect1.x+5,input_rect1.y+5))
                                    if suave and fade<100:
                                            textsaved=fontsss.render("Saved Successfully",1, (255,255,255))
                                            win.blit(textsaved,(1000,660))
                                    button14.draw1()
                                    button15.draw1()
                            else:    
                                        button11.draw1()
                                        button12.draw1()
                                        button13.draw1()
                            if goingtounknown:
                                if suave and fade<100:    
                                        textsavedunknown=fontsss.render("Saved Successfully",1, (255,0,105))
                                        win.blit(textsavedunknown,(1302,607))
                            
                            win.blit(img1,(950,100))
                    win.blit(img,(345,100))
                    
                    button6.draw1()
                    button10.draw1()
                    
                    
                    
                    
            else:
                    textinfo1=fontsss.render("Upload Known Faces And Unkown Faces Folder",1, (255,255,255))
                    win.blit(textinfo1,(400,250))
                    button1.draw1()
                    button2.draw1()
                    if known_uploaded and unknown_uploaded:
                            button5.draw1()
                    button7.draw1()
                    button9.draw1()
    if start and not bp and not lulw:
        button8.draw1()    
        if im.get_width()>399:
            win.blit(im,(478,160))
        else:
            win.blit(im,(558,110))
        
        button16.draw1()
        button17.draw1()
        #win.blit(b1,(690,610))
        #win.blit(b2,(750,610))
        
    #if (start or once1) and not lulw:    
        #font = pygame.font.SysFont('arial', 40, True)
        #text = font.render(d[l][1] , 1, (255,0,0))
    if bp and start and not lulw:
        # Perform actions when the button is pressed
        
        
        win.blit(load,(455,400))
        pygame.draw.rect(win, GREEN, loading_bar_rect)
        #pygame.draw.rect(win,  (192, 192, 192), loading_bar_rect1,3)
        fontss = pygame.font.SysFont('comicsans', 30, True)
        text3 = fontss.render("Loading",1,(210, 0, 50))
        win.blit(text3,(635,500))
          
            
    
    pygame.display.update()

known_uploaded=False
unknown_uploaded=False
button1 = Button('Known Faces',200,40,(300,350),5,'#475F77','#354B5E','#D74B4B')
button2 = Button('Unknown Faces',200,40,(1000,350),5,'#475F77','#354B5E','#D74B4B')
button3 = Button('Upload File',200,40,(650,350),5,'#475F77','#354B5E','#D74B4B')
button4 = Button('Start',200,40,(650, 550),5,'#f7ff0a','#cdf01d','#00FF00')
button5 = Button('Next',100,40,(675, 450),5,'#e100ff','#8f219e','#ed2b62')
button6 = Button('Go Back',200,40,(650, 550),5,'#e100ff','#8f219e','#ed2b62')
button7 = Button('How to upload',200,40,(1290, 90),5,'#e100ff','#8f219e','#ed2b62')
button8 = Button('Upload Again',200,40,(80, 150),5,'#e100ff','#8f219e','#ed2b62')
button9 = Button('Take Picture',200,40,(650, 350),5,'#e100ff','#8f219e','#ed2b62')
button10 = Button('Click',100,40,(545, 450),5,'#e100ff','#8f219e','#ed2b62')
button11 = Button('Known Faces',200,40,(967,557),5,'#475F77','#354B5E','#D74B4B')
button12 = Button('Unknown Faces',200,40,(1278,558),5,'#475F77','#354B5E','#D74B4B')
button13 = Button('Save To',100,40,(1170, 507),5,'#475F77','#354B5E','#D74B4B')
button14 = Button('save',100,40,(1176, 620),5,'#475F77','#354B5E','#D74B4B')
button15 = Button('<-',60,40,(960, 576),5,'#475F77','#354B5E','#D74B4B')
button16 = Button('<-',60,40,(690, 630),5,'#475F77','#354B5E','#D74B4B')
button17 = Button('->',60,40,(750, 630),5,'#475F77','#354B5E','#D74B4B')
rstart=True
lulw=False
howto=False
sade=False
bade=False
image1=None
takepic=False
goingtoknown=False
goingtounknown=False
input_rect1=pygame.Rect(1160, 572,150,32)
active1=False
suave=False
color_passive1=pygame.Color("green")
color_active1=pygame.Color("chocolate")
color1=color_passive1
lc=''
naam=0
fade=0
while (run):
        
        keys=pygame.key.get_pressed()
        
        
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                    break
                if event.type==pygame.MOUSEBUTTONDOWN:
                        print(event.pos)
                        if input_rect1.collidepoint(event.pos):
                                active1=True
                                color1=color_active1
                        else:
                                active1=False
                                color1=color_passive1
            
                if event.type==pygame.KEYDOWN:
                        if active1:
                
                                if event.key==pygame.K_BACKSPACE:
                                    lc=lc[:-1]
                                elif event.key==pygame.K_RETURN:
                                    active2=True
                                    active1=False
                                    color1=color_passive1
                                else:
                                    lc+=event.unicode
                
                if (keys[pygame.K_RIGHT] or button17.pressed) and (l<(len(d)-1)and start):
                    l+=1
                    button17.pressed=False
                if (keys[pygame.K_LEFT] or button16.pressed) and (l>0 and start):
                    l-=1
                    button16.pressed=False
                if (button7.pressed):
                        howto=True
                        button7.pressed=False
                if (button3.pressed):
                        rstart=False
                        button3.pressed=False
                if (button5.pressed and known_uploaded and unknown_uploaded):
                        kekw=True
                        
                        button5.pressed=False
                if button4.pressed:
                        if not lulw:
                                #rstart=True
                                start=True
                                kekw=False
                                bp=True
                                once=False
                                once1=True
                        button4.pressed=False       
                if (button1.pressed):
                        
                    path= askdirectory()
                    print(path)
                    if  path:
                            known_uploaded=True
                    button1.pressed=False
                if (button2.pressed):
                    path1= askdirectory()
                    print(path1)
                    if  path1:
                            unknown_uploaded=True
                    button2.pressed=False
                if (button6.pressed or button8.pressed):
                        start=False
                        rstart=False
                        kekw=False
                        try:
                                pa4 = os.path.join("./", "Tes") 
                                shutil.rmtree(pa4)
                        except:
                                print("hello")
                        button6.pressed=False
                        button8.pressed=False
                        howto=False
                        takepic=False
                        bade=False
                        known_faces = []
                        known_names = []
                        image1=None
                        l=0
                        i=0
                        d.clear()
                        show=False
                        goingtoknown=False
                        suave=False
                        webcam.stop()
                if (button9.pressed):
                        if not cameranotfound:
                                try:
                                        pat = os.path.join("./", "Known")
                                        pat1 = os.path.join("./", "Unknown")
                                        
                                        os.mkdir(pat)
                                        os.mkdir(pat1)
                                        
                                except:
                                        pass
                                try:
                                      pat2 = os.path.join("./", "Tes")
                                      os.mkdir(pat2)
                                except:
                                        pass
                                takepic=True
                                button9.pressed=False
                if button10.pressed:
                        im=webcam.get_image();
                        naam=str(naam)
                        pygame.image.save(im,"Tes/"+naam+".jpeg")
                        noom="Tes/"+naam+".jpeg"
                        nom=naam+".jpeg"
                        naam=int(naam)
                        naam+=1
                        clicked=True
                        show=True
                        button10.pressed=False
                if button11.pressed:
                        goingtoknown=True
                        button11.pressed=False
                if button12.pressed:
                        goingtounknown=True
                        #origin = noom
                        #target = '/Unknown'
                        source_path = os.path.join("Tes", nom)
                        target_path = os.path.join("Unknown", nom)
                        suave=True
                        shutil.copyfile(source_path, target_path)
                        button12.pressed=False
                if button14.pressed:
                        suave=True
                        try:
                                      pat3 = os.path.join("./Known", lc)
                                      os.mkdir(pat3)
                        except:
                                        pass
                        try:        
                                source_path = os.path.join("Tes", nom)
                                target_path = os.path.join("Known/"+lc, nom)
                                shutil.copyfile(source_path, target_path)
                        except:
                                pass
                if button15.pressed:
                        goingtoknown=False
                        button15.pressed=False
                #if event.type == pygame.MOUSEBUTTONDOWN and known_uploaded and unknown_uploaded:
            
                   # if button_rect.collidepoint(event.pos):
                    #    start = True
                     #   bp=True
                      #  once=False
                       # once1=True
                #if (keys[pygame.K_RETURN] and once) and known_uploaded and unknown_uploaded:
                 #     start = True
                  #    bp=True
                   #   once=False
                    #  once1=True
        
                                  
        
        if kekw:
                
                try:
                     for name in os.listdir(path):
                        for filename in os.listdir(f'{path}/{name}'):

                            
                                    image = face_recognition.load_image_file(f'{path}/{name}/{filename}')
                        if not sade:
                                lulw=False
                        kekw=True
                        start=False
                        
                        
                except:
                        lulw=True
                else:
                        
                 if not bade:       
                         sade=False
                         #lulw=False
                
        if start and once1 and not lulw:
                
           try:
            for name in os.listdir(path):

            
                        for filename in os.listdir(f'{path}/{name}'):

                    
                            image = face_recognition.load_image_file(f'{path}/{name}/{filename}')

                            
                            encoding = face_recognition.face_encodings(image)[0]

                            
                            known_faces.append(encoding)
                            known_names.append(name)
                            
                    
                  
            for filename in os.listdir(path1):
                
                
                print(f'Filename {filename}', end='')
                image = face_recognition.load_image_file(f'{path1}/{filename}')

                
                locations = face_recognition.face_locations(image, model=MODEL)

                
                encodings = face_recognition.face_encodings(image, locations)

                
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                
                print(f', found {len(encodings)} face(s)')
                for face_encoding, face_location in zip(encodings, locations):

                    
                    results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

                    
                    match = None
                    if True in results:  
                        match = known_names[results.index(True)]
                        print(f' - {match} from {results}')
                         
                        
                        top_left = (face_location[3], face_location[0])
                        bottom_right = (face_location[1], face_location[2])

                       
                        color = name_to_color(match)

                        
                        cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                        
                        top_left = (face_location[3], face_location[2])
                        bottom_right = (face_location[1], face_location[2] + 22)

                        
                        cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

                        # Write a name
                        cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX , 1, (200, 200, 200), FONT_THICKNESS)
                        st="Person Detected"
                    else:
                        st="Not Detected"
                img=cvimage_to_pygame(image)        
                w = img.get_width()
                h = img.get_height()
                d[i]=[image,st,w,h]
                i+=1
                once1=False
            lulw=False
            kekw=False
            start=True
            
           except:
                 image=None
                 locations=None
                 encodings=None
                 bade=True 
                 lulw=True
                 once1=True
                 kekw=True
                 #start=False
                 sade=True
                 #print("wha")
              
        if not once1 and start:
            image1=pygame.transform.scale(cvimage_to_pygame(d[l][0]),modify_image_pixel(d[l][2],d[l][3]))
        #else:
         #   image1=t1[0]
        if ddl<7:
            ddl+=1
        else:
            ddl=0
        if xx<20 and not bp:
            xx+=0.25
        if start and bbl<8 and bp and ddl==7 and not lulw:
            bbl+=1
        elif start and bp and ddl==7 and not lulw:
            bbl=0
        if start and loading_bar_rect.width<180 and not lulw:
            loading_bar_rect.width+=1
        elif start and loading_bar_rect.width>=180 and not lulw and not (loading_bar_rect.width == loading_bar_width):
            loading_bar_rect.width+=5    
        if (loading_bar_rect.width == loading_bar_width) and not lulw:
            bp=False
            loading_bar_rect.width=0
        draw(image1,bp)
        pygame.display.update()
        if suave:
                fade+=5
        if fade>100:
                fade=0
                suave=False
        clock.tick(50)
        
pygame.quit()
if not cameranotfound:  
        webcam.stop()

try:
        pa4 = os.path.join("./", "Tes") 
        shutil.rmtree(pa4)
except:
        print("hello")
