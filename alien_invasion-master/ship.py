# -*- coding: cp936 -*-
# ����һ���ɴ�����,p212

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self, ai_settings, screen):
        """��ʼ���ɴ����������ʼλ��"""
        super(Ship,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # ���طɴ�ͼ�񲢻�ȡ����Ӿ���,���ȼ���ͼ��
        # ��ȡ�������ͼ������ԣ�ͼ������Ļ�е����ԣ��ȷɴ�����Ļ�е�����
        # ����ʾ��Ļ�ľ��ε����Դ��ݸ�self.screen_sect�У�Ship����Ļ�е����Ծ�ȷ����
        self.image = pygame.image.load('images/ship.bmp') 
        self.rect = self.image.get_rect() 
        self.screen_rect = screen.get_rect() 
        
        # ��ÿ���·ɴ�������Ļ�ײ�����
        # �ɴ����ĵ�x���������Ϊ��ʾ��Ļ�ľ������Ե�centerx
        # �ɴ��±�Ե��y���������Ϊ��ʾ��Ļ�ľ������Ե�bottom
        self.rect.centerx = self.screen_rect.centerx 
        self.rect.bottom = self.screen_rect.bottom
        
        # �ڷɴ�������center�д洢������ֵ
        self.center = float(self.rect.centerx)
        
        # �ƶ���־
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """�����ƶ���־�����ɴ���λ��"""
        # ���·ɴ���centerֵ��������rect
        if self.moving_right and self.rect.right < self.screen_rect.right: # and��������������������������and�������ΪTrut,ͬʱ�ұ�С���ұ�Ե�Ż�ͬʱִ�У���Ҫ����and���߶�ҪС���ұ�Ե��
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # ����self.center����rect����
        self.rect.centerx = self.center
        
    def blitme(self):
        """��ָ��λ�û��Ʒɴ�������rect����ȷ����λ�ý��ɴ�ͼ���������Ļ��"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """�÷ɴ�����Ļ�о���"""
        self.center = self.screen_rect.centerx
