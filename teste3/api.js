// =========================
// AUTH
// =========================

// POST - login
function login(username, password) {
  const credenciais = { username, password };

  fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credenciais),
  })
    .then(response => {
      if (!response.ok) throw new Error('Erro no login');
      return response.json();
    })
    .then(data => {
      console.log('Login realizado:', data);
    })
    .catch(error => console.error(error));
}

// =========================
// BANCO
// =========================

// GET - rota protegida
function rotaProtegida() {
  fetch('http://localhost:8000/banco/protected')
    .then(response => {
      if (!response.ok) throw new Error('Erro na rota protegida');
      return response.json();
    })
    .then(data => console.log('Protected route:', data))
    .catch(error => console.error(error));
}

// POST - criar cliente
function criarCliente(nome, cpf, endereco, data_nascimento) {
  const cliente = { nome, cpf, endereco, data_nascimento };

  fetch('http://localhost:8000/banco/clientes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cliente),
  })
    .then(response => {
      if (!response.ok) throw new Error('Erro ao criar cliente');
      return response.json();
    })
    .then(data => console.log('Cliente criado:', data))
    .catch(error => console.error(error));
}

// POST - criar conta
function criarConta(numero, cpf) {
  const conta = { numero, cpf };

  fetch('http://localhost:8000/banco/contas/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(conta),
  })
    .then(response => {
      if (!response.ok) throw new Error('Erro ao criar conta');
      return response.json();
    })
    .then(data => console.log('Conta criada:', data))
    .catch(error => console.error(error));
}

// POST - criar transação
function criarTransacao(conta_origem, conta_destino, valor) {
  const transacao = { conta_origem, conta_destino, valor };

  fetch('http://localhost:8000/banco/transacoes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(transacao),
  })
    .then(response => {
      if (!response.ok) throw new Error('Erro ao criar transação');
      return response.json();
    })
    .then(data => console.log('Transação criada:', data))
    .catch(error => console.error(error));
}

// GET - consultar conta
function consultarConta(conta) {
  fetch(`http://localhost:8000/banco/contas/${conta}`)
    .then(response => {
      if (!response.ok) throw new Error('Erro ao consultar conta');
      return response.json();
    })
    .then(data => console.log('Conta consultada:', data))
    .catch(error => console.error(error));
}

// =========================
// GET endpoints extras
// =========================

// GET - listar clientes
function listarClientes() {
  fetch('http://localhost:8000/get/clientes')
    .then(response => {
      if (!response.ok) throw new Error('Erro ao listar clientes');
      return response.json();
    })
    .then(data => console.log('Lista de clientes:', data))
    .catch(error => console.error(error));
}

// GET - listar contas
function listarContas() {
  fetch('http://localhost:8000/get/contas')
    .then(response => {
      if (!response.ok) throw new Error('Erro ao listar contas');
      return response.json();
    })
    .then(data => console.log('Lista de contas:', data))
    .catch(error => console.error(error));
}

// =========================
// CRUD extra para clientes
// =========================

// PUT - atualizar cliente
function atualizarCliente(id, cliente) {
  fetch(`http://localhost:8000/clientes/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cliente),
  })
    .then(response => {
      if (!response.ok) throw new Error('Erro ao atualizar cliente');
      return response.json();
    })
    .then(data => console.log('Cliente atualizado:', data))
    .catch(error => console.error(error));
}

// DELETE - deletar cliente
function deletarCliente(id) {
  fetch(`http://localhost:8000/clientes/${id}`, {
    method: 'DELETE',
  })
    .then(response => {
      if (!response.ok) throw new Error('Erro ao deletar cliente');
      console.log('Cliente deletado com sucesso');
    })
    .catch(error => console.error(error));
}
