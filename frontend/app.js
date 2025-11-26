document.addEventListener("DOMContentLoaded", () => {
  const queries = [
    { id: 1, title: "Faturamento mensal por filial", rota: "/relatorios/faturamento-mensal-filial", fields: [{ name: "ano", type: "number", placeholder: "Ex: 2025" }, { name: "mes", type: "number", placeholder: "1-12" }] },
    { id: 2, title: "Top clientes que mais gastaram", rota: "/relatorios/top-clientes-mais-gastaram", fields: [{ name: "limite", type: "number", placeholder: "Default: 10" }] },
    { id: 3, title: "Ticket médio fidelizado vs não fidelizado", rota: "/relatorios/ticket-medio-fidelizado", fields: [{ name: "ano", type: "number", placeholder: "Ex: 2025" }, { name: "mes", type: "number", placeholder: "1-12" }] },
    { id: 4, title: "Ranking de funcionários por vendas", rota: "/relatorios/ranking-funcionarios-vendas", fields: [{ name: "limite", type: "number", placeholder: "Default: 10" }] },
    { id: 5, title: "Produtos mais vendidos", rota: "/relatorios/produtos-mais-vendidos", fields: [{ name: "quantidade_minima", type: "number", placeholder: "Default: 50" }] },
    { id: 6, title: "Produtos com maior índice de devolução", rota: "/relatorios/produtos-maior-indice-devolucao", fields: [{ name: "limite", type: "number", placeholder: "Default: 10" }] },
    { id: 7, title: "Produtos com estoque abaixo do mínimo", rota: "/relatorios/produtos-estoque-abaixo-minimo", fields: [{ name: "endereco_filial", type: "text", placeholder: "Opcional" }] },
    { id: 8, title: "Fornecedores por volume de pedidos", rota: "/relatorios/fornecedores-maior-volume-pedidos", fields: [{ name: "limite", type: "number", placeholder: "Default: 10" }] },
    { id: 9, title: "Distribuição por forma de pagamento", rota: "/relatorios/distribuicao-vendas-forma-pagamento", fields: [{ name: "ano", type: "number", placeholder: "Ex: 2025" }, { name: "mes", type: "number", placeholder: "1-12" }] },
    { id: 10, title: "Clientes com gasto acima da média", rota: "/relatorios/clientes-gasto-acima-media", fields: [{ name: "limite", type: "number", placeholder: "Opcional" }] }
  ];

  const tabButtons = document.getElementById("tab-buttons");
  const tabContents = document.getElementById("tab-contents");

  // Botão Home
  const homeBtn = document.createElement("button");
  homeBtn.textContent = "Home";
  homeBtn.classList.add("active");
  homeBtn.addEventListener("click", openHome);
  tabButtons.appendChild(homeBtn);

  const homeContent = document.createElement("div");
  homeContent.classList.add("active");
  homeContent.innerHTML = `
    <div class="card">
      <p>Bem-vindos à <strong>Curious about fashion</strong>! Somos uma loja de roupas femininas, trazendo estilo e elegância para o seu dia a dia.</p>
    </div>
  `;
  tabContents.appendChild(homeContent);

  // Criar botões e conteúdos das queries
  queries.forEach((q, index) => {
    const btn = document.createElement("button");
    btn.textContent = q.title;
    btn.addEventListener("click", () => openTab(index + 1));
    tabButtons.appendChild(btn);

    const tab = document.createElement("div");
    tab.innerHTML = `
        <div class="card">
        <h2>${q.title}</h2> <!-- Título adicionado aqui -->
        <form data-rota="${q.rota}" id="form-${q.id}">
            ${q.fields.map(f => `
                <label>${f.name}
                    <input name="${f.name}" type="${f.type}" placeholder="${f.placeholder || ''}">
                </label>`).join('')}
              <button type="submit">Executar</button>
        </form>
            <div class="output" id="output-${q.id}"></div>
         </div>
`;
    tab.querySelector("form").addEventListener("submit", (e) => handleSubmit(e, q.id));
    tabContents.appendChild(tab);

    //carrossel
    const slidesContainer = document.querySelector(".carousel .slides");
  const slides = document.querySelectorAll(".carousel img");
  const prevBtn = document.querySelector(".carousel .prev");
  const nextBtn = document.querySelector(".carousel .next");
  let currentIndex = 0;

  function showSlide(index) {
    const offset = -index * 100;
    slidesContainer.style.transform = `translateX(${offset}%)`;
  }

  prevBtn.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(currentIndex);
  });

  nextBtn.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
  });

  // Carrossel automático (opcional)
  setInterval(() => {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
  }, 5000); // troca a cada 5 segundos

  });

  function openHome() {
    document.querySelectorAll(".sidebar button").forEach(b => b.classList.remove("active"));
    homeBtn.classList.add("active");
    document.querySelectorAll(".main-content > div").forEach(d => d.classList.remove("active"));
    homeContent.classList.add("active");
  }

  function openTab(index) {
    document.querySelectorAll(".sidebar button").forEach((b, i) => b.classList.toggle("active", i === index));
    document.querySelectorAll(".main-content > div").forEach((t, i) => t.classList.toggle("active", i === index));
  }

  async function handleSubmit(event, id) {
    event.preventDefault();
    const form = event.target;
    const rota = form.getAttribute("data-rota");
    const baseUrl = "http://localhost:8000"; 
    const params = new URLSearchParams();
    for (const el of form.elements) {
      if (el.name && el.value !== "") params.append(el.name, el.value);
    }
    const url = `${baseUrl}${rota}${params.toString() ? "?" + params.toString() : ""}`;
    const output = document.getElementById(`output-${id}`);
    output.textContent = "Carregando...";
    try {
      const res = await fetch(url);
      let data;
      try { data = await res.json(); } catch { 
        const text = await res.text();
        throw new Error(`Resposta não-JSON (status ${res.status}): ${text}`);
      }
      if (!res.ok) throw new Error(JSON.stringify(data));
      renderOutput(data, output);
    } catch (err) {
      output.textContent = "Erro: " + err.message;
    }
  }

  function renderOutput(data, output) {
    if (Array.isArray(data) && data.length > 0 && typeof data[0] === "object") {
      const table = document.createElement("table");
      const header = table.createTHead();
      const headerRow = header.insertRow();
      Object.keys(data[0]).forEach(key => {
        const th = document.createElement("th");
        th.textContent = key;
        headerRow.appendChild(th);
      });
      const tbody = table.createTBody();
      data.forEach(row => {
        const tr = tbody.insertRow();
        Object.values(row).forEach(val => {
          const td = tr.insertCell();
          td.textContent = val;
        });
      });
      output.innerHTML = "";
      output.appendChild(table);
    } else {
      output.textContent = JSON.stringify(data, null, 2);
    }
  }
});
