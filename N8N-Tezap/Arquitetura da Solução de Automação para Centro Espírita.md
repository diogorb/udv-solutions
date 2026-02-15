# Arquitetura da Solução de Automação para Centro Espírita

## Visão Geral

A solução proposta consiste em um agente automatizado que integra o WhatsApp Business com o sistema UDVNMG para automatizar três processos principais: consulta de valores a pagar, processamento de comprovantes de pagamento e emissão de recibos. A arquitetura foi projetada para ser robusta, escalável e de fácil manutenção, utilizando N8N como plataforma principal de automação.

## Componentes da Arquitetura

### 1. Interface de Comunicação (WhatsApp Business API)

O ponto de entrada da solução é a integração com a WhatsApp Business Cloud API através do N8N. Esta interface permite que os usuários interajam com o sistema através de mensagens de texto e envio de documentos PDF.

**Funcionalidades:**
- Recebimento de mensagens de texto para consultas de valores
- Recebimento de documentos PDF (comprovantes de pagamento)
- Envio de respostas automáticas com informações de débitos
- Envio de imagens de recibos gerados

**Fluxo de Comunicação:**
1. Usuário envia mensagem via WhatsApp
2. N8N recebe a mensagem através do webhook da WhatsApp Business API
3. Sistema processa a solicitação
4. Resposta é enviada de volta via WhatsApp

### 2. Módulo de Processamento de PDF

Este módulo é responsável por extrair informações relevantes dos comprovantes de pagamento enviados pelos usuários.

**Tecnologias Utilizadas:**
- N8N Read PDF node para extração de texto
- Expressões regulares para identificação de padrões
- Validação de CNPJ do destinatário

**Dados Extraídos:**
- Valor da transferência/pagamento
- CNPJ do recebedor (validação se é o centro espírita: 07.124.906/0001-67)
- Nome do pagador
- Data da transação
- Tipo de comprovante (PIX, TED, DOC, etc.)

### 3. Módulo de Automação Web (Interação com UDVNMG)

Este é o componente mais complexo da solução, responsável por automatizar as interações com o sistema UDVNMG através de automação web.

**Funcionalidades:**
- Login automático no sistema UDVNMG
- Consulta de valores a pagar por associado
- Registro de pagamentos recebidos
- Geração e captura de recibos
- Envio de recibos por e-mail (através do sistema)

**Tecnologia:**
- N8N HTTP Request nodes para interações com formulários web
- N8N HTML Extract nodes para parsing de dados das páginas
- Puppeteer ou Playwright (via N8N) para automação de browser quando necessário

### 4. Módulo de Captura de Tela

Para atender ao requisito específico de tirar print do recibo e enviar via WhatsApp, este módulo será responsável por:

**Funcionalidades:**
- Captura de tela da página do recibo no sistema UDVNMG
- Processamento da imagem (recorte, otimização)
- Preparação para envio via WhatsApp

**Implementação:**
- Utilização de ferramentas de screenshot via N8N
- Processamento de imagem para garantir qualidade adequada
- Armazenamento temporário das imagens

## Fluxos de Trabalho Detalhados

### Fluxo 1: Consulta de Valores a Pagar

```
1. Usuário envia mensagem: "Consultar débitos [Nome/CPF]"
2. N8N recebe mensagem via WhatsApp webhook
3. Sistema extrai nome/CPF da mensagem
4. Automação web faz login no UDVNMG
5. Navega para seção de consulta
6. Busca pelo associado
7. Extrai informações de débitos
8. Formata resposta
9. Envia resposta via WhatsApp
```

### Fluxo 2: Processamento de Comprovante de Pagamento

```
1. Usuário envia PDF/imagem do comprovante via WhatsApp
2. N8N recebe arquivo via WhatsApp webhook
3. Sistema baixa e processa o arquivo
4. Extrai dados relevantes (valor, CNPJ, nome, data)
5. Valida se CNPJ corresponde ao centro espírita
6. Se válido:
   a. Faz login no UDVNMG
   b. Navega para seção de recebimento
   c. Registra o pagamento
   d. Gera recibo
   e. Captura tela do recibo
   f. Envia recibo via WhatsApp
7. Se inválido:
   a. Envia mensagem de erro explicativa
```

### Fluxo 3: Emissão de Recibo Manual

