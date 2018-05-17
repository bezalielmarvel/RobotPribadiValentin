from PIL import Image
from PIL import ImageDraw
import math
import time


class DetecteBalise():
    def __init__(self, nom_image):
        self.image = Image.open(nom_image)
        self.image_visual = Image.open(nom_image)
        self.balise = True
        self.w_bal = 0
        self.h_bal = 0
        self.image.show()
        self.conv_rgby_pixels()
        self.image.show()
        self.detecter_rgby_zones()
        self.verif_balise()
        self.visual_balise()
#        self.show_param()


    def conv_rgby_pixels(self):
        w, h = self.image.size
        for y in range(h):
            for x in range(w):
                r,g,b = self.image.getpixel((x, y))
                # white
                self.image.putpixel((x, y),(255,255,255))
                # red
                if r - g > 70 and r - b > 70:
                    self.image.putpixel((x, y),(255,0,0))
                # blue
                if b - r > 35 and b - g > 35:
                    self.image.putpixel((x, y),(0,0,255))
                # yellow
                if r - b > 70 and g - b > 70:
                    self.image.putpixel((x, y),(255,255,0))
                # green
                if g - r > 10 and g - b > 10:
                    self.image.putpixel((x, y),(0,255,0))

    def detecter_rgby_zones(self):
        w, h = self.image.size
        w1, h1 = 72, 48
        pas = 10
        cmpt_r = 0
        w_r = 0
        h_r = 0
        cmpt_g = 0
        w_g = 0
        h_g = 0
        cmpt_b = 0
        w_b = 0
        h_b = 0
        cmpt_y = 0
        w_y = 0
        h_y = 0
        self.w_r_c = 0
        self.h_r_c = 0
        self.w_g_c = 0
        self.h_g_c = 0
        self.w_b_c = 0
        self.h_b_c = 0
        self.w_y_c = 0
        self.h_y_c = 0
        
        self.w_bal = round((self.w_r_c + self.w_g_c + self.w_b_c + self.w_y_c)/4)
        self.h_bal = round((self.h_r_c + self.h_g_c + self.h_b_c + self.h_y_c)/4)
        for y in range(0,h - h1,pas):
            for x in range(0,w - w1,pas):
                
                image_crop = self.image.crop((x,y,x+w1,y+h1))
                l_hist = image_crop.histogram()
                l_r = l_hist[0:256]
                l_g = l_hist[256:512]
                l_b = l_hist[512:768]
                # red
                if ( l_r[255]/(h1*w1) >= 0.9 and l_g[255]/(h1*w1) <= 0.1 and l_b[255]/(h1*w1) <= 0.1 ):
                    w_r += x+w1/2
                    h_r += y+h1/2
                    cmpt_r += 1
                # green
                if ( l_r[255]/(h1*w1) <= 0.1 and l_g[255]/(h1*w1) >= 0.9 and l_b[255]/(h1*w1) <= 0.1 ):
                    w_g += x+w1/2
                    h_g += y+h1/2
                    cmpt_g += 1
                # blue
                if ( l_r[255]/(h1*w1) <= 0.1 and l_g[255]/(h1*w1) <= 0.1 and l_b[255]/(h1*w1) >= 0.9 ):
                    w_b += x+w1/2
                    h_b += y+h1/2
                    cmpt_b += 1
                # yellow
                if ( l_r[255]/(h1*w1) >= 0.9 and l_g[255]/(h1*w1) >= 0.9 and l_b[255]/(h1*w1) <= 0.1 ):
                    w_y += x+w1/2
                    h_y += y+h1/2
                    cmpt_y += 1
    
    
        if cmpt_r != 0:
            self.w_r_c = round(w_r/cmpt_r)
            self.h_r_c = round(h_r/cmpt_r)
        if cmpt_g != 0:
            self.w_g_c = round(w_g/cmpt_g)
            self.h_g_c = round(h_g/cmpt_g)
        if cmpt_b != 0:
            self.w_b_c = round(w_b/cmpt_b)
            self.h_b_c = round(h_b/cmpt_b)
        if cmpt_y != 0:
            self.w_y_c = round(w_y/cmpt_y)
            self.h_y_c = round(h_y/cmpt_y)
        if cmpt_r != 0 and cmpt_g != 0 and cmpt_b != 0 and cmpt_y != 0:
            self.w_bal = round((self.w_r_c + self.w_g_c + self.w_b_c + self.w_y_c)/4)
            self.h_bal = round((self.h_r_c + self.h_g_c + self.h_b_c + self.h_y_c)/4)
        else:
            self.balise = False


    def verif_balise (self):
        
        if self.balise == False :
            return
        
        dist_y_r = math.sqrt(math.pow((self.w_r_c - self.w_r_c),2)+math.pow((self.h_y_c - self.h_r_c),2))
        dist_y_g = math.sqrt(math.pow((self.w_y_c - self.w_g_c),2)+math.pow((self.h_y_c - self.h_g_c),2))
        dist_g_b = math.sqrt(math.pow((self.w_g_c - self.w_b_c),2)+math.pow((self.h_g_c - self.h_b_c),2))
        dist_r_b = math.sqrt(math.pow((self.w_r_c - self.w_b_c),2)+math.pow((self.h_r_c - self.h_b_c),2))
        perim = dist_y_r + dist_y_g + dist_g_b + dist_r_b
    
        prop_yr = dist_y_r/(perim)
        prop_yg = dist_y_g/(perim)
        prop_gb = dist_g_b/(perim)
        prop_rb = dist_r_b/(perim)


        if ( prop_yr<0.10 or prop_yr > 0.30 ) :
            self.balise = False
