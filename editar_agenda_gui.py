#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface gráfica para editar os dados da agenda da Federação de SAFs
"""

import json
import os
import shutil
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk

try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class EditorAgendaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Agenda - Federação de SAFs")
        self.root.geometry("1000x700")

        self.dados = None
        self.arquivo_atual = 'agenda_data.json'

        # Criar menu
        self.criar_menu()

        # Criar barra de ferramentas com botões
        self.criar_barra_ferramentas()

        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Carregar dados
        self.carregar_dados()

        # Criar abas
        self.criar_abas()

    def criar_menu(self):
        """Cria o menu principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Abrir...", command=self.abrir_arquivo)
        menu_arquivo.add_command(
            label="Salvar", command=self.salvar_dados, accelerator="Ctrl+S"
        )
        menu_arquivo.add_command(label="Salvar como...", command=self.salvar_como)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(
            label="Gerar Word", command=self.gerar_word, accelerator="Ctrl+G"
        )
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.root.quit)

        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)

        # Atalhos de teclado
        self.root.bind('<Control-s>', lambda e: self.salvar_dados())
        self.root.bind('<Control-S>', lambda e: self.salvar_dados())
        self.root.bind('<Control-g>', lambda e: self.gerar_word())
        self.root.bind('<Control-G>', lambda e: self.gerar_word())

    def criar_barra_ferramentas(self):
        """Cria barra de ferramentas com botões de ação"""
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)

        # Botão Salvar
        btn_salvar = ttk.Button(
            toolbar_frame, text="💾 Salvar", command=self.salvar_dados, width=15
        )
        btn_salvar.pack(side=tk.LEFT, padx=2)

        # Botão Gerar Word
        btn_gerar = ttk.Button(
            toolbar_frame, text="📄 Gerar Word", command=self.gerar_word, width=15
        )
        btn_gerar.pack(side=tk.LEFT, padx=2)

        # Separador
        separator = ttk.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Label de status
        self.status_label = ttk.Label(
            toolbar_frame, text="Pronto", relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_label.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)

    def carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        try:
            with open(self.arquivo_atual, 'r', encoding='utf-8') as f:
                self.dados = json.load(f)
        except FileNotFoundError:
            messagebox.showerror(
                "Erro", f"Arquivo '{self.arquivo_atual}' não encontrado!"
            )
            self.dados = self.criar_estrutura_vazia()
        except json.JSONDecodeError as e:
            messagebox.showerror("Erro", f"Erro ao ler JSON: {e}")
            self.dados = self.criar_estrutura_vazia()

    def criar_estrutura_vazia(self):
        """Cria uma estrutura vazia de dados"""
        return {
            "ano": datetime.now().year,
            "presidente": {"nome": "", "mensagem": ""},
            "diretoria": [],
            "safs": [],
            "atividades_realizadas_2023": [],
            "atividades_planejadas_2024": {
                "janeiro": [],
                "fevereiro": [],
                "marco": [],
                "abril": [],
                "maio": [],
                "junho": [],
                "julho": [],
                "agosto": [],
                "setembro": [],
                "outubro": [],
                "novembro": [],
                "dezembro": [],
            },
            "informacoes_gerais": {
                "missionario_oracao": {
                    "nome": "",
                    "data_nascimento": "",
                    "campo": "",
                    "whatsapp": "",
                },
                "observacoes": [],
                "lema": [],
            },
        }

    def criar_abas(self):
        """Cria todas as abas do editor"""
        # Aba 1: Informações Gerais
        self.aba_info = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_info, text="Informações Gerais")
        self.criar_aba_info_gerais()

        # Aba 2: Diretoria
        self.aba_diretoria = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_diretoria, text="Diretoria")
        self.criar_aba_diretoria()

        # Aba 3: SAFs
        self.aba_safs = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_safs, text="SAFs")
        self.criar_aba_safs()

        # Aba 4: Atividades Planejadas
        self.aba_atividades_planejadas = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_atividades_planejadas, text="Atividades Planejadas")
        self.criar_aba_atividades_planejadas()

        # Aba 5: Atividades Realizadas
        self.aba_atividades_realizadas = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_atividades_realizadas, text="Atividades Realizadas")
        self.criar_aba_atividades_realizadas()

        # Aba 6: Informações Gerais (Missionário, Observações)
        self.aba_info_gerais = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_info_gerais, text="Outras Informações")
        self.criar_aba_outras_info()

    def criar_aba_info_gerais(self):
        """Cria a aba de informações gerais"""
        frame = ttk.LabelFrame(self.aba_info, text="Dados Principais", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Ano
        ttk.Label(frame, text="Ano:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ano_var = tk.StringVar(value=str(self.dados.get('ano', '')))
        ttk.Entry(frame, textvariable=self.ano_var, width=10).grid(
            row=0, column=1, sticky=tk.W, pady=5
        )

        # Nome da Presidente
        ttk.Label(frame, text="Nome da Presidente:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.presidente_nome_var = tk.StringVar(
            value=self.dados.get('presidente', {}).get('nome', '')
        )
        ttk.Entry(frame, textvariable=self.presidente_nome_var, width=50).grid(
            row=1, column=1, sticky=tk.W, pady=5
        )

        # Foto da Presidente
        ttk.Label(frame, text="Foto da Presidente:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.presidente_foto_var = tk.StringVar(
            value=self.dados.get('presidente', {}).get('foto', '')
        )
        foto_entry_pres = ttk.Entry(
            frame, textvariable=self.presidente_foto_var, width=40
        )
        foto_entry_pres.grid(row=2, column=1, sticky=tk.W, pady=5)

        def selecionar_foto_presidente():
            arquivo = filedialog.askopenfilename(
                title="Selecionar Foto da Presidente",
                filetypes=[
                    ("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("Todos os arquivos", "*.*"),
                ],
            )
            if arquivo:
                nome_arquivo = self.copiar_foto_para_pasta_fotos(arquivo)
                if nome_arquivo:
                    self.presidente_foto_var.set(nome_arquivo)

        ttk.Button(
            frame, text="Selecionar Foto", command=selecionar_foto_presidente
        ).grid(row=2, column=1, sticky=tk.E, padx=5)

        # Mensagem da Presidente
        ttk.Label(frame, text="Mensagem da Presidente:").grid(
            row=3, column=0, sticky=tk.NW, pady=5
        )
        self.presidente_mensagem_text = scrolledtext.ScrolledText(
            frame, width=60, height=15, wrap=tk.WORD
        )
        self.presidente_mensagem_text.grid(row=3, column=1, sticky=tk.W, pady=5)
        self.presidente_mensagem_text.insert(
            '1.0', self.dados.get('presidente', {}).get('mensagem', '')
        )

    def criar_aba_diretoria(self):
        """Cria a aba de diretoria"""
        # Frame principal com scroll
        main_frame = ttk.Frame(self.aba_diretoria)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame de botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            btn_frame, text="Adicionar Membro", command=self.adicionar_membro_diretoria
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Editar Selecionado", command=self.editar_membro_diretoria
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Remover Selecionado", command=self.remover_membro_diretoria
        ).pack(side=tk.LEFT, padx=5)

        # Treeview para lista
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_diretoria = ttk.Treeview(
            tree_frame,
            columns=('Cargo', 'Nome', 'DN', 'Email'),
            show='headings',
            height=15,
        )
        self.tree_diretoria.heading('Cargo', text='Cargo')
        self.tree_diretoria.heading('Nome', text='Nome')
        self.tree_diretoria.heading('DN', text='Data Nasc.')
        self.tree_diretoria.heading('Email', text='Email')

        self.tree_diretoria.column('Cargo', width=200)
        self.tree_diretoria.column('Nome', width=250)
        self.tree_diretoria.column('DN', width=100)
        self.tree_diretoria.column('Email', width=200)

        scrollbar_diretoria = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree_diretoria.yview
        )
        self.tree_diretoria.configure(yscrollcommand=scrollbar_diretoria.set)

        self.tree_diretoria.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_diretoria.pack(side=tk.RIGHT, fill=tk.Y)

        self.atualizar_lista_diretoria()

    def criar_aba_safs(self):
        """Cria a aba de SAFs"""
        main_frame = ttk.Frame(self.aba_safs)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Adicionar SAF", command=self.adicionar_saf).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Editar Selecionada", command=self.editar_saf).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            btn_frame, text="Remover Selecionada", command=self.remover_saf
        ).pack(side=tk.LEFT, padx=5)

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_safs = ttk.Treeview(
            tree_frame,
            columns=('Num', 'Nome', 'Presidente', 'Pastor'),
            show='headings',
            height=15,
        )
        self.tree_safs.heading('Num', text='#')
        self.tree_safs.heading('Nome', text='Nome da SAF')
        self.tree_safs.heading('Presidente', text='Presidente')
        self.tree_safs.heading('Pastor', text='Pastor')

        self.tree_safs.column('Num', width=50)
        self.tree_safs.column('Nome', width=300)
        self.tree_safs.column('Presidente', width=200)
        self.tree_safs.column('Pastor', width=200)

        scrollbar_safs = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree_safs.yview
        )
        self.tree_safs.configure(yscrollcommand=scrollbar_safs.set)

        self.tree_safs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_safs.pack(side=tk.RIGHT, fill=tk.Y)

        self.atualizar_lista_safs()

    def criar_aba_atividades_planejadas(self):
        """Cria a aba de atividades planejadas"""
        main_frame = ttk.Frame(self.aba_atividades_planejadas)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame de seleção de mês
        mes_frame = ttk.LabelFrame(main_frame, text="Selecionar Mês", padding=10)
        mes_frame.pack(fill=tk.X, pady=5)

        self.mes_var = tk.StringVar(value="janeiro")
        meses = [
            'janeiro',
            'fevereiro',
            'marco',
            'abril',
            'maio',
            'junho',
            'julho',
            'agosto',
            'setembro',
            'outubro',
            'novembro',
            'dezembro',
        ]
        meses_nomes = [
            'Janeiro',
            'Fevereiro',
            'Março',
            'Abril',
            'Maio',
            'Junho',
            'Julho',
            'Agosto',
            'Setembro',
            'Outubro',
            'Novembro',
            'Dezembro',
        ]

        mes_combo = ttk.Combobox(
            mes_frame,
            textvariable=self.mes_var,
            values=meses_nomes,
            state='readonly',
            width=20,
        )
        mes_combo.pack(side=tk.LEFT, padx=5)
        mes_combo.bind(
            '<<ComboboxSelected>>',
            lambda e: self.atualizar_lista_atividades_planejadas(),
        )

        btn_frame = ttk.Frame(mes_frame)
        btn_frame.pack(side=tk.LEFT, padx=10)

        ttk.Button(
            btn_frame, text="Adicionar", command=self.adicionar_atividade_planejada
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame, text="Editar", command=self.editar_atividade_planejada
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame, text="Remover", command=self.remover_atividade_planejada
        ).pack(side=tk.LEFT, padx=2)

        # Lista de atividades
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox_atividades = tk.Listbox(list_frame, height=20)
        scrollbar_ativ = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.listbox_atividades.yview
        )
        self.listbox_atividades.configure(yscrollcommand=scrollbar_ativ.set)

        self.listbox_atividades.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_ativ.pack(side=tk.RIGHT, fill=tk.Y)

        self.atualizar_lista_atividades_planejadas()

    def criar_aba_atividades_realizadas(self):
        """Cria a aba de atividades realizadas"""
        main_frame = ttk.Frame(self.aba_atividades_realizadas)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            btn_frame, text="Adicionar", command=self.adicionar_atividade_realizada
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Editar", command=self.editar_atividade_realizada
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Remover", command=self.remover_atividade_realizada
        ).pack(side=tk.LEFT, padx=5)

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox_atividades_realizadas = tk.Listbox(list_frame, height=20)
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.listbox_atividades_realizadas.yview,
        )
        self.listbox_atividades_realizadas.configure(yscrollcommand=scrollbar.set)

        self.listbox_atividades_realizadas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.atualizar_lista_atividades_realizadas()

    def criar_aba_outras_info(self):
        """Cria a aba de outras informações"""
        main_frame = ttk.Frame(self.aba_info_gerais)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Missionário de Oração
        miss_frame = ttk.LabelFrame(
            main_frame, text="Missionário de Oração", padding=10
        )
        miss_frame.pack(fill=tk.X, pady=5)

        ttk.Label(miss_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.miss_nome_var = tk.StringVar()
        ttk.Entry(miss_frame, textvariable=self.miss_nome_var, width=40).grid(
            row=0, column=1, sticky=tk.W, pady=2
        )

        ttk.Label(miss_frame, text="Data Nasc.:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.miss_data_var = tk.StringVar()
        ttk.Entry(miss_frame, textvariable=self.miss_data_var, width=20).grid(
            row=1, column=1, sticky=tk.W, pady=2
        )

        ttk.Label(miss_frame, text="Campo:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.miss_campo_var = tk.StringVar()
        ttk.Entry(miss_frame, textvariable=self.miss_campo_var, width=40).grid(
            row=2, column=1, sticky=tk.W, pady=2
        )

        ttk.Label(miss_frame, text="WhatsApp:").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.miss_whats_var = tk.StringVar()
        ttk.Entry(miss_frame, textvariable=self.miss_whats_var, width=20).grid(
            row=3, column=1, sticky=tk.W, pady=2
        )

        # Foto do Missionário
        ttk.Label(miss_frame, text="Foto:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.miss_foto_var = tk.StringVar()
        foto_entry_miss = ttk.Entry(
            miss_frame, textvariable=self.miss_foto_var, width=30
        )
        foto_entry_miss.grid(row=4, column=1, sticky=tk.W, pady=2)

        def selecionar_foto_missionario():
            arquivo = filedialog.askopenfilename(
                title="Selecionar Foto do Missionário",
                filetypes=[
                    ("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("Todos os arquivos", "*.*"),
                ],
            )
            if arquivo:
                nome_arquivo = self.copiar_foto_para_pasta_fotos(arquivo)
                if nome_arquivo:
                    self.miss_foto_var.set(nome_arquivo)

        ttk.Button(
            miss_frame, text="Selecionar Foto", command=selecionar_foto_missionario
        ).grid(row=4, column=1, sticky=tk.E, padx=5, pady=2)

        # Observações
        obs_frame = ttk.LabelFrame(main_frame, text="Observações", padding=10)
        obs_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        obs_btn_frame = ttk.Frame(obs_frame)
        obs_btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            obs_btn_frame, text="Adicionar", command=self.adicionar_observacao
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(obs_btn_frame, text="Editar", command=self.editar_observacao).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(obs_btn_frame, text="Remover", command=self.remover_observacao).pack(
            side=tk.LEFT, padx=5
        )

        self.listbox_observacoes = tk.Listbox(obs_frame, height=10)
        scrollbar_obs = ttk.Scrollbar(
            obs_frame, orient=tk.VERTICAL, command=self.listbox_observacoes.yview
        )
        self.listbox_observacoes.configure(yscrollcommand=scrollbar_obs.set)

        self.listbox_observacoes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_obs.pack(side=tk.RIGHT, fill=tk.Y)

        self.carregar_outras_info()

    # Métodos de atualização de listas
    def atualizar_lista_diretoria(self):
        """Atualiza a lista de diretoria"""
        for item in self.tree_diretoria.get_children():
            self.tree_diretoria.delete(item)

        for membro in self.dados.get('diretoria', []):
            self.tree_diretoria.insert(
                '',
                tk.END,
                values=(
                    membro.get('cargo', ''),
                    membro.get('nome', ''),
                    membro.get('data_nascimento', ''),
                    membro.get('email', ''),
                ),
            )

    def atualizar_lista_safs(self):
        """Atualiza a lista de SAFs"""
        for item in self.tree_safs.get_children():
            self.tree_safs.delete(item)

        for saf in self.dados.get('safs', []):
            pres_nome = (
                saf.get('presidente', {}).get('nome', '')
                if saf.get('presidente')
                else ''
            )
            pastor_nome = (
                saf.get('pastor', {}).get('nome', '') if saf.get('pastor') else ''
            )
            self.tree_safs.insert(
                '',
                tk.END,
                values=(
                    saf.get('numero', ''),
                    saf.get('nome', ''),
                    pres_nome,
                    pastor_nome,
                ),
            )

    def atualizar_lista_atividades_planejadas(self):
        """Atualiza a lista de atividades planejadas"""
        self.listbox_atividades.delete(0, tk.END)
        mes = self.mes_var.get()
        meses_map = {
            'Janeiro': 'janeiro',
            'Fevereiro': 'fevereiro',
            'Março': 'marco',
            'Abril': 'abril',
            'Maio': 'maio',
            'Junho': 'junho',
            'Julho': 'julho',
            'Agosto': 'agosto',
            'Setembro': 'setembro',
            'Outubro': 'outubro',
            'Novembro': 'novembro',
            'Dezembro': 'dezembro',
        }
        mes_key = meses_map.get(mes, 'janeiro')

        atividades = self.dados.get('atividades_planejadas_2024', {}).get(mes_key, [])
        for ativ in atividades:
            data_str = f"{ativ.get('data', '')} – " if ativ.get('data') else ""
            self.listbox_atividades.insert(
                tk.END, f"{data_str}{ativ.get('descricao', '')}"
            )

    def atualizar_lista_atividades_realizadas(self):
        """Atualiza a lista de atividades realizadas"""
        self.listbox_atividades_realizadas.delete(0, tk.END)
        atividades = self.dados.get('atividades_realizadas_2023', [])
        for ativ in atividades:
            data_str = f"{ativ.get('data', '')} – " if ativ.get('data') else ""
            self.listbox_atividades_realizadas.insert(
                tk.END, f"{data_str}{ativ.get('descricao', '')}"
            )

    def carregar_outras_info(self):
        """Carrega outras informações"""
        info = self.dados.get('informacoes_gerais', {})
        miss = info.get('missionario_oracao', {})

        self.miss_nome_var.set(miss.get('nome', ''))
        self.miss_data_var.set(miss.get('data_nascimento', ''))
        self.miss_campo_var.set(miss.get('campo', ''))
        self.miss_whats_var.set(miss.get('whatsapp', ''))
        self.miss_foto_var.set(miss.get('foto', ''))

        self.listbox_observacoes.delete(0, tk.END)
        for obs in info.get('observacoes', []):
            self.listbox_observacoes.insert(tk.END, obs)

    # Métodos de diálogos
    def copiar_foto_para_pasta_fotos(self, caminho_origem):
        """Copia foto para a pasta fotos do projeto"""
        if not caminho_origem or not os.path.exists(caminho_origem):
            return None

        # Criar pasta fotos se não existir
        pasta_atual = os.path.dirname(os.path.abspath(self.arquivo_atual))
        pasta_fotos = os.path.join(pasta_atual, 'fotos')
        os.makedirs(pasta_fotos, exist_ok=True)

        # Copiar arquivo
        nome_arquivo = os.path.basename(caminho_origem)
        caminho_destino = os.path.join(pasta_fotos, nome_arquivo)

        try:
            shutil.copy2(caminho_origem, caminho_destino)
            return nome_arquivo  # Retorna apenas o nome do arquivo
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar foto: {e}")
            return None

    def dialog_membro_diretoria(self, membro=None):
        """Diálogo para adicionar/editar membro da diretoria"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Membro da Diretoria" if membro else "Novo Membro")
        dialog.geometry("550x420")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Cargo:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        cargo_var = tk.StringVar(value=membro.get('cargo', '') if membro else '')
        ttk.Entry(dialog, textvariable=cargo_var, width=40).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(dialog, text="Nome:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        nome_var = tk.StringVar(value=membro.get('nome', '') if membro else '')
        ttk.Entry(dialog, textvariable=nome_var, width=40).grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Label(dialog, text="Data Nascimento (DD/MM):").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )
        data_var = tk.StringVar(
            value=membro.get('data_nascimento', '') if membro else ''
        )
        ttk.Entry(dialog, textvariable=data_var, width=20).grid(
            row=2, column=1, padx=5, pady=5
        )

        ttk.Label(dialog, text="Email:").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5
        )
        email_var = tk.StringVar(value=membro.get('email', '') if membro else '')
        ttk.Entry(dialog, textvariable=email_var, width=40).grid(
            row=3, column=1, padx=5, pady=5
        )

        ttk.Label(dialog, text="Endereço:").grid(
            row=4, column=0, sticky=tk.W, padx=5, pady=5
        )
        endereco_var = tk.StringVar(value=membro.get('endereco', '') if membro else '')
        ttk.Entry(dialog, textvariable=endereco_var, width=40).grid(
            row=4, column=1, padx=5, pady=5
        )

        # Campo de foto
        foto_var = tk.StringVar(value=membro.get('foto', '') if membro else '')
        ttk.Label(dialog, text="Foto:").grid(
            row=5, column=0, sticky=tk.W, padx=5, pady=5
        )
        foto_entry = ttk.Entry(dialog, textvariable=foto_var, width=30)
        foto_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        def selecionar_foto():
            arquivo = filedialog.askopenfilename(
                title="Selecionar Foto",
                filetypes=[
                    ("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("Todos os arquivos", "*.*"),
                ],
            )
            if arquivo:
                nome_arquivo = self.copiar_foto_para_pasta_fotos(arquivo)
                if nome_arquivo:
                    foto_var.set(nome_arquivo)

        ttk.Button(dialog, text="Selecionar Foto", command=selecionar_foto).grid(
            row=5, column=1, padx=5, pady=5, sticky=tk.E
        )

        def salvar():
            novo_membro = {
                "cargo": cargo_var.get(),
                "nome": nome_var.get(),
                "data_nascimento": data_var.get(),
            }
            if email_var.get():
                novo_membro["email"] = email_var.get()
            if endereco_var.get():
                novo_membro["endereco"] = endereco_var.get()
            if foto_var.get():
                novo_membro["foto"] = foto_var.get()

            if membro:
                idx = self.dados['diretoria'].index(membro)
                self.dados['diretoria'][idx] = novo_membro
            else:
                self.dados['diretoria'].append(novo_membro)

            self.atualizar_lista_diretoria()
            dialog.destroy()

        ttk.Button(dialog, text="Salvar", command=salvar).grid(row=6, column=1, pady=10)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).grid(
            row=6, column=0, pady=10
        )

    def dialog_saf(self, saf=None):
        """Diálogo para adicionar/editar SAF"""
        dialog = tk.Toplevel(self.root)
        dialog.title("SAF" if saf else "Nova SAF")
        dialog.geometry("600x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Notebook para organizar
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Aba Geral
        aba_geral = ttk.Frame(notebook)
        notebook.add(aba_geral, text="Geral")

        ttk.Label(aba_geral, text="Nome da SAF:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        nome_var = tk.StringVar(value=saf.get('nome', '') if saf else '')
        ttk.Entry(aba_geral, textvariable=nome_var, width=50).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(aba_geral, text="Endereço da Igreja:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        endereco_var = tk.StringVar(value=saf.get('endereco', '') if saf else '')
        ttk.Entry(aba_geral, textvariable=endereco_var, width=50).grid(
            row=1, column=1, padx=5, pady=5
        )

        # Foto da SAF
        ttk.Label(aba_geral, text="Foto da SAF/Igreja:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )
        foto_saf_var = tk.StringVar(value=saf.get('foto', '') if saf else '')
        foto_entry_saf = ttk.Entry(aba_geral, textvariable=foto_saf_var, width=40)
        foto_entry_saf.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        def selecionar_foto_saf():
            arquivo = filedialog.askopenfilename(
                title="Selecionar Foto da SAF/Igreja",
                filetypes=[
                    ("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("Todos os arquivos", "*.*"),
                ],
            )
            if arquivo:
                nome_arquivo = self.copiar_foto_para_pasta_fotos(arquivo)
                if nome_arquivo:
                    foto_saf_var.set(nome_arquivo)

        ttk.Button(aba_geral, text="Selecionar Foto", command=selecionar_foto_saf).grid(
            row=2, column=1, sticky=tk.E, padx=5
        )

        # Aba Pastor
        aba_pastor = ttk.Frame(notebook)
        notebook.add(aba_pastor, text="Pastor")

        ttk.Label(aba_pastor, text="Nome:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        pastor_nome_var = tk.StringVar(
            value=(
                saf.get('pastor', {}).get('nome', '')
                if saf and saf.get('pastor')
                else ''
            )
        )
        ttk.Entry(aba_pastor, textvariable=pastor_nome_var, width=40).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(aba_pastor, text="Data Nasc. (DD/MM):").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        pastor_data_var = tk.StringVar(
            value=(
                saf.get('pastor', {}).get('data_nascimento', '')
                if saf and saf.get('pastor')
                else ''
            )
        )
        ttk.Entry(aba_pastor, textvariable=pastor_data_var, width=20).grid(
            row=1, column=1, padx=5, pady=5
        )

        # Aba Presidente
        aba_pres = ttk.Frame(notebook)
        notebook.add(aba_pres, text="Presidente")

        ttk.Label(aba_pres, text="Nome:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        pres_nome_var = tk.StringVar(
            value=(
                saf.get('presidente', {}).get('nome', '')
                if saf and saf.get('presidente')
                else ''
            )
        )
        ttk.Entry(aba_pres, textvariable=pres_nome_var, width=40).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(aba_pres, text="Data Nasc. (DD/MM):").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        pres_data_var = tk.StringVar(
            value=(
                saf.get('presidente', {}).get('data_nascimento', '')
                if saf and saf.get('presidente')
                else ''
            )
        )
        ttk.Entry(aba_pres, textvariable=pres_data_var, width=20).grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Label(aba_pres, text="Endereço:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )
        pres_end_var = tk.StringVar(
            value=(
                saf.get('presidente', {}).get('endereco', '')
                if saf and saf.get('presidente')
                else ''
            )
        )
        ttk.Entry(aba_pres, textvariable=pres_end_var, width=40).grid(
            row=2, column=1, padx=5, pady=5
        )

        ttk.Label(aba_pres, text="CEP:").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5
        )
        pres_cep_var = tk.StringVar(
            value=(
                saf.get('presidente', {}).get('cep', '')
                if saf and saf.get('presidente')
                else ''
            )
        )
        ttk.Entry(aba_pres, textvariable=pres_cep_var, width=20).grid(
            row=3, column=1, padx=5, pady=5
        )

        ttk.Label(aba_pres, text="Telefone:").grid(
            row=4, column=0, sticky=tk.W, padx=5, pady=5
        )
        pres_tel_var = tk.StringVar(
            value=(
                saf.get('presidente', {}).get('telefone', '')
                if saf and saf.get('presidente')
                else ''
            )
        )
        ttk.Entry(aba_pres, textvariable=pres_tel_var, width=20).grid(
            row=4, column=1, padx=5, pady=5
        )

        ttk.Label(aba_pres, text="Email:").grid(
            row=5, column=0, sticky=tk.W, padx=5, pady=5
        )
        pres_email_var = tk.StringVar(
            value=(
                saf.get('presidente', {}).get('email', '')
                if saf and saf.get('presidente')
                else ''
            )
        )
        ttk.Entry(aba_pres, textvariable=pres_email_var, width=40).grid(
            row=5, column=1, padx=5, pady=5
        )

        # Aba Conselheiro e Aniversário
        aba_outros = ttk.Frame(notebook)
        notebook.add(aba_outros, text="Outros")

        ttk.Label(aba_outros, text="Conselheiro - Nome:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        cons_nome_var = tk.StringVar(
            value=(
                saf.get('conselheiro', {}).get('nome', '')
                if saf and saf.get('conselheiro')
                else ''
            )
        )
        ttk.Entry(aba_outros, textvariable=cons_nome_var, width=40).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(aba_outros, text="Conselheiro - Data Nasc. (DD/MM):").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        cons_data_var = tk.StringVar(
            value=(
                saf.get('conselheiro', {}).get('data_nascimento', '')
                if saf and saf.get('conselheiro')
                else ''
            )
        )
        ttk.Entry(aba_outros, textvariable=cons_data_var, width=20).grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Label(aba_outros, text="Aniversário - Data (DD/MM):").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )
        aniv_data_var = tk.StringVar(
            value=(
                saf.get('aniversario', {}).get('data', '')
                if saf and saf.get('aniversario')
                else ''
            )
        )
        ttk.Entry(aba_outros, textvariable=aniv_data_var, width=20).grid(
            row=2, column=1, padx=5, pady=5
        )

        ttk.Label(aba_outros, text="Aniversário - Anos:").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5
        )
        aniv_anos_var = tk.StringVar(
            value=(
                str(saf.get('aniversario', {}).get('anos', ''))
                if saf and saf.get('aniversario')
                else ''
            )
        )
        ttk.Entry(aba_outros, textvariable=aniv_anos_var, width=20).grid(
            row=3, column=1, padx=5, pady=5
        )

        def salvar():
            nova_saf = {
                "numero": (
                    saf.get('numero', len(self.dados['safs']) + 1)
                    if saf
                    else len(self.dados['safs']) + 1
                ),
                "nome": nome_var.get(),
                "endereco": endereco_var.get(),
                "foto": foto_saf_var.get() if foto_saf_var.get() else None,
                "pastor": {
                    "nome": pastor_nome_var.get(),
                    "data_nascimento": pastor_data_var.get(),
                },
                "presidente": {
                    "nome": pres_nome_var.get(),
                    "data_nascimento": pres_data_var.get(),
                    "endereco": pres_end_var.get(),
                    "cep": pres_cep_var.get(),
                    "telefone": pres_tel_var.get(),
                },
                "conselheiro": {
                    "nome": cons_nome_var.get(),
                    "data_nascimento": cons_data_var.get(),
                },
                "aniversario": {
                    "data": aniv_data_var.get(),
                    "anos": (
                        int(aniv_anos_var.get()) if aniv_anos_var.get().isdigit() else 0
                    ),
                },
            }
            if pres_email_var.get():
                nova_saf['presidente']['email'] = pres_email_var.get()

            # Remover foto se estiver vazia
            if not nova_saf.get('foto'):
                nova_saf.pop('foto', None)

            if saf:
                idx = self.dados['safs'].index(saf)
                self.dados['safs'][idx] = nova_saf
            else:
                self.dados['safs'].append(nova_saf)

            self.atualizar_lista_safs()
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=salvar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(
            side=tk.LEFT, padx=5
        )

    def dialog_atividade(self, atividade=None, planejada=True):
        """Diálogo para adicionar/editar atividade"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Atividade" if atividade else "Nova Atividade")
        dialog.geometry("500x200")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Data (ex: 15/03 ou '1º Domingo'):").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        data_var = tk.StringVar(value=atividade.get('data', '') if atividade else '')
        ttk.Entry(dialog, textvariable=data_var, width=40).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(dialog, text="Descrição:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        desc_var = tk.StringVar(
            value=atividade.get('descricao', '') if atividade else ''
        )
        ttk.Entry(dialog, textvariable=desc_var, width=40).grid(
            row=1, column=1, padx=5, pady=5
        )

        def salvar():
            nova_atividade = {"data": data_var.get(), "descricao": desc_var.get()}

            if planejada:
                mes = self.mes_var.get()
                meses_map = {
                    'Janeiro': 'janeiro',
                    'Fevereiro': 'fevereiro',
                    'Março': 'marco',
                    'Abril': 'abril',
                    'Maio': 'maio',
                    'Junho': 'junho',
                    'Julho': 'julho',
                    'Agosto': 'agosto',
                    'Setembro': 'setembro',
                    'Outubro': 'outubro',
                    'Novembro': 'novembro',
                    'Dezembro': 'dezembro',
                }
                mes_key = meses_map.get(mes, 'janeiro')

                if atividade:
                    atividades = self.dados.get('atividades_planejadas_2024', {}).get(
                        mes_key, []
                    )
                    idx = atividades.index(atividade)
                    atividades[idx] = nova_atividade
                else:
                    if 'atividades_planejadas_2024' not in self.dados:
                        self.dados['atividades_planejadas_2024'] = {}
                    if mes_key not in self.dados['atividades_planejadas_2024']:
                        self.dados['atividades_planejadas_2024'][mes_key] = []
                    self.dados['atividades_planejadas_2024'][mes_key].append(
                        nova_atividade
                    )

                self.atualizar_lista_atividades_planejadas()
            else:
                if atividade:
                    idx = self.dados['atividades_realizadas_2023'].index(atividade)
                    self.dados['atividades_realizadas_2023'][idx] = nova_atividade
                else:
                    if 'atividades_realizadas_2023' not in self.dados:
                        self.dados['atividades_realizadas_2023'] = []
                    self.dados['atividades_realizadas_2023'].append(nova_atividade)

                self.atualizar_lista_atividades_realizadas()

            dialog.destroy()

        ttk.Button(dialog, text="Salvar", command=salvar).grid(row=2, column=1, pady=10)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).grid(
            row=2, column=0, pady=10
        )

    # Métodos de ação
    def adicionar_membro_diretoria(self):
        self.dialog_membro_diretoria()

    def editar_membro_diretoria(self):
        selecionado = self.tree_diretoria.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para editar!")
            return

        item = self.tree_diretoria.item(selecionado[0])
        valores = item['values']
        cargo = valores[0]

        membro = next((m for m in self.dados['diretoria'] if m['cargo'] == cargo), None)
        if membro:
            self.dialog_membro_diretoria(membro)

    def remover_membro_diretoria(self):
        selecionado = self.tree_diretoria.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para remover!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente remover este membro?"):
            item = self.tree_diretoria.item(selecionado[0])
            valores = item['values']
            cargo = valores[0]

            self.dados['diretoria'] = [
                m for m in self.dados['diretoria'] if m['cargo'] != cargo
            ]
            self.atualizar_lista_diretoria()

    def adicionar_saf(self):
        self.dialog_saf()

    def editar_saf(self):
        selecionado = self.tree_safs.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma SAF para editar!")
            return

        item = self.tree_safs.item(selecionado[0])
        num = int(item['values'][0])

        saf = next((s for s in self.dados['safs'] if s['numero'] == num), None)
        if saf:
            self.dialog_saf(saf)

    def remover_saf(self):
        selecionado = self.tree_safs.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma SAF para remover!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente remover esta SAF?"):
            item = self.tree_safs.item(selecionado[0])
            num = int(item['values'][0])

            self.dados['safs'] = [s for s in self.dados['safs'] if s['numero'] != num]
            # Renumerar
            for i, s in enumerate(self.dados['safs'], 1):
                s['numero'] = i
            self.atualizar_lista_safs()

    def adicionar_atividade_planejada(self):
        self.dialog_atividade(planejada=True)

    def editar_atividade_planejada(self):
        selecionado = self.listbox_atividades.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma atividade para editar!")
            return

        mes = self.mes_var.get()
        meses_map = {
            'Janeiro': 'janeiro',
            'Fevereiro': 'fevereiro',
            'Março': 'marco',
            'Abril': 'abril',
            'Maio': 'maio',
            'Junho': 'junho',
            'Julho': 'julho',
            'Agosto': 'agosto',
            'Setembro': 'setembro',
            'Outubro': 'outubro',
            'Novembro': 'novembro',
            'Dezembro': 'dezembro',
        }
        mes_key = meses_map.get(mes, 'janeiro')

        atividades = self.dados.get('atividades_planejadas_2024', {}).get(mes_key, [])
        atividade = atividades[selecionado[0]]
        self.dialog_atividade(atividade, planejada=True)

    def remover_atividade_planejada(self):
        selecionado = self.listbox_atividades.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma atividade para remover!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente remover esta atividade?"):
            mes = self.mes_var.get()
            meses_map = {
                'Janeiro': 'janeiro',
                'Fevereiro': 'fevereiro',
                'Março': 'marco',
                'Abril': 'abril',
                'Maio': 'maio',
                'Junho': 'junho',
                'Julho': 'julho',
                'Agosto': 'agosto',
                'Setembro': 'setembro',
                'Outubro': 'outubro',
                'Novembro': 'novembro',
                'Dezembro': 'dezembro',
            }
            mes_key = meses_map.get(mes, 'janeiro')

            atividades = self.dados.get('atividades_planejadas_2024', {}).get(
                mes_key, []
            )
            atividades.pop(selecionado[0])
            self.atualizar_lista_atividades_planejadas()

    def adicionar_atividade_realizada(self):
        self.dialog_atividade(planejada=False)

    def editar_atividade_realizada(self):
        selecionado = self.listbox_atividades_realizadas.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma atividade para editar!")
            return

        atividades = self.dados.get('atividades_realizadas_2023', [])
        atividade = atividades[selecionado[0]]
        self.dialog_atividade(atividade, planejada=False)

    def remover_atividade_realizada(self):
        selecionado = self.listbox_atividades_realizadas.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma atividade para remover!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente remover esta atividade?"):
            atividades = self.dados.get('atividades_realizadas_2023', [])
            atividades.pop(selecionado[0])
            self.atualizar_lista_atividades_realizadas()

    def adicionar_observacao(self):
        obs = simpledialog.askstring("Nova Observação", "Digite a observação:")
        if obs:
            if 'informacoes_gerais' not in self.dados:
                self.dados['informacoes_gerais'] = {}
            if 'observacoes' not in self.dados['informacoes_gerais']:
                self.dados['informacoes_gerais']['observacoes'] = []
            self.dados['informacoes_gerais']['observacoes'].append(obs)
            self.listbox_observacoes.insert(tk.END, obs)

    def editar_observacao(self):
        selecionado = self.listbox_observacoes.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma observação para editar!")
            return

        obs_atual = self.listbox_observacoes.get(selecionado[0])
        nova_obs = simpledialog.askstring(
            "Editar Observação", "Nova observação:", initialvalue=obs_atual
        )
        if nova_obs:
            self.dados['informacoes_gerais']['observacoes'][selecionado[0]] = nova_obs
            self.listbox_observacoes.delete(selecionado[0])
            self.listbox_observacoes.insert(selecionado[0], nova_obs)

    def remover_observacao(self):
        selecionado = self.listbox_observacoes.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma observação para remover!")
            return

        if messagebox.askyesno(
            "Confirmar", "Deseja realmente remover esta observação?"
        ):
            self.dados['informacoes_gerais']['observacoes'].pop(selecionado[0])
            self.listbox_observacoes.delete(selecionado[0])

    # Métodos de arquivo
    def abrir_arquivo(self):
        arquivo = filedialog.askopenfilename(
            title="Abrir arquivo JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if arquivo:
            self.arquivo_atual = arquivo
            self.carregar_dados()
            self.criar_abas()  # Recriar abas com novos dados

    def salvar_dados(self):
        """Salva os dados atuais"""
        # Atualizar dados das abas
        self.dados['ano'] = (
            int(self.ano_var.get())
            if self.ano_var.get().isdigit()
            else self.dados.get('ano', 2024)
        )
        self.dados['presidente']['nome'] = self.presidente_nome_var.get()
        self.dados['presidente']['mensagem'] = self.presidente_mensagem_text.get(
            '1.0', tk.END
        ).strip()
        if self.presidente_foto_var.get():
            self.dados['presidente']['foto'] = self.presidente_foto_var.get()
        elif 'foto' in self.dados.get('presidente', {}):
            del self.dados['presidente']['foto']

        # Atualizar informações gerais
        if 'informacoes_gerais' not in self.dados:
            self.dados['informacoes_gerais'] = {}
        self.dados['informacoes_gerais']['missionario_oracao'] = {
            'nome': self.miss_nome_var.get(),
            'data_nascimento': self.miss_data_var.get(),
            'campo': self.miss_campo_var.get(),
            'whatsapp': self.miss_whats_var.get(),
        }
        if self.miss_foto_var.get():
            self.dados['informacoes_gerais']['missionario_oracao'][
                'foto'
            ] = self.miss_foto_var.get()
        elif 'foto' in self.dados['informacoes_gerais']['missionario_oracao']:
            del self.dados['informacoes_gerais']['missionario_oracao']['foto']

        try:
            with open(self.arquivo_atual, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Sucesso", f"Dados salvos em '{self.arquivo_atual}'")
            # Atualizar status
            if hasattr(self, 'status_label'):
                self.status_label.config(
                    text=f"Salvo: {os.path.basename(self.arquivo_atual)}"
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Erro ao salvar: {e}")

    def salvar_como(self):
        arquivo = filedialog.asksaveasfilename(
            title="Salvar como",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if arquivo:
            self.arquivo_atual = arquivo
            self.salvar_dados()

    def gerar_word(self):
        """Gera o documento Word"""
        self.salvar_dados()  # Salvar antes de gerar
        try:
            import os
            import subprocess
            import sys

            # Obter ano do JSON
            ano = self.dados.get('ano', 2024)
            nome_padrao = f"Agenda {ano}.docx"

            # Pedir ao usuário o nome do arquivo
            nome_arquivo = simpledialog.askstring(
                "Nome do Arquivo",
                f"Digite o nome do arquivo Word:\n(Deixe em branco para usar: {nome_padrao})",
                initialvalue=nome_padrao,
            )

            # Se cancelar, não fazer nada
            if nome_arquivo is None:
                return

            # Se deixar em branco, usar o padrão
            if nome_arquivo.strip() == "":
                nome_arquivo = nome_padrao

            # Garantir que termina com .docx
            if not nome_arquivo.endswith('.docx'):
                nome_arquivo += '.docx'

            # Atualizar status
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Gerando Word...")
            self.root.update()  # Atualizar interface

            # Usar python ou python3 dependendo do sistema
            python_cmd = sys.executable if hasattr(sys, 'executable') else 'python'

            # Obter caminho do script gerar_agenda.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(script_dir, 'gerar_agenda.py')

            # Executar gerar_agenda.py com o nome do arquivo especificado
            result = subprocess.run(
                [python_cmd, script_path, self.arquivo_atual, nome_arquivo],
                check=True,
                capture_output=True,
                text=True,
            )
            messagebox.showinfo(
                "Sucesso",
                f"Documento Word gerado com sucesso!\n\nArquivo: {nome_arquivo}",
            )
            # Atualizar status
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Word gerado: {nome_arquivo}")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            messagebox.showerror("Erro", f"Erro ao gerar Word:\n{error_msg}")
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Erro ao gerar Word")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo gerar_agenda.py não encontrado!")
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Erro: gerar_agenda.py não encontrado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar Word: {e}")
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Erro: {str(e)[:30]}")

    def mostrar_sobre(self):
        messagebox.showinfo(
            "Sobre",
            "Editor de Agenda - Federação de SAFs\n\nVersão 1.0\n\nSistema para gerenciar e editar a agenda anual da Federação de SAFs.",
        )


def main():
    root = tk.Tk()
    app = EditorAgendaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
