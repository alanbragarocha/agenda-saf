# 📸 Guia de Uso - Fotos na Agenda

## Como Adicionar Fotos

Agora você pode adicionar fotos na agenda! As fotos serão incluídas automaticamente no documento Word gerado.

### ✅ Onde Adicionar Fotos:

1. **Foto da Presidente** - Na aba "Informações Gerais"
2. **Fotos dos Membros da Diretoria** - Ao editar cada membro
3. **Foto de cada SAF** - Na aba "SAFs", ao editar cada SAF
4. **Foto do Missionário de Oração** - Na aba "Outras Informações"

### 📋 Como Adicionar uma Foto:

1. Clique no botão **"Selecionar Foto"** no formulário correspondente
2. Escolha a imagem do seu computador
3. A foto será **automaticamente copiada** para a pasta `fotos/` do projeto
4. Salve o formulário

### 📁 Localização das Fotos:

- **Pasta de armazenamento**: `fotos/` (dentro da pasta do projeto)
- **Formato recomendado**: JPG, PNG, GIF ou BMP
- **Tamanho recomendado**: 
  - Fotos de perfil (pessoas): 300x400 pixels
  - Fotos de SAF/Igreja: 800x600 pixels

### 💡 Dicas:

- ✅ As fotos são copiadas para a pasta `fotos/` automaticamente
- ✅ Você pode usar caminhos relativos ou absolutos
- ✅ Se a foto não for encontrada, o programa avisará mas continuará funcionando
- ✅ Fotos são opcionais - o programa funciona normalmente sem elas

### 🔧 Estrutura no JSON:

As fotos são armazenadas como caminho relativo no JSON:

```json
{
  "presidente": {
    "nome": "Maria Lúcia...",
    "foto": "presidente.jpg"
  },
  "diretoria": [
    {
      "cargo": "Presidente",
      "nome": "Maria",
      "foto": "presidente_diretoria.jpg"
    }
  ],
  "safs": [
    {
      "numero": 1,
      "nome": "SAF Central",
      "foto": "saf_central.jpg"
    }
  ],
  "informacoes_gerais": {
    "missionario_oracao": {
      "nome": "Rev. João",
      "foto": "missionario.jpg"
    }
  }
}
```

### ⚠️ Importante:

- Mantenha a pasta `fotos/` junto com o projeto
- Ao gerar o Word, certifique-se de que as fotos estão na pasta `fotos/`
- Se mover o projeto, mova a pasta `fotos/` também
- Fotos muito grandes podem aumentar o tamanho do documento Word

### 🎯 Tamanhos das Fotos no Word:

- **Foto da Presidente**: 1.5" x 2.0" (centro)
- **Fotos da Diretoria**: 1.2" x 1.6" (centro)
- **Foto da SAF**: 2.0" x 1.5" (centro)
- **Foto do Missionário**: 1.5" x 2.0" (centro)

Tudo pronto! Agora você pode adicionar fotos à sua agenda! 📸✨
