# git init Utilizando Redes de Petri Estocásticas (SPN)

Este repositório contém os arquivos de configuração, modelos, scripts de simulação analítica, relatórios brutos e gráficos desenvolvidos para o **Trabalho 07 (Avaliação de Desempenho de Sistemas)**, referente ao **Contexto 7: Rede de Computadores Universitária (Roteador e Buffer Limitado)**.

**Autor:** Marcos Eduardo Barbosa Pachêco  
**Curso:** Bacharelado em Sistemas de Informação — Universidade Federal do Piauí (UFPI)  

---

## 📋 Sobre o Projeto

O crescimento contínuo do tráfego de dados em redes universitárias submete os roteadores de borda a regimes frequentes de congestionamento e contenção de recursos. Este projeto modela formalmente o subsistema de encaminhamento de pacotes de um roteador equipado com múltiplos núcleos de processamento ($C\_NUC$) e buffer de capacidade finita ($C\_BUF$) utilizando **Redes de Petri Estocásticas (SPN)**.

Por meio de simulações estocásticas em regime estacionário na ferramenta **Jupiter Analytics** e validação analítica via **Python**, avaliam-se cinco métricas fundamentais:
* **Utilização ($U$):** Percentual médio de ocupação dos núcleos de processamento.
* **Vazão / Throughput ($TP$):** Taxa efetiva de pacotes transmitidos por milissegundo.
* **Tempo Médio de Resposta ($MRT$):** Tempo total médio de permanência de um pacote no sistema (fila + processamento).
* **Tempo Médio na Fila ($MQT$):** Tempo médio de espera no buffer antes da alocação de um núcleo.
* **Probabilidade de Descarte ($DP$):** Percentual de pacotes rejeitados (*tail drop*) por esgotamento do buffer.

---

## 📂 Estrutura do Repositório

```text
trabalho07-spn-roteador/
│
├── README.md                  
├── simulador_spn.py          
├── figures/                  
│   ├── exp_e1_mrt.png         
│   ├── exp_e2_descarte.png   
│   ├── exp_e3_buffer.png      
│   └── exp_e4_combinado.png   
├── model/                     
│   └── modelo_spn.png         
└── outputs/                   
    └── analysis-report.txt    
```

---

## 🚀 Como Executar o Script de Simulação

Para reproduzir os gráficos analíticos (`E1` a `E4`) localmente em sua máquina, certifique-se de ter o **Python 3.8+** instalado e siga os passos abaixo:

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/trabalho07-spn-roteador.git
   cd trabalho07-spn-roteador
   ```

2. **Instale as dependências necessárias:**
   ```bash
   pip install numpy matplotlib
   ```

3. **Execute o script gerador de gráficos:**
   ```bash
   python simulador_spn.py
   ```
   Os arquivos `.png` serão salvos automaticamente no diretório atual.

---

## 📊 Resumo dos Experimentos Realizados

* **Experimento E1 (Variação de $AR$):** Demonstra o comportamento não linear da latência ($MRT$ e $MQT$) conforme a taxa de chegada aumenta de $0,02$ para $0,10\text{ pacotes/ms}$.
* **Experimento E2 (Variação de $C\_NUC$):** Evidencia que o subdimensionamento de núcleos ($C\_NUC = 2$) leva o roteador ao colapso precoce ($DP \ge 90\%$), enquanto $C\_NUC = 8$ suprime perdas e reduz a fila a valores próximos de zero.
* **Experimento E3 (Variação de $C\_BUF$):** Comprova o fenômeno de *bufferbloat*: aumentar o tamanho do buffer de $5$ para $50$ posições sob núcleos saturados não eleva a vazão, mas degrada severamente o tempo médio de resposta.
* **Experimento E4 (Cenários Combinados):** Compara três perfis de dimensionamento (*Básico*, *Padrão* e *Expandido*), demonstrando que o escalonamento conjunto de núcleos e buffer (*Cenário C*) mantém o $MRT < 100\text{ ms}$ e o descarte em $2,5\%$ mesmo sob alta demanda.

---

## 🔗 Links Complementares

* **Vídeo de Apresentação (5 min):** [Assista no YouTube](https://youtu.be/SEU_LINK_DO_VIDEO)
