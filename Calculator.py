import tkinter as tk
import math


class Solver:
    def calculate(self, expr: str) -> str: 
        expr = expr.replace('√', 'math.sqrt')
        expr = expr.replace('×', '*')
        expr = expr.replace('^', '**')
        expr = expr.replace('acos', 'math.acos')
        expr = expr.replace('asin', 'math.asin')
        expr = expr.replace('atg', 'math.atan')
        expr = expr.replace('log', 'math.log')
        expr = expr.replace('fact', 'math.factorial')
        expr = expr.replace('e', '*10**')
        
        try:
            answer = eval(expr)
        except Exception as ex:
            return 'Invalid Input'
        else:
            if len(str(answer)) > 20:
                return '{:.10e}'.format(answer)
            else:
                return answer


class MemoryCell:
    def __init__(self, master):
        self.value = 0.0
        self.master = master    

    def add(self, number: float):
        self.value += number

    def subtract(self, number: float):
        self.value -= number

    def clear(self):
        self.value = 0.0

    def copy(self):
        self.master.clipboard_append(self.value)

    def get(self) -> float:
        return self.value
 

class Memory:
    def __init__(self, master, cells_number=1):
        self.mem_list = None
        self.cell_idx = 0
        self.master = master

        self.initialize(cells_number)

    def initialize(self, cells_number):
        self.mem_list = list()
        for _ in range(cells_number):
            self.mem_list.append(MemoryCell(self.master))

    def current_cell(self) -> MemoryCell:
        return self.mem_list[self.cell_idx]

    def change_cell(self, cell_idx: int):
        self.cell_idx = cell_idx


class InterfaceObject:
    def __init__(self):
        self.obj = None

    def delete(self):
        self.obj.destroy()


class Keyboard(InterfaceObject):
    def __init__(self, frame):
        self.button_rows_desc = list()
        self.button_objs = list()
        self.frame = frame

    def bind_buttons(self, mem_obj, scr_obj):
        pass

    def attach(self):
        current_row = 1
        current_col = 0

        for row in self.button_rows_desc:
            for name, callback in row.items():
                new_btn = tk.Button(self.frame, text=name, 
                    width=5, height=1, command=callback)
                new_btn.grid(row=current_row, column=current_col)
                self.button_objs.append(new_btn)
                current_col += 1
        
            current_col = 0
            current_row += 1
            
    def delete(self):
        for button in self.button_objs:
            button.destroy()


class StandartKeyboard(Keyboard):
    def bind_buttons(self, memory_obj, screen_obj, solver_obj, mode_changer):
        self.button_rows_desc.append({
            '(': lambda: screen_obj.add_char('('),
            ')': lambda: screen_obj.add_char(')')
        })
        self.button_rows_desc.append({
            'M+': lambda: memory_obj.current_cell().add(screen_obj.get()),
            'M-': lambda: memory_obj.current_cell().subtract(screen_obj.get()),
            'MR': lambda: screen_obj.add_char(memory_obj.current_cell().get()),
            'MC': lambda: memory_obj.current_cell().clear(),
            'MS': lambda: memory_obj.current_cell().copy()
        })
        
        self.button_rows_desc.append({
            '7': lambda: screen_obj.add_char(7),
            '8': lambda: screen_obj.add_char(8),
            '9': lambda: screen_obj.add_char(9),
            '÷': lambda: screen_obj.add_char('/'),
            'CE': lambda: screen_obj.clear_line()
        })
        self.button_rows_desc.append({
            '4': lambda: screen_obj.add_char(4),
            '5': lambda: screen_obj.add_char(5),
            '6': lambda: screen_obj.add_char(6),
            '*': lambda: screen_obj.add_char('×'),
            '√': lambda: screen_obj.add_char('√(')
        })
        self.button_rows_desc.append({
            '1': lambda: screen_obj.add_char(1),
            '2': lambda: screen_obj.add_char(2),
            '3': lambda: screen_obj.add_char(3),
            '-': lambda: screen_obj.add_char('-'),
            '^': lambda: screen_obj.add_char('^')
        })
        self.button_rows_desc.append({
            '0': lambda: screen_obj.add_char(0),
            '.': lambda: screen_obj.add_char('.'),
            '+': lambda: screen_obj.add_char('+'),
            '=': lambda: screen_obj.add_answer(
                    solver_obj.calculate(screen_obj.get_expr())
            ),
            'Adv': mode_changer
        })


