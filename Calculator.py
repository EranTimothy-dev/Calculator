#Importing libraries
import tkinter as tk


#initializing colors and fonts
Light_gray = "#F5F5F5"
Label_color = "#25265E"
White = "#FFFFFF"
Off_white = "#F8FAFF"
Light_blue = "#CCEDFF"

Small_font_style = ("Arial", 16)
Large_font_style = ("Arial", 40, "bold")
Digits_font_style= ("Arial", 24, "bold")
Default_font_style= ("Arial", 20)

#Class that contains components and functionality of the calculator
class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("370x500")#375x667
        self.window.resizable(0,0)#Disable resizing for this window
        self.window.title("Calculator")#Name of app

        #to add display labels in the textbox
        self.total_expression = ""
        self.current_expression = ""

        #create 2 frames one for the display and other for the buttons
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits ={
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            0:(4,2), '.':(4,1)
            }
        
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)#For the zero row
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x, weight=1)#since weight was given a non zero value it can expand to the whole frame
            self.buttons_frame.columnconfigure(x, weight=1)
            
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()
    
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digits = key: self.add_to_expression(digits))
        for key in self.operations:
            self.window.bind(key, lambda event, operator = key: self.append_operator(operator))


    def create_special_buttons(self):#if methods not initialized it will not show on cal
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()


    #method to create display labels to display the calculations and its output
    def create_display_labels(self):
        #for total label
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=Light_gray, fg=Label_color, 
                               padx=24, font=Small_font_style)#anchor=tk.E positions the text to the right(East) side of the page
        total_label.pack(expand=True, fill="both")

        #for current label
        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=Light_gray, fg=Label_color, 
                               padx=24, font=Large_font_style)#anchor=tk.E positions the text to the right(East) side of the page
        label.pack(expand=True, fill="both")

        return total_label, label

    #define ubove 2 methods
    def create_display_frame(self):
        #since this is made inside the main window we use self.window
        frame = tk.Frame(self.window, height = 221, bg = Light_gray)
        frame.pack(expand = True, fill = "both")#these arguments will allow us to expand and fill any empty space around it
        return frame
    
    #method to add a given value the current expression
    def add_to_expression(self, value):#this method will take in a value
        self.current_expression += str(value)#append given value to the current expression but convert to string since can only concatenate str not int
        self.update_label()#method made below to update current expression

        
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=White, fg=Label_color, #place the digits in the dict in the buttons frame and convert to string
                               font=Digits_font_style, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))#use lambda function since command should be a function and not a method
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)#use the values in the dict to set the placement of numbers
            #NSEW - North, South, East, West. Argument is used so that buttons stick to all sides and fills up the entire pixel
             
    def create_operator_buttons(self):
        i = 0#the operators shuld be placed in the 4 th column button before the last row of digit button
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=Off_white, fg=Label_color, font=Default_font_style, 
                               borderwidth=0, command= lambda x=operator : self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1#creates each button in another row as for loop runs

    #append operator to current expression, and then append it to the total expression then clear the current expression for the next expression
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        #updating
        self.update_total_label()
        self.update_label()

    #create functionality for the clear sign
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=Off_white, fg=Label_color, font=Default_font_style, 
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=Off_white, fg=Label_color, font=Default_font_style, 
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=Off_white, fg=Label_color, font=Default_font_style, 
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    #create functionality for the equals sign
    def evaluate(self):
        self.total_expression += self.current_expression #sets the big value to the smaller value area
        self.update_total_label()#updates the above line accordingly

        try:    
            self.current_expression = str(eval(self.total_expression))#eval function computes the given numbers even if its a string
            self.total_expression = "" #clear the total expression
        except:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=Light_blue, fg=Label_color, font=Default_font_style, 
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)
      
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand = True, fill="both")
        return frame
    
    #methods to update the total and current values displayed in the create_display_frame
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])#the slicer makes sure the answer doesn't go past the given text area, A.K.A truncating the answer


    #method to run the window
    def run(self):
        self.window.mainloop()


if __name__ == "__main__" :
    #create object called calc
    calc = Calculator()
    calc.run()#run method of calc

