<script setup>
import { ref, onMounted } from 'vue'

const dadosBanco = ref(null)

onMounted(async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/banco-status')
    dadosBanco.value = await resposta.json()
  } catch (erro) {
    console.error("Erro ao buscar dados na API:", erro)
  }
})
</script>

<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="logo">
        <h2>SIGAgro 🌱</h2>
      </div>
      <nav class="menu">
        <a href="#" class="menu-item active">Visão Geral</a>
        <a href="#" class="menu-item">Equipamentos</a>
        <a href="#" class="menu-item">Zonas de Cultivo</a>
        <a href="#" class="menu-item">Sensores</a>
      </nav>
    </aside>

    <main class="main-content">
      <header class="topbar">
        <h1>Visão Geral do Sistema</h1>
        <div class="status-badge" :class="{ connected: dadosBanco }">
          {{ dadosBanco ? 'Banco Conectado' : 'Conectando...' }}
        </div>
      </header>

      <section class="cards-grid">
        <div class="card">
          <h3>Status da Irrigação</h3>
          <p class="big-number">Normal</p>
          <span class="subtitle">Última leitura há 5 min</span>
        </div>
        
        <div class="card">
          <h3>Equipamentos Ativos</h3>
          <p class="big-number">0</p>
          <span class="subtitle">Cadastre o primeiro ativo</span>
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
    </main>
  </div>
</template>

<style>
/* Reset básico e tipografia */
:root {
  --bg-dark: #121212;
  --bg-panel: #1e1e1e;
  --bg-card: #2a2a2a;
  --accent: #42b883;
  --text-main: #ffffff;
  --text-muted: #a0a0a0;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif; /* Perfeito para trocar por uma fonte customizada depois */
  background-color: var(--bg-dark);
  color: var(--text-main);
}

/* Layout do Dashboard */
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 250px;
  background-color: var(--bg-panel);
  padding: 2rem 1rem;
  border-right: 1px solid #333;
}

.logo h2 {
  color: var(--accent);
  margin-top: 0;
  margin-bottom: 2rem;
  padding-left: 1rem;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-item {
  color: var(--text-muted);
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  transition: all 0.2s;
}

.menu-item:hover, .menu-item.active {
  background-color: rgba(66, 184, 131, 0.1);
  color: var(--accent);
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 2rem 3rem;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  background-color: #333;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.connected {
  background-color: rgba(66, 184, 131, 0.2);
  color: var(--accent);
}

/* Grid de Cards */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.card {
  background-color: var(--bg-card);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #333;
}

.card h3 {
  margin-top: 0;
  color: var(--text-muted);
  font-size: 1rem;
  font-weight: 500;
}

.big-number {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0.5rem 0;
}

.subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
}

/* Tags das tabelas */
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.tag {
  background-color: #333;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-family: monospace;
}
</style>