class AdvancedKeyboard(Keyboard):
    def bind_buttons(self, memory_obj, screen_obj, solver_obj, mode_changer):
        self.button_rows_desc.append({
            '(': lambda: screen_obj.add_char('('),
            ')': lambda: screen_obj.add_char(')'),
            ',': lambda: screen_obj.add_char(',')
        })
        self.button_rows_desc.append({
            'M+': lambda: memory_obj.current_cell().add(screen_obj.get()),
            'M-': lambda: memory_obj.current_cell().subtract(screen_obj.get()),
            'MR': lambda: screen_obj.add_char(memory_obj.current_cell().get()),
            'MC': lambda: memory_obj.current_cell().clear(),
            'MS': lambda: memory_obj.current_cell().copy()
        })
        self.button_rows_desc.append({
            'M1': lambda: memory_obj.change_cell(0),
            'M2': lambda: memory_obj.change_cell(1),
            'M3': lambda: memory_obj.change_cell(2),
            'M4': lambda: memory_obj.change_cell(3),
            'M5': lambda: memory_obj.change_cell(4)
        })
        self.button_rows_desc.append({
            'M6': lambda: memory_obj.change_cell(5),
            'M7': lambda: memory_obj.change_cell(6),
            'M8': lambda: memory_obj.change_cell(7),
            'M9': lambda: memory_obj.change_cell(8),
            'CE': lambda: screen_obj.clear_line()
        })
        self.button_rows_desc.append({
            'acos': lambda: screen_obj.add_char('acos('),
            'asin': lambda: screen_obj.add_char('asin('),
            'atg': lambda: screen_obj.add_char('atg('),
            'log_xy': lambda: screen_obj.add_char('log('),
            'n!': lambda: screen_obj.add_char('fact(')
        })
        self.button_rows_desc.append({
            '7': lambda: screen_obj.add_char(7),
            '8': lambda: screen_obj.add_char(8),
            '9': lambda: screen_obj.add_char(9),
            '÷': lambda: screen_obj.add_char('/'),
            '←': lambda: screen_obj.delete_last_position()
        })
        self.button_rows_desc.append({
            '4': lambda: screen_obj.add_char(4),
            '5': lambda: screen_obj.add_char(5),
            '6': lambda: screen_obj.add_char(6),
            '*': lambda: screen_obj.add_char('×'),
            '√': lambda: screen_obj.add_char('√(')
        })
        self.button_rows_desc.append({
            '1': lambda: screen_obj.add_char(1),
            '2': lambda: screen_obj.add_char(2),
            '3': lambda: screen_obj.add_char(3),
            '-': lambda: screen_obj.add_char('-'),
            '^': lambda: screen_obj.add_char('^')
        })
        self.button_rows_desc.append({
            '0': lambda: screen_obj.add_char(0),
            '.': lambda: screen_obj.add_char('.'),
            '+': lambda: screen_obj.add_char('+'),
            '=': lambda: screen_obj.add_answer(
                solver_obj.calculate(screen_obj.get_expr())          
            ),
            'Adv': mode_changer
        })


class Screen(InterfaceObject):
    def __init__(self):
        super().__init__()
        self.width=24
        self.height=10
        self.font=('Arial', 18)

    def create(self, master):
        pass

    def attach(self):
        self.obj.grid(row=0, column=0, columnspan=6, sticky='w')
        self.obj.focus_set()
        self.obj.configure(state='disable')

    def add_char(self):
        pass

    def get(self):
        pass

    def get_expr(self) -> str:
        self.obj.configure(state='normal')
        answer = self.obj.get()
        self.obj.configure(state='disabled')

        return answer

    def delete_last_position(self):
        self.obj.configure(state='normal')

        if self.obj.get() != 'Invalid Input!':
            temp = self.obj.get()[:-1]
            self.obj.delete(0, tk.END)
            self.obj.insert(0, temp)
        else:
            self.obj.delete(0, tk.END)

        self.obj.configure(state='disabled')
    
    def clear_line(self):
        self.obj.configure(state='normal')
        self.obj.delete(0, tk.END)
        self.obj.configure(state='disabled')

    def add_answer(self, answer):
        pass


