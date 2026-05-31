<script setup>
import { ref, onMounted } from 'vue'

const dadosBanco = ref(null)
const listaEquipamentos = ref([])
const abaAtual = ref('visaoGeral') 

// Modelo reativo para capturar os dados digitados no formulário
const novoEquipamento = ref({
  nome: '',
  categoria: 'Veiculo',
  modelo: '',
  nro_serie_chassi: ''
})

// Função centralizada para carregar todos os dados da API
const carregarDadosDoSistema = async () => {
  try {
    // 1. Puxa o status das tabelas
    const resBanco = await fetch('http://127.0.0.1:8000/banco-status')
    dadosBanco.value = await resBanco.json()

    // 2. Puxa os equipamentos reais salvos no banco
    const resEquip = await fetch('http://127.0.0.1:8000/equipamentos')
    listaEquipamentos.value = await resEquip.json()
  } catch (erro) {
    console.error("Falha ao atualizar dados da API:", erro)
  }
}

// Função executada quando o usuário clica no botão de salvar
const dispararCadastro = async () => {
  if (!novoEquipamento.value.nome) {
    alert("O nome do equipamento é obrigatório!")
    return
  }

  try {
    const resposta = await fetch('http://127.0.0.1:8000/equipamentos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(novoEquipamento.value)
    })

    if (resposta.ok) {
      alert("Sucesso! O dado trafegou e foi salvo no MySQL. 💾")
      // Limpa os campos do formulário para o próximo cadastro
      novoEquipamento.value = { nome: '', categoria: 'Veiculo', modelo: '', nro_serie_chassi: '' }
      // Recarrega a lista do banco para atualizar o contador da home e a tabela
      await carregarDadosDoSistema()
    } else {
      const respostaErro = await resposta.json()
      alert("Erro do Servidor: " + (respostaErro.detail || "Falha desconhecida"))
    }
  } catch (erro) {
    console.error("Erro na conexão:", erro)
    alert("Não foi possível alcançar a API.")
  }
}

onMounted(() => {
  carregarDadosDoSistema()
})
</script>