```
1. Usuário solicita emissão de recibo: "Emitir recibo [Nome] [Valor] [Tipo]"
2. N8N processa solicitação
3. Faz login no UDVNMG
4. Navega para seção de recebimento
5. Preenche dados do recibo
6. Confirma emissão
7. Clica no ícone de e-mail
8. Captura tela do recibo
9. Envia imagem via WhatsApp
```

## Considerações de Segurança

### Autenticação no Sistema UDVNMG

As credenciais de acesso ao sistema UDVNMG devem ser armazenadas de forma segura:
- Utilização de variáveis de ambiente no N8N
- Criptografia das credenciais sensíveis
- Rotação periódica de senhas

### Validação de Dados

- Validação rigorosa de CPF/CNPJ
- Verificação de formatos de arquivo aceitos
- Sanitização de inputs para prevenir ataques

### Controle de Acesso

- Lista de números de WhatsApp autorizados
- Implementação de rate limiting para prevenir spam
- Logs detalhados de todas as operações

## Tecnologias e Ferramentas

### Plataforma Principal
- **N8N**: Orquestração de workflows e automação

### Integrações
- **WhatsApp Business Cloud API**: Comunicação via WhatsApp
- **PDF.co ou similar**: Processamento avançado de PDF (se necessário)
- **Puppeteer/Playwright**: Automação de browser para casos complexos

### Infraestrutura
- **Servidor VPS**: Para hospedar N8N
- **Banco de dados**: Para logs e cache (SQLite ou PostgreSQL)
- **Armazenamento**: Para arquivos temporários

## Estimativa de Custos

### N8N Cloud (Recomendado para início)
- **Plano Starter**: $20/mês (2.5k execuções, 5 workflows ativos)
- **Plano Pro**: $50/mês (10k execuções, 15 workflows ativos)

### WhatsApp Business API
- **Meta (Facebook)**: Gratuito para até 1.000 conversas/mês
- **Custos adicionais**: $0.005-0.009 por conversa adicional

### Infraestrutura (Alternativa Self-hosted)
- **VPS**: $10-30/mês dependendo das especificações
- **Domínio**: $10-15/ano

### Total Estimado
- **Opção Cloud**: $20-50/mês + custos mínimos do WhatsApp
- **Opção Self-hosted**: $10-30/mês + custos mínimos do WhatsApp

## Vantagens da Solução Proposta

### Eficiência Operacional
- Redução significativa do tempo gasto em tarefas manuais
- Processamento automático de comprovantes 24/7
- Resposta imediata a consultas de débitos

### Precisão e Confiabilidade
- Eliminação de erros humanos na digitação
- Validação automática de dados
- Rastreabilidade completa de operações

### Experiência do Usuário
- Interface familiar (WhatsApp)
- Respostas rápidas e precisas
- Recibos enviados automaticamente

### Escalabilidade
- Capacidade de processar múltiplas solicitações simultaneamente
- Fácil adição de novos recursos
- Adaptável a mudanças no sistema UDVNMG

## Limitações e Considerações

### Dependências Externas
- Disponibilidade do sistema UDVNMG
- Estabilidade da API do WhatsApp Business
- Mudanças na interface do sistema UDVNMG podem requerer ajustes

### Manutenção
- Monitoramento contínuo necessário
- Atualizações periódicas dos workflows
- Backup regular das configurações

### Compliance
- Necessidade de adequação à LGPD
- Políticas de retenção de dados
- Consentimento dos usuários para processamento automatizado

## Próximos Passos para Implementação

### Fase 1: Configuração Inicial
1. Criação de conta N8N
2. Configuração da WhatsApp Business API
3. Desenvolvimento dos workflows básicos

### Fase 2: Desenvolvimento dos Módulos
1. Implementação do módulo de processamento de PDF
2. Desenvolvimento da automação web para UDVNMG
3. Integração dos componentes

### Fase 3: Testes e Refinamento
1. Testes com dados reais
2. Ajustes de performance
3. Implementação de logs e monitoramento

### Fase 4: Deploy e Treinamento
1. Deploy em ambiente de produção
2. Treinamento da equipe
3. Documentação de uso

Esta arquitetura fornece uma base sólida para a implementação da solução de automação, balanceando funcionalidade, segurança e facilidade de manutenção.

