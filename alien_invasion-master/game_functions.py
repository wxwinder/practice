# -*- coding: cp936 -*-
# ������Ϸ�е����ö������ﶨ��

import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets): 
    #���������ƶ�����ʵ���ɴ���Ҫ��һ���βηɴ���ship�Ƿɴ���һ��ʵ��
    """��Ӧ����"""
    if event.key == pygame.K_RIGHT:
        # ����һֱ�ƶ��ɴ�
        ship.moving_right = True  # ship.moving_right��shipʵ���е�һ������
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q: # ������q������Ϸ
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """�����û�е������ƣ��ͷ���һ���ӵ�"""
    # ����һ���ӵ�����������뵽����bullets�У�
    # �����Ļ�ӵ��Ƿ�С�����õ��ӵ����������½�,��Ȼ���¿ո�û���κβ���
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    
def check_keyup_events(event, ship):
    """��Ӧ�ɿ�����"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
    bullets):
    """��Ӧ����������¼�"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
                
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # �β�mouse_x��mouse_y����������ȡ�����ԣ���Ϊcheck_play_button������ʵ��
            # ����check_events������Ҫʹ��mouse_x��mouse_y�������β����治��Ҫ
            check_play_button(ai_settings, screen, stats, sb, play_button, 
                ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
        aliens, bullets, mouse_x, mouse_y):
    """����ҵ���PLAY��ťʱ��ʼ��Ϸ"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # ������Ϸ����
        ai_settings.initialize_dynamic_settings()
        
        # ���ع��
        pygame.mouse.set_visible(False)
        
        # ������Ϸͳ����Ϣ
        stats.reset_stats()
        stats.game_active = True
        
        # ���üǷ���ͼ��
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # ����������б����ӵ��б�
        aliens.empty()
        bullets.empty()
        
        # ����һȺ�µ������ˣ����÷ɴ����еײ�
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """�����ӵ���λ�ã��Ƴ�����ʧ���ӵ�"""
    # �����ӵ���λ�ã����������д�����һ�����ڴ洢�ӵ��ı���bullets = Group()��
    # update()��bulletģ���е�һ������
    bullets.update() 
    
    # ɾ������ʧ���ӵ�
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # ����Ƿ����ӵ����������ˣ�����У���ɾ����Ӧ���ӵ���������
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
        aliens, bullets)
            
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
        aliens, bullets):
    # ��Ӧ�ӵ��������˵���ײ
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # ����һȺ�µ�������(�ô�����Ҳ���Է���update_aliens�����У���Ӧ�޸������򼴿ɣ�
    # ����������ÿ�ζ��Ǵ���ȫ��ѭ��һ�Σ����ڸ����ӵ����߸��������˷������涼����)
    if len(aliens) == 0:
        # ɾ�����е��ӵ����ӿ���Ϸ���࣬���½�һȺ������,�����һ���ȼ�
        bullets.empty()
        ai_settings.increase_speed()
        
        # ��ߵȼ�
        stats.level += 1
        sb.prep_level()
        
        # ����һȺ�µ�������
        create_fleet(ai_settings, screen, ship, aliens)
    
def check_fleet_edges(ai_settings, aliens):
    """�������˵�����Ļ��Եʱ��ȡ��Ӧ�Ĵ�ʩ"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """����Ⱥ���������ƣ����ı����ǵķ���"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1 

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """��Ӧ��������ײ���ķɴ�"""
    if stats.ships_left > 0:
        # ��ships_left��ȥ1
        stats.ships_left -= 1
        
        # ���¼Ƿ���
        sb.prep_ships()
        
        # ����������б����ӵ��б�
        aliens.empty()
        bullets.empty()
        
        # ����һȺ�µ������ˣ������ɴ��ŵ���Ļ�׶�����
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # ��ͣһ����Ϸʱ��,�����˺ͷɴ�������ɺ�����ͣһ�����Ȼ����ִ�и�����Ļ�ĳ���
        # ������Ļ����������ʾ���е������˺ͷɴ�����Ϸ�ٴο�ʼ
        sleep(2)
    
    else:
        aliens.empty()
        bullets.empty()
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """����Ƿ��������˵�����Ļ�ײ�"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # ��ɴ���������ײ��һ������
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # ֻҪ��⵽��һ���ɴ�����ײ����ͽ���ѭ��������break���
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """����Ƿ��������˴�����Ļ��Ե����������Ⱥ�����˵�λ��"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # ��������˺ͷɴ�֮�����ײ
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
    # ����Ƿ��������˵�����Ļ�׶�
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
          
def get_number_aliens_x(ai_settings, alien_width):
    """����ÿ�п������ɶ��ٸ�������"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """������Ļ�������ɶ�����������"""
    available_space_y = (ai_settings.screen_height - 
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """����һ�������˲�������ڵ�ǰ��"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x # x������Ҫת����rect�����ԣ���������������������˵ĺ���
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number # ѭ��ʱ��һ���к�Ϊ0���õ���һ��y��ߣ��������´�������
    aliens.add(alien) # aliens������һ���б������ڹ���������
    
def create_fleet(ai_settings, screen, ship, aliens):
    """����������Ⱥ"""
    # ����һ�������ˣ�������һ�п������ɶ��ٸ������ˣ������˼��Ϊ�����˵Ŀ���
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width) # ע�⣺�����ڸô�ֱ��дalien_width,�ô���alien.rect.width��һ����֪��ֵ����Ϊʵ�δ��ݸ�alien_width�β�
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
                                    alien.rect.height)
    
    # ����������Ⱥ����һ��ѭ��ʱ�к�Ϊ0������������0-5��������������ˣ�Ȼ��ڶ���ѭ���к�Ϊ1������������
    for row_number in range(number_rows): 
        for alien_number in range(number_aliens_x):
            # ����һ�������˲�������뵱ǰ��
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
    play_button):
    """������Ļ�ϵ�ͼ�񣬲��л�������Ļ"""
    # ÿ��ѭ��ʱ���ػ���Ļ
    screen.fill(ai_settings.bg_color)

    # �ڷɴ��������˺����ػ������ӵ�
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # ���Ʒɴ�
    ship.blitme()
    
    # ���������ˣ����Ʊ����е�ÿ�������ˣ����Ƶ�λ����Ԫ�ص�����rect����
    aliens.draw(screen) 
    
    # ��ʾ�÷�
    sb.show_score()
    
    # �����Ϸ���ڷǻ״̬���ͻ���һ��PLAY��ť,
    # Ϊ����PLAY��ť��ͼ�������棬���Ʒɴ��ӵ�֮����������ť
    # ��Ϸ������stats.game_active = False��˫�񶨾���True,��Ļ�Ͼͻ�һ��PLAY��ť
    if not stats.game_active:
        play_button.draw_button()

    # ��������Ƶ���Ļ�ɼ�
    pygame.display.flip()
    
def check_high_score(stats, sb):
    """����Ƿ������µ���ߵ÷�"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()