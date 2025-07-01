import threading
from model import scraper_ml
from view import ScraperMl


class ScraperController:
    def __init__(self):
        self.view = ScraperMl()
        self.view.button_scrape.configure(command=self.start_scraper)

    def start_scraper(self):
        termo = self.view.entry_search.get().strip().replace(" ", "-")
        paginas = self.view.entry_pages.get().strip()

        if not termo:
            self.view.set_status("Digite um termo para busca!")
            return

        if not paginas.isdigit() or int(paginas) < 1:
            self.view.set_status("Número de páginas inválido!")
            return

        self.view.set_status("Iniciando coleta...")

        thread = threading.Thread(target=self.run_scraper,
                                  args=(termo, int(paginas)), daemon=True)
        thread.start()

    def run_scraper(self, termo, paginas):
        try:
            arquivo = scraper_ml(termo, paginas)
            self.view.set_status(
                f"Coleta finalizada! Arquivo salvo: {arquivo}")

        except Exception as e:
            self.view.set_status(f"Erro: {e}")

    def run(self):
        self.view.mainloop()


ScraperController().run()
