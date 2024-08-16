from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import chess
import chess.engine

import time
import random
import re

class ChessBot:
    def __init__(self, username, password, headless = False, disable_notifications = True) -> None:
        self.url = "https://chess.com/"
        self.color = ""
        self.username = username
        self.password = password
        self.driver = None
        self.setup_driver(headless, disable_notifications)
    
    def setup_driver(self, headless, disable_notifications):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
        
        if disable_notifications:
            chrome_options.add_argument("--disable-notifications")
        
        self.service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.get(self.url)
    
    def switch_to_normal_mode(self):
        self.driver.quit()
        
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.get(self.url)

    
    def login(self) -> bool:
        self.driver.get('https://www.chess.com/login')
        
        try:
            email_input = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
            )
            password_input = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
            )
            submit_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
        except:
            return 'TLE'

        email_input.send_keys(self.username)
        password_input.send_keys(self.password)
        submit_button.click()

        cnt = 0
        while cnt < 20:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.url_changes('https://www.chess.com/login')
                )
                current_url = self.driver.current_url
                if "https://www.chess.com/home" in current_url:
                    return True
            except:
                cnt+=1
            return False
    
    def new_game(self, random_value):
        while True:
            try:
                self.driver.get('https://www.chess.com/play/online/new')

                new_game = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-tab="newGame"].tabs-tab.tabs-active'))
                )
                self.driver.execute_script("arguments[0].scrollIntoView();", new_game)
                new_game.click()

                options = WebDriverWait(self.driver, 50).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'selector-button-button'))
                            )
                self.driver.execute_script("arguments[0].scrollIntoView();", options)
                options.click()

                more_options = WebDriverWait(self.driver, 50).until(
                            EC.presence_of_element_located((By.XPATH, "//span[@class='toggle-custom-game-label' and text()='More Time Controls']"))
                            )
                self.driver.execute_script("arguments[0].scrollIntoView();", more_options)
                more_options.click()

                mode = WebDriverWait(self.driver, 50).until(
                            EC.presence_of_element_located((By.XPATH, f'//button[contains(@class, "time-selector-button-button") and text()="{random_value}"]'))
                            )
                self.driver.execute_script("arguments[0].scrollIntoView();", mode)
                mode.click()

                play_button = WebDriverWait(self.driver, 50).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.cc-button-full'))
                            )
                #sidebar = WebDriverWait(self.driver, 50).until(
                    #EC.presence_of_element_located((By.ID, 'board-layout-sidebar'))
                    #)
                #self.driver.execute_script("arguments[0].scrollTop = 0;", sidebar)
                play_button.click()
                try:
                    play_fair_button = WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located((By.XPATH, "//button[@class='cc-button-component cc-button-primary cc-button-xx-large cc-button-full fair-play-button']"))
                                )
                    play_fair_button.click()
                except:
                    pass
                break
            except:
                print('Play button could not be clicked, trying again...')

        #play_button = WebDriverWait(self.driver, 50).until(
        #    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.cc-button-full'))
        #)
        #actions = ActionChains(self.driver)
        #actions.move_to_element(play_button).perform()
        #play_button.click()
    
    def start_game(self):
        play_button = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'index-guest-button-title'))
                    )
        play_button.click()

        pop_up = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.ID, 'guest-button'))
                    )
        pop_up.click()

        new_game = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.cc-button-component.cc-button-primary.cc-button-xx-large.cc-button-full'))
                    )
        new_game.click()

    def rating_to_skill_level(self, rating):
        if rating < 800:
            return 1
        elif rating < 900:
            return 2
        elif rating < 1000:
            return 3
        elif rating < 1100:
            return 4
        elif rating < 1200:
            return 5
        elif rating < 1300:
            return 6
        elif rating < 1400:
            return 7
        elif rating < 1500:
            return 8
        elif rating < 1600:
            return 9
        elif rating < 1700:
            return 10
        elif rating < 1800:
            return 11
        elif rating < 1900:
            return 12
        elif rating < 2000:
            return 13
        elif rating < 2100:
            return 14
        elif rating < 2200:
            return 15
        elif rating < 2300:
            return 16
        elif rating < 2400:
            return 17
        elif rating < 2500:
            return 18
        elif rating < 2700:
            return 19
        else:
            return 20


    def get_skill_level(self):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, ".user-tagline-rating")
            rating_text = element.text
            rating_match = re.search(r'\((\d+)\)', rating_text)
        except NoSuchElementException:
            rating_match = None

        if rating_match:
            rating = int(rating_match.group(1))
        else:
            rating = 1200
        
        skill_level = self.rating_to_skill_level(rating)
        print(f'Skill Level: {skill_level}')

        return skill_level


    def get_best_move(self, fen, skill_level, game_mode):
        stockfish_path = 'stockfish-windows-x86-64-avx2.exe'

        board = chess.Board(fen)

        try:
            time_per_move = self.get_move_time(game_mode)
        except Exception as e:
            print(e)

        #print(f'Time for stockfish: {time_per_move}')

        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            engine.configure({"Skill Level": skill_level})
            result = engine.play(board, chess.engine.Limit(time=time_per_move))
            best_move = result.move
        
        return best_move
    
    def get_move_time(self, random_value):
        if random_value == '10 min':
            return random.uniform(0.1, 4.5)
        elif random_value == '15 | 10':
            return random.uniform(0.3, 12.5)
        elif random_value == '20 min':
            return random.uniform(5.3, 11.4)
        elif random_value == '30 min':
            return random.uniform(3.2, 13.8)
        elif random_value == '60 min':
            return random.uniform(4.6, 19.4)
        elif random_value == '10 | 5':
            return random.uniform(0.1, 6.3)

        elif random_value == '3 min':
            return random.uniform(0.3, 2)
        elif random_value == '5 min':
            return random.uniform(0.5, 3)
        elif random_value == '5 | 5':
            return random.uniform(0.1, 3.9)
        elif random_value == '5 | 2':
            return random.uniform(0.1, 1.4)
        elif random_value == '3 | 2':
            return random.uniform(0.1, 1.2)

        elif random_value == '30 sec':
            return random.uniform(0.1, 0.2)
        elif random_value == '20 sec | 1':
            return random.uniform(0.1, 0.2)
        elif random_value == '1 min':
            return random.uniform(0.1, 0.2)
        elif random_value == '1 | 1':
            return random.uniform(0.1, 0.2)
        elif random_value == '2 | 1':
            return random.uniform(0.1, 0.2)
        else:
            return random.uniform(0.1, 1)

    def board_to_fen(self, board):
        fen_rows = []
        for row in board:
            fen_row = ''
            empty_count = 0
            for square in row:
                if square == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += square
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)
        return '/'.join(fen_rows) + ' ' + self.color + ' KQkq - 0 1'

    def convert_to_FEN(self):
        figures = self.driver.find_elements(By.CSS_SELECTOR, ".piece")
        board = [["." for _ in range(8)] for _ in range(8)]

        for figure in figures:
            classes = figure.get_attribute("class").split()
            piece_type = ''
            position_class = ''

            for class_name in classes:
                if class_name.startswith('w') or class_name.startswith('b'):
                    piece_class = class_name
                    piece_type = piece_class[1]
                    if piece_class[0] == 'w':
                        piece_type = piece_type.upper()
                elif class_name.startswith('square-'):
                    position_class = class_name

            if position_class:
                file = int(position_class[8]) - 1
                rank = int(position_class[7]) - 1

                board[8 - file - 1][rank] = piece_type
        
        fen = self.board_to_fen(board)
        print(f'Fen: {fen}')
        print()
        for row in board:
            print(row)
        print()

        return fen

    def get_square_info(self, square_class):
        script = f"""
        const element = document.querySelector('.{square_class}');
        if (element) {{
            const rect = element.getBoundingClientRect();
            return {{
                centerX: rect.left + rect.width / 2,
                centerY: rect.top + rect.height / 2,
                width: rect.width,
                height: rect.height
            }};
        }} else {{
            return null;
        }}
        """
        square_info = self.driver.execute_script(script)
        
        if square_info is None:
            raise Exception(f"Element with class '{square_class}' not found.")
        
        return square_info

    def play_move(self, move):
        move_str = move.uci()
        print(f'Move: {move_str}')
        start_square = move_str[:2]
        end_square = move_str[2:]

        start_x = ord(start_square[0]) - ord('a') + 1
        start_y = int(start_square[1])
        end_x = ord(end_square[0]) - ord('a') + 1
        end_y = int(end_square[1])

        start_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, f'square-{start_x}{start_y}'))
        )
        square = self.get_square_info(f'square-{start_x}{start_y}')

        start_element.click()
        
        delta_x = end_x - start_x
        delta_y = start_y - end_y

        if self.color == 'b':
            delta_x = -delta_x
            delta_y = -delta_y

        second_click = webdriver.common.action_chains.ActionChains(self.driver)
        second_click.move_to_element_with_offset(start_element, delta_x * square['height'] , delta_y * square['height'])
        second_click.click()
        second_click.perform()
        #print('drugi klik izvrsen')

        if len(end_square) == 3:
            promotion_piece = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'.promotion-piece.{self.color}{end_square[2]}'))
            )

            if promotion_piece:
                promotion_piece.click()
            else:
                print("Promotion piece not found.")



    def play_round(self, play_again = False, is_grind_mode = False):
        #print('LJUDI USO JE U PLAYROUND')
        while True:
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resign-button-label"))
                )
                break
            except:
                if is_grind_mode or self.stop_event.is_set():
                    try:
                        cancel_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "outgoing-challenge-box-cancel"))
                        )
                        cancel_button.click()
                    except:
                        print('Cancel button is not found')
                    return
                #print('60 seconds have passed')

        self.driver.execute_script("window.scrollTo(0, 0);")

        game_mode = self.driver.find_element(By.XPATH, "//span[contains(text(), 'min') or contains(text(), 'sec') or contains(text(), '|')]").get_attribute('textContent').strip()
        game_mode = game_mode.replace("New ", "").strip()
        #print('Game mode je ')
        #print(game_mode)
        
        stopwatch = self.driver.find_element(By.CLASS_NAME, 'clock-bottom')
        if 'clock-white' in stopwatch.get_attribute('class'):
            self.color = 'w'
        else:
            self.color = 'b'
        #print('JUPIIII')
        while True:
            try:
                # Waiting for element
                start_time = time.time()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.clock-component.clock-bottom.clock-player-turn"))
                )
                end_time = time.time()
                print(f"Wait: {end_time - start_time:.2f} seconds")

                # Convert to FEN
                start_time = time.time()
                fen = self.convert_to_FEN()
                end_time = time.time()
                print(f"Convert to FEN: {end_time - start_time:.2f} seconds")
                
                # Get skill level
                start_time = time.time()
                skill_level = self.get_skill_level()
                end_time = time.time()
                print(f"Get skill level: {end_time - start_time:.2f} seconds")
                
                # Get best move
                start_time = time.time()
                move = self.get_best_move(fen, skill_level, game_mode)
                end_time = time.time()
                print(f"Get best move: {end_time - start_time:.2f} seconds")
                
                # Play move
                start_time = time.time()
                self.play_move(move)
                end_time = time.time()
                print(f"Play move: {end_time - start_time:.2f} seconds")
            except:
                try:
                    try:
                        close_game_review_button = WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, "//span[@class='game-review-popup-close icon-font-chess x']"))
                        )
                        close_game_review_button.click()
                    except:
                        pass
                    game_over = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "game-over-buttons-button") and .//span[starts-with(text(), "New")]]'))
                    )
                    if game_over and play_again and not self.stop_event.is_set():
                        #time.sleep(2)
                        game_over.click()
                        print("Button clicked successfully!")
                    #else:
                        #print('ALOOOOO nije se kliknuo a nadjen je')
                    #print(game_over)
                    #print(game_over.get_attribute('class'))
                    #print(game_over.text)
                    if game_over:
                        #print('Break NO 1 je puko')
                        break
                except Exception as e:
                    try:
                        decline_button = self.driver.find_element(By.XPATH, '//button[contains(@class, "game-over-buttons-button") and .//span[starts-with(text(), "Decline")]]')
                        if play_again and not self.stop_event.is_set():
                            decline_button.click()
                            game_over = self.driver.find_element(By.XPATH, '//button[contains(@class, "game-over-buttons-button") and .//span[starts-with(text(), "New")]]')
                            #time.sleep(2)
                            game_over.click()
                            print("Button clicked successfully!")
                        #print('Break NO 2 je puko')
                        break
                    except:
                        print('Move could not be played, Play Again is not found, Decline button is not found')
                        self.driver.execute_script("window.scrollTo(0, 0);")
    

    #def auto_detect_board(self, play_again = False):
        #while True:
            #self.play_round(play_again)
            #if self.stop_event.is_set():
                #return
    
    def setup_auto_detect_board(self, play_again, stop_event):
        self.stop_event = stop_event
        while True:
            self.play_round(play_again = play_again, is_grind_mode = False)
            if self.stop_event.is_set():
                return

    def setup_grind_mode(self, stop_event, selected_options):
        self.stop_event = stop_event
        #print('USO je u grind mode')

        game = random.choice(list(selected_options.keys()))
        game_mode = random.choice(selected_options[game])
        self.new_game(game_mode)

        number_of_games = random.randint(1, 4)

        while True:
            if number_of_games == 1:
                play_again = False
            else:
                play_again = True
            
            #print(play_again)
            self.play_round(play_again = play_again, is_grind_mode = True)

            if self.stop_event.is_set():
                return
            
            number_of_games-=1
            if number_of_games == 0:
                game = random.choice(list(selected_options.keys()))
                game_mode = random.choice(selected_options[game])
                self.new_game(game_mode)
                number_of_games = random.randint(1, 4)

    #def start(self):
    #    self.login()
     #   self.new_game()
       # while True:
      #      self.play_round()
        