#            print("distance entre Y et R non coherente")
#            print(prop_yr,perim,dist_y_r)

        if ( prop_gb<0.10 or prop_gb > 0.30 ):
#            print("distance entre G et B non coherente")
            self.balise = False
#            print(dist_g_b,perim,prop_gb)

        if ( prop_yg<0.19 or prop_yg > 0.39 ):
#            print("distance entre Y et G non coherente")
            self.balise = False
#            print(prop_yg,perim,dist_y_g)

        if ( prop_rb<0.19 or prop_rb > 0.39 ):
#            print("distance entre R et B non coherente")
            self.balise = False
#            print(dist_r_b,perim,prop_rb)


    def visual_balise(self):

        eX, eY = 10, 10
        cen_bal = (self.w_bal - eX/2, self.h_bal - eY/2, self.w_bal + eX/2, self.h_bal + eY/2)
        cen_r = (self.w_r_c - eX/2, self.h_r_c - eY/2, self.w_r_c + eX/2, self.h_r_c + eY/2)
        cen_g = (self.w_g_c - eX/2, self.h_g_c - eY/2, self.w_g_c + eX/2, self.h_g_c + eY/2)
        cen_b = (self.w_b_c - eX/2, self.h_b_c - eY/2, self.w_b_c + eX/2, self.h_b_c + eY/2)
        cen_y = (self.w_y_c - eX/2, self.h_y_c - eY/2, self.w_y_c + eX/2, self.h_y_c + eY/2)
        draw = ImageDraw.Draw(self.image_visual)
        draw.ellipse(cen_bal, fill=128)
        draw.ellipse(cen_r, fill=1)
        draw.ellipse(cen_g, fill=1)
        draw.ellipse(cen_b, fill=1)
        draw.ellipse(cen_y, fill=1)
        self.image_visual.show()
    
    
    def param_balise (self):
        if self.balise == False :
            return
        print("red:    (",self.w_r_c,",",self.h_r_c,")")
        print("green:  (",self.w_g_c,",",self.h_g_c,")")
        print("blue:   (",self.w_b_c,",",self.h_b_c,")")
        print("yellow: (",self.w_y_c,",",self.h_y_c,")")
        print("balise: (",self.w_bal,",",self.h_bal,")")
            
    def resultat_balise (self):
        if self.balise == False :
            return False
        else:
            return (self.w_bal,self.h_bal)

    def save_image_date (self):
        structTime = time.localtime()
        timestring = 'img_{}_{}_{}_{}_{}_{}'.format(structTime.tm_year, structTime.tm_mon,structTime.tm_mday,structTime.tm_hour,structTime.tm_min,structTime.tm_sec)
        self.image_visual.save('/Users/valentyngerushta/UPMC/2I013/robotPhys/saved/{}.png'.format(timestring))

if __name__=="__main__":
### test complexite ###
    start_time = time.time()
    DetecteBalise("../strategie/image1.png")
    print("--- %s seconds ---" % (time.time() - start_time))
### test image ###
    print(DetecteBalise("../strategie/image1.png").resultat_balise())
#    print(DetecteBalise("image2.png").resultat_balise())
#    print(DetecteBalise("image3.png").resultat_balise())
#    print(DetecteBalise("image4.png").resultat_balise())
#    print(DetecteBalise("image5.png").resultat_balise())
#    print(DetecteBalise("image6.png").resultat_balise())
