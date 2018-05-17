from PIL import Image
from PIL import ImageDraw
import math
import time

class DetecteBalise():
    """
        permet de detecter si image contient une balise jaune(hg), vert(hd), rouge(bg), bleu(bd)
        ( h: en haut / b: en bas / g: à gauche / d: à droite )
        si balise est detecte: donne des coordonnees(en pixels) du centre de la balise et de centres carres j, v, r, b
    """
        
    def __init__(self, image):
        self.start_time = time.time()
        self.image = image
#        self.image_visual = image   #rq:baisse l'efficacite!
        self.balise = True
        self.w_bal = 0
        self.h_bal = 0
        self.quantize_image()
        self.detecter_rgby_zones()
        self.verif_balise()
#        self.visual_balise()    #rq: baisse l'efficacite!

    #quantization d'une image
    def quantize_image(self):
        self.image = self.image.quantize(colors=256, method=2, kmeans=0, palette=None)
        self.image = self.image.convert("RGB")

## calculer les centres des carres jaune, vert, rouge, blue et de la balise
    def detecter_rgby_zones(self):
    
        #larg et haut de l'image
        w, h = self.image.size
        #larg et haut du carre qui parcourt l'image
        w1, h1 = 36, 24
        #pas vertic et horiz de parcours
        pas_w, pas_h  = 27, 18
        #nb de pixels dans le carre
        nb_pix = w1*h1
        #param pour calculer des centres de carres j,v,r,b
        cmpt_r, w_r, h_r = 0,0,0
        cmpt_g, w_g, h_g = 0,0,0
        cmpt_b, w_b, h_b = 0,0,0
        cmpt_y, w_y, h_y = 0,0,0
        #coordonees des centres de carres j,v,r,b (en pixels)
        self.w_r_c, self.h_r_c = 0,0
        self.w_g_c, self.h_g_c = 0,0
        self.w_b_c, self.h_b_c = 0,0
        #coordonees de la balise (en pixels)
        self.w_y_c, self.h_y_c = 0,0
        
        #parcours d'une image avec carre w1xh1
        for y in range(0,h - h1,pas_h):
            for x in range(0,w - w1,pas_w):
                image_crop = self.image.crop((x,y,x+w1,y+h1))
                #liste des couleurs et leurs quantite dans le petit carre
                liste_couleurs = image_crop.getcolors()
                
                somme_rouge = 0
                somme_vert = 0
                somme_bleu = 0
                somme_jaune = 0

                #calcule la nb de pixels r, v, b, j
                for i in liste_couleurs:
                    #rouge
                    if i[1][0] - i[1][1] > 70 and i[1][0] - i[1][2] > 70:
                        somme_rouge += i[0]
                    #vert
                    if i[1][1] - i[1][0] > 10 and i[1][1] - i[1][2] > 10:
                        somme_vert += i[0]
                    #bleu
                    if i[1][2] - i[1][0] > 35 and i[1][2] - i[1][1] > 35:
                        somme_bleu += i[0]
                    #jaune
                    if i[1][0] - i[1][2] > 70 and i[1][1] - i[1][2] > 70:
                        somme_jaune += i[0]
               
               #proportions des couleurs r, g, v, j dans le carre
                prop_rouge = somme_rouge/nb_pix
                prop_vert = somme_vert/nb_pix
                prop_blue = somme_bleu/nb_pix
                prop_jaune = somme_jaune/nb_pix
                
                #calcule la moyenne de coordonnees des carres du certain couleur
                #rouge
                if ( prop_rouge >= 0.90 ):
                    w_r += x+w1/2
                    h_r += y+h1/2
                    cmpt_r += 1
                #vert
                if ( prop_vert >= 0.60 ):
                    w_g += x+w1/2
                    h_g += y+h1/2
                    cmpt_g += 1
                #bleu
                if ( prop_blue >= 0.60 ):
                    w_b += x+w1/2
                    h_b += y+h1/2
                    cmpt_b += 1
                #jaune
                if ( prop_jaune >= 0.90 ):
                    w_y += x+w1/2
                    h_y += y+h1/2
                    cmpt_y += 1
        
        #coordonnees finales / si un des carres n'est pas detecter => balise non-detecte
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
        #balise non detecte
        else:
            self.balise = False

## verifie si les coordonees sont coherentes
    def verif_balise (self):
        
        if self.balise == False :
            return
        
        #calcule les distances entre des centre de carres
        dist_y_r = math.sqrt(math.pow((self.w_r_c - self.w_r_c),2)+math.pow((self.h_y_c - self.h_r_c),2))
        dist_y_g = math.sqrt(math.pow((self.w_y_c - self.w_g_c),2)+math.pow((self.h_y_c - self.h_g_c),2))
        dist_g_b = math.sqrt(math.pow((self.w_g_c - self.w_b_c),2)+math.pow((self.h_g_c - self.h_b_c),2))
        dist_r_b = math.sqrt(math.pow((self.w_r_c - self.w_b_c),2)+math.pow((self.h_r_c - self.h_b_c),2))

        perim = dist_y_r + dist_y_g + dist_g_b + dist_r_b
    
        prop_yr = dist_y_r/(perim)
        prop_yg = dist_y_g/(perim)
        prop_gb = dist_g_b/(perim)
        prop_rb = dist_r_b/(perim)

        #si distance n'est pas coherente alors => balise non-detecte
        if ( prop_yr<0.10 or prop_yr > 0.30 ) :
            self.balise = False
