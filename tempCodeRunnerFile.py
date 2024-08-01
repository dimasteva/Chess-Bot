stopwatch = self.driver.find_element(By.CLASS_NAME, 'clock-bottom')
        if 'clock-white' in stopwatch.get_attribute('class'):
            self.color = 'white'
        else:
            self.color = 'black'