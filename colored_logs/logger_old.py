from typing import Optional
import os, time, re

from colored import style, fg



from enum import Enum
class LogInfo(Enum):
    LogType = 0,
    ID = 1,
    Icon = 2,
    ThreadName = 3,
    Time = 4



class Logger:
    def __init__(
        self,
        print_log_type: bool = True,
        print_time: bool = True,
        id: Optional[str] = None,
        use_icons: bool = True,
        info_color: str = 'B4AEA8',
        success_color: str = '3EA966',
        warning_color: str = 'F28F3B',
        error_color: str = 'A22B24',
        fail_color: str = 'C8553D',
        dim_color: str = '918B86'
    ):
        self.set_print_log_type(print_log_type)
        self.set_print_time(print_time)
        self.set_id(id)
        self.set_use_icons(use_icons)

        self._info_color = 'B4AEA8'
        self.set_info_color(info_color)

        self._success_color = '3EA966'
        self.set_success_color(success_color)

        self._warning_color = 'F28F3B'
        self.set_warning_color(warning_color)

        self._error_color = 'C8553D'
        self.set_error_color(error_color)

        self._fail_color = 'C8553D'
        self.set_fail_color(fail_color)

        self._dim_color = '918B86'
        self.set_dim_color(dim_color)

    # SETTERS
    def set_print_log_type(
        self,
        print_log_type: bool = True
    ):
        self.print_log_type = print_log_type
    
    def set_print_time(
        self,
        print_time: bool = True
    ):
        self.print_time = print_time
    
    def set_id(
        self,
        id: Optional[str] = None
    ):
        self.id = id
    
    def set_use_icons(
        self,
        use_icons: bool = True
    ):
        self.use_icons = use_icons
    
    def set_info_color(
        self,
        info_color: str
    ):
        self._info_color = info_color or self._info_color
    
    def set_success_color(
        self,
        success_color: str
    ):
        self._success_color = success_color or self._success_color
    
    def set_warning_color(
        self,
        warning_color: str
    ):
        self._warning_color = warning_color or self._warning_color
    
    def set_error_color(
        self,
        error_color: str
    ):
        self._error_color = error_color or self._error_color
    
    def set_fail_color(
        self,
        fail_color: str
    ):
        self._fail_color = fail_color or self._fail_color
    
    def set_dim_color(
        self,
        dim_color: str
    ):
        self._dim_color = dim_color or self._dim_color
    

    # LOGGING FUNCS
    def info(self, *values: object):
        values = ('ℹ',) + values
        self.__log(
            self._info_color,
            values
        )
    
    def stop_progress(self):
        try:
            self.progress_thread.terminate()
            self.progress_thread = None
        except:
            pass
    
    def start_progress(
        self,
        *values: object,
        animation_version: int = 0
    ):
        if type(animation_version) != type(int) or animation_version > 3 or animation_version < 0:
            animation_version = None

        from threading import Thread
        import threading
        from multiprocessing import Process

        print(threading.current_thread())

        self.stop_progress()
        self.progress_thread = Process(target=self.__progress, args=(values,))
        self.progress_thread.start()
    
    def __progress(self, values: object):
        if self.use_icons:
            values = ('◔',) + values
        
        import threading
        print(threading.current_thread().getName())
        
        start_time = int(time.time())
        i = 0

        ERASE_LINE = '\033[2K\033[1G'

        while True:
            diff_s = int(time.time()) - start_time
            # dot_count = ((i%3)+1)
            # dot_str = '.' * dot_count + ' ' * (3-dot_count)
            # dot_strs = ['◜ ', ' ◝', ' ◞', '◟ ']
            # dot_strs = ['◆', '◈', '◇', '◈']
            # dot_strs = ['◴', '◷', '◶', '◵']
            # dot_strs = ['◴   ', ' ◷  ', '  ◶ ', '   ◵', '  ◶ ', ' ◷  ']
            dot_strs = [
                '⸳·⸳․․․․․',
                '․⸳·⸳․․․․',
                '․․⸳·⸳․․․',
                '․․․⸳·⸳․․',
                '․․․․⸳·⸳․',
                '․․․․․⸳·⸳',

                '․․․․⸳·⸳․',
                '․․․⸳·⸳․․',
                '․․⸳·⸳․․․',
                '․⸳·⸳․․․․',

                # '⸳․․․․․⸳·',
                # '·⸳․․․․․⸳'
            ]
            
            # dot_strs = ['✈     ✈', ' ✈    ', '  ✈   ', '   ✈  ', '    ✈ ']#s, '     ✈']
            # dot_strs = ['✢       ', ' ✣      ', '  ✤     ', '   ✦    ','    +   ', '     ✦  ', '      ✤ ', '       ✣']
            # dot_strs = ['⌏', '⌎', '⌌', '⌍']
            dot_strs = ['▪▫▫▫▫', '▫▪▫▫▫', '▫▫▪▫▫', '▫▫▫▪▫', '▫▫▫▫▪', '▫▫▫▪▫', '▫▫▪▫▫', '▫▪▫▫▫']
            dot_str = dot_strs[i%len(dot_strs)]
            time_str = '⧗ ' + time.strftime('%H:%M:%S', time.gmtime(diff_s))

            # print(ERASE_LINE, end='\r')

            _values = values + (dot_str, time_str)

            self.__log('5893C4', _values, log_type=' PROGRESS', end='\r')
            i += 1

            time.sleep(0.075)
    
    def subtle(self, *values: object):
        old_print_log_type = self.print_log_type
        old_id = self.id
        self.print_log_type = False
        self.id = None

        self.__log(
            self._info_color,
            values
        )

        self.print_log_type = old_print_log_type
        self.id = old_id
    
    def success(self, *values: object):
        if self.use_icons:
            values = ('✔',) + values

        self.__log(
            self._success_color,
            values
        )
    
    def fail(self, *values: object):
        if self.use_icons:
            values = ('✘',) + values

        self.__log(
            self._fail_color,
            values
        )
    
    def warning(self, *values: object):
        if self.use_icons:
            values = ('!',) + values

        self.__log(
            self._warning_color,
            values
        )
    
    def error(self, *values: object):
        if self.use_icons:
            values = ('☠',) + values

        self.__log(
            self._error_color,
            values
        )
    
    # PRIVATE METHODS
    def __log(
        self,
        color_hex: str,
        values: object,
        separator: str = ' ',
        log_type: Optional[str] = None,
        end: Optional[str] = None
    ):
        log_fg_color = fg(self.__hex(color_hex))
        dim_color = fg(self.__hex(self._dim_color))
        content = ''

        for value in values:
            if len(content) > 0:
                content += separator
            
            content += str(value)
        
        if self.print_log_type:
            if log_type is None:
                import sys

                log_type = sys._getframe().f_back.f_code.co_name
            
            log_type = self.__uniform_len_string(log_type.upper(), 10)
        else:
            log_type = None

        id = None
        if self.id is not None and len(self.id) > 0:
            id = self.__uniform_len_string(self.id, 14)
        
        content = style.BOLD + log_fg_color + content + style.RESET

        log = ''

        if log_type is not None:
            log += style.BOLD + log_fg_color + log_type + style.RESET
        
        log += style.BOLD + dim_color

        if id is not None:
            if log_type is not None:
                log += ' - '
            
            log += id + ' - '
        elif log_type is not None:
            log += ' - '
        
        log += style.RESET
        log += style.BOLD + log_fg_color + content + style.RESET

        if self.print_time:
            log = self.__log_by_optionally_adding_time(log, style.BOLD + dim_color)

        print(log, end=end)
    
    
    def __hex(
        self,
        hex: str
    ) -> str:
        if not hex.startswith('#'):
            hex = '#' + hex
        
        return hex
    
    def __uniform_len_string(
        self,
        string: str,
        preferred_length: int = 8,
        filling_char: str = ' '
    ) -> str:
        while len(string) < preferred_length:
            string += filling_char
        
        if len(string) > preferred_length:
            string = string[:preferred_length-1] + '.'
        
        return string
    
    def __log_by_optionally_adding_time(
        self,
        log: str,
        _style: str
    ) -> str:
        max_console_len = self.__console_max_chars_per_line()
        filler_char = ' '
        unescaped_log = self.__string_without_ansii(log)

        if len(unescaped_log) < max_console_len:
            time_log = self.__time()
            minimum_spaces = 2

            if len(unescaped_log) + len(time_log) + minimum_spaces < max_console_len:
                while len(unescaped_log) < max_console_len - len(time_log):
                    unescaped_log += filler_char
                    log += filler_char
                
                log += _style + time_log + style.RESET
        
        return log
    
    def __time(self) -> str:
        return time.strftime("%H:%M:%S", time.localtime())
    
    def __console_max_chars_per_line(self) -> int:
        _, columns = os.popen('stty size', 'r').read().split()

        return int(columns)
    
    def __string_without_ansii(
        self,
        string: str
    ) -> str:
        ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')

        return ansi_escape.sub('', string)