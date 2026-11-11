import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk

# Configuração de Tema Profissional
ctk.set_appearance_mode("System")  # Segue o modo do Windows (Dark/Light)
ctk.set_default_color_theme("blue")

# Estrutura de Categorias
categorias = [
    "Bíblias",
    "Livros",
    "Brochuras e livretos",
    "Formulários e itens",
    "Folhetos",
    "Revistas para o público"
]

# Dados do Inventário Pré-preenchidos (Estrutura: [Qtd 1, Qtd 2, Qtd 3])
inventario = {cat: {} for cat in categorias}

inventario["Bíblias"] = {
    "(nwt) Tradução do Novo Mundo": [0, 0, 0],
    "(nwtls) TNM (revisada - grande)": [0, 0, 0],
    "(nwtpkt) TNM (revisada - edição pequena)": [0, 0, 0],
    "Outros": [0, 0, 0]
}

inventario["Livros"] = {
    "(be) Beneficie-se": [0, 0, 0],
    "(bhs) Entender a Bíblia!": [0, 0, 0],
    "(bt) Testemunho Cabal": [3, 0, 0],
    "(cf) 'Meu Seguidor'": [0, 0, 0],
    "(cl) Achegue-se": [0, 0, 0],
    "(ia) Imite": [0, 0, 0],
    "(jr) Jeremias e a Mensagem de Deus para Nós": [0, 0, 0],
    "(kr) O Reino de Deus já Governa!": [0, 0, 0],
    "(lfb) Lições da Bíblia": [4, 0, 0],
    "(lff) Seja Feliz para Sempre! (livro)": [30, 0, 0],
    "(lr) Instrutor": [1, 0, 0],
    "(lvs) Continue a Amar a Deus": [16, 0, 0],
    "(od) Organizados": [21, 0, 0],
    "(rr) Adoração Pura": [0, 0, 0],
    "(scl) Princípios Bíblicos para a Vida Cristã": [5, 0, 0],
    "(sjj) Cante de Coração": [0, 0, 0],
    "(sjjls) Cante de Coração (edição grande)": [0, 0, 0],
    "(sjjyls) Cante de Coração — sem pauta": [1, 0, 0],
    "(wcg) Coragem": [12, 0, 0],
    "(yp1) Os Jovens Perguntam, Volume 1": [5, 0, 0],
    "(yp2) Os Jovens Perguntam, Volume 2": [5, 0, 0]
}

inventario["Brochuras e livretos"] = {
    "(ay) Leitura e Escrita": [3, 0, 0],
    "(hf) Família": [0, 0, 0],
    "(hl) Vida Feliz": [0, 0, 0],
    "(la) Vida Satisfatória": [0, 0, 0],
    "(lc) A Vida -- Teve um Criador?": [6, 0, 0],
    "(ld) Escute a Deus": [300, 0, 0],
    "(lf) Origem da Vida": [0, 0, 0],
    "(lffi) Seja Feliz para Sempre! (brochura)": [690, 0, 0],
    "(ll) Escute e Viva": [5, 0, 0],
    "(lmd) Ame as Pessoas": [1, 0, 0],
    "(mb) Minhas Primeiras Lições da Bíblia": [4, 0, 0],
    "(pc) Verdadeira Paz e Felicidade": [0, 0, 0],
    "(ph) Caminho": [0, 0, 0],
    "(rk) Verdadeira Fé": [0, 0, 0],
    "(sp) Espíritos dos Mortos": [0, 0, 0],
    "(th) Melhore": [9, 0, 0],
    "(wfg) Aprenda com a Sabedoria de Jesus": [83, 0, 0],
    "(ypq) 10 Perguntas": [0, 0, 0],
    "Outros": [0, 0, 0]
}


class ModernInventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inventário Campinho/Praça Seca v1.02")
        self.geometry("1150x700")
        self.minsize(1000, 620)

        self.categoria_atual = "Bíblias"
        self.item_selecionado = None

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._criar_menu_lateral()
        self._criar_painel_principal()
        self._criar_painel_detalhes()

        self.selecionar_categoria("Bíblias")

    def _criar_menu_lateral(self):
        """ Painel Lateral Esquerdo """
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="📦 Inventário\nv1.02",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        self.cat_buttons = {}
        for index, cat in enumerate(categorias, start=1):
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=cat,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color="#1f538d",
                height=38,
                font=ctk.CTkFont(size=13),
                command=lambda c=cat: self.selecionar_categoria(c)
            )
            btn.grid(row=index, column=0, padx=10, pady=2, sticky="ew")
            self.cat_buttons[cat] = btn

        self.reset_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="🔄 Iniciar Contagem",
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=36,
            command=self.iniciar_contagem
        )
        self.reset_btn.grid(row=9, column=0, padx=15, pady=(10, 5), sticky="ew")

        self.export_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="📥 Exportar CSV",
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            command=self.exportar_csv
        )
        self.export_btn.grid(row=10, column=0, padx=15, pady=(5, 20), sticky="ew")

    def _criar_painel_principal(self):
        """ Área Central """
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        self.lbl_titulo_cat = ctk.CTkLabel(
            self.header_frame,
            text="Bíblias",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl_titulo_cat.pack(side="left")

        self.lbl_total_cat = ctk.CTkLabel(
            self.header_frame,
            text="Total de itens: 0",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.lbl_total_cat.pack(side="right", padx=10)

        # Barra de Pesquisa e Botões Compactos Azuis
        self.action_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.action_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.action_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.action_bar,
            placeholder_text="🔍 Pesquisar publicação nesta categoria...",
            height=32
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.atualizar_lista_itens())

        # Botões Azuis Compactos
        self.btn_add = ctk.CTkButton(
            self.action_bar,
            text="+ Novo",
            width=75,
            height=32,
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.adicionar_item
        )
        self.btn_add.grid(row=0, column=1, padx=(0, 5))

        self.btn_remove = ctk.CTkButton(
            self.action_bar,
            text="🗑️ Remover",
            width=90,
            height=32,
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.remover_item
        )
        self.btn_remove.grid(row=0, column=2, padx=(0, 5))

        self.btn_qr = ctk.CTkButton(
            self.action_bar,
            text="📷 QR Code",
            width=90,
            height=32,
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.scan_qr_code
        )
        self.btn_qr.grid(row=0, column=3)

        self.items_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Itens Cadastrados")
        self.items_scroll_frame.grid(row=2, column=0, sticky="nsew")
        self.items_scroll_frame.grid_columnconfigure(0, weight=1)

    def _criar_painel_detalhes(self):
        """ Painel Direito para Capa """
        self.details_frame = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.details_frame.grid(row=0, column=2, padx=(0, 20), pady=20, sticky="nsew")
        self.details_frame.grid_propagate(False)

        lbl_painel = ctk.CTkLabel(
            self.details_frame,
            text="Capa da Publicação",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lbl_painel.pack(pady=(20, 10))

        self.img_box = ctk.CTkLabel(
            self.details_frame,
            text="Selecione um item\npara visualizar",
            width=210,
            height=280,
            fg_color=("gray85", "gray25"),
            corner_radius=8
        )
        self.img_box.pack(padx=20, pady=10)

        self.lbl_info_nome = ctk.CTkLabel(
            self.details_frame,
            text="-",
            font=ctk.CTkFont(size=13, weight="bold"),
            wraplength=210
        )
        self.lbl_info_nome.pack(pady=(10, 2))

        self.lbl_info_codigo = ctk.CTkLabel(
            self.details_frame,
            text="Código: N/A",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.lbl_info_codigo.pack(pady=(0, 15))

    def selecionar_categoria(self, cat):
        self.categoria_atual = cat
        self.lbl_titulo_cat.configure(text=cat)

        for c_name, btn in self.cat_buttons.items():
            if c_name == cat:
                btn.configure(fg_color="#1f538d", text_color="white", font=ctk.CTkFont(size=13, weight="bold"))
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"), font=ctk.CTkFont(size=13))

        self.atualizar_lista_itens()

    def atualizar_lista_itens(self):
        """ Renderiza os cards com Fonte Maior no Nome e 3 Campos Menores de Qtd """
        for widget in self.items_scroll_frame.winfo_children():
            widget.destroy()

        termo_busca = self.search_entry.get().lower().strip()
        itens_cat = inventario.get(self.categoria_atual, {})

        total_unidades = sum(sum(q) for q in itens_cat.values())
        self.lbl_total_cat.configure(text=f"Total no Estoque: {total_unidades} unid.")

        row_idx = 0
        for nome_item, qtds in itens_cat.items():
            if termo_busca and termo_busca not in nome_item.lower():
                continue

            card = ctk.CTkFrame(self.items_scroll_frame, height=52)
            card.grid(row=row_idx, column=0, sticky="ew", padx=5, pady=4)
            card.grid_columnconfigure(0, weight=1)

            # Nome da Publicação com FONTE MAIOR (15pt Bold)
            btn_item = ctk.CTkButton(
                card,
                text=nome_item,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray30"),
                font=ctk.CTkFont(size=15, weight="bold"),
                command=lambda n=nome_item: self.selecionar_item(n)
            )
            btn_item.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

            # Container dos 3 Campos de Quantidade + Total
            ctrl_frame = ctk.CTkFrame(card, fg_color="transparent")
            ctrl_frame.grid(row=0, column=1, padx=10)

            entries = []
            for i in range(3):
                e = ctk.CTkEntry(ctrl_frame, width=42, height=28, justify="center", font=ctk.CTkFont(size=11))
                e.insert(0, str(qtds[i]))
                e.pack(side="left", padx=2)
                e.bind("<FocusOut>", lambda ev, n=nome_item, idx=i, entry=e: self.atualizar_qtd_campo(n, idx, entry.get()))
                e.bind("<Return>", lambda ev, n=nome_item, idx=i, entry=e: self.atualizar_qtd_campo(n, idx, entry.get()))
                entries.append(e)

            # Rótulo com o Total Calculado da Publicação
            total_item = sum(qtds)
            lbl_total_item = ctk.CTkLabel(
                ctrl_frame,
                text=f"Total: {total_item}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#1f538d",
                width=65
            )
            lbl_total_item.pack(side="left", padx=(6, 2))

            row_idx += 1

    def atualizar_qtd_campo(self, nome_item, index, valor_str):
        if valor_str.isdigit():
            inventario[self.categoria_atual][nome_item][index] = int(valor_str)
        self.atualizar_lista_itens()

    def selecionar_item(self, nome_item):
        self.item_selecionado = nome_item
        self.lbl_info_nome.configure(text=nome_item)

        codigo = None
        if nome_item.startswith("("):
            fim = nome_item.find(")")
            if fim != -1:
                codigo = nome_item[1:fim].lower()

        self.lbl_info_codigo.configure(text=f"Código: {codigo.upper() if codigo else 'N/A'}")

        if codigo:
            caminho_png = os.path.join("imagens", f"{codigo}.png")
            caminho_jpg = os.path.join("imagens", f"{codigo}.jpg")

            caminho_final = caminho_png if os.path.exists(caminho_png) else (
                caminho_jpg if os.path.exists(caminho_jpg) else None)

            if caminho_final:
                try:
                    pil_img = Image.open(caminho_final)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(160, 230))
                    self.img_box.configure(image=ctk_img, text="")
                    return
                except Exception as e:
                    print(f"Erro imagem: {e}")

        self.img_box.configure(image="", text="Imagem indisponível\n(imagens/codigo.png)")

    def adicionar_item(self):
        dialog = ctk.CTkInputDialog(text="Digite o nome da publicação:\n(Ex: '(code) Nome do Livro')", title="Novo Item")
        nome = dialog.get_input()
        if nome:
            nome = nome.strip()
            if nome in inventario[self.categoria_atual]:
                messagebox.showwarning("Aviso", "Este item já existe nesta categoria!")
                return
            inventario[self.categoria_atual][nome] = [0, 0, 0]
            self.atualizar_lista_itens()

    def remover_item(self):
        """ Remove o item selecionado da categoria atual """
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Clique no nome de uma publicação para selecioná-la antes de remover.")
            return

        if self.item_selecionado not in inventario[self.categoria_atual]:
            messagebox.showwarning("Aviso", "A publicação selecionada não pertence a esta categoria.")
            return

        confirmacao = messagebox.askyesno(
            "Confirmar Remoção",
            f"Deseja realmente remover '{self.item_selecionado}' da categoria '{self.categoria_atual}'?"
        )
        if confirmacao:
            del inventario[self.categoria_atual][self.item_selecionado]
            self.item_selecionado = None
            self.lbl_info_nome.configure(text="-")
            self.lbl_info_codigo.configure(text="Código: N/A")
            self.img_box.configure(image="", text="Selecione um item\npara visualizar")
            self.atualizar_lista_itens()
            messagebox.showinfo("Sucesso", "Publicação removida com sucesso!")

    def scan_qr_code(self):
        """ Leitor de QR Code usando Webcam e OpenCV """
        try:
            import cv2
        except ImportError:
            messagebox.showerror(
                "Biblioteca Ausente",
                "Para utilizar o leitor de QR Code, instale o OpenCV executando no terminal:\n\npip install opencv-python"
            )
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Erro de Câmera", "Não foi possível acessar a webcam.")
            return

        detector = cv2.QRCodeDetector()
        codigo_encontrado = None

        messagebox.showinfo("Scanner de QR Code", "Aponte o QR Code para a câmera.\nA janela fechará automaticamente ao identificar.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            data, bbox, _ = detector.detectAndDecode(frame)
            if data:
                codigo_encontrado = data.strip()
                break

            cv2.imshow("Scanner QR Code - Pressione ESC para cancelar", frame)
            if cv2.waitKey(1) == 27:  # Tecla ESC
                break

        cap.release()
        cv2.destroyAllWindows()

        if codigo_encontrado:
            # Tenta localizar a publicação pelo código lido
            self._localizar_por_qrcode(codigo_encontrado)

    def _localizar_por_qrcode(self, texto_qr):
        """ Procura a publicação no inventário correspondente ao texto/link do QR Code """
        texto_lower = texto_qr.lower()
        encontrado = False

        for cat, itens in inventario.items():
            for item in itens:
                sigla = None
                if item.startswith("("):
                    fim = item.find(")")
                    if fim != -1:
                        sigla = item[1:fim].lower()

                if sigla and (sigla in texto_lower or sigla == texto_lower):
                    self.selecionar_categoria(cat)
                    self.selecionar_item(item)
                    messagebox.showinfo("QR Code Lido!", f"Publicação encontrada:\n\n{item}")
                    encontrado = True
                    break
            if encontrado:
                break

        if not encontrado:
            messagebox.showwarning("Não Encontrado", f"Nenhuma publicação cadastrada corresponde ao código lido:\n'{texto_qr}'")

    def iniciar_contagem(self):
        resposta = messagebox.askyesno(
            "Iniciar Contagem",
            "Deseja zerar todas as quantidades do inventário para iniciar uma nova contagem?\n\nEsta ação zerará o estoque de todos os itens."
        )
        if resposta:
            for cat in inventario:
                for item in inventario[cat]:
                    inventario[cat][item] = [0, 0, 0]
            self.atualizar_lista_itens()
            messagebox.showinfo("Contagem Iniciada", "Todas as quantidades foram zeradas. Boa contagem!")

    def exportar_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="relatorio_inventario_campinho_v1.02.csv",
            title="Exportar Relatório",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow(["Categoria", "Publicacao", "Qtd 1", "Qtd 2", "Qtd 3", "Total"])

                    total_geral = 0
                    for cat, items in inventario.items():
                        for item, (q1, q2, q3) in items.items():
                            t = q1 + q2 + q3
                            writer.writerow([cat, item, q1, q2, q3, t])
                            total_geral += t
                    writer.writerow(["", "", "", "", "", ""])
                    writer.writerow(["TOTAL GERAL", "", "", "", "", total_geral])
                messagebox.showinfo("Sucesso", f"Relatório exportado em:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar:\n{e}")


if __name__ == "__main__":
    app = ModernInventoryApp()
    app.mainloop()