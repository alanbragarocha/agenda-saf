#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface web simples para editar os dados da agenda
Execute e acesse http://localhost:5000 no navegador
"""

import json
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import os

app = Flask(__name__)
ARQUIVO_JSON = 'agenda_data.json'

# Template HTML simples
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Editor de Agenda - Federação de SAFs</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
        .tabs { display: flex; border-bottom: 2px solid #ddd; margin-bottom: 20px; }
        .tab { padding: 10px 20px; cursor: pointer; background: #f0f0f0; border: none; border-top-left-radius: 5px; border-top-right-radius: 5px; margin-right: 5px; }
        .tab.active { background: #4CAF50; color: white; }
        .tab-content { display: none; padding: 20px; }
        .tab-content.active { display: block; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #4CAF50; color: white; }
        tr:hover { background: #f5f5f5; }
        button { padding: 8px 15px; margin: 5px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #45a049; }
        button.danger { background: #f44336; }
        button.danger:hover { background: #da190b; }
        input, textarea, select { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; width: 300px; }
        textarea { width: 100%; height: 150px; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        .success { background: #4CAF50; color: white; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .error { background: #f44336; color: white; padding: 10px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Editor de Agenda - Federação de SAFs</h1>

        <div class="tabs">
            <button class="tab active" onclick="showTab('info')">Informações Gerais</button>
            <button class="tab" onclick="showTab('diretoria')">Diretoria</button>
            <button class="tab" onclick="showTab('safs')">SAFs</button>
            <button class="tab" onclick="showTab('atividades')">Atividades</button>
            <button class="tab" onclick="showTab('outras')">Outras Info</button>
        </div>

        <div id="info" class="tab-content active">
            <h2>Informações Gerais</h2>
            <form method="POST" action="/salvar_info">
                <div class="form-group">
                    <label>Ano:</label>
                    <input type="number" name="ano" value="{{ dados.ano }}" required>
                </div>
                <div class="form-group">
                    <label>Nome da Presidente:</label>
                    <input type="text" name="presidente_nome" value="{{ dados.presidente.nome }}" required>
                </div>
                <div class="form-group">
                    <label>Mensagem da Presidente:</label>
                    <textarea name="presidente_mensagem" required>{{ dados.presidente.mensagem }}</textarea>
                </div>
                <button type="submit">Salvar</button>
            </form>
        </div>

        <div id="diretoria" class="tab-content">
            <h2>Diretoria</h2>
            <button onclick="window.location.href='/adicionar_membro'">➕ Adicionar Membro</button>
            <table>
                <tr>
                    <th>Cargo</th>
                    <th>Nome</th>
                    <th>Data Nasc.</th>
                    <th>Email</th>
                    <th>Ações</th>
                </tr>
                {% for membro in dados.diretoria %}
                <tr>
                    <td>{{ membro.cargo }}</td>
                    <td>{{ membro.nome }}</td>
                    <td>{{ membro.data_nascimento }}</td>
                    <td>{{ membro.email or '' }}</td>
                    <td>
                        <a href="/editar_membro/{{ loop.index0 }}"><button>Editar</button></a>
                        <a href="/remover_membro/{{ loop.index0 }}"><button class="danger">Remover</button></a>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div id="safs" class="tab-content">
            <h2>SAFs</h2>
            <button onclick="window.location.href='/adicionar_saf'">➕ Adicionar SAF</button>
            <table>
                <tr>
                    <th>#</th>
                    <th>Nome</th>
                    <th>Presidente</th>
                    <th>Pastor</th>
                    <th>Ações</th>
                </tr>
                {% for saf in dados.safs %}
                <tr>
                    <td>{{ saf.numero }}</td>
                    <td>{{ saf.nome }}</td>
                    <td>{{ saf.presidente.nome if saf.presidente else '' }}</td>
                    <td>{{ saf.pastor.nome if saf.pastor else '' }}</td>
                    <td>
                        <a href="/editar_saf/{{ loop.index0 }}"><button>Editar</button></a>
                        <a href="/remover_saf/{{ loop.index0 }}"><button class="danger">Remover</button></a>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div id="atividades" class="tab-content">
            <h2>Atividades</h2>
            <h3>Planejadas</h3>
            <select id="mes_atividade" onchange="carregarAtividades()">
                <option value="janeiro">Janeiro</option>
                <option value="fevereiro">Fevereiro</option>
                <option value="marco">Março</option>
                <option value="abril">Abril</option>
                <option value="maio">Maio</option>
                <option value="junho">Junho</option>
                <option value="julho">Julho</option>
                <option value="agosto">Agosto</option>
                <option value="setembro">Setembro</option>
                <option value="outubro">Outubro</option>
                <option value="novembro">Novembro</option>
                <option value="dezembro">Dezembro</option>
            </select>
            <button onclick="adicionarAtividade()">➕ Adicionar</button>
            <div id="lista_atividades"></div>

            <h3>Realizadas</h3>
            <button onclick="window.location.href='/adicionar_atividade_realizada'">➕ Adicionar</button>
            <table>
                <tr>
                    <th>Data</th>
                    <th>Descrição</th>
                    <th>Ações</th>
                </tr>
                {% for ativ in dados.atividades_realizadas_2023 %}
                <tr>
                    <td>{{ ativ.data or '' }}</td>
                    <td>{{ ativ.descricao }}</td>
                    <td>
                        <a href="/editar_atividade_realizada/{{ loop.index0 }}"><button>Editar</button></a>
                        <a href="/remover_atividade_realizada/{{ loop.index0 }}"><button class="danger">Remover</button></a>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div id="outras" class="tab-content">
            <h2>Outras Informações</h2>
            <h3>Missionário de Oração</h3>
            <form method="POST" action="/salvar_missionario">
                <div class="form-group">
                    <label>Nome:</label>
                    <input type="text" name="nome" value="{{ dados.informacoes_gerais.missionario_oracao.nome if dados.informacoes_gerais.missionario_oracao else '' }}">
                </div>
                <div class="form-group">
                    <label>Data Nasc.:</label>
                    <input type="text" name="data_nascimento" value="{{ dados.informacoes_gerais.missionario_oracao.data_nascimento if dados.informacoes_gerais.missionario_oracao else '' }}">
                </div>
                <div class="form-group">
                    <label>Campo:</label>
                    <input type="text" name="campo" value="{{ dados.informacoes_gerais.missionario_oracao.campo if dados.informacoes_gerais.missionario_oracao else '' }}">
                </div>
                <div class="form-group">
                    <label>WhatsApp:</label>
                    <input type="text" name="whatsapp" value="{{ dados.informacoes_gerais.missionario_oracao.whatsapp if dados.informacoes_gerais.missionario_oracao else '' }}">
                </div>
                <button type="submit">Salvar</button>
            </form>

            <h3>Observações</h3>
            <form method="POST" action="/adicionar_observacao">
                <input type="text" name="observacao" placeholder="Nova observação" style="width: 500px;">
                <button type="submit">Adicionar</button>
            </form>
            <ul>
                {% for obs in dados.informacoes_gerais.observacoes %}
                <li>
                    {{ obs }}
                    <a href="/remover_observacao/{{ loop.index0 }}"><button class="danger" style="padding: 3px 8px;">Remover</button></a>
                </li>
                {% endfor %}
            </ul>
        </div>

        <div style="margin-top: 30px; padding: 20px; background: #e8f5e9; border-radius: 4px;">
            <h3>Gerar Documento Word</h3>
            <a href="/gerar_word"><button style="background: #2196F3; padding: 10px 20px;">📄 Gerar Agenda Word</button></a>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // Esconder todas as abas
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // Mostrar aba selecionada
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function carregarAtividades() {
            const mes = document.getElementById('mes_atividade').value;
            fetch(`/api/atividades/${mes}`)
                .then(r => r.json())
                .then(data => {
                    let html = '<table><tr><th>Data</th><th>Descrição</th><th>Ações</th></tr>';
                    data.forEach((ativ, idx) => {
                        html += `<tr><td>${ativ.data || ''}</td><td>${ativ.descricao}</td><td><a href="/editar_atividade/${mes}/${idx}"><button>Editar</button></a> <a href="/remover_atividade/${mes}/${idx}"><button class="danger">Remover</button></a></td></tr>`;
                    });
                    html += '</table>';
                    document.getElementById('lista_atividades').innerHTML = html;
                });
        }

        function adicionarAtividade() {
            const mes = document.getElementById('mes_atividade').value;
            window.location.href = `/adicionar_atividade/${mes}`;
        }

        // Carregar atividades ao iniciar
        carregarAtividades();
    </script>
</body>
</html>
"""

