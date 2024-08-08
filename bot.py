from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import re

import chess
import chess.engine

import time


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
            email_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
            )
            password_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
            )
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
        except:
            print('Nije se ucitalo')
            return False #moraces da promenis messagebox da bude da je presporo a ne wrong credentials

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
    
    def new_game(self):
        self.driver.get('https://www.chess.com/play/online/new')

        #list = self.driver.find_element(By.CLASS_NAME, 'selector-button-button')
        #list.click()
        #time.sleep(3)
        #print('Proslo1')
        #rapid = self.driver.find_element(By.XPATH, '//button[contains(@class, "time-selector-button-button") and text()="3 min"]')
        #rapid.click()
        #time.sleep(3)
        #print('Proslo2')
        play_button = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.cc-button-full'))
                    )
        play_button.click()  
        print('Proslo3')       
    
    def start_game(self):
        play_button = self.driver.find_element(By.CLASS_NAME, 'index-guest-button-title')
        play_button.click()

        pop_up = self.driver.find_element(By.ID, 'guest-button')
        pop_up.click()

        new_game = self.driver.find_element(By.CSS_SELECTOR, '.cc-button-component.cc-button-primary.cc-button-xx-large.cc-button-full')
        new_game.click()

    def rating_to_skill_level(self, rating):
        if rating < 1100:
            return 8
        if rating < 1200:
            return 9
        elif rating < 1300:
            return 10
        elif rating < 1400:
            return 11
        elif rating < 1500:
            return 12
        elif rating < 1600:
            return 13
        elif rating < 1700:
            return 14
        elif rating < 1800:
            return 15
        elif rating < 1900:
            return 16
        elif rating < 2000:
            return 17
        elif rating < 2100:
            return 18
        elif rating < 2200:
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
        
        skill_level = self.rating_to_skill_level(rating) - 4
        print(skill_level)
        return skill_level


    def get_best_move(self, fen, skill_level):
        stockfish_path = 'stockfish-windows-x86-64-avx2.exe'

        board = chess.Board(fen)
        print(skill_level)

        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            engine.configure({"Skill Level": skill_level})
            result = engine.play(board, chess.engine.Limit(time=1.0))
            best_move = result.move
        
        return best_move
    
    def invert_chessboard(self, board):
        return [row[::-1] for row in board[::-1]]
    
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
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resign-button-label"))
        )

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
        print(fen)

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
        
        start_square = move_str[:2]
        end_square = move_str[2:]

        start_x = ord(start_square[0]) - ord('a') + 1
        start_y = int(start_square[1])
        end_x = ord(end_square[0]) - ord('a') + 1
        end_y = int(end_square[1])

        start_element = self.driver.find_element(By.CLASS_NAME, f'square-{start_x}{start_y}')
        square = self.get_square_info(f'square-{start_x}{start_y}')

        first_click = webdriver.common.action_chains.ActionChains(self.driver)
        first_click.move_to_element_with_offset(start_element, 0, 0)
        first_click.click()
        first_click.perform()
        
        delta_x = end_x - start_x
        delta_y = start_y - end_y

        if self.color == 'b':
            delta_x = -delta_x
            delta_y = -delta_y

        second_click = webdriver.common.action_chains.ActionChains(self.driver)
        second_click.move_to_element_with_offset(start_element, delta_x * square['height'] , delta_y * square['height'])
        second_click.click()
        second_click.perform()

        if len(end_square) == 3:
            multiply = 0

            if end_square[2] == 'n':
                multiply = 1
            elif end_square[2] == 'r':
                multiply = 2
            elif end_square[2] == 'b':
                multiply = 3

            time.sleep(1)

            third_click = webdriver.common.action_chains.ActionChains(self.driver)
            third_click.move_to_element_with_offset(start_element, delta_x * square['height'], delta_y * square['height'] + multiply * square['height'])
            third_click.click()
            third_click.perform()



    def play_round(self, play_again = False):
        self.driver.execute_script("window.scrollTo(0, 0);")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resign-button-label"))
        )
        
        stopwatch = self.driver.find_element(By.CLASS_NAME, 'clock-bottom')
        if 'clock-white' in stopwatch.get_attribute('class'):
            self.color = 'w'
        else:
            self.color = 'b'
        while True:
            try:
                # Waiting for element
                start_time = time.time()
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.clock-component.clock-bottom.clock-player-turn"))
                )
                end_time = time.time()
                print(f"Wait: {end_time - start_time:.2f} sekundi")

                # Convert to FEN
                start_time = time.time()
                fen = self.convert_to_FEN()
                end_time = time.time()
                print(f"Convert to FEN: {end_time - start_time:.2f} sekundi")
                
                # Get skill level
                start_time = time.time()
                skill_level = self.get_skill_level()
                end_time = time.time()
                print(f"Get skill level: {end_time - start_time:.2f} sekundi")
                
                # Get best move
                start_time = time.time()
                move = self.get_best_move(fen, skill_level)
                end_time = time.time()
                print(f"Get best move: {end_time - start_time:.2f} sekundi")
                
                # Play move
                start_time = time.time()
                self.play_move(move)
                end_time = time.time()
                print(f"Play move: {end_time - start_time:.2f} sekundi")
            except:
                try:
                    game_over = self.driver.find_element(By.XPATH, '//button[contains(@class, "game-over-buttons-button") and .//span[starts-with(text(), "New")]]')
                    if play_again and not self.stop_event:
                        time.sleep(2)
                        game_over.click()
                        print("Button clicked successfully!")
                    break
                except Exception as e:
                    try:
                        decline_button = self.driver.find_element(By.XPATH, '//button[contains(@class, "game-over-buttons-button") and .//span[starts-with(text(), "Decline")]]')
                        if play_again and not self.stop_event:
                            decline_button.click()
                            game_over = self.driver.find_element(By.XPATH, '//button[contains(@class, "game-over-buttons-button") and .//span[starts-with(text(), "New")]]')
                            time.sleep(2)
                            game_over.click()
                            print("Button clicked successfully!")
                        break
                    except:
                        print('Decline button is not found')
    

    def auto_detect_board(self, play_again = False):
        while True:
            try:
                WebDriverWait(self.driver, 50).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resign-button-label"))
                        )
                break
            except:
                print('Proslo 50')

        self.play_round(play_again)
    
    def grind_mode(self):
        self.new_game()
        self.play_round(True)
        print('GOTOCA RUNDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    
    def setup_auto_detect_board(self, play_again, stop_event):
        self.stop_event = stop_event
        while True:
            self.auto_detect_board(play_again)
            if self.stop_event.is_set():
                return

    def setup_grind_mode(self, stop_event):
        self.stop_event = stop_event
        while True:
            self.grind_mode()
            if self.stop_event.is_set():
                return

    #def start(self):
    #    self.login()
     #   self.new_game()
       # while True:
      #      self.play_round()
        