# VigilIA – Agente de Segurança Digital com IA

## Descrição

VigilIA é um agente inteligente para análise automatizada de logs de firewall, capaz de detectar comportamentos suspeitos de IPs e gerar alertas em tempo real. Desenvolvido em Python com foco em modularidade e fácil expansão.

## Funcionalidades

- Leitura e parse de logs de firewall
- Identificação de IPs com múltiplos bloqueios
- Geração de alertas no console (com opção de integração Telegram)
- Pipeline simples e extensível para análise de segurança

## Tecnologias

- Python 3.x  
- pandas  
- requests (para integração Telegram)

## Estrutura do projeto

## Como usar

1. Clone o repositório  
2. Instale dependências:  
   `pip install -r requirements.txt`  
3. Configure variáveis de ambiente para alertas Telegram (opcional)  
4. Execute o pipeline:  
   `python src/main.py --input logs/firewall.log --limite 3`

## Contribuições

Pull requests são bem-vindos! Abra issues para sugestões e bugs.

## Contato

Robson Vieira - roviemealclube@gmail.com
LinkedIn: [Robson Vieira]https://www.linkedin.com/in/robson-vieira94
GitHub: [Robson Vieira](https://github.com/RobsonViieira)