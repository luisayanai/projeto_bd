document.addEventListener("DOMContentLoaded", () => {

  /** NOVA estrutura agrupada */
  const grupos = {
    "Filial": [
      { id: 1, title: "Faturamento mensal por filial", rota: "/relatorios/faturamento-mensal-filial",
        fields: [
          { label: "Ano de consulta", name: "ano", type: "number", placeholder: "Exemplo: 2025" },
          { label: "Mês de consulta", name: "mes", type: "number", placeholder: "1-12" }
        ]
      }
    ],

    "Funcionários": [
      { id: 4, title: "Ranking de funcionários por vendas", rota: "/relatorios/ranking-funcionarios-vendas",
        fields: [
          { label: "Quantidade de funcionários", name: "limite", type: "number", placeholder: "Exemplo: 10" }
        ]
      }
    ],

    "Clientes": [
      { id: 2, title: "Top clientes que mais gastaram", rota: "/relatorios/top-clientes-mais-gastaram",
        fields: [
          { label: "Quantidade de clientes", name: "limite", type: "number", placeholder: "Exemplo: 10" }
        ]
      },
      { id: 10, title: "Clientes com gasto acima da média", rota: "/relatorios/clientes-gasto-acima-media",
        fields: [
          { label: "Quantidade de clientes", name: "limite", type: "number", placeholder: "Opcional" }
        ]
      }
    ],

    "Fornecedores": [
      { id: 8, title: "Fornecedores por volume de pedidos", rota: "/relatorios/fornecedores-maior-volume-pedidos",
        fields: [
          { label: "Quantidade de fornecedores", name: "limite", type: "number", placeholder: "Exemplo: 10" }
        ]
      }
    ],

    "Produtos": [
      { id: 5, title: "Produtos mais vendidos", rota: "/relatorios/produtos-mais-vendidos",
        fields: [
          { label: "Quantidade de produtos", name: "limite", type: "number", placeholder: "Exemplo: 10" }
        ]
      },
      { id: 6, title: "Produtos com maior índice de devolução", rota: "/relatorios/produtos-maior-indice-devolucao",
        fields: [
          { label: "Quantidade de produtos", name: "limite", type: "number", placeholder: "Exemplo: 10" }
        ]
      },
      { id: 7, title: "Produtos com estoque abaixo do mínimo", rota: "/relatorios/produtos-estoque-abaixo-minimo",
        fields: [
          { label: "Endereço de filial", name: "endereco_filial", type: "text", placeholder: "Opcional" }
        ]
      }
    ],

    "Formas de Pagamento": [
      { id: 9, title: "Distribuição por forma de pagamento", rota: "/relatorios/distribuicao-vendas-forma-pagamento",
        fields: [
          { label: "Ano de consulta", name: "ano", type: "number", placeholder: "Exemplo: 2025" },
          { label: "Mês de consulta", name: "mes", type: "number", placeholder: "1-12" }
        ]
      },
      { id: 3, title: "Valor médio gasto por clientes fidelizados e não fidelizados", rota: "/relatorios/ticket-medio-fidelizado",
        fields: [
          { label: "Ano de consulta", name: "ano", type: "number", placeholder: "Exemplo: 2025" },
          { label: "Mês", name: "mes", type: "number", placeholder: "1-12" }
        ]
      }
    ]
  };

  const tabButtons = document.getElementById("tab-buttons");
  const tabContents = document.getElementById("tab-contents");

  

  // ----------------- FUNÇÃO GLOBAL -----------------
  function marcarAtivo(elemento) {
    document.querySelectorAll("#tab-buttons button, #tab-buttons li")
      .forEach(el => el.classList.remove("active"));
    elemento.classList.add("active");
  }

  // ----------------- HOME -----------------
  const homeBtn = document.createElement("button");
  homeBtn.textContent = "Home";
  homeBtn.classList.add("active");
  homeBtn.addEventListener("click", () => {
    marcarAtivo(homeBtn);
    openHome();
  });
  tabButtons.appendChild(homeBtn);

  const homeContent = document.createElement("div");
  homeContent.classList.add("active");
  homeContent.innerHTML = `
      <div class="card">
        <p>Bem-vindos à <strong>Curious about fashion</strong>! Somos uma loja de roupas femininas, trazendo estilo e elegância para o seu dia a dia.</p>
      </div>

      <div class="carousel">
        <div class="slides">
          <img src="roupa1.jpg" alt="Roupa 1">
          <img src="roupa2.jpg" alt="Roupa 2">
          <img src="roupa3.jpg" alt="Roupa 3">
        </div>
        <button class="prev"">&#10094;</button>
        <button class="next">&#10095;</button>
      </div>
  `;
  
  tabContents.appendChild(homeContent);

  // --------------- MENU AGRUPADO ----------------
  Object.entries(grupos).forEach(([grupo, itens]) => {

    // Botão principal
    const grupoBtn = document.createElement("button");
    grupoBtn.classList.add("grupo-btn");
    grupoBtn.textContent = grupo;

    // Ativar grupo ao clicar
    grupoBtn.addEventListener("click", () => {
      marcarAtivo(grupoBtn);
      subList.style.display = subList.style.display === "none" ? "block" : "none";
    });

    const subList = document.createElement("ul");
    subList.classList.add("submenu");
    subList.style.display = "none";

    tabButtons.appendChild(grupoBtn);
    tabButtons.appendChild(subList);

    // Criar sub-itens
    itens.forEach(q => {

      const li = document.createElement("li");
      li.textContent = q.title;

      li.addEventListener("click", () => {
        marcarAtivo(li);
        openTab(q.id);
      });

      subList.appendChild(li);

      // Conteúdo
      const tab = document.createElement("div");
      tab.innerHTML = `
            <div class="card">
              <h2>${q.title}</h2>
              <form id="form-${q.id}" data-rota="${q.rota}">
                ${q.fields.map(f => `
                  <label>${f.label || f.name}
                    <input name="${f.name}" type="${f.type}" placeholder="${f.placeholder}">
                  </label>
                `).join('')}
                <button type="submit">Executar</button>
              </form>
              <div class="output" id="output-${q.id}"></div>
            </div>
      `;

      tab.querySelector("form").addEventListener("submit", e => handleSubmit(e, q.id));
      tabContents.appendChild(tab);
    });
    
  

  });
// ----- CARROSSEL -----
  const slidesContainer = document.querySelector(".carousel .slides");
  const slides = document.querySelectorAll(".carousel img");
  const prevBtn = document.querySelector(".carousel .prev");
  const nextBtn = document.querySelector(".carousel .next");

  if (!slidesContainer || !prevBtn || !nextBtn) {
    console.warn("Carrossel não encontrado no DOM.");
    return;
  }

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
  }, 5000);

  // --------------- FUNÇÕES -----------------

  function openHome() {
    document.querySelectorAll(".main-content > div")
      .forEach(d => d.classList.remove("active"));
    homeContent.classList.add("active");
  }

  function openTab(id) {
    document.querySelectorAll(".main-content > div")
      .forEach(t => t.classList.remove("active"));
    document.getElementById(`form-${id}`).parentElement.parentElement.classList.add("active");
  }

  async function handleSubmit(event, id) {
    event.preventDefault();
    const form = event.target;
    const rota = form.getAttribute("data-rota");
    const baseUrl = "http://localhost:8000";

    const params = new URLSearchParams();
    for (let el of form.elements) {
      if (el.name && el.value !== "") params.append(el.name, el.value);
    }

    const url = `${baseUrl}${rota}${params.toString() ? "?" + params.toString() : ""}`;
    const output = document.getElementById(`output-${id}`);
    output.textContent = "Carregando...";

    try {
      const res = await fetch(url);
      const data = await res.json();
      renderOutput(data, output);
    } catch (err) {
      output.textContent = "Erro: " + err.message;
    }
  }


  function renderOutput(data, output) {
    if (Array.isArray(data) && data.length) {
      const table = document.createElement("table");

      const thead = table.createTHead();
      const trHead = thead.insertRow();
      Object.keys(data[0]).forEach(key => {
        const th = document.createElement("th");
        th.textContent = key;
        trHead.appendChild(th);
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
