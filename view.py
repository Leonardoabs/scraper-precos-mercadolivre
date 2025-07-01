import customtkinter as ctk
from os import getlogin

# Cores
AZUL_ML = "#1A237E"
BRANCO = "#FFFFFF"
VERDE_SUAVE = "#388E3C"
VERMELHO_ERRO = "#b30000"
CINZA_CLARO = "#E0E0E0"


class ScraperMl(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mercado Livre Scraper")
        self.geometry("440x320")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=BRANCO)

        self.hostname = getlogin()
        self.create_widgets()

    def create_widgets(self):
        # Título principal
        self.label_title = ctk.CTkLabel(
            self,
            text=f"Olá, {self.hostname} 👋",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=AZUL_ML
        )
        self.label_title.pack(pady=(30, 5))

        # Subtítulo
        self.label_subtitle = ctk.CTkLabel(
            self,
            text="Mercado Livre Price Scraper",
            font=ctk.CTkFont(size=16),
            text_color=AZUL_ML
        )
        self.label_subtitle.pack(pady=(0, 25))

        # Entry para busca com borda sutil
        self.entry_search = ctk.CTkEntry(
            self,
            placeholder_text="Termo para busca (ex: garrafa)",
            font=ctk.CTkFont(size=14),
            fg_color=BRANCO,
            text_color=AZUL_ML,
            border_color=CINZA_CLARO,
            border_width=1,
            corner_radius=6,
            height=35,
            justify="left"
        )
        self.entry_search.pack(padx=40, pady=(0, 10), fill="x")

        # Entry para número de páginas com borda sutil
        self.entry_pages = ctk.CTkEntry(
            self,
            placeholder_text="Número de páginas (ex: 1)",
            font=ctk.CTkFont(size=14),
            fg_color=BRANCO,
            text_color=AZUL_ML,
            border_color=CINZA_CLARO,
            border_width=1,
            corner_radius=6,
            height=35,
            justify="left"
        )
        self.entry_pages.pack(padx=40, pady=(0, 20), fill="x")

        # Botão de ação
        self.button_scrape = ctk.CTkButton(
            self,
            text="Iniciar Coleta",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=AZUL_ML,
            hover_color="#122066",
            corner_radius=8,
            height=40,
            width=150
        )
        self.button_scrape.pack(pady=(0, 15))

        # Label de status
        self.label_status = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=AZUL_ML,
            anchor="w"
        )
        self.label_status.pack(padx=40, fill="x")

    def set_status(self, message, error=False):
        color = VERMELHO_ERRO if error else VERDE_SUAVE
        self.label_status.configure(text=message, text_color=color)
