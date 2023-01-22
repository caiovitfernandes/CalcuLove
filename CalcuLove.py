import tkinter as tk
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkinter import simpledialog
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import pickle
import os
from tkinter import ttk


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
    time_label.config(text=f"Já estamos juntos há:\n{delta.years} anos, {delta.months} meses, {delta.days} dias, {delta.hours} horas, {delta.minutes} minutos e {delta.seconds} segundos.")
    root.after(1000, update_time)


def on_closing():
    root.destroy()

def change_background_color(event):
    selected_color = color_combobox.get()
    if selected_color == "Azul":
        root.configure(bg='blue')
        time_label.config(bg='blue')
        alterar_data_button.config(bg='blue')
        exit_button.config(bg='blue')
    elif selected_color == "Rosa":
        root.configure(bg='#ff69b4')
        time_label.config(bg='#ff69b4')
        alterar_data_button.config(bg='#ff69b4')
        exit_button.config(bg='#ff69b4')
    elif selected_color == "Preto":
        root.configure(bg='black')
        time_label.config(bg='black',fg='white')
        alterar_data_button.config(bg='black',fg='white')
        exit_button.config(bg='black',fg='white')
    elif selected_color == "Amarelo":
        root.configure(bg='#ffffe0')
        time_label.config(bg='#ffffe0',fg='black')
        alterar_data_button.config(bg='#ffffe0',fg='black')
        exit_button.config(bg='#ffffe0',fg='black')


# data/hora de referência (19 de setembro de 2019 às 21:00)
reference_date = load_reference_date()

# carregando o arquivo de ícone


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