<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="logo">
        <h2>SIGAgro 🌱</h2>
      </div>
      <nav class="menu">
        <a href="#" class="menu-item" :class="{ active: abaAtual === 'visaoGeral' }" @click.prevent="abaAtual = 'visaoGeral'">Visão Geral</a>
        <a href="#" class="menu-item" :class="{ active: abaAtual === 'equipamentos' }" @click.prevent="abaAtual = 'equipamentos'">Equipamentos</a>
        <a href="#" class="menu-item" :class="{ active: abaAtual === 'zonas' }" @click.prevent="abaAtual = 'zonas'">Zonas de Cultivo</a>
        <a href="#" class="menu-item" :class="{ active: abaAtual === 'sensores' }" @click.prevent="abaAtual = 'sensores'">Sensores</a>
      </nav>
    </aside>

    <main class="main-content">
      <header class="topbar">
        <h1>
          {{ abaAtual === 'visaoGeral' ? 'Visão Geral do Sistema' : '' }}
          {{ abaAtual === 'equipamentos' ? 'Gestão de Equipamentos' : '' }}
          {{ abaAtual === 'zonas' ? 'Zonas de Cultivo' : '' }}
          {{ abaAtual === 'sensores' ? 'Telemetria e Sensores' : '' }}
        </h1>
        <div class="status-badge" :class="{ connected: dadosBanco }">
          {{ dadosBanco ? 'Banco Conectado' : 'Conectando...' }}
        </div>
      </header>

      <section v-if="abaAtual === 'visaoGeral'" class="cards-grid">
        <div class="card">
          <h3>Status da Irrigação</h3>
          <p class="big-number">Normal</p>
          <span class="subtitle">Última leitura há 5 min</span>
        </div>
        
        <div class="card">
          <h3>Equipamentos Ativos</h3>
          <p class="big-number" style="color: #42b883;">{{ listaEquipamentos.length }}</p>
          <span class="subtitle">{{ listaEquipamentos.length > 0 ? 'Ativos rodando e mapeados' : 'Nenhum item registrado' }}</span>
        </div>

        <div class="card system-card" v-if="dadosBanco">
          <h3>Tabelas do Sistema</h3>
          <div class="tags-container">
            <span class="tag" v-for="(tabela, index) in dadosBanco.tabelas_encontradas" :key="index">
              {{ tabela.Tables_in_sigagro }}
            </span>
          </div>
        </div>
      </section>

      <section v-if="abaAtual === 'equipamentos'" class="equipamentos-container">
        <div class="card form-card">
          <h3>Registrar Novo Ativo de Campo</h3>
          <form @submit.prevent="dispararCadastro" class="cadastro-form">
            <div class="form-group">
              <label>Nome do Equipamento *</label>
              <input v-model="novoEquipamento.nome" type="text" placeholder="Ex: Trator John Deere 5075E, Sensor de Solo Vasos" required />
            </div>

            <div class="form-group">
              <label>Categoria</label>
              <select v-model="novoEquipamento.categoria">
                <option value="Veiculo">Veículo / Maquinário</option>
                <option value="Implemento">Implemento Agrícola</option>
                <option value="Irrigacao">Sistema de Irrigação / Válvulas</option>
                <option value="Sensor">Sensor de Telemetria</option>
              </select>
            </div>

            <div class="form-group">
              <label>Modelo</label>
              <input v-model="novoEquipamento.modelo" type="text" placeholder="Ex: V1-Arduino, JD-2026" />
            </div>

            <div class="form-group">
              <label>Número de Série / Chassi</label>
              <input v-model="novoEquipamento.nro_serie_chassi" type="text" placeholder="Ex: SN-883192, CH-99123" />
            </div>

            <button type="submit" class="btn-submit">Salvar no Banco de Dados 💾</button>
          </form>
        </div>

        <div class="card table-card" style="margin-top: 2rem;">
          <h3>Registros Encontrados no MySQL</h3>
          
          <div v-if="listaEquipamentos.length === 0" style="color: var(--text-muted); padding: 1rem 0;">
            Nenhum equipamento cadastrado ainda. Use o formulário acima para criar o primeiro registro!
          </div>
          
          <div v-else class="table-responsive">
            <table class="dados-tabela">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nome</th>
                  <th>Categoria</th>
                  <th>Modelo</th>
                  <th>Nº de Série</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="equip in listaEquipamentos" :key="equip.id">
                  <td>{{ equip.id }}</td>
                  <td style="font-weight: 600;">{{ equip.nome }}</td>
                  <td><span class="badge-cat">{{ equip.categoria }}</span></td>
                  <td>{{ equip.modelo || '-' }}</td>
                  <td style="font-family: monospace; color: #a0a0a0;">{{ equip.nro_serie_chassi || '-' }}</td>
                  <td><span class="badge-status disponivel">{{ equip.status }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section v-if="abaAtual === 'zonas'">
        <div class="card">
          <h3>Áreas de Plantio e Zonas de Manejo</h3>
          <p style="color: var(--text-muted); margin-top: 1rem;">
            Espaço reservado para o mapeamento e configuração dos canteiros e sistemas de gotejamento das mudas.
          </p>
        </div>
      </section>

      <section v-if="abaAtual === 'sensores'">
        <div class="card">
          <h3>Monitoramento de Telemetria</h3>
          <p style="color: var(--text-muted); margin-top: 1rem;">
            Aqui entrarão as leituras em tempo real coletadas do ambiente (umidade do solo, temperatura e luminosidade).
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<style>
:root {
  --bg-dark: #121212;
  --bg-panel: #1e1e1e;
  --bg-card: #2a2a2a;
  --accent: #42b883;
  --text-main: #ffffff;
  --text-muted: #a0a0a0;
  --input-bg: #1a1a1a;
  --border-color: #383838;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif; 
  background-color: var(--bg-dark);
  color: var(--text-main);
}

.dashboard-layout { display: flex; min-height: 100vh; }
.sidebar { width: 250px; background-color: var(--bg-panel); padding: 2rem 1rem; border-right: 1px solid var(--border-color); flex-shrink: 0; }
.logo h2 { color: var(--accent); margin-top: 0; margin-bottom: 2rem; padding-left: 1rem; }
.menu { display: flex; flex-direction: column; gap: 0.5rem; }
.menu-item { color: var(--text-muted); text-decoration: none; padding: 0.75rem 1rem; border-radius: 8px; transition: all 0.2s; }
.menu-item:hover, .menu-item.active { background-color: rgba(66, 184, 131, 0.1); color: var(--accent); }
.main-content { flex: 1; padding: 2rem 3rem; overflow-y: auto; }
.topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3rem; }
.status-badge { padding: 0.5rem 1rem; background-color: #333; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.status-badge.connected { background-color: rgba(66, 184, 131, 0.2); color: var(--accent); }
.cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
.card { background-color: var(--bg-card); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border-color); }
.card h3 { margin-top: 0; color: var(--text-muted); font-size: 1rem; font-weight: 500; margin-bottom: 1rem; }
.big-number { font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; }
.subtitle { font-size: 0.85rem; color: var(--text-muted); }
.tags-container { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }
.tag { background-color: #333; padding: 0.4rem 0.8rem; border-radius: 4px; font-size: 0.8rem; font-family: monospace; }

/* CSS do Formulário */
.cadastro-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
}
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-group label { font-size: 0.85rem; color: var(--text-muted); }
.form-group input, .form-group select {
  background-color: var(--input-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 0.7rem;
  color: white;
  font-size: 0.95rem;
}
.form-group input:focus, .form-group select:focus { border-color: var(--accent); outline: none; }
.btn-submit {
  grid-column: span 2;
  background-color: var(--accent);
  color: #121212;
  border: none;
  border-radius: 6px;
  padding: 0.8rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: opacity 0.2s;
}
.btn-submit:hover { opacity: 0.9; }

/* CSS da Tabela */
.table-responsive { overflow-x: auto; margin-top: 1rem; }
.dados-tabela { width: 100%; border-collapse: collapse; text-align: left; }
.dados-tabela th, .dados-tabela td { padding: 0.8rem; border-bottom: 1px solid var(--border-color); font-size: 0.95rem; }
.dados-tabela th { color: var(--text-muted); font-weight: 500; }
.badge-cat { background-color: #3a3a3a; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; }
.badge-status.disponivel { color: var(--accent); background-color: rgba(66, 184, 131, 0.1); padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600; }
</style>