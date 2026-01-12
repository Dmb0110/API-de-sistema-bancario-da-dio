from fastapi import FastAPI
from app.database.session import Base, engine
from app.rotas_principais import api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="API de sistema bancário",
    description="Gerenciador de sistema bancário",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://127.0.0.1:5500"] se usar Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Inicializa o banco de forma assíncrona
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Cria as tabelas se não existirem
        await conn.run_sync(Base.metadata.create_all)

# Inclui as rotas definidas em routers_bancario
app.include_router(api_router)



# Monta a pasta "teste3" como estática
app.mount("/teste3", StaticFiles(directory="teste3"), name="teste3")




'''


<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Clientes e Contas</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #4facfe, #00f2fe);
      margin: 0;
      padding: 0;
    }

    header {
      background: #004080;
      color: white;
      padding: 15px;
      display: flex;
      align-items: center;
      justify-content: flex-start; /* botão à esquerda */
      position: fixed; /* fixa o header no topo */
      top: 0;
      left: 0;
      width: 100%;
      z-index: 1000;
    }

    header a {
      text-decoration: none;
      color: white;
      font-weight: bold;
      background: #0066cc;
      padding: 8px 12px;
      border-radius: 5px;
      transition: background 0.3s;
    }

    header a:hover {
      background: #0099ff;
    }

    h1 {
      margin: 0 auto;
      text-align: center;
      flex-grow: 1;
    }

    .container {
      margin: 100px auto 30px auto; /* espaço para não ficar atrás do header fixo */
      width: 600px;
      background: white;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
      color: #555;
    }

    input {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      background: #4facfe;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #00c6fb;
    }

    #listaClientes, #resultado {
      margin-top: 20px;
      padding: 10px;
      background: #f0f0f0;
      border-radius: 5px;
      font-size: 14px;
      color: #333;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <header>
    <a href="index.html">← Voltar</a>
    <h1>Clientes e Contas</h1>
  </header>

  <div class="container">
    <h2>📋 IDs de Clientes</h2>
    <div id="listaClientes">Carregando clientes...</div>

    <h2>🔍 Buscar Cliente por ID</h2>
    <form id="formBusca">
      <label for="clienteId">ID do Cliente</label>
      <input type="number" id="clienteId" required>
      <button type="submit">Buscar</button>
    </form>

    <div id="resultado"></div>
  </div>

  <script>
    const CLIENTES_URL = "http://localhost:8000/get/clientes";
    const CONTAS_URL = "http://localhost:8000/get/cliente/{cliente_id}";

    // Listar todos os clientes (apenas IDs)
    async function listarClientes() {
      try {
        const resp = await fetch(CLIENTES_URL);
        if (!resp.ok) throw new Error("Erro ao carregar clientes");

        const clientes = await resp.json();
        const listaDiv = document.getElementById("listaClientes");

        if (clientes.length === 0) {
          listaDiv.textContent = "Nenhum cliente encontrado.";
          return;
        }

        listaDiv.innerHTML = clientes.map(c => `<p><strong>ID:</strong> ${c.id}</p>`).join("");
      } catch (error) {
        document.getElementById("listaClientes").textContent = "Erro: " + error.message;
      }
    }

    // Buscar cliente por ID e mostrar suas contas
    async function buscarCliente(id) {
      try {
        const respCliente = await fetch(`${CLIENTES_URL}/${id}`);
        if (!respCliente.ok) throw new Error("Cliente não encontrado");

        const cliente = await respCliente.json();

        const respContas = await fetch(`${CONTAS_URL}/${id}`);
        let contas = [];
        if (respContas.ok) {
          contas = await respContas.json();
        }

        const resultadoDiv = document.getElementById("resultado");
        resultadoDiv.innerHTML = `
          <h3>Dados do Cliente</h3>
          <p><strong>ID:</strong> ${cliente.id}</p>
          <p><strong>Nome:</strong> ${cliente.nome}</p>
          <p><strong>CPF:</strong> ${cliente.cpf}</p>
          <p><strong>Endereço:</strong> ${cliente.endereco}</p>
          <p><strong>Nascimento:</strong> ${cliente.data_nascimento}</p>

          <h3>Contas</h3>
          ${contas.length > 0 
            ? contas.map(ct => `<p><strong>Número:</strong> ${ct.numero} | <strong>Saldo:</strong> ${ct.saldo}</p>`).join("")
            : "<p>Esse cliente não possui contas.</p>"}
        `;
      } catch (error) {
        document.getElementById("resultado").textContent = "Erro: " + error.message;
      }
    }

    document.getElementById("formBusca").addEventListener("submit", async (event) => {
      event.preventDefault();
      const id = document.getElementById("clienteId").value;
      buscarCliente(id);
    });

    listarClientes();
  </script>
</body>
</html>








<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Clientes e Contas</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #4facfe, #00f2fe);
      margin: 0;
      padding: 0;
    }

    header {
      background: #004080;
      color: white;
      padding: 15px;
      display: flex;
      align-items: center;
      justify-content: flex-start; /* garante que o botão fique à esquerda */
      position: fixed; /* fixa o header no topo */
      top: 0;
      left: 0;
      width: 100%;
      z-index: 1000;
    }

    header a {
      text-decoration: none;
      color: white;
      font-weight: bold;
      background: #0066cc;
      padding: 8px 12px;
      border-radius: 5px;
      transition: background 0.3s;
    }

    header a:hover {
      background: #0099ff;
    }

    h1 {
      margin: 0 auto; /* centraliza o título */
      text-align: center;
      flex-grow: 1;
    }

    .container {
      margin: 100px auto 30px auto; /* espaço para não ficar atrás do header fixo */
      width: 600px;
      background: white;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
      color: #555;
    }

    input {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      background: #4facfe;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #00c6fb;
    }

    #listaClientes, #resultado {
      margin-top: 20px;
      padding: 10px;
      background: #f0f0f0;
      border-radius: 5px;
      font-size: 14px;
      color: #333;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <header>
    <a href="index.html">← Voltar</a>
    <h1>Clientes e Contas</h1>
  </header>

  <div class="container">
    <h2>📋 IDs de Clientes</h2>
    <div id="listaClientes">Carregando clientes...</div>

    <h2>🔍 Buscar Cliente por ID</h2>
    <form id="formBusca">
      <label for="clienteId">ID do Cliente</label>
      <input type="number" id="clienteId" required>
      <button type="submit">Buscar</button>
    </form>

    <div id="resultado"></div>
  </div>

  <script>
    const CLIENTES_URL = "http://localhost:8000/banco/clientes";
    const CONTAS_URL = "http://localhost:8000/banco/contas/{conta}";

    async function listarClientes() {
      const token = localStorage.getItem("token");
      if (!token) {
        window.location.href = "login.html";
        return;
      }

      try {
        const resp = await fetch(CLIENTES_URL, {
          method: "GET",
          headers: { "Authorization": "Bearer " + token }
        });

        if (!resp.ok) throw new Error("Erro ao carregar clientes");

        const clientes = await resp.json();
        const listaDiv = document.getElementById("listaClientes");

        if (clientes.length === 0) {
          listaDiv.textContent = "Nenhum cliente encontrado.";
          return;
        }

        listaDiv.innerHTML = clientes.map(c => `<p><strong>ID:</strong> ${c.id}</p>`).join("");
      } catch (error) {
        document.getElementById("listaClientes").textContent = "Erro: " + error.message;
      }
    }

    async function buscarCliente(id) {
      const token = localStorage.getItem("token");
      if (!token) {
        window.location.href = "login.html";
        return;
      }

      try {
        const respCliente = await fetch(`${CLIENTES_URL}/${id}`, {
          method: "GET",
          headers: { "Authorization": "Bearer " + token }
        });

        if (!respCliente.ok) throw new Error("Cliente não encontrado");

        const cliente = await respCliente.json();

        const respContas = await fetch(`${CONTAS_URL}/${id}`, {
          method: "GET",
          headers: { "Authorization": "Bearer " + token }
        });

        let contas = [];
        if (respContas.ok) {
          contas = await respContas.json();
        }

        const resultadoDiv = document.getElementById("resultado");
        resultadoDiv.innerHTML = `
          <h3>Dados do Cliente</h3>
          <p><strong>ID:</strong> ${cliente.id}</p>
          <p><strong>Nome:</strong> ${cliente.nome}</p>
          <p><strong>CPF:</strong> ${cliente.cpf}</p>
          <p><strong>Endereço:</strong> ${cliente.endereco}</p>
          <p><strong>Nascimento:</strong> ${cliente.data_nascimento}</p>

          <h3>Contas</h3>
          ${contas.length > 0 
            ? contas.map(ct => `<p><strong>Número:</strong> ${ct.numero} | <strong>Saldo:</strong> ${ct.saldo}</p>`).join("")
            : "<p>Esse cliente não possui contas.</p>"}
        `;
      } catch (error) {
        document.getElementById("resultado").textContent = "Erro: " + error.message;
      }
    }

    document.getElementById("formBusca").addEventListener("submit", async (event) => {
      event.preventDefault();
      const id = document.getElementById("clienteId").value;
      buscarCliente(id);
    });

    listarClientes();
  </script>
</body>
</html>








<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Criar Transação</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #4facfe, #00f2fe);
      margin: 0;
      padding: 0;
    }

    header {
      background: #004080;
      color: white;
      padding: 15px;
      display: flex;
      align-items: center;
    }

    header a {
      text-decoration: none;
      color: white;
      font-weight: bold;
      margin-right: 20px;
      background: #0066cc;
      padding: 8px 12px;
      border-radius: 5px;
      transition: background 0.3s;
    }

    header a:hover {
      background: #0099ff;
    }

    h1 {
      margin: 0;
      flex-grow: 1;
      text-align: center;
    }

    .container {
      margin: 30px auto;
      width: 400px;
      background: white;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
      color: #555;
    }

    input, select {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      background: #4facfe;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #00c6fb;
    }

    #resposta {
      margin-top: 20px;
      padding: 10px;
      background: #f0f0f0;
      border-radius: 5px;
      font-size: 14px;
      color: #333;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <header>
    <a href="index.html">← Voltar</a>
    <h1>Criar Transação</h1>
  </header>

  <div class="container">
    <form id="formTransacao">
      <label for="numero">Número da Conta</label>
      <input type="text" id="numero" required>

      <label for="tipo">Tipo de Transação</label>
      <select id="tipo" required>
        <option value="">Selecione...</option>
        <option value="deposito">Depósito</option>
        <option value="saque">Saque</option>
        <option value="transferencia">Transferência</option>
      </select>

      <label for="valor">Valor</label>
      <input type="number" id="valor" step="0.01" required>

      <button type="submit">Enviar Transação</button>
    </form>

    <div id="resposta"></div>
  </div>

  <script>
    const API_URL = "http://localhost:8000/banco/transacoes";

    async function criarTransacao(numero, tipo, valor) {
      const token = localStorage.getItem("token"); // recupera token salvo no login
      if (!token) {
        // se não houver token, redireciona para login
        window.location.href = "login.html";
        return;
      }

      const transacao = { 
        numero_conta: parseInt(numero),
        tipo_de_transacao: tipo, 
        valor: parseFloat(valor) 
      };

      const resp = await fetch(API_URL, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token   // envia token no header
        },
        body: JSON.stringify(transacao),
      });

      if (!resp.ok) {
        throw new Error("Erro ao criar transação");
      }

      return resp.json();
    }

    document.getElementById("formTransacao").addEventListener("submit", async (event) => {
      event.preventDefault();

      const numero = document.getElementById("numero").value;
      const tipo = document.getElementById("tipo").value;
      const valor = document.getElementById("valor").value;

      try {
        const data = await criarTransacao(numero, tipo, valor);
        document.getElementById("resposta").textContent = "Transação criada: " + JSON.stringify(data);
      } catch (error) {
        document.getElementById("resposta").textContent = "Erro: " + error.message;
      }
    });
  </script>
</body>
</html>







<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Criar Transação</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #4facfe, #00f2fe);
      margin: 0;
      padding: 0;
    }

    header {
      background: #004080;
      color: white;
      padding: 15px;
      display: flex;
      align-items: center;
    }

    header a {
      text-decoration: none;
      color: white;
      font-weight: bold;
      margin-right: 20px;
      background: #0066cc;
      padding: 8px 12px;
      border-radius: 5px;
      transition: background 0.3s;
    }

    header a:hover {
      background: #0099ff;
    }

    h1 {
      margin: 0;
      flex-grow: 1;
      text-align: center;
    }

    .container {
      margin: 30px auto;
      width: 400px;
      background: white;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
      color: #555;
    }

    input, select {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      background: #4facfe;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #00c6fb;
    }

    #resposta {
      margin-top: 20px;
      padding: 10px;
      background: #f0f0f0;
      border-radius: 5px;
      font-size: 14px;
      color: #333;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <header>
    <a href="index.html">← Voltar</a>
    <h1>Criar Transação</h1>
  </header>

  <div class="container">
    <form id="formTransacao">
      <label for="numero">Número da Conta</label>
      <input type="text" id="numero" required>

      <label for="tipo">Tipo de Transação</label>
      <select id="tipo" required>
        <option value="">Selecione...</option>
        <option value="deposito">Depósito</option>
        <option value="saque">Saque</option>
        <option value="transferencia">Transferência</option>
      </select>

      <label for="valor">Valor</label>
      <input type="number" id="valor" step="0.01" required>

      <button type="submit">Enviar Transação</button>
    </form>

    <div id="resposta"></div>
  </div>

  <script>
    const API_URL = "http://localhost:8000/banco/transacoes";

    async function criarTransacao(numero, tipo, valor) {
      const transacao = { 
        numero_conta: parseInt(numero),
        tipo_de_transacao: tipo, 
        valor: parseFloat(valor) 
      };

      const resp = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(transacao),
      });

      if (!resp.ok) {
        throw new Error("Erro ao criar transação");
      }

      return resp.json();
    }

    document.getElementById("formTransacao").addEventListener("submit", async (event) => {
      event.preventDefault();

      const numero = document.getElementById("numero").value;
      const tipo = document.getElementById("tipo").value;
      const valor = document.getElementById("valor").value;

      try {
        const data = await criarTransacao(numero, tipo, valor);
        document.getElementById("resposta").textContent = "Transação criada: " + JSON.stringify(data);
      } catch (error) {
        document.getElementById("resposta").textContent = "Erro: " + error.message;
      }
    });
  </script>
</body>
</html>











<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #4facfe, #00f2fe);
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    .container {
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
      width: 350px;
    }

    h1 {
      text-align: center;
      color: #333;
    }

    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
      color: #555;
    }

    input {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      background: #4facfe;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #00c6fb;
    }

    #resposta {
      margin-top: 20px;
      padding: 10px;
      background: #f0f0f0;
      border-radius: 5px;
      font-size: 14px;
      color: #333;
      word-wrap: break-word;
    }

    .voltar {
      margin-top: 15px;
      text-align: center;
    }

    .voltar a {
      text-decoration: none;
      color: #004080;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Login</h1>
    <form id="formLogin">
      <label for="username">Usuário</label>
      <input type="text" id="username" required>

      <label for="password">Senha</label>
      <input type="password" id="password" required>

      <button type="submit">Entrar</button>
    </form>

    <div id="resposta"></div>

    <div class="voltar">
      <a href="index.html">← Voltar para Página Principal</a>
    </div>
  </div>

  <script>
    const API_URL = "http://localhost:8000/auth/login"; // ajuste conforme sua rota

    async function login(username, password) {
      const dados = { username, password };

      const resp = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
      });

      if (!resp.ok) {
        throw new Error("Erro ao fazer login");
      }

      return resp.json();
    }

    document.getElementById("formLogin").addEventListener("submit", async (event) => {
      event.preventDefault();

      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      try {
        const data = await login(username, password);
        document.getElementById("resposta").textContent = "Login realizado: " + JSON.stringify(data);
        // Exemplo: guardar token no localStorage
        if (data.access_token) {
          localStorage.setItem("token", data.access_token);
        }
      } catch (error) {
        document.getElementById("resposta").textContent = "Erro: " + error.message;
      }
    });
  </script>
</body>
</html>







<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Cadastro e Transações</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #4facfe, #00f2fe);
      margin: 0;
      padding: 0;
    }

    header {
      background: #004080;
      color: white;
      padding: 15px;
      display: flex;
      align-items: center;
    }

    header a {
      text-decoration: none;
      color: white;
      font-weight: bold;
      margin-right: 20px;
      background: #0066cc;
      padding: 8px 12px;
      border-radius: 5px;
      transition: background 0.3s;
    }

    header a:hover {
      background: #0099ff;
    }

    h1 {
      margin: 0;
      flex-grow: 1;
      text-align: center;
    }

    .container {
      margin: 30px auto;
      width: 400px;
      background: white;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
      color: #555;
    }

    input {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      background: #4facfe;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #00c6fb;
    }

    #resposta {
      margin-top: 20px;
      padding: 10px;
      background: #f0f0f0;
      border-radius: 5px;
      font-size: 14px;
      color: #333;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <header>
    <a href="index.html">← Voltar</a>
    <h1>Cadastro e Transações</h1>
  </header>

  <div class="container">
    <form id="formCadastro">
      <label for="username">Usuário</label>
      <input type="text" id="username" required>

      <label for="password">Senha</label>
      <input type="password" id="password" required>

      <button type="submit">Cadastrar / Logar</button>
    </form>

    <form id="formTransacao" style="display:none;">
      <label for="valor">Valor da Transação</label>
      <input type="number" id="valor" required>

      <label for="descricao">Descrição</label>
      <input type="text" id="descricao" required>

      <button type="submit">Enviar Transação</button>
    </form>

    <div id="resposta"></div>
  </div>

  <script>
    const API_AUTH = "http://localhost:8000/auth/register"; // ou /auth/login
    const API_TRANSACAO = "http://localhost:8000/banco/transacoes";
    let token = null;

    // Cadastro/Login
    document.getElementById("formCadastro").addEventListener("submit", async (event) => {
      event.preventDefault();
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      try {
        const resp = await fetch(API_AUTH, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        if (!resp.ok) throw new Error("Erro ao cadastrar/logar");

        const data = await resp.json();
        token = data.access_token; // assume que backend retorna { "access_token": "..." }

        document.getElementById("resposta").textContent = "Token recebido: " + token;
        document.getElementById("formTransacao").style.display = "block";
      } catch (error) {
        document.getElementById("resposta").textContent = "Erro: " + error.message;
      }
    });

    // Transação
    document.getElementById("formTransacao").addEventListener("submit", async (event) => {
      event.preventDefault();
      const valor = document.getElementById("valor").value;
      const descricao = document.getElementById("descricao").value;

      try {
        const resp = await fetch(API_TRANSACAO, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
          },
          body: JSON.stringify({ valor, descricao }),
        });

        if (!resp.ok) throw new Error("Erro ao enviar transação");

        const data = await resp.json();
        document.getElementById("resposta").textContent = "Transação criada: " + JSON.stringify(data);
      } catch (error) {
        document.getElementById("resposta").textContent = "Erro: " + error.message;
      }
    });
  </script>
</body>
</html>








    .acoes {
      margin-top: 30px;
      display: flex;
      justify-content: center;
      gap: 20px;
      flex-wrap: wrap;
    }

    .btn {
      display: inline-block;
      padding: 15px 25px;
      font-size: 16px;
      border-radius: 8px;
      cursor: pointer;
      background: #004080;
      color: white;
      text-decoration: none;
      transition: background 0.3s;
    }

    .btn:hover {
      background: #0066cc;
    }

    






    <!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Criar Conta</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #4facfe, #00f2fe);
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    .container {
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
      width: 350px;
    }

    h1 {
      text-align: center;
      color: #333;
    }

    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
      color: #555;
    }

    input {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
      transition: border-color 0.3s;
    }

    input:focus {
      border-color: #4facfe;
      outline: none;
    }

    button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      background: #4facfe;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #00c6fb;
    }

    #resposta {
      margin-top: 20px;
      padding: 10px;
      background: #f0f0f0;
      border-radius: 5px;
      font-size: 14px;
      color: #333;
      word-wrap: break-word;
    }

    .voltar {
      margin-top: 15px;
      text-align: center;
    }

    .voltar a {
      text-decoration: none;
      color: #004080;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Criar Conta</h1>
    <form id="form">
      <label for="numero">Número da Conta</label>
      <input type="text" id="numero" required>

      <label for="cliente_id">ID do Cliente</label>
      <input type="text" id="cliente_id" required>

      <label for="saldo">Saldo Inicial</label>
      <input type="number" id="saldo" required>

      <button type="submit">Criar Conta</button>
    </form>

    <div id="resposta"></div>

    <div class="voltar">
      <a href="../index.html">← Voltar para Página Principal</a>
    </div>
  </div>

  <script>
    async function criarConta(numero, cliente_id, saldo_inicial) {
      const conta = { numero, cliente_id, saldo_inicial };

      const resp = await fetch('http://localhost:8000/banco/contas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(conta),
      });

      if (!resp.ok) {
        throw new Error("Erro ao criar conta");
      }

      return resp.json();
    }

    document.getElementById("form").addEventListener("submit", async (event) => {
      event.preventDefault();

      const numero = document.getElementById("numero").value;
      const cliente_id = document.getElementById("cliente_id").value;
      const saldo = document.getElementById("saldo").value;

      try {
        const data = await criarConta(numero, cliente_id, saldo);
        document.getElementById("resposta").textContent = "Conta criada com sucesso: " + JSON.stringify(data);
      } catch (error) {
        document.getElementById("resposta").textContent = "Erro: " + error.message;
      }
    });
  </script>
</body>
</html>

'''