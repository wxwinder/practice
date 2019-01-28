# -*- coding: cp936 -*-
# ����һ���յ�Pygame����

import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
from pygame.sprite import Group

def run_game():
    
    # ��ʼ����Ϸ,���ú���Ļ����
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
    (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # ����һ��Play��ť��������Ϸ��ʼǰ������������ǰ��
    play_button = Button(ai_settings, screen, "PLAY")
    
    # ����һ�ҷɴ���ʵ��,ship������Ļ�ϴ�����һ�ҷɴ���
    # ship��һ��ʵ�������ƣ���ship��ģ��ship�������޹�
    ship = Ship(ai_settings, screen)
    
    # ����һ�����ڴ洢�ӵ��ı��飬Group�࣬�������б��������ÿһ���ӵ������ں��ڵĹ���
    bullets = Group()
    
    # ����һ�������˱���,�������ÿһ��������
    aliens = Group()
    
    # ����������Ⱥ
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # ����һ�����ڴ洢��Ϸͳ����Ϣ��ʵ��,�������Ʒ���
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # ��ʼ��Ϸ����ѭ��
    while True:
        
        # �����ҵ����룬���Ӽ��̺�����¼�
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
            aliens, bullets)
        
        # ��Ϸ���ڻ״̬ʱ��ִ�����³��򣬷ɴ����꣬��Ϸ��ֹͣ������
        if stats.game_active:
            
            # ���·ɴ���λ��
            ship.update() #����shipʵ���еķ���update,ship��һ��ʵ����������shipģ��
            
            # ��������δ��ʧ�ӵ���λ��
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, 
                bullets)
            
            # ���������˵�λ��
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
        
        # ʹ�ø��º�ķɴ����ӵ�λ�����»�����Ļ��������Ļ�ϵ�ͼ�񣬲��л�������Ļ
        # ������ĻҪ����ѭ��������������еĴ���ִ��һ�飬Ϊ������Ļ�ṩ�����е���Ϣ
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
            bullets, play_button)

        
run_game()