#            print("distance entre Y et R non coherente")
#            print(prop_yr,perim,dist_y_r)

        if ( prop_gb<0.10 or prop_gb > 0.30 ):
            self.balise = False
#            print("distance entre G et B non coherente")
#            print(dist_g_b,perim,prop_gb)

        if ( prop_yg<0.19 or prop_yg > 0.39 ):
            self.balise = False
#            print("distance entre Y et G non coherente")
#            print(prop_yg,perim,dist_y_g)

        if ( prop_rb<0.19 or prop_rb > 0.39 ):
            self.balise = False
#            print("distance entre R et B non coherente")
#            print(dist_r_b,perim,prop_rb)

    # marquer sur l'image la position de la balise et afficher
    def visual_balise(self):
        eX, eY = 10, 10
        cen_bal = (self.w_bal - eX/2, self.h_bal - eY/2, self.w_bal + eX/2, self.h_bal + eY/2)
        cen_r = (self.w_r_c - eX/2, self.h_r_c - eY/2, self.w_r_c + eX/2, self.h_r_c + eY/2)
        cen_g = (self.w_g_c - eX/2, self.h_g_c - eY/2, self.w_g_c + eX/2, self.h_g_c + eY/2)
        cen_b = (self.w_b_c - eX/2, self.h_b_c - eY/2, self.w_b_c + eX/2, self.h_b_c + eY/2)
        cen_y = (self.w_y_c - eX/2, self.h_y_c - eY/2, self.w_y_c + eX/2, self.h_y_c + eY/2)
        draw = ImageDraw.Draw(self.image_visual)
        draw.ellipse(cen_bal, fill=(230,230,230))
        draw.ellipse(cen_r, fill=(230,0,0))
        draw.ellipse(cen_g, fill=(0,230,0))
        draw.ellipse(cen_b, fill=(0,0,230))
        draw.ellipse(cen_y, fill=(230,230,0))
        self.image_visual.show()

    def param_balise (self):
        if self.balise == False :
            return
        print("red:    (",self.w_r_c,",",self.h_r_c,")")
        print("green:  (",self.w_g_c,",",self.h_g_c,")")
        print("blue:   (",self.w_b_c,",",self.h_b_c,")")
        print("yellow: (",self.w_y_c,",",self.h_y_c,")")
        print("balise: (",self.w_bal,",",self.h_bal,")")
    
    #coordonnes de la balise
    def resultat_balise (self):
        if self.balise == False :
            return False
        else:
            return (self.w_bal,self.h_bal)
    #test efficacite(temps)
    def test_vitesse(self):
        if self.balise == False :
            print("--- %s seconds ---" % (time.time() - self.start_time))
            return False
        else:
            print("--- %s seconds ---" % (time.time() - self.start_time))
            return (self.w_bal,self.h_bal)


    def save_image_date (self):
        structTime = time.localtime()
        timestring = 'img_{}_{}_{}_{}_{}_{}'.format(structTime.tm_year, structTime.tm_mon,structTime.tm_mday,structTime.tm_hour,structTime.tm_min,structTime.tm_sec)
        self.image_visual.save('/Users/valentyngerushta/UPMC/2I013/robotPhys/saved/{}.png'.format(timestring))

    #l'ange sur lequel il faut tourner le robot
    def angle_balise (self):
        if self.balise == False :
            return False
        else:
            # focal length
            f = 633
            # distance en m d'une zone du papier(balise)
            w = 0.09
            #nombre de pixels entre centres des carres
            p = ((self.w_g_c - self.w_y_c)+(self.w_b_c - self.w_r_c))/2
            # distance entre camera et balise
            d = (w*f)/p
            w_c = self.image.size[0]/2
            # angle
            angle_rad = math.atan(w/d)
            angle_deg = (180/math.pi)*angle_rad
            # angle et sens
            if (self.w_bal<w_c):
                return round(-angle_deg,1)
            else:
                return round(angle_deg,1)


if __name__=="__main__":
  ## test temps ###
   image = Image.open("image1.png")
   print(DetecteBalise(image).test_vitesse())
   image = Image.open("image2.png")
   print(DetecteBalise(image).test_vitesse())
   image = Image.open("image3.png")
   print(DetecteBalise(image).test_vitesse())
   image = Image.open("image4.png")
   print(DetecteBalise(image).test_vitesse())
   image = Image.open("image5.png")
   print(DetecteBalise(image).test_vitesse())
   image = Image.open("image6.png")
   print(DetecteBalise(image).test_vitesse())


  ## test coordonees de balise ###
   image = Image.open("image1.png")
   print(DetecteBalise(image).resultat_balise())
   image = Image.open("image2.png")
   print(DetecteBalise(image).resultat_balise())
   image = Image.open("image3.png")
   print(DetecteBalise(image).resultat_balise())
   image = Image.open("image4.png")
   print(DetecteBalise(image).resultat_balise())
   image = Image.open("image5.png")
   print(DetecteBalise(image).resultat_balise())
   image = Image.open("image6.png")
   print(DetecteBalise(image).resultat_balise())

  ## test angle a tourner ###
   image = Image.open("image1.png")
   print(DetecteBalise(image).angle_balise())
   image = Image.open("image2.png")
   print(DetecteBalise(image).angle_balise())
   image = Image.open("image3.png")
   print(DetecteBalise(image).angle_balise())
   image = Image.open("image4.png")
   print(DetecteBalise(image).angle_balise())
   image = Image.open("image5.png")
   print(DetecteBalise(image).angle_balise())
   image = Image.open("image6.png")
   print(DetecteBalise(image).angle_balise())

