# Editor de Agenda - Federação de SAFs

Sistema completo para edição e geração de agendas em formato Word (.docx) com suporte a fotos, formatação profissional e layout em duas colunas.

## 📋 Índice

- [Instalação](#instalação)
- [Uso Rápido](#uso-rápido)
- [Interface Gráfica](#interface-gráfica)
- [Geração de Documentos Word](#geração-de-documentos-word)
- [Estrutura de Dados](#estrutura-de-dados)
- [Fotos](#fotos)
- [Criar Executável](#criar-executável)
- [Solução de Problemas](#solução-de-problemas)

---

## 🚀 Instalação

### Windows (Recomendado)

**Opção 1: Instalação Automática**
1. Execute `instalar.bat`
2. O instalador verificará Python, instalará dependências e configurará tudo

**Opção 2: Instalação Manual**
1. Instale Python 3.8+ de https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante a instalação
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Linux/Mac

```bash
# Instalar Python (se necessário)
sudo apt-get install python3 python3-pip  # Ubuntu/Debian
brew install python3                       # macOS

# Instalar dependências
pip install -r requirements.txt
```

---

## ⚡ Uso Rápido

### Executar Interface Gráfica

```bash
python editar_agenda_gui.py
```

### Gerar Documento Word

**Pela Interface:**
- Clique em "📄 Gerar Word" ou use **Ctrl+G**
- Escolha o nome do arquivo na caixa de diálogo
- O documento será gerado automaticamente

**Pela Linha de Comando:**
```bash
python gerar_agenda.py
```

---

## 🖥️ Interface Gráfica

A interface gráfica oferece edição visual e intuitiva de todos os dados da agenda.

### Funcionalidades

**6 Abas Principais:**

1. **Informações Gerais**
   - Ano da agenda
   - Nome e mensagem da presidente
   - Foto da presidente

2. **Diretoria**
   - Visualizar membros em tabela
   - Adicionar/editar/remover membros
   - Campos: cargo, nome, data nascimento, email, endereço, foto

3. **SAFs**
   - Visualizar todas as SAFs
   - Adicionar/editar/remover SAFs
   - Dados completos: endereço, pastor, presidente, conselheiro, aniversário, foto

4. **Atividades Planejadas**
   - Organizadas por mês
   - Adicionar/editar/remover atividades
   - Selecionar mês no dropdown

5. **Atividades Realizadas**
   - Lista de atividades do ano anterior
   - Adicionar/editar/remover atividades

6. **Outras Informações**
   - Missionário de Oração (nome, data nascimento, campo, WhatsApp, foto)
   - Observações (lista editável)
   - Lema (texto centralizado)

### Atalhos de Teclado

- **Ctrl+S**: Salvar alterações
- **Ctrl+G**: Gerar documento Word
- **Ctrl+O**: Abrir arquivo JSON diferente

### Menu Arquivo

- **Abrir...**: Abre um arquivo JSON diferente
- **Salvar**: Salva alterações no arquivo atual
- **Salvar como...**: Salva em um novo arquivo
- **Gerar Word**: Gera o documento Word
- **Sair**: Fecha a aplicação

---

## 📄 Geração de Documentos Word

### Formato do Documento

O documento gerado possui:

- **Layout**: 2 colunas verticais com linha divisória preta central
- **Orientação**: Paisagem (landscape)
- **Fonte**: Arial
  - Títulos de seção: 14pt, negrito
  - Subtítulos: 12pt, negrito
  - Texto normal: 12pt
  - Detalhes: 10pt
- **Alinhamento**: Justificado
- **Margens**: 0.4" (todas)
- **Fotos**: Formato 3x4, posicionadas à esquerda das informações

### Nome do Arquivo

- O nome do arquivo usa automaticamente o ano do JSON
- Você pode personalizar o nome ao gerar o Word
- Exemplo: "Agenda 2026.docx" ou "Agenda 2026 - Final.docx"

---

## 📊 Estrutura de Dados

O arquivo `agenda_data.json` contém:

```json
{
  "ano": 2026,
  "presidente": {
    "nome": "Nome da Presidente",
    "mensagem": "Mensagem...",
    "foto": "foto.jpg"
  },
  "diretoria": [
    {
      "cargo": "Presidente",
      "nome": "Nome",
      "data_nascimento": "DD/MM",
      "email": "email@exemplo.com",
      "endereco": "Endereço completo",
      "foto": "foto.jpg"
    }
  ],
  "safs": [
    {
      "numero": 1,
      "nome": "Nome da SAF",
      "endereco": "Endereço",
      "foto": "foto.jpg",
      "pastor": {
        "nome": "Nome do Pastor",
        "data_nascimento": "DD/MM"
      },
      "presidente": {
        "nome": "Nome",
        "data_nascimento": "DD/MM",
        "telefone": "(XX) XXXXX-XXXX",
        "email": "email@exemplo.com"
      },
      "conselheiro": {
        "nome": "Nome",
        "data_nascimento": "DD/MM"
      },
      "aniversario": {
        "data": "DD/MM",
        "anos": 50
      }
    }
  ],
  "atividades_realizadas_2023": [
    {
      "data": "DD/MM",
      "descricao": "Descrição da atividade"
    }
  ],
  "atividades_planejadas_2024": {
    "janeiro": [
      {
        "data": "DD/MM",
        "descricao": "Descrição"
      }
    ]
  },
  "informacoes_gerais": {
    "missionario_oracao": {
      "nome": "Rev. Nome",
      "data_nascimento": "DD/MM",
      "campo": "Nome do Campo",
      "whatsapp": "XX-XXXXX-XXXX",
      "foto": "foto.jpg"
    },
    "observacoes": [
      "Observação 1",
      "Observação 2"
    ],
    "lema": [
      "Linha 1 do lema",
      "Linha 2 do lema"
    ]
  }
}
```

---

## 📸 Fotos

### Como Adicionar Fotos

1. Na interface gráfica, ao editar um membro/SAF/missionário
2. Clique em "Selecionar Foto"
3. Escolha a imagem do seu computador
4. A foto será copiada automaticamente para a pasta `fotos/`
5. Salve o formulário

### Localização

- **Pasta**: `fotos/` (dentro da pasta do projeto)
- **Formatos suportados**: JPG, PNG, GIF, BMP
- **Tamanho recomendado**: 300x400 pixels (fotos de perfil)

### Formato no Documento

- **Proporção**: 3x4 (largura:altura)
- **Posicionamento**: À esquerda das informações
- **Redimensionamento**: Automático para manter proporção

### Importante

- Mantenha a pasta `fotos/` junto com o projeto
- Fotos são opcionais - o programa funciona sem elas
- Se mover o projeto, mova a pasta `fotos/` também

---

## 📦 Criar Executável (.exe)

Para criar um executável standalone (não precisa de Python instalado):

### Windows

```bash
criar_executavel.bat
```

O executável será criado em: `dist\EditorAgendaSAF.exe`

**Importante**: Copie o arquivo `agenda_data.json` para a mesma pasta do `.exe`

### Criar Instalador Profissional

Se você tem Inno Setup instalado:

```bash
criar_instalador.bat
```

Escolha a opção 2 ou 3 para criar um instalador profissional.

---

## 🔧 Solução de Problemas

### Python não encontrado

- Verifique se Python está instalado: `python --version`
- Certifique-se de que Python está no PATH
- Reinicie o terminal após instalar Python

### Erro ao instalar dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt --user
```

### Erro ao gerar Word

- Certifique-se de que `gerar_agenda.py` está na mesma pasta
- Verifique se o arquivo `agenda_data.json` existe
- Feche o documento Word se estiver aberto antes de gerar novamente

### Interface não aparece (tkinter)

**Windows**: Tkinter geralmente vem com Python

**Linux**:
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

**Verificar**:
```bash
python -c "import tkinter; print('OK')"
```

### Fotos não aparecem no Word

- Verifique se as fotos estão na pasta `fotos/`
- Confirme que o caminho no JSON está correto
- Certifique-se de que os arquivos de foto existem

---

## 📁 Estrutura de Arquivos

```
agenda-saf/
├── agenda_data.json          # Dados principais (obrigatório)
├── editar_agenda_gui.py      # Interface gráfica principal
├── gerar_agenda.py           # Gerador de documentos Word
├── extrair_fotos.py          # Extrair fotos de documentos Word
├── requirements.txt          # Dependências Python
├── instalar.bat              # Instalador automático (Windows)
├── criar_executavel.bat      # Criar executável .exe
├── criar_instalador.bat      # Criar instalador profissional
├── instalador.iss            # Script Inno Setup
├── setup.py                  # Instalação via pip
├── fotos/                    # Pasta com fotos
└── README.md                 # Este arquivo
```

---

## 🎯 Requisitos

- **Python**: 3.8 ou superior
- **Dependências**:
  - `python-docx` >= 0.8.11
  - `Pillow` >= 10.0.0
- **Sistema Operacional**: Windows, Linux ou macOS

---

## 📝 Licença

Este projeto foi desenvolvido para a Federação de SAFs de Macaé.

---

## 💡 Dicas

- ✅ Sempre salve antes de fechar a interface (Ctrl+S)
- ✅ Faça backup do arquivo `agenda_data.json` regularmente
- ✅ Use nomes descritivos para as fotos (ex: "presidente_maria.jpg")
- ✅ O ano do documento é definido no campo "ano" do JSON
- ✅ Você pode editar o JSON manualmente se preferir

---

**Versão**: 1.0.0  
**Última atualização**: 2026
