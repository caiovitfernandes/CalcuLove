import tkinter as tk
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkinter import simpledialog
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import pickle
import os
from tkinter import ttk

color_map = {
    "Azul": "blue",
    "Rosa": "#ff69b4",
    "Preto": "black",
    "Amarelo": "#ffffe0"
}


def choose_reference_date():
    while True:
        reference_datetime_str = simpledialog.askstring("Quando é o Aniversário?", "Insira a data em que o relacionamento começou. ATENÇÃO!!! A data e a hora devem estar no formato dd/mm/aaaa hh:mm", parent=root)
        try:
            reference_datetime = datetime.strptime(reference_datetime_str, "%d/%m/%Y %H:%M")
            break
        except ValueError:
            messagebox.showerror("Formato inválido", "Por favor insira a data e hora no formato dd/mm/aaaa hh:mm")
    return reference_datetime

def update_reference_date():
    new_reference_date = choose_reference_date()
    save_reference_date(new_reference_date)
    update_time()


def save_reference_date(date):
    with open('reference_date.pkl', 'wb') as file:
        pickle.dump(date, file)

def load_reference_date():
    if os.path.exists('reference_date.pkl'):
        with open('reference_date.pkl', 'rb') as file:
            reference_date = pickle.load(file)
            return reference_date
    else:
        return None

def update_time():
    reference_date = load_reference_date()
    now = datetime.now()
    delta = relativedelta(now, reference_date)
    bg_color = load_bg_color()
    if bg_color:
        mapped_color = color_map.get(bg_color)
        root.configure(bg=mapped_color)
    time_label.config(text=f"Já estamos juntos há:\n{delta.years} anos, {delta.months} meses, {delta.days} dias, {delta.hours} horas, {delta.minutes} minutos e {delta.seconds} segundos.")
    root.after(1000, update_time)


def on_closing():
    root.destroy()

def change_background_color(event):
    selected_color = color_combobox.get()
    mapped_color = color_map.get(selected_color)
    if mapped_color:
        root.configure(bg=mapped_color)
        if selected_color == "Amarelo":
            time_label.configure(bg=mapped_color,fg='black')
            alterar_data_button.configure(bg=mapped_color,fg='black')
            exit_button.configure(bg=mapped_color,fg='black')
        else:
            time_label.configure(bg=mapped_color,fg='white')
            alterar_data_button.configure(bg=mapped_color,fg='white')
            exit_button.configure(bg=mapped_color,fg='white')
        save_bg_color(selected_color)


def save_bg_color(color):
    mapped_color = color_map.get(color)
    with open('bg_color.pkl', 'wb') as file:
        pickle.dump(mapped_color, file)

        
def load_bg_color():
    if os.path.exists('bg_color.pkl'):
        with open('bg_color.pkl', 'rb') as file:
            color = pickle.load(file)
            return color
    else:
        return None


# data/hora de referência (19 de setembro de 2019 às 21:00)
reference_date = load_reference_date()

# criar a janela principal
root = tk.Tk()
root.title("CalcuLove")
root.configure(bg='#ff69b4') # alterando a cor de fundo da janela
root.overrideredirect(True)
root.geometry("250x100+10+10")
root.attributes("-topmost", True)
root.attributes("-alpha", 1)


#códigos para transparência
def on_focusout(event):
    root.attributes("-alpha", 0.2)

def on_focusin(event):
    root.attributes("-alpha", 1)

root.bind("<FocusOut>", on_focusout)
root.bind("<FocusIn>", on_focusin)

# Verificar se o arquivo de configuração existe
if os.path.exists('reference_date.pkl'):
    reference_date = load_reference_date()
else:
    root.lift()
    reference_date = choose_reference_date()
    save_reference_date(reference_date)

# criar a label para mostrar a diferença
time_label = tk.Label(root, font=("Comic Sans MS", 10, "bold"), fg="white", bg='#ff69b4')
time_label.pack()

# criar botão sair
alterar_data_button = tk.Button(root, text="Alterar data", font=("Comic Sans MS", 7), command=update_reference_date,bg='#ff69b4')
exit_button = tk.Button(root, text="Sair", font=("Comic Sans MS", 7), command=on_closing,bg='#ff69b4')
exit_button.pack(side='left')
alterar_data_button.pack(side='right')

exit_button.config(padx=70)
alterar_data_button.config(padx=60)

#Criando o dropdown de cores
background_colors = ["Azul", "Rosa", "Preto", "Amarelo"]

# carregando a cor de fundo
color = load_bg_color()
if color:
    root.configure(bg=color)
    time_label.configure(bg=color)
    alterar_data_button.configure(bg=color)
    exit_button.configure(bg=color)

if color:
    mapped_color = color_map.get(color)
    root.configure(bg=mapped_color)
    if color == "#ffffe0":
        time_label.configure(fg='black')
        alterar_data_button.configure(fg='black')
        exit_button.configure(fg='black')
    else:
        time_label.configure(fg='white')
        alterar_data_button.configure(fg='white')
        exit_button.configure(fg='white')

var = tk.StringVar()
color_combobox = ttk.Combobox(root, values=background_colors, textvariable = var)
color_combobox.set("Fundo:")
color_combobox.pack(side = 'bottom')
color_combobox.config(width=6, height=5)
color_combobox.config(exportselection=False)

color_combobox.bind("<<ComboboxSelected>>", change_background_color)

# pegando as medidas da tela
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# pegando as medidas da janela
window_width = int(screen_width*0.32)
window_height = int(screen_height*0.10)

# definindo as posições x e y
pos_x = screen_width - window_width
pos_y = screen_height - window_height -40

# definindo o tamanho e posição da janela
root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

# atualizar a label pela primeira vez
update_time()

# iniciar o loop de eventos
root.mainloop()
