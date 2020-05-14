import math
from threading import Thread

from dpt.engine.gui.menu import Text
import dpt.engine.gui.menu as menu
import pygame
import tkinter as tk
import dpt.engine.gui.menu as Menu

from tkinter import simpledialog
from dpt.engine.fileManager import FileManager
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.gui.menu.simpleSprite import SimpleSprite
from dpt.engine.loader import UnreachableRessourceError
from dpt.engine.scenes import Scenes
from dpt.engine.tileManager import TileManager
from dpt.engine.loader import RessourceLoader
from dpt.game import Game
from dpt.engine.gui.menu import Timer
from dpt.engine.webCommunications import WebCommunication
from dpt.engine.effectsManagement import EffectsManagement

try:
    bg = RessourceLoader.get("dpt.images.environment.background.default_sky")
    bg = pygame.transform.smoothscale(bg, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
except:
    pass


def do_synch_anims():
    """Gère les annimations synchronisées"""
    # Lava
    if Game.anim_count_lava + 1 >= 208:
        Game.anim_count_lava = 0
    else:
        Game.anim_count_lava += 1

    # Water
    if Game.anim_count_water + 1 >= 104:
        Game.anim_count_water = 0
    else:
        Game.anim_count_water += 1

    # Coins
    if Game.anim_count_coins + 1 >= 144:
        Game.anim_count_coins = 0
    else:
        Game.anim_count_coins += 1


# Mainloops
def level_loop():
    """Boucle des niveaux"""
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            TileManager.editor_panel_group.empty()
            Checkbox.checkbox_group.empty()
            TileEditor.panel_open = False
            TileEditor.update()
            Scenes.pause()
        elif event.type == Game.PLAYER_DEATH_EVENT:
            if TileEditor.enabled_editor and not TileEditor.is_editing:
                TileEditor.is_editing = True
                for clouds in TileManager.clouds_group:
                    clouds.kill()

                Game.gui["editor_button"].text_sprite.kill()
                Game.gui["editor_button"].text_sprite = SimpleSprite(math.floor(143 * Game.DISPLAY_RATIO),
                                                                     math.floor(35 * Game.DISPLAY_RATIO),
                                                                     RessourceLoader.get("dpt.images.gui.symbols.TEXT_START"))

                TileEditor.panel_open = False
                Checkbox.checkbox_group.empty()
                TileManager.clouds_group.empty()
                TileManager.load_level(TileManager.levelName)
            return
        elif event.type == Game.BUTTON_EVENT and event.button == Game.gui["editor_button"]:
            TileEditor.is_editing = not TileEditor.is_editing
            if TileEditor.is_editing:
                Game.gui["editor_button"].text_sprite.kill()
                Game.gui["editor_button"].text_sprite = SimpleSprite(math.floor(143 * Game.DISPLAY_RATIO),
                                                                     math.floor(35 * Game.DISPLAY_RATIO),
                                                                     RessourceLoader.get("dpt.images.gui.symbols.TEXT_START"))
                for clouds in TileManager.clouds_group:
                    clouds.kill()
            else:
                Game.gui["editor_button"].text_sprite.kill()
                Game.gui["editor_button"].text_sprite = SimpleSprite(math.floor(148 * Game.DISPLAY_RATIO),
                                                                     math.floor(35 * Game.DISPLAY_RATIO),
                                                                     RessourceLoader.get("dpt.images.gui.symbols.TEXT_MENU"))
            TileEditor.panel_open = False
            Checkbox.checkbox_group.empty()
            TileManager.clouds_group.empty()
            TileManager.load_level(TileManager.levelName)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and TileEditor.is_editing:
                TileManager.scroll_up()
            elif event.button == 5 and TileEditor.is_editing:
                TileManager.scroll_down()
        elif event.type == Game.TIMER_FINISHED_EVENT:
            Scenes.game_over()

    do_synch_anims()
    TileManager.out_of_window()
    TileManager.camera.update(Game.player_sprite)
    TileEditor.update()

    try:
        TileManager.editor_panel_group.update()
        TileManager.editor_panel_group.draw(Game.surface)
    except pygame.error:
        Game.get_logger(__name__).critical("Error when drawing editorPanelGroup")
        Game.get_logger(__name__).critical("Content: ")
        for sp in TileManager.editor_panel_group:
            try:
                Game.get_logger(__name__).critical("    " + str(sp.block))
            except AttributeError:
                pass
        raise

    TileEditor.ghost_block_group.draw(Game.surface)

    if not TileEditor.is_editing:
        EffectsManagement.update()
        Button.main_loop()
        Timer.main_loop()
    else:
        if Game.gui["window"].rect.collidepoint(pygame.mouse.get_pos()):
            menu.Button.main_loop()
            menu.Checkbox.main_loop()
        else:
            Menu.main_loop()

    WebCommunication.update()

    if not TileEditor.is_editing:
        TileManager.heart_group.update()

    if TileEditor.enabled_editor:
        Game.draw_cursor()


def pause_loop():
    """Boucle de pause"""
    Game.surface.blit(bg, (0, 0))

    def kill_menu():
        for key, item in Game.gui.items():
            if key[:2] == "p_":
                item.kill()

    TileManager.camera.update(Game.player_sprite, True)

    menu.main_loop()

    for event in Game.events:
        if event.type == pygame.QUIT:
            if WebCommunication.sessionName is not None:
                WebCommunication.close()
            if TileEditor.is_editing:
                FileManager.save_file(TileEditor.created_level)
            Game.run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            kill_menu()

            def music():
                pygame.mixer.unpause()
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_volume(0)

                for i in range(0, 101):
                    pygame.time.wait(2)
                    pygame.mixer.music.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"] * (i / 100))

            Thread(target=music).start()
            Game.loop = Game.loop = level_loop
            return
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["p_button_resume"]:
                Game.loop = level_loop
                kill_menu()

                def music():
                    pygame.mixer.unpause()
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0)

                    for i in range(0, 101):
                        pygame.time.wait(10)
                        pygame.mixer.music.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"] * (i / 100))

                Thread(target=music).start()
                return
            elif event.button == Game.gui["p_button_restart_save"] and not TileEditor.enabled_editor:
                if "last_checkpoint" in Game.temp:
                    del Game.temp["last_checkpoint"]
                    del Game.temp["respawn"]
                    try:
                        RessourceLoader.get("dpt.entities.interactible.Coin").coin_checkpoint_list = []
                    except UnreachableRessourceError:
                        pass
                kill_menu()
                TileManager.load_level(TileManager.levelName)
                EffectsManagement.create_effects_image()
                EffectsManagement.reset()
                EffectsManagement.vote()
                Game.loop = level_loop
                return
            elif event.button == Game.gui["p_button_restart_save"] and TileEditor.enabled_editor:
                kill_menu()
                FileManager.save_file(TileEditor.created_level)
                Game.loop = level_loop
            elif event.button == Game.gui["p_button_main_menu"]:
                if WebCommunication.sessionName is not None:
                    WebCommunication.close()
                if TileEditor.is_editing:
                    FileManager.save_file(TileEditor.created_level)
                try:
                    RessourceLoader.get("dpt.entities.interactible.Coin").coin_checkpoint_list = []
                except UnreachableRessourceError:
                    pass
                Menu.delete_items()
                Scenes.main_menu()
                return
            elif event.button == Game.gui["p_button_quit"]:
                if WebCommunication.sessionName is not None:
                    WebCommunication.close()
                if TileEditor.is_editing:
                    FileManager.save_file(TileEditor.created_level)
                Game.run = False

    WebCommunication.update()
    Game.draw_cursor()