def carregar_dados():
    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "ano": 2024,
            "presidente": {"nome": "", "mensagem": ""},
            "diretoria": [],
            "safs": [],
            "atividades_realizadas_2023": [],
            "atividades_planejadas_2024": {m: [] for m in ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']},
            "informacoes_gerais": {
                "missionario_oracao": {"nome": "", "data_nascimento": "", "campo": "", "whatsapp": ""},
                "observacoes": [],
                "lema": []
            }
        }

def salvar_dados(dados):
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    dados = carregar_dados()
    return render_template_string(TEMPLATE, dados=dados)

@app.route('/salvar_info', methods=['POST'])
def salvar_info():
    dados = carregar_dados()
    dados['ano'] = int(request.form['ano'])
    dados['presidente']['nome'] = request.form['presidente_nome']
    dados['presidente']['mensagem'] = request.form['presidente_mensagem']
    salvar_dados(dados)
    return redirect('/')

@app.route('/api/atividades/<mes>')
def api_atividades(mes):
    dados = carregar_dados()
    atividades = dados.get('atividades_planejadas_2024', {}).get(mes, [])
    return jsonify(atividades)

if __name__ == '__main__':
    print("=" * 60)
    print("Interface Web - Editor de Agenda")
    print("=" * 60)
    print(f"Acesse: http://localhost:5000")
    print("Pressione Ctrl+C para parar")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
