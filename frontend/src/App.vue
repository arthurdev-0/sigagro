<script setup>
import { ref, onMounted } from 'vue'

// Variável reativa para guardar a resposta do nosso back-end
const dadosBanco = ref(null)

// Quando a tela carregar, fazemos o pedido para o garçom (API)
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
  <main style="padding: 2rem; font-family: sans-serif; background-color: #1e1e1e; color: white; min-height: 100vh;">
    <h1>Painel SIGAgro 🌱</h1>
    
    <div v-if="dadosBanco" style="background-color: #2d2d2d; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
      <h2 style="color: #42b883;">{{ dadosBanco.mensagem }}</h2>
      
      <h3>Tabelas prontas para uso:</h3>
      <ul>
        <li v-for="(tabela, index) in dadosBanco.tabelas_encontradas" :key="index" style="margin-bottom: 0.5rem;">
          {{ tabela }}
        </li>
      </ul>
    </div>
    
    <div v-else>
      <p>Tentando conectar com o servidor Python...</p>
    </div>
  </main>
</template>

<style>
/* Resetando a margem padrão do navegador para o nosso fundo escuro cobrir tudo */
body { margin: 0; }
</style>