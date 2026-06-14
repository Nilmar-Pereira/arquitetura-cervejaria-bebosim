# Architecture Decision Records — Cervejaria BeboSim

---

## ADR-01: Adoção do Estilo Arquitetural Model-View-Controller(MVC)

**Contexto:**
Necessidade de organizar um sistema web com múltiplos modulos CRUD e diferentes
perfis de usuario, separando claramente as responsabilidades de interface, controle e dados.

**Decisão:**
Adotar o estilo arquitetural MVC (Model-View-Controller), separando a aplicacão em camadas de apresentação (View), controle (Controller) e lógica de negócio e dados (Model).

**Status:** Aceita

**Consequências:**
- Separação clara de responsabilidades entre as camadas;
- Facilidade de manutenção e evolução do sistema;
- Complexidade inicial maior na organização do projeto.

---

## ADR-02: Uso de Banco de Dados MySQL

**Contexto:**
Necessidade de persistir dados de múltiplas entidades inter-relacionadas como funcionários, clientes, produtos, pedidos, equipes, embalagens e campanhas publicitárias.

**Decisão:**
Utilizar o MySQL como sistema gerenciador de banco de dados relacional para armazenamento e recuperação de todos os dados do sistema.

**Status:** Aceita

**Consequências:**
- solução gratuita e open-source;
- Boa perfomance para o volume de dados esperado;
- Requer administração especalizada em SQL.

---

## ADR-03: Gerenciamento de Pedidos com Validação de Dependências

**Contexto:**
Um pedido depende obrigatoriamente de produto, vendedor e cliente previamente cadastrados, exigindo validações para garantir integridade dos dados.

**Decisão:**
Implementar validação de dependências no Controller antes de persistir os dados, reforçadas por chaves estrangeiras no banco de dados MySQL.

**Status:** Aceita

**Consequências:**
- Consistência e integridade dos dados de venda garantidas;
- Viabiliza os relatórios gerenciais previstos nos requisitos funcionais;
- Em cenários de migração ou importação de dados, a exigência de integridade referencial pode dificultar a inserção de registros históricos.

---

## ADR-04: Geração de Relatórios Gerenciais por Período

**Contexto:**
O sistema deve consolidar dados de múltiplos módulos para gerar relatórios gerenciais filtráveis por período, exigindo consultas complexas ao banco de dados.


**Decisão:**
Implementar a geração de relatórios no Model com consultas SQL otimizadas, renderizando os resultados diretamente no browser via View.

**Status:** Aceita

**Consequências:**
- Centralização da lógica de relatórios facilita manutenção;
- Consultas complexas podem degradar desempenho em grandes volumes.

---

## ADR-05: Gerenciamento de Campanhas Publicitárias

**Contexto:**
O módulo de campanhas armazena dados financeiros sensíveis como valor previsto, valor de retorno e percentual de aumento de vendas, além de datas de início e término.

**Decisão:**
Implementar validações no Controller para datas e valores financeiros, vinculando cada campanha a um produto existente no sistema.

**Status:** Aceita

**Consequências:**
- Validações evitam cadastros inconsistentes;
- Vínculo com produtos permite análises cruzadas com vendas;
- Obrigatoriedade do vínculo limita campanhas institucionais.

---

## ADR-06: Interface Web com Componentes Padrão e Perfis de Acesso

**Contexto:**
O sistema  ́e acessado por diferentes perfis de usuário (Administrador, Gerente Geral, Ge-
rente de Unidade e Atendente), cada um com permissões distintas

**Decisão:**
Implementar a View com componentes HTML/CSS/JavaScript padr ̃ao, com o Controller
verificando o perfil autenticado e disponibilizando apenas as funcionalidades permitidas.

**Status:** Aceita

**Consequências:**
- Compatibilidade com diferentes navegadores garantida;
- Controle de acesso por perfil aumenta a segurança;
- Manutenção de múltiplas views aumenta o volume de código.

---

## ADR-07: Estratégia de Manutenibilidade e Desempenho

**Contexto:**
O sistema deve executar operações de forma  ́agil e suportar manutenções sem interrupção
do serviço, conforme exigido pelos requisitos NF004 e NF005.

**Decisão:**
Adotar  ́ındices nos campos de busca frequente no MySQL e estruturar o sistema de forma modular no MVC, permitindo atualizações por módulo sem afetar os demais.

**Status:** Aceita

**Consequências:**
- Redução do tempo de resposta nas operações de pesquisa;
- Manutenções pontuais sem interrupção do sistema;
- Índices aumentam espaço em disco e impactam operações de escrita.

---

## ADR-08: Gerenciamento de Embalagens Vinculadas a Produtos

**Contexto:**
Cada embalagem deve estar obrigatoriamente vinculada a um produto cadastrado, com dados de custo, volume e tipo relevantes para o controle de produção.

**Decisão:**
Implementar validação no Controller para garantir que o produto vinculado exista, utilizando chave estrangeira no banco para reforçar a integridade do vínculo.

**Status:** Aceita

**Consequências:**
- Integridade do vínculo produto-embalagem garantida;
- Validações previnem cadastros com dados inválidos;
- Ordem de cadastro obrigatória pode ser inconveniente operacionalmente.