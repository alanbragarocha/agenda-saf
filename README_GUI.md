# Interface Gráfica - Editor de Agenda

## Como usar a Interface Gráfica

A interface gráfica oferece uma forma visual e intuitiva de editar todos os dados da agenda.

### Iniciar a Interface

```bash
python3 editar_agenda_gui.py
```

### Funcionalidades

A interface possui **6 abas** principais:

#### 1. **Informações Gerais**
- Editar o ano da agenda
- Editar nome da presidente
- Editar mensagem da presidente (com editor de texto completo)

#### 2. **Diretoria**
- Visualizar todos os membros em uma tabela
- Adicionar novos membros
- Editar membros existentes (clique em "Editar Selecionado")
- Remover membros

**Campos editáveis:**
- Cargo
- Nome
- Data de nascimento (DD/MM)
- Email
- Endereço

#### 3. **SAFs**
- Visualizar todas as SAFs em uma tabela
- Adicionar novas SAFs
- Editar SAFs existentes (com abas organizadas)
- Remover SAFs

**Cada SAF possui:**
- Dados gerais (nome, endereço da igreja)
- Dados do pastor (nome, data de nascimento)
- Dados do presidente (nome, data nasc., endereço, CEP, telefone, email)
- Dados do conselheiro (nome, data de nascimento)
- Aniversário (data e anos)

#### 4. **Atividades Planejadas**
- Selecionar o mês desejado no menu dropdown
- Visualizar atividades do mês selecionado
- Adicionar novas atividades
- Editar atividades existentes
- Remover atividades

#### 5. **Atividades Realizadas**
- Visualizar todas as atividades realizadas
- Adicionar novas atividades
- Editar atividades existentes
- Remover atividades

#### 6. **Outras Informações**
- **Missionário de Oração:**
  - Nome
  - Data de nascimento
  - Campo
  - WhatsApp

- **Observações:**
  - Lista de observações
  - Adicionar/editar/remover observações

### Menu Arquivo

- **Abrir...**: Abre um arquivo JSON diferente
- **Salvar**: Salva as alterações no arquivo atual
- **Salvar como...**: Salva em um novo arquivo
- **Gerar Word**: Gera o documento Word automaticamente (requer `gerar_agenda.py`)
- **Sair**: Fecha a aplicação

### Dicas de Uso

1. **Sempre salve antes de fechar**: Use "Salvar" ou "Salvar como..." antes de fechar a aplicação
2. **Selecione antes de editar**: Clique no item na lista/tabela antes de clicar em "Editar"
3. **Confirmação de remoção**: O sistema pede confirmação antes de remover itens
4. **Geração automática**: Após salvar, você pode gerar o Word diretamente pelo menu

### Requisitos

- Python 3.x
- tkinter (geralmente já vem com Python)
- python-docx (para gerar Word - instale com `pip install python-docx`)

### Vantagens da Interface Gráfica

✅ Visual e intuitiva  
✅ Não precisa conhecer JSON  
✅ Validação de dados  
✅ Organização por abas  
✅ Fácil adicionar/editar/remover  
✅ Geração de Word integrada  

### Comparação com Editor de Linha de Comando

| Recurso | GUI | CLI |
|---------|-----|-----|
| Facilidade de uso | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Visualização | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Edição rápida | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Adequado para iniciantes | ⭐⭐⭐⭐⭐ | ⭐⭐ |

Use a interface gráfica se preferir uma experiência visual e mais amigável!
