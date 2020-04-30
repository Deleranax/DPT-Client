import math
import pygame

from dpt.game import Game


class Scenes:
    logger = Game.get_logger("Scenes")

    @classmethod
    def editor(cls, level):
        """Met en place les élèments d'éditeur

        :param level: Niveau à charger

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        cls.logger.info("Displaying EDITOR")
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor

        # Nettoyage
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.progressbar import ProgressBar
        from dpt.engine.gui.menu.checkbox import Checkbox
        Button.buttonsGroup.empty()
        Button.text_sprite_buttonsGroup.empty()
        ProgressBar.progress_bar_group.empty()
        ProgressBar.bar_group.empty()
        Checkbox.checkbox_group.empty()

        # Gestion des ressources
        RessourceLoader.add_pending("dpt.images.gui.buttons.BTN_GREEN_RECT_*")
        RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
        RessourceLoader.add_pending("dpt.images.gui.buttons.btn_checkbox_out")
        RessourceLoader.add_pending("dpt.images.gui.buttons.btn_checkbox_in")

        # Initialisation du TileManager
        TileEditor.in_editor = True
        if not TileManager.load_level(level):
            return False

        # Ajout du bouton d'éditeur
        from dpt.engine.gui.menu import Text
        Game.gui = {"editor_button": Button(0, Game.surface.get_size()[1] - math.floor(50 * Game.DISPLAY_RATIO),
                                            math.floor(127 * Game.DISPLAY_RATIO),
                                            math.floor(46 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_RECT_OUT"),
                                            pushed_image=RessourceLoader.get(
                                                "dpt.images.gui.buttons.BTN_GREEN_RECT_IN"), text="Jouer"),
                    "players_text": Text(Game.surface.get_size()[0] - math.floor(Game.DISPLAY_RATIO * 220),
                                         0,
                                         "Joueurs connectés : 000",
                                         math.floor(25 * Game.DISPLAY_RATIO),
                                         (0, 0, 0),
                                         "dpt.fonts.DINOT_CondBlack")}

        Game.temp["player_count_check"] = 0

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def level(cls, level):
        """Met en place les élèments de niveau

        :param level: Niveau à charger

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        cls.logger.info("Displaying LEVEL")
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor
        from dpt.engine.effectsManagement import effectsManagement

        # Initialisation du TileManager
        TileEditor.in_editor = False
        if not TileManager.load_level(level):
            return False

        # Initialisation de la gestion des effets
        Game.effects_management = effectsManagement()
        Game.count = 0

        from dpt.engine.gui.menu import Text
        Game.gui = {"players_text": Text(Game.surface.get_size()[0] - math.floor(Game.DISPLAY_RATIO * 220),
                                         0,
                                         "Joueurs connectés : 000",
                                         math.floor(25 * Game.DISPLAY_RATIO),
                                         (0, 0, 0),
                                         "dpt.fonts.DINOT_CondBlack")}

        Game.temp["player_count_check"] = 0

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def pause(cls):
        """Met en place les élèments du menu pause

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        from dpt.engine.loader import RessourceLoader
        cls.logger.info("Displaying PAUSE")

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)

        buttons_gap_y = math.floor(15 * Game.DISPLAY_RATIO)
        buttons_starting_y = math.floor((Game.surface.get_size()[1] / 2) - button_height * 2 - buttons_gap_y * 1.5) + math.floor(32 * Game.DISPLAY_RATIO)
        buttons_x = (Game.surface.get_size()[0] // 2) - (button_width // 2)

        Game.gui = {"window": Window(0, 0, 3, 9, centerx=Game.surface.get_size()[0] // 2, centery=Game.surface.get_size()[1] // 2),
                    "title": Text(0,
                                  buttons_starting_y - math.floor(90 * Game.DISPLAY_RATIO),
                                  "Pause",
                                  math.floor(50 * Game.DISPLAY_RATIO),
                                  (0, 0, 0),
                                  "dpt.fonts.DINOT_CondBlack",
                                  centerx=Game.surface.get_size()[0] // 2),
                    "button_resume": Button(buttons_x, buttons_starting_y, button_width, button_height,
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                         math.floor(50 * Game.DISPLAY_RATIO),
                                                                         RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_restart": Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height), button_width, button_height,
                                             RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_OUT"),
                                             pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_IN"),
                                             text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                          math.floor(40 * Game.DISPLAY_RATIO),
                                                                          RessourceLoader.get("dpt.images.gui.symbols.SYMB_REPLAY"))),
                    "button_main_menu": Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height) * 2, button_width, button_height,
                                               RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                               pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                               text_sprite=TextSpriteButton(math.floor(50 * Game.DISPLAY_RATIO),
                                                                            math.floor(38 * Game.DISPLAY_RATIO),
                                                                            RessourceLoader.get("dpt.images.gui.symbols.SYMB_MENU"))),
                    "button_quit": Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height) * 3,
                                          button_width,
                                          button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                       math.floor(50 * Game.DISPLAY_RATIO),
                                                                       RessourceLoader.get("dpt.images.gui.symbols.SYMB_X")))}

        # Loops
        Game.temp["prev_loop"] = Game.loop

        from dpt.engine.mainLoop import pause_loop
        Game.loop = pause_loop
        return True

    @classmethod
    def main_menu(cls, load=True):
        """Met en place les élèments du menu principale

        :param load: (Re)Charge les ressources
        :type load: bool

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        cls.logger.info("Displaying MAIN_MENU")
        from dpt.engine.loader import RessourceLoader

        # Gestion des ressources
        if load:
            RessourceLoader.unload()
            RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
            RessourceLoader.add_pending("dpt.images.gui.*")
            RessourceLoader.add_pending("dpt.images.dpt")
            RessourceLoader.add_pending("dpt.fonts.*")
            RessourceLoader.add_pending("dpt.sounds.musics.story_time")
            RessourceLoader.add_pending("dpt.sounds.sfx.switch6")
            RessourceLoader.load()

        # Gestion de la musique
        if load:
            pygame.mixer_music.load(RessourceLoader.get("dpt.sounds.musics.story_time"))
            pygame.mixer_music.play(-1)

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
        from dpt.engine.gui.menu import Window
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)
        buttons_gap_x = math.floor(80 * Game.DISPLAY_RATIO)
        buttons_starting_x = math.floor((Game.surface.get_size()[0] / 2) - button_width * 2 - buttons_gap_x * 1.5)
        buttons_y = (Game.surface.get_size()[1] // 4) * 3 + 50 * Game.DISPLAY_RATIO
        Game.gui = {"button_play": Button(buttons_starting_x, buttons_y, button_width, button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                       math.floor(50 * Game.DISPLAY_RATIO),
                                                                       RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_editor": Button(buttons_starting_x + (button_width + buttons_gap_x), buttons_y,
                                            button_width,
                                            button_height,
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                         math.floor(50 * Game.DISPLAY_RATIO),
                                                                         RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLUS"))),
                    "button_settings": Button(buttons_starting_x + (button_width + buttons_gap_x) * 2, buttons_y,
                                              button_width,
                                              button_height,
                                              RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                              pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                              text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                           math.floor(50 * Game.DISPLAY_RATIO),
                                                                           RessourceLoader.get("dpt.images.gui.symbols.SYMB_SETTINGS"))),
                    "button_quit": Button(buttons_starting_x + (button_width + buttons_gap_x) * 3, buttons_y,
                                          button_width,
                                          button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                       math.floor(50 * Game.DISPLAY_RATIO),
                                                                       RessourceLoader.get("dpt.images.gui.symbols.SYMB_X"))),
                    "window": Window((Game.surface.get_size()[0] // 2) - math.floor(122 * 3 * Game.DISPLAY_RATIO),
                                     buttons_y + button_height // 2 - math.floor(64 * 1.5 * Game.DISPLAY_RATIO), 6, 3)}

        # Loops
        from dpt.engine.mainLoop import main_menu_loop
        Game.loop = main_menu_loop
        return True

    @classmethod
    def settings_menu(cls):
        """Met en place les élèments du menu des paramètres

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """

        cls.logger.info("Displaying SETTINGS_MENU")
        from dpt.engine.loader import RessourceLoader

        # Ajout du GUI
        from dpt.engine.gui.menu.slider import Slider
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
        from dpt.engine.gui.menu.text import Text
        from dpt.engine.gui.menu.radioButton import RadioButton

        btn_list = []

        Game.gui = {"window_sound": Window(410 * Game.DISPLAY_RATIO, 190 * Game.DISPLAY_RATIO, 9, 5),
                    "sound_title": Text(math.floor(810 * Game.DISPLAY_RATIO),
                                        math.floor(200 * Game.DISPLAY_RATIO),
                                        "Options sonores",
                                        math.floor(50 * Game.DISPLAY_RATIO),
                                        (0, 0, 0),
                                        "dpt.fonts.DINOT_CondBlack"),
                    "general_volume_slider": Slider(math.floor(480 * Game.DISPLAY_RATIO),
                                                    math.floor(330 * Game.DISPLAY_RATIO),
                                                    math.floor(960 * Game.DISPLAY_RATIO),
                                                    math.floor(50 * Game.DISPLAY_RATIO),
                                                    Game.settings["general_volume"],
                                                    image_left=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_19"),
                                                    image_left_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_7"),
                                                    image_right=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_1"),
                                                    image_right_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_13"),
                                                    image_slide=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_2"),
                                                    image_slide_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_8"),
                                                    image_progress_bar_frame=RessourceLoader.get("dpt.images.gui.ui.UI_BARFRAME"),
                                                    image_progress_bar_bar=RessourceLoader.get("dpt.images.gui.ui.UI_FULLBAR")),
                    "general_volume_title": Text(math.floor(890 * Game.DISPLAY_RATIO),
                                                 math.floor(295 * Game.DISPLAY_RATIO),
                                                 "Volume général",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),
                    "music_volume_slider": Slider(math.floor(480 * Game.DISPLAY_RATIO),
                                                  math.floor(380 * Game.DISPLAY_RATIO),
                                                  math.floor(470 * Game.DISPLAY_RATIO),
                                                  math.floor(50 * Game.DISPLAY_RATIO),
                                                  Game.settings["music_volume"],
                                                  image_left=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_17"),
                                                  image_left_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_5"),
                                                  image_right=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_23"),
                                                  image_right_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_11"),
                                                  image_slide=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_12"),
                                                  image_slide_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_6"),
                                                  image_progress_bar_frame=RessourceLoader.get("dpt.images.gui.ui.UI_BARFRAME"),
                                                  image_progress_bar_bar=RessourceLoader.get("dpt.images.gui.ui.UI_COLORBAR_2")),
                    "music_volume_title": Text(math.floor(620 * Game.DISPLAY_RATIO),
                                               math.floor(430 * Game.DISPLAY_RATIO),
                                               "Volume de la musique",
                                               math.floor(25 * Game.DISPLAY_RATIO),
                                               (0, 0, 0),
                                               "dpt.fonts.DINOT_CondBlack"),
                    "sound_volume_slider": Slider(math.floor(970 * Game.DISPLAY_RATIO),
                                                  math.floor(380 * Game.DISPLAY_RATIO),
                                                  math.floor(470 * Game.DISPLAY_RATIO),
                                                  math.floor(50 * Game.DISPLAY_RATIO),
                                                  Game.settings["sound_volume"],
                                                  image_left=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_16"),
                                                  image_left_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_4"),
                                                  image_right=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_22"),
                                                  image_right_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_10"),
                                                  image_slide=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_11"),
                                                  image_slide_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_5"),
                                                  image_progress_bar_frame=RessourceLoader.get("dpt.images.gui.ui.UI_BARFRAME"),
                                                  image_progress_bar_bar=RessourceLoader.get("dpt.images.gui.ui.UI_COLORBAR_3")),
                    "sound_volume_title": Text(math.floor(1125 * Game.DISPLAY_RATIO),
                                               math.floor(430 * Game.DISPLAY_RATIO),
                                               "Volume des effets",
                                               math.floor(25 * Game.DISPLAY_RATIO),
                                               (0, 0, 0),
                                               "dpt.fonts.DINOT_CondBlack"),

                    "window_graphics": Window(math.floor(409 * Game.DISPLAY_RATIO), math.floor(505 * Game.DISPLAY_RATIO), 5, 6),
                    "graphics_title": Text(math.floor(550 * Game.DISPLAY_RATIO),
                                           math.floor(515 * Game.DISPLAY_RATIO),
                                           "Options graphiques",
                                           math.floor(50 * Game.DISPLAY_RATIO),
                                           (0, 0, 0),
                                           "dpt.fonts.DINOT_CondBlack"),
                    "left_button": Button(math.floor(490 * Game.DISPLAY_RATIO),
                                          math.floor(800 * Game.DISPLAY_RATIO),
                                          math.floor(43 * Game.DISPLAY_RATIO),
                                          math.floor(50 * Game.DISPLAY_RATIO),
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_19"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_7")),
                    "right_button": Button(math.floor(890 * Game.DISPLAY_RATIO),
                                           math.floor(800 * Game.DISPLAY_RATIO),
                                           math.floor(43 * Game.DISPLAY_RATIO),
                                           math.floor(50 * Game.DISPLAY_RATIO),
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_1"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_13")),
                    "graphics_text": Text(math.floor(550 * Game.DISPLAY_RATIO),
                                          math.floor(800 * Game.DISPLAY_RATIO),
                                          "Par défaut",
                                          math.floor(30 * Game.DISPLAY_RATIO),
                                          (0, 0, 0),
                                          "dpt.fonts.DINOT_CondBlack",
                                          centerx=math.floor(711 * Game.DISPLAY_RATIO),
                                          centery=math.floor(825 * Game.DISPLAY_RATIO)),

                    "window_server": Window(math.floor(1022 * Game.DISPLAY_RATIO), math.floor(505 * Game.DISPLAY_RATIO), 4, 6),
                    "server_title": Text(math.floor(1080 * Game.DISPLAY_RATIO),
                                         math.floor(515 * Game.DISPLAY_RATIO),
                                         "Options de connexion",
                                         math.floor(50 * Game.DISPLAY_RATIO),
                                         (0, 0, 0),
                                         "dpt.fonts.DINOT_CondBlack"),
                    "default_server_button": RadioButton(math.floor(1100 * Game.DISPLAY_RATIO),
                                                         math.floor(625 * Game.DISPLAY_RATIO),
                                                         0.7,
                                                         btn_list),
                    "custom_server_button": RadioButton(math.floor(1100 * Game.DISPLAY_RATIO),
                                                        math.floor(675 * Game.DISPLAY_RATIO),
                                                        0.7,
                                                        btn_list),
                    "default_server_text": Text(math.floor(1150 * Game.DISPLAY_RATIO),
                                                math.floor(620 * Game.DISPLAY_RATIO),
                                                "Serveur officiel",
                                                math.floor(30 * Game.DISPLAY_RATIO),
                                                (0, 0, 0),
                                                "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text": Text(math.floor(1150 * Game.DISPLAY_RATIO),
                                               math.floor(670 * Game.DISPLAY_RATIO),
                                               "Serveur privé",
                                               math.floor(30 * Game.DISPLAY_RATIO),
                                               (0, 0, 0),
                                               "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text_button": Button(math.floor(1330 * Game.DISPLAY_RATIO),
                                                        math.floor(665 * Game.DISPLAY_RATIO),
                                                        math.floor(69 * Game.DISPLAY_RATIO),
                                                        math.floor(52 * Game.DISPLAY_RATIO),
                                                        RessourceLoader.get("dpt.images.gui.buttons.BTN_PLAIN_2"),
                                                        text_sprite=TextSpriteButton(math.floor(40 * Game.DISPLAY_RATIO),
                                                                                     math.floor(30 * Game.DISPLAY_RATIO),
                                                                                     RessourceLoader.get("dpt.images.gui.symbols.SYMB_MENU"))),
                    "custom_server_text_1": Text(math.floor(1100 * Game.DISPLAY_RATIO),
                                                 math.floor(710 * Game.DISPLAY_RATIO),
                                                 "Attention, cet option permet de se",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text_2": Text(math.floor(1100 * Game.DISPLAY_RATIO),
                                                 math.floor(735 * Game.DISPLAY_RATIO),
                                                 "connecter à un serveur, pas de le créer !",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text_3": Text(math.floor(1100 * Game.DISPLAY_RATIO),
                                                 math.floor(760 * Game.DISPLAY_RATIO),
                                                 "Voir la documentation pour plus d'infor-",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text_4": Text(math.floor(1100 * Game.DISPLAY_RATIO),
                                                 math.floor(785 * Game.DISPLAY_RATIO),
                                                 "mations sur la création de serveurs.",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),

                    "window_menu": Window(50 * Game.DISPLAY_RATIO, 0, 2, 6, centery=Game.surface.get_size()[1] // 2),
                    "apply_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                           math.floor(390 * Game.DISPLAY_RATIO),
                                           math.floor(92 * Game.DISPLAY_RATIO),
                                           math.floor(95 * Game.DISPLAY_RATIO),
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                           text_sprite=TextSpriteButton(math.floor(50 * Game.DISPLAY_RATIO),
                                                                        math.floor(47 * Game.DISPLAY_RATIO),
                                                                        RessourceLoader.get("dpt.images.gui.symbols.SYMB_CHECK"))),
                    "cancel_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                            math.floor(495 * Game.DISPLAY_RATIO),
                                            math.floor(92 * Game.DISPLAY_RATIO),
                                            math.floor(95 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                         math.floor(50 * Game.DISPLAY_RATIO),
                                                                         RessourceLoader.get("dpt.images.gui.symbols.SYMB_BIGX"))),
                    "return_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                            math.floor(600 * Game.DISPLAY_RATIO),
                                            math.floor(92 * Game.DISPLAY_RATIO),
                                            math.floor(95 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                         math.floor(33 * Game.DISPLAY_RATIO),
                                                                         RessourceLoader.get("dpt.images.gui.symbols.SYMB_LEFTARROW")))
                    }

        if Game.settings["server_address"] == Game.DEFAULT_SERVER_ADDRESS:
            Game.gui["default_server_button"].value = True
        else:
            Game.gui["custom_server_button"].value = True

        Game.temp["display_size"] = Game.settings["display_size"]
        Game.temp["prev"] = Game.settings.copy()

        # Loops
        from dpt.engine.mainLoop import settings_menu_loop
        Game.loop = settings_menu_loop
        return True

    @classmethod
    def levels_menu(cls):
        """Met en place les élèments du menu de choix de niveau

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """

    @classmethod
    def start_level(cls, level):
        """Met en place les élèments du menu de début de niveau

        :param level: Niveau à charger

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        from dpt.engine.loader import RessourceLoader
        cls.logger.info("Displaying START_LEVEL")

        # WebComs
        from dpt.engine.webCommunications import Communication
        Game.com = Communication()
        if not Game.com.create():
            Scenes.return_error(["Impossible de se connecter au serveur de jeu.",
                                 "Verifiez votre connexion internet et réessayer",
                                 " ",
                                 "Si le problème persiste, vous pouvez nous contacter sur Discord",
                                 "Dwight Studio Hub: discord.gg/yZwuNqN",
                                 "(Lien copié dans le presse-papier)"])

            from tkinter import Tk
            root = Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append("https://discord.gg/yZwuNqN")
            root.update()
            root.destroy()
            return

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)

        Game.gui = {"window": Window(0, 0, 10, 10, centerx=Game.surface.get_size()[0] // 2, centery=Game.surface.get_size()[1] // 2),
                    "title": Text(0,
                                  math.floor(230 * Game.DISPLAY_RATIO),
                                  "Démarrer une nouvelle session",
                                  math.floor(50 * Game.DISPLAY_RATIO),
                                  (0, 0, 0),
                                  "dpt.fonts.DINOT_CondBlack",
                                  centerx=Game.surface.get_size()[0] // 2),
                    "session1": Text(0,
                                     math.floor(320 * Game.DISPLAY_RATIO),
                                     "ID de session :",
                                     math.floor(40 * Game.DISPLAY_RATIO),
                                     (0, 0, 0),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.surface.get_size()[0] // 2),
                    "session2": Text(0,
                                     math.floor(350 * Game.DISPLAY_RATIO),
                                     Game.com.sessionName,
                                     math.floor(120 * Game.DISPLAY_RATIO),
                                     (84, 66, 243),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.surface.get_size()[0] // 2),
                    "session3": Text(0,
                                     math.floor(525 * Game.DISPLAY_RATIO),
                                     "ou utilisez directement le lien",
                                     math.floor(40 * Game.DISPLAY_RATIO),
                                     (0, 0, 0),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.surface.get_size()[0] // 2),
                    "session4": Text(0,
                                     math.floor(555 * Game.DISPLAY_RATIO),
                                     Game.settings["server_address"] + "/?session=" + Game.com.sessionName,
                                     math.floor(80 * Game.DISPLAY_RATIO),
                                     (84, 66, 243),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.surface.get_size()[0] // 2),
                    "session5": Text(0,
                                     math.floor(635 * Game.DISPLAY_RATIO),
                                     "(Le lien a été copié dans votre presse-papier)",
                                     math.floor(40 * Game.DISPLAY_RATIO),
                                     (0, 0, 0),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.surface.get_size()[0] // 2),
                    "button_start": Button(math.floor(Game.surface.get_size()[0] / 2 + 50 * Game.DISPLAY_RATIO),
                                           math.floor(Game.DISPLAY_RATIO * 720), button_width, button_height,
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                           text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                        math.floor(50 * Game.DISPLAY_RATIO),
                                                                        RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_main_menu": Button(math.floor(Game.surface.get_size()[0] / 2 - button_width - 50 * Game.DISPLAY_RATIO),
                                               math.floor(Game.DISPLAY_RATIO * 720),
                                               button_width,
                                               button_height,
                                               RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                               pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                               text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                            math.floor(50 * Game.DISPLAY_RATIO),
                                                                            RessourceLoader.get("dpt.images.gui.symbols.SYMB_X"))),
                    "players_text": Text(Game.surface.get_size()[0] - math.floor(Game.DISPLAY_RATIO * 220),
                                         0,
                                         "Joueurs connectés : 000",
                                         math.floor(25 * Game.DISPLAY_RATIO),
                                         (0, 0, 0),
                                         "dpt.fonts.DINOT_CondBlack")}

        from tkinter import Tk
        root = Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append("http://" + Game.settings["server_address"] + "/?session=" + Game.com.sessionName)
        root.update()
        root.destroy()

        Game.temp["next_level"] = level
        Game.temp["player_count_check"] = 0

        # Loops
        from dpt.engine.mainLoop import start_level_loop
        Game.loop = start_level_loop
        return True

    @classmethod
    def end_level(cls):
        """Met en place les élèments du menu de fin de niveau

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        pass

    @classmethod
    def game_over(cls):
        """Met en place les élèments du menu d'échec

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        pass

    @classmethod
    def return_error(cls, messages):
        """Met en place les élèments du menu d'erreur

        :param messages: Messages d'erreur
        :type messages: list

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        Scenes.main_menu(False)

        cls.logger.info("Displaying RETURN_ERROR")

        # Ajout du GUI
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        from random import randint

        Game.gui.update({"window_error": Window(0, 0, 6, 4, centerx=Game.surface.get_size()[0] // 2, centery=Game.surface.get_size()[1] // 2),
                         "title_error": Text(0,
                                             math.floor(425 * Game.DISPLAY_RATIO),
                                             "Erreur",
                                             math.floor(50 * Game.DISPLAY_RATIO),
                                             (0, 0, 0),
                                             "dpt.fonts.DINOT_CondBlack",
                                             centerx=Game.surface.get_size()[0] // 2)})

        for i in range(len(messages)):
            Game.gui["message_" + str(randint(1000, 9999))] = Text(0, 0, messages[i],
                                                                   math.floor(25 * Game.DISPLAY_RATIO),
                                                                   (254, 0, 61),
                                                                   "dpt.fonts.DINOT_CondBlack",
                                                                   centerx=Game.surface.get_size()[0] // 2,
                                                                   centery=(Game.surface.get_size()[1] // 2 + math.floor(30 * Game.DISPLAY_RATIO) - (math.floor(12.5 * Game.DISPLAY_RATIO) * len(messages)) + (math.floor((25 * i) * Game.DISPLAY_RATIO))))

        # Loops
        from dpt.engine.mainLoop import main_menu_loop
        Game.loop = main_menu_loop
        return True