class StandartScreen(Screen):
    def __init__(self, master):
        super().__init__()
        self.obj = tk.Entry(master, width=self.width, font=self.font)
        self.attach()

    def add_char(self, char):
        self.obj.configure(state='normal')

        if self.obj.get() == 'Invalid Input!':
            self.obj.delete(0, tk.END)
        self.obj.insert(tk.END, char)

        self.obj.configure(state='disabled')

    def get(self) -> float:
        self.obj.configure(state='normal')

        value_str = self.obj.get()
        try:
            result = float(value_str)
        except Exception as ex:
            self.obj.delete(0, tk.END)
            self.obj.insert(0, 'Is not number!')
            result = 0.0

        self.obj.configure(state='disabled')

        return result

    def add_answer(self, answer):
        self.clear_line()
        self.add_char(answer)


class AdvancedScreen(Screen):
    def __init__(self, master):
        super().__init__()
        self.cur_line = 0
        self.cur_col = 0
        self.lines = list()
        self.lines.append('')
        self.obj = tk.Text(master, width=self.width, height=self.height,
            font=self.font)
        self.attach()
        
    def add_char(self, char):
        char = str(char)
        self.lines[-1] += char

        self.display_lines()

    def clear_line(self):
        self.lines[-1] = ''

        self.display_lines()

    def delete_last_position(self):
        new_val = self.lines[-1][:-1]
        self.lines[-1] = new_val

        self.display_lines()

    def get_expr(self):
        answer = self.lines[-1]

        return answer

    def display_lines(self):
        self.obj.configure(state='normal')
        
        self.obj.delete('1.0', 'end')

        content = ''
        for line in self.lines:
            line = line + '\n'
            content += line
        self.obj.insert('1.0', content)

        self.obj.configure(state='disabled')

    def add_answer(self, answer):
        answer = str(answer)

        if len(self.lines) >= self.height-1:
            self.lines = self.lines[2:]
        self.lines.append(answer)
        self.lines.append('')

        self.display_lines()

    def get(self) -> float:
        try:
            answer = float(self.lines[-1])
        except Exception:
            answer = None
            self.add_answer('ERROR!')

        return answer
        

class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        self.screen = StandartScreen(self.master)
        self.keyboard = StandartKeyboard(self)
        self.memory = Memory(1)
        self.solver = Solver()

        self.create_standart_interface()

    def create_standart_interface(self):
        self.clear_interface()

        self.screen = StandartScreen(self.master)
        self.memory = Memory(self.master, cells_number=1)
        self.solver = Solver()
        self.keyboard = StandartKeyboard(self)
        self.keyboard.bind_buttons(self.memory, self.screen, self.solver, self.change_mode)
        self.keyboard.attach()

        self.grid()

    def create_advanced_interface(self):
        self.clear_interface()

        self.screen = AdvancedScreen(self.master)

        self.memory = Memory(self.master, cells_number=9)

        self.solver = Solver()

        self.keyboard = AdvancedKeyboard(self)
        self.keyboard.bind_buttons(self.memory, self.screen, self.solver, self.change_mode)
        self.keyboard.attach()

        self.grid()

    def change_mode(self):
        if isinstance(self.screen, StandartScreen) and isinstance(self.keyboard, StandartKeyboard):
            self.create_advanced_interface()
        elif isinstance(self.screen, AdvancedScreen) and isinstance(self.keyboard, AdvancedKeyboard):
            self.create_standart_interface()

    def clear_interface(self):
        self.screen.delete()
        self.keyboard.delete()
        self.screen = None
        self.keyboard = None
        self.solver = None


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Calculator')
    root.geometry()

    app = Application(root)
    root.mainloop()
