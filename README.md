# Sistema de Automação da Agenda da Federação de SAFs

Este sistema automatiza a criação e gerenciamento da agenda anual da Federação de SAFs de Macaé.

## Arquivos

- `agenda_data.json` - Arquivo JSON com todos os dados estruturados da agenda
- `gerar_agenda.py` - Script para gerar o documento Word a partir do JSON
- `editar_agenda.py` - Interface de linha de comando para editar os dados
- `editar_agenda_gui.py` - **Interface gráfica** para editar os dados (recomendado!)
- `requirements.txt` - Dependências Python necessárias

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Gerar o documento Word

Para gerar a agenda em formato Word a partir do arquivo JSON:

```bash
python3 gerar_agenda.py
```

Ou especificando arquivos customizados:

```bash
python3 gerar_agenda.py agenda_data.json "Agenda 2024.docx"
```

### Editar os dados

#### Opção 1: Interface Gráfica (Recomendado) 🎨

Para uma experiência visual e intuitiva:

```bash
python3 editar_agenda_gui.py
```

A interface gráfica oferece:
- ✅ Visualização em tabelas e listas
- ✅ Edição com formulários organizados
- ✅ Abas para diferentes seções
- ✅ Fácil adicionar/editar/remover itens
- ✅ Geração de Word integrada

Veja mais detalhes em `README_GUI.md`

#### Opção 2: Interface de Linha de Comando

Para editar via terminal:

```bash
python3 editar_agenda.py
```

O editor permite:
- Editar membros da diretoria
- Editar informações das SAFs
- Adicionar atividades planejadas
- Visualizar os dados em formato JSON

### Editar manualmente o JSON

Você também pode editar diretamente o arquivo `agenda_data.json` usando qualquer editor de texto. O formato é autoexplicativo e bem estruturado.

## Estrutura dos Dados

O arquivo `agenda_data.json` contém:

- **ano**: Ano da agenda
- **presidente**: Informações e mensagem da presidente
- **diretoria**: Lista de membros da diretoria com cargos, nomes, datas de nascimento, emails e endereços
- **safs**: Lista de todas as SAFs com informações completas (endereço, pastor, presidente, conselheiro, aniversário)
- **atividades_realizadas_2023**: Lista de atividades realizadas no ano anterior
- **atividades_planejadas_2024**: Atividades planejadas organizadas por mês
- **informacoes_gerais**: Informações adicionais (missionário de oração, observações, lema)

## Vantagens da Automação

1. **Facilidade de atualização**: Basta editar o JSON e gerar novamente o documento
2. **Consistência**: Formatação padronizada automaticamente
3. **Versionamento**: O JSON pode ser versionado no Git
4. **Reutilização**: Dados podem ser usados para gerar outros documentos ou relatórios
5. **Busca e filtragem**: Fácil encontrar informações específicas no JSON

## Próximos Passos (Sugestões)

- Interface web para edição
- Geração automática de calendário
- Exportação para PDF
- Integração com banco de dados
- Geração de relatórios estatísticos
