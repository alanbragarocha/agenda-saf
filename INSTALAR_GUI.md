# Como Instalar e Usar a Interface Gráfica

## Problema: tkinter não instalado

Se você recebeu o erro `ModuleNotFoundError: No module named 'tkinter'`, siga as instruções abaixo:

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install python3-tk
```

### Linux (Fedora/RHEL)

```bash
sudo dnf install python3-tkinter
```

### Linux (Arch)

```bash
sudo pacman -S tk
```

### Verificar instalação

```bash
python3 -c "import tkinter; print('tkinter instalado com sucesso!')"
```

### Executar a interface gráfica

```bash
python3 editar_agenda_gui.py
```

---

## Alternativa: Interface Web (sem tkinter)

Se não conseguir instalar tkinter, você pode usar a interface web:

### 1. Instalar Flask

```bash
pip3 install flask
```

### 2. Executar servidor web

```bash
python3 editar_agenda_web.py
```

### 3. Abrir no navegador

Acesse: http://localhost:5000

---

## Alternativa: Editor de Linha de Comando

Se preferir não instalar nada adicional, use o editor de linha de comando:

```bash
python3 editar_agenda.py
```

Este editor funciona sem dependências adicionais e oferece todas as funcionalidades!

---

## Resumo das Opções

| Opção | Requisitos | Facilidade |
|-------|-----------|------------|
| **GUI (tkinter)** | `python3-tk` | ⭐⭐⭐⭐⭐ |
| **Web (Flask)** | `flask` | ⭐⭐⭐⭐ |
| **CLI** | Nenhum | ⭐⭐⭐ |

Recomendação: Use o **CLI** (`editar_agenda.py`) se quiser começar imediatamente sem instalar nada!