def main_menu_loop():
    """Boucle du menu principale"""
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["button_play"]:
                menu.delete_items()
                Scenes.level_selector()
                return
            elif event.button == Game.gui["button_editor"]:
                menu.delete_items()

                # Musiques et sons
                def music():
                    pygame.mixer.fadeout(1000)
                    pygame.mixer.music.fadeout(1000)

                Thread(target=music).start()

                Scenes.editor({
                    "tiles": {},
                    "infos": {}
                })
                return
            elif event.button == Game.gui["button_settings"]:
                menu.delete_items()
                Scenes.settings_menu()
                return
            elif event.button == Game.gui["button_quit"]:
                menu.delete_items()

                # Musiques et sons
                def music():
                    pygame.mixer.fadeout(1000)
                    pygame.mixer.music.fadeout(1000)

                Thread(target=music).start()
                Game.run = False
                return

    image = RessourceLoader.get("dpt.images.dpt")
    image = pygame.transform.smoothscale(image,
                                         (math.floor(1480 * Game.DISPLAY_RATIO), math.floor(600 * Game.DISPLAY_RATIO)))
    rect = image.get_rect()
    rect.centerx = Game.WINDOW_WIDTH // 2
    rect.bottom = (Game.WINDOW_HEIGHT // 4) * 3
    Game.surface.blit(image, rect)

    menu.main_loop()
    Game.draw_cursor()


def settings_menu_loop():
    """Boucle du menu des paramètres"""
    Game.surface.blit(bg, (0, 0))

    ds = Game.temp["display_size"]
    Game.gui["graphics_text"].text, w, h = Game.display_list[ds]

    menu.main_loop()

    def apply_settings():
        Game.settings["general_volume"] = Game.gui["general_volume_slider"].value
        Game.settings["music_volume"] = Game.gui["music_volume_slider"].value
        Game.settings["sound_volume"] = Game.gui["sound_volume_slider"].value

        Game.settings["display_size"] = ds

        if "s" in Game.temp and Game.gui["custom_server_button"]:
            Game.settings["server_address"] = Game.temp["s"]
        elif Game.gui["default_server_button"]:
            Game.settings["server_address"] = Game.DEFAULT_SERVER_ADDRESS
        pygame.mixer_music.set_volume(Game.settings["general_volume"] * Game.settings["music_volume"])

        if Game.temp["prev"]["display_size"] != Game.settings["display_size"]:
            Game.update_display()
            global bg
            bg = RessourceLoader.get("dpt.images.environment.background.default_sky")
            bg = pygame.transform.smoothscale(bg, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
            menu.delete_items()
            Game.save_profile()
            Game.temp = {}
            Scenes.settings_menu()

        Game.save_profile()

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            apply_settings()
            menu.delete_items()
            Game.temp = {}
            Scenes.main_menu(load=False)
            return
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["left_button"]:
                Game.temp["display_size"] -= 1
                Game.temp["display_size"] = max(Game.temp["display_size"], 0)
                Game.temp["display_size"] = min(Game.temp["display_size"], len(Game.display_list) - 1)
            if event.button == Game.gui["right_button"]:
                Game.temp["display_size"] += 1
                Game.temp["display_size"] = max(Game.temp["display_size"], 0)
                Game.temp["display_size"] = min(Game.temp["display_size"], len(Game.display_list) - 1)
            if event.button == Game.gui["apply_button"]:
                apply_settings()
            if event.button == Game.gui["cancel_button"]:
                pygame.mixer_music.set_volume(Game.settings["general_volume"] * Game.settings["music_volume"])
                menu.delete_items()
                Game.save_profile()
                Game.temp = {}
                Scenes.main_menu(load=False)
                return
            if event.button == Game.gui["return_button"]:
                apply_settings()
                menu.delete_items()
                Game.temp = {}
                Scenes.main_menu(load=False)
                return
            if event.button == Game.gui["custom_server_text_button"]:
                root = tk.Tk()
                root.withdraw()
                s = simpledialog.askstring("Adresse du serveur", "URL (sans le http(s)://)", parent=root, )
                if s is not None:
                    Game.temp["s"] = s

    rect1 = pygame.rect.Rect(0,
                             math.floor(600 * Game.DISPLAY_RATIO),
                             math.floor(175 * (Game.WINDOW_WIDTH / Game.WINDOW_HEIGHT) * Game.DISPLAY_RATIO),
                             math.floor(175 * Game.DISPLAY_RATIO))
    rect1.centerx = Game.gui["window_graphics"].rect.centerx

    if w == 0:
        w = Game.SCREEN_WIDTH
    if h == 0:
        h = Game.SCREEN_HEIGHT

    w_rect_t = math.floor((w / Game.SCREEN_WIDTH) * rect1.width)
    h_rect_t = math.floor((h / Game.SCREEN_HEIGHT) * rect1.height)

    w_rect = min(w_rect_t, rect1.width)
    h_rect = min(h_rect_t, rect1.height)

    rect1.width = math.floor((w_rect / w_rect_t) * rect1.width)
    rect1.height = math.floor((h_rect / h_rect_t) * rect1.height)

    rect2 = pygame.rect.Rect(rect1.x,
                             math.floor(600 * Game.DISPLAY_RATIO),
                             w_rect,
                             h_rect)

    pygame.draw.rect(Game.surface, (255, 255, 255, 2), rect1)
    pygame.draw.rect(Game.surface, (0, 0, 0), rect2, width=3)

    Game.draw_cursor()


def start_level_loop():
    """Boucle de début de niveau"""
    Game.surface.blit(bg, (0, 0))

    menu.main_loop()

    for event in Game.events:
        if event.type == pygame.QUIT:
            WebCommunication.close()
            Game.run = False
            return
        if event.type == Game.BUTTON_EVENT:
            menu.delete_items()
            if event.button == Game.gui["button_previous"]:
                WebCommunication.close()
                Scenes.level_selector_detail()
                return
            elif event.button == Game.gui["button_start"]:
                # Musiques et sons
                def music():
                    pygame.mixer.fadeout(1000)
                    pygame.mixer.music.fadeout(1000)

                Thread(target=music).start()
                Scenes.level(Game.temp["next_level"])
                return

    menu.main_loop()

    WebCommunication.update()
    Game.draw_cursor()


def loading_loop(kill=False):
    """Boucle de chargement. Boucle spécial car non executée dans game"""
    from dpt.engine.gui.menu import ProgressBar
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
            return

    if Game.temp["count"] >= 20:
        Game.temp["text"] += "."
        if Game.temp["text"] == "....":
            Game.temp["text"] = ""
        Game.temp["count"] = 0
    Game.temp["count"] += 1

    # Afficahe de la progressbar
    ProgressBar.bar_group.draw(Game.surface)
    ProgressBar.progress_bar_group.draw(Game.surface)

    # Affichage du text
    Game.temp["text_rendered"] = Game.temp["font"].render("Chargement" + Game.temp["text"], True, (0, 0, 0))
    Game.surface.blit(Game.temp["text_rendered"], Game.temp["rect"])

    Game.events = pygame.event.get()

    WebCommunication.update()

    Game.display_debug_info()
    Game.window.update()

    if kill:
        ProgressBar.bar_group.empty()
        ProgressBar.progress_bar_group.empty()


def game_over_loop():
    """Boucle de game over"""
    Game.surface.blit(bg, (0, 0))

    def kill_menu():
        for key, item in Game.gui.copy().items():
            if key[:3] == "go_":
                item.kill()

    TileManager.camera.update(Game.player_sprite, True)

    menu.main_loop()

    for event in Game.events:
        if event.type == pygame.QUIT:
            if WebCommunication.sessionName is not None:
                WebCommunication.close()
            if TileEditor.is_editing:
                FileManager.save_file(TileEditor.created_level)
            Game.run = False
            return
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["go_button_checkpoint"]:
                kill_menu()
                TileManager.load_level(TileManager.levelName)
                if "coins" in Game.temp:
                    Game.temp["coins"] = Game.temp["coins"] // 2
                if "respawn" in Game.temp:
                    Game.temp["respawn"] += 1
                else:
                    Game.temp["respawn"] = 1
                EffectsManagement.create_effects_image()
                EffectsManagement.reset()
                EffectsManagement.vote()
                Game.loop = level_loop
                return
            elif event.button == Game.gui["go_button_main_menu"]:
                if WebCommunication.sessionName is not None:
                    try:
                        del Game.temp["last_checkpoint"]
                        del Game.temp["respawn"]
                    except KeyError:
                        pass
                    WebCommunication.close()
                try:
                    RessourceLoader.get("dpt.entities.interactible.Coin").coin_checkpoint_list = []
                except UnreachableRessourceError:
                    pass
                menu.delete_items()
                Scenes.main_menu()
                return
            elif event.button == Game.gui["go_button_quit"]:
                if WebCommunication.sessionName is not None:
                    try:
                        del Game.temp["last_checkpoint"]
                        del Game.temp["respawn"]
                    except KeyError:
                        pass
                    WebCommunication.close()
                Game.run = False

    WebCommunication.update()
    Game.draw_cursor()


def end_level_loop():
    """Boucle de fin de niveau"""
    Game.surface.blit(bg, (0, 0))

    Game.gui["fade"].update()

    if not Game.gui["fade"].done:
        TileManager.camera.update(Game.player_sprite, True)
        Game.gui["fade"].draw(Game.surface)
    else:
        Game.gui["fade"].draw(Game.surface)
        menu.main_loop()

        for event in Game.events:
            if event.type == pygame.QUIT:
                if WebCommunication.sessionName is not None:
                    WebCommunication.close()
                if TileEditor.is_editing:
                    FileManager.save_file(TileEditor.created_level)
                Game.run = False
                return
            if event.type == Game.BUTTON_EVENT:
                if event.button == Game.gui["el_button_main_menu"]:
                    if WebCommunication.sessionName is not None:
                        try:
                            del Game.temp["last_checkpoint"]
                            del Game.temp["respawn"]
                            RessourceLoader.get("dpt.entities.interactible.Coin").coin_checkpoint_list = []
                        except KeyError:
                            pass
                        WebCommunication.close()
                    menu.delete_items()
                    Scenes.main_menu()
                    return
                elif event.button == Game.gui["el_button_name"]:
                    root = tk.Tk()
                    root.withdraw()
                    s = simpledialog.askstring("Nom", "Entrez un nom personnalisé pour le tableau des scores (Annuler pour utiliser la date)", parent=root, )
                    if s is not None:
                        try:
                            del Game.saves[TileManager.levelName][Game.temp["time"]]
                        except KeyError:
                            pass
                        Game.saves[TileManager.levelName].update({s: Game.temp["score"]})
                        Game.save_profile()
                    return
                elif event.button == Game.gui["el_button_quit"]:
                    if WebCommunication.sessionName is not None:
                        try:
                            del Game.temp["last_checkpoint"]
                            del Game.temp["respawn"]
                            RessourceLoader.get("dpt.entities.interactible.Coin").coin_checkpoint_list = []
                        except KeyError:
                            pass
                        WebCommunication.close()
                    Game.run = False

        if Game.temp["chrono"] == 30:
            button_height = math.floor(95 * Game.DISPLAY_RATIO)
            buttons_gap_y = math.floor(15 * Game.DISPLAY_RATIO)
            buttons_starting_y = math.floor((Game.WINDOW_HEIGHT / 2) - button_height * 2 - buttons_gap_y * 1.5) + math.floor(32 * Game.DISPLAY_RATIO)

            Game.gui["el_detail_title"] = Text(0,
                                               buttons_starting_y + math.floor(190 * Game.DISPLAY_RATIO),
                                               "Détails du score",
                                               math.floor(25 * Game.DISPLAY_RATIO),
                                               (0, 0, 0),
                                               "dpt.fonts.DINOT_CondBlack",
                                               centerx=Game.WINDOW_WIDTH // 2),

        elif Game.temp["chrono"] == 40:
            button_height = math.floor(95 * Game.DISPLAY_RATIO)
            buttons_gap_y = math.floor(15 * Game.DISPLAY_RATIO)
            buttons_starting_y = math.floor((Game.WINDOW_HEIGHT / 2) - button_height * 2 - buttons_gap_y * 1.5) + math.floor(32 * Game.DISPLAY_RATIO)

            nb = 0
            if "respawn" in Game.temp:
                nb = Game.temp["respawn"] * 500

            Game.gui["el_detail_respawn_title"] = Text(Game.WINDOW_WIDTH // 2 - math.floor(100 * Game.DISPLAY_RATIO),
                                                       buttons_starting_y + math.floor(220 * Game.DISPLAY_RATIO),
                                                       "Réapparition(s)",
                                                       math.floor(20 * Game.DISPLAY_RATIO),
                                                       (0, 0, 0),
                                                       "dpt.fonts.DINOT_CondBlack"),
            Game.gui["el_detail_respawn_score"] = Text(Game.WINDOW_WIDTH // 2 + math.floor(50 * Game.DISPLAY_RATIO),
                                                       buttons_starting_y + math.floor(220 * Game.DISPLAY_RATIO),
                                                       "- " + str(nb),
                                                       math.floor(20 * Game.DISPLAY_RATIO),
                                                       (193, 39, 45),
                                                       "dpt.fonts.DINOT_CondBlack"),

        elif Game.temp["chrono"] == 50 and "coins" in Game.temp:
            button_height = math.floor(95 * Game.DISPLAY_RATIO)
            buttons_gap_y = math.floor(15 * Game.DISPLAY_RATIO)
            buttons_starting_y = math.floor((Game.WINDOW_HEIGHT / 2) - button_height * 2 - buttons_gap_y * 1.5) + math.floor(32 * Game.DISPLAY_RATIO)

            Game.gui["el_detail_coins_title"] = Text(Game.WINDOW_WIDTH // 2 - math.floor(100 * Game.DISPLAY_RATIO),
                                                     buttons_starting_y + math.floor(240 * Game.DISPLAY_RATIO),
                                                     "Pièces collectées",
                                                     math.floor(20 * Game.DISPLAY_RATIO),
                                                     (0, 0, 0),
                                                     "dpt.fonts.DINOT_CondBlack"),
            Game.gui["el_detail_coins_score"] = Text(Game.WINDOW_WIDTH // 2 + math.floor(50 * Game.DISPLAY_RATIO),
                                                     buttons_starting_y + math.floor(240 * Game.DISPLAY_RATIO),
                                                     "+ " + str(Game.temp["coins"] * 50),
                                                     math.floor(20 * Game.DISPLAY_RATIO),
                                                     (39, 193, 45),
                                                     "dpt.fonts.DINOT_CondBlack"),

        elif Game.temp["chrono"] == 60:
            button_height = math.floor(95 * Game.DISPLAY_RATIO)
            buttons_gap_y = math.floor(15 * Game.DISPLAY_RATIO)
            buttons_starting_y = math.floor((Game.WINDOW_HEIGHT / 2) - button_height * 2 - buttons_gap_y * 1.5) + math.floor(32 * Game.DISPLAY_RATIO)

            Game.gui["el_detail_coins_title"] = Text(Game.WINDOW_WIDTH // 2 - math.floor(100 * Game.DISPLAY_RATIO),
                                                     buttons_starting_y + math.floor(260 * Game.DISPLAY_RATIO),
                                                     "Bonus de temps",
                                                     math.floor(20 * Game.DISPLAY_RATIO),
                                                     (0, 0, 0),
                                                     "dpt.fonts.DINOT_CondBlack"),
            Game.gui["el_detail_coins_score"] = Text(Game.WINDOW_WIDTH // 2 + math.floor(50 * Game.DISPLAY_RATIO),
                                                     buttons_starting_y + math.floor(260 * Game.DISPLAY_RATIO),
                                                     "+ " + str(Timer.time * 10),
                                                     math.floor(20 * Game.DISPLAY_RATIO),
                                                     (39, 193, 45),
                                                     "dpt.fonts.DINOT_CondBlack"),

        if not pygame.mixer_music.get_busy():
            if Game.temp["score_sound"]:
                Game.temp["score_sound"] = False
                sound = RessourceLoader.get("dpt.sounds.sfx.sfx_score_count")
                sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                sound.play(-1)

            if Game.temp["score_display"] < Game.temp["score"]:
                Game.temp["score_display"] += Game.temp["score"] // (3 * 60)
                if not Game.temp["1_done"]:
                    Game.gui["star_1"].run = Game.temp["score_display"] >= 1000
                    Game.temp["1_done"] = Game.temp["score_display"] >= 1000
                if not Game.temp["2_done"]:
                    Game.gui["star_2"].run = Game.temp["score_display"] >= 2000
                    Game.temp["2_done"] = Game.temp["score_display"] >= 2000
                if not Game.temp["3_done"]:
                    Game.gui["star_3"].run = Game.temp["score_display"] >= 3000
                    Game.temp["3_done"] = Game.temp["score_display"] >= 3000
                Game.gui["el_title_score"].text = str(Game.temp["score_display"])
            else:
                pygame.mixer.stop()
                Game.gui["el_title_score"].text = str(Game.temp["score"])
                Game.temp["chrono"] += 1

        if Game.temp["1_done"] and not Game.temp["2_done"] and not Game.temp["3_done"]:
            Game.gui["star_3"].update()
            Game.gui["star_2"].update()
            Game.gui["star_1"].update()
        elif Game.temp["2_done"] and Game.temp["1_done"] and not Game.temp["3_done"]:
            Game.gui["star_1"].update()
            Game.gui["star_3"].update()
            Game.gui["star_2"].update()
        elif Game.temp["2_done"] and Game.temp["1_done"] and Game.temp["3_done"]:
            Game.gui["star_1"].update()
            Game.gui["star_2"].update()
            Game.gui["star_3"].update()
        elif not Game.temp["1_done"] and not Game.temp["2_done"] and not Game.temp["3_done"]:
            Game.gui["star_3"].update()
            Game.gui["star_2"].update()
            Game.gui["star_1"].update()

    Game.draw_cursor()


def level_selector_loop():
    """Boucle de selection des niveaux"""
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["button_previous"]:
                menu.delete_items()
                Scenes.main_menu(False)
                return

    menu.main_loop()
    Game.draw_cursor()


def level_selector_detail_loop():
    """Boucle de details de selection des niveaux"""
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["button_start"]:
                menu.delete_items()

                # Initialisation de la session
                from dpt.engine.webCommunications import WebCommunication
                from dpt.engine.webCommunications import CommunicationError

                reply = WebCommunication.init_connection()

                if isinstance(reply, CommunicationError):
                    Scenes.return_error(str(reply),
                                        " ",
                                        "Si le problème persiste, vous pouvez nous contacter sur Discord",
                                        "Dwight Studio Hub: discord.gg/yZwuNqN",
                                        "(Lien copié dans le presse-papier)")

                    from tkinter import Tk
                    root = Tk()
                    root.withdraw()
                    root.clipboard_clear()
                    root.clipboard_append("https://discord.gg/yZwuNqN")
                    root.update()
                    root.destroy()
                    return

                Scenes.start_level()
                return
            elif event.button == Game.gui["button_main_menu"]:
                menu.delete_items()
                Scenes.level_selector()
                return

    menu.main_loop()
    Game.draw_cursor()
