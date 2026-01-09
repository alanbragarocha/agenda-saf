# 🪟 Guia de Instalação para Windows

Este guia explica como instalar e executar o Sistema de Agenda da Federação de SAFs no Windows.

## ⚡ Opção 1: Executar Diretamente (Mais Simples)

### Passo 1: Instalar Python

1. Baixe Python 3.8 ou superior de: https://www.python.org/downloads/
2. **IMPORTANTE**: Durante a instalação, marque a opção **"Add Python to PATH"**
3. Clique em "Install Now"

### Passo 2: Instalar Dependências

1. Abra o PowerShell ou Prompt de Comando nesta pasta
2. Execute:
```batch
setup_windows.bat
```

Ou manualmente:
```batch
pip install -r requirements.txt
```

### Passo 3: Executar o Programa

**Interface Gráfica (Recomendado):**
```batch
python editar_agenda_gui.py
```

**Interface Web:**
```batch
python editar_agenda_web.py
```
Depois acesse: http://localhost:5000

**Gerar Documento Word:**
```batch
python gerar_agenda.py
```

---

## 📦 Opção 2: Criar Executável (.exe)

Se você quiser criar um arquivo `.exe` que pode ser executado sem precisar do Python instalado:

### Passo 1: Instalar Dependências (se ainda não fez)
```batch
setup_windows.bat
```

### Passo 2: Criar o Executável
```batch
criar_executavel.bat
```

### Passo 3: Usar o Executável

1. O executável será criado em: `dist\EditorAgendaSAF.exe`
2. **IMPORTANTE**: Copie o arquivo `agenda_data.json` para a mesma pasta do `.exe`
3. Execute o `EditorAgendaSAF.exe` normalmente (duplo clique)

---

## 🎯 Comparação: Python vs C#

### ✅ **Python (Recomendado) - Vantagens:**

- ✅ **Já funciona no Windows** - Não precisa mudar nada
- ✅ **Código já está pronto** - Funciona imediatamente
- ✅ **Interface Gráfica funcional** - Tkinter já está implementado
- ✅ **Executável possível** - PyInstaller cria .exe facilmente
- ✅ **Multiplataforma** - Funciona em Windows, Linux e Mac
- ✅ **Fácil manutenção** - Código simples e direto
- ✅ **Bibliotecas prontas** - python-docx funciona perfeitamente

### ❌ **C# - Desvantagens:**

- ❌ **Reescrever tudo** - Todo o código teria que ser convertido
- ❌ **Mais trabalho** - Semanas de desenvolvimento
- ❌ **Sem vantagem real** - Não traz benefício para este projeto
- ❌ **Apenas Windows** - Perde compatibilidade com Linux/Mac
- ❌ **Dependências complexas** - Necessita bibliotecas específicas para Word

### 💡 **Recomendação:**

**Use Python!** O projeto já está pronto e funciona perfeitamente no Windows. Basta executar `setup_windows.bat` e está pronto para usar.

---

## 🔧 Solução de Problemas

### Python não encontrado
- Certifique-se de ter instalado Python
- Verifique se marcou "Add Python to PATH" durante a instalação
- Reinicie o terminal após instalar Python

### Erro ao instalar dependências
```batch
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Executável não funciona
- Certifique-se de que o arquivo `agenda_data.json` está na mesma pasta do `.exe`
- Tente criar o executável novamente com `criar_executavel.bat`

### Interface não aparece
- Tkinter vem com Python, mas pode precisar ser instalado separadamente em algumas versões:
```batch
pip install tk
```

---

## 📝 Estrutura de Arquivos

```
agenda-saf/
├── agenda_data.json              # Dados da agenda (obrigatório)
├── editar_agenda_gui.py          # Interface gráfica principal
├── gerar_agenda.py               # Gerador de documento Word
├── requirements.txt              # Dependências Python
├── setup_windows.bat             # Script de instalação
├── criar_executavel.bat          # Script para criar .exe
└── README_WINDOWS.md             # Este arquivo
```

---

## 🚀 Uso Rápido

1. **Instalar**: Execute `setup_windows.bat`
2. **Usar**: Execute `python editar_agenda_gui.py`
3. **Gerar Word**: Use o menu "Arquivo > Gerar Word" na interface

Pronto! O sistema está funcionando no Windows. 🎉
