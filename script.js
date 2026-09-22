// URL da sua API ou endpoint que retorna as leituras do banco de dados
const API_URL = "http://localhost/api/leituras.php"; // Altere conforme o seu ambiente (ou cliente Supabase)

async function buscarDadosIoT() {
  try {
    const resposta = await fetch(API_URL);
    const dados = await resposta.json();

    if (dados && dados.length > 0) {
      // Pega a medição mais recente (último item ou primeiro, dependendo de como sua API ordena)
      const ultimaLeitura = dados[dados.length - 1];

      // Atualiza os cards principais
      document.getElementById("temp-atual").innerText =
        `${Number(ultimaLeitura.temperatura).toFixed(1)} °C`;
      document.getElementById("umid-atual").innerText =
        `${Number(ultimaLeitura.umidade).toFixed(1)} %`;
      document.getElementById("disp-atual").innerText =
        ultimaLeitura.dispositivo;
      document.getElementById("hora-atual").innerText = ultimaLeitura.data_hora;

      // Atualiza a tabela de histórico
      atualizarTabela(dados);
    }
  } catch (erro) {
    console.error("Erro ao buscar dados da API:", erro);
  }
}

function atualizarTabela(historico) {
  const tbody = document.getElementById("tabela-historico");
  tbody.innerHTML = ""; // Limpa a tabela antes de preencher

  // Mostra as últimas medições (invertido para exibir as mais recentes no topo, se preferir)
  const ultimas = [...historico].reverse().slice(0, 10); // Pega até 10 registros

  ultimas.forEach((item) => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
            <td>${item.data_hora}</td>
            <td>${item.dispositivo}</td>
            <td>${Number(item.temperatura).toFixed(1)} °C</td>
            <td>${Number(item.umidade).toFixed(1)} %</td>
        `;

    tbody.appendChild(tr);
  });
}

// Executa a busca assim que a página carrega
buscarDadosIoT();

// Configura a atualização automática a cada 5 segundos (Nível 2 do desafio)
setInterval(buscarDadosIoT, 5000);
