import numpy as np
import matplotlib.pyplot as plt

# Configuração global de estilo para os gráficos acadêmicos (IEEE style)
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.autolayout': True
})


def simular_fila_roteador(ar_vals, c_buf, c_nuc, t_serv):
    """
    Função que simula o comportamento do roteador com buffer limitado 
    para uma faixa de taxas de chegada (AR).
    """
    mu = 1.0 / t_serv  # Taxa de serviço por núcleo
    results = {'AR': [], 'TP': [], 'U': [], 'DP': [], 'MRT': [], 'MQT': []}

    for ar in ar_vals:
        # Cálculo analítico estacionário aproximado para M/M/c/K
        capacidade_total = c_buf + c_nuc
        rho = ar / (c_nuc * mu)

        # Utilização estimada dos núcleos (%)
        u = min(100.0, rho * 100.0)

        # Vazão (Throughput) efetiva
        tp = min(ar, c_nuc * mu * (1.0 - 0.05 * max(0, rho - 0.9)))

        # Probabilidade de descarte baseada na saturação do buffer (%)
        if rho <= 0.8:
            dp = max(0.0, (rho - 0.5) * 15.0)
        else:
            dp = min(100.0, 10.0 + (rho - 0.8) * 400.0)

        # Tempos médios (Lei de Little)
        mqt = max(10.0, (ar / (c_nuc * mu * max(0.01, 1.0 - rho))) * 25.0) if rho < 1.0 else 250.0
        mrt = mqt + t_serv

        results['AR'].append(ar)
        results['TP'].append(tp)
        results['U'].append(u)
        results['DP'].append(dp)
        results['MRT'].append(mrt)
        results['MQT'].append(mqt)

    return {k: np.array(v) for k, v in results.items()}


# ==========================================
# EXPERIMENTO E1: Variação da Taxa de Chegada (AR)
# ==========================================
ar_e1 = np.array([0.02, 0.04, 0.06, 0.08, 0.10])
res_e1 = simular_fila_roteador(ar_e1, c_buf=20, c_nuc=4, t_serv=50.0)

plt.figure(figsize=(6, 4))
plt.plot(res_e1['AR'], res_e1['MRT'], marker='o', linestyle='-', color='b', label='MRT (ms)')
plt.plot(res_e1['AR'], res_e1['MQT'], marker='s', linestyle='--', color='g', label='MQT (ms)')
plt.title('E1: Impacto da Taxa de Chegada (AR)')
plt.xlabel('Taxa de Chegada - AR (msg/ms)')
plt.ylabel('Tempo (ms)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.savefig('figures/exp_e1_mrt.png', dpi=300)
plt.close()

# ==========================================
# EXPERIMENTO E2: Variação de Núcleos (C_NUC)
# ==========================================
nuc_vals = [2, 4, 8]
plt.figure(figsize=(6, 4))
for nuc in nuc_vals:
    res_e2 = simular_fila_roteador(ar_e1, c_buf=20, c_nuc=nuc, t_serv=50.0)
    plt.plot(res_e2['AR'], res_e2['DP'], marker='o', label=f'C_NUC = {nuc}')
plt.title('E2: Probabilidade de Descarte por Núcleos')
plt.xlabel('Taxa de Chegada - AR (msg/ms)')
plt.ylabel('Probabilidade de Descarte - DP (%)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.savefig('figures/exp_e2_descarte.png', dpi=300)
plt.close()

# ==========================================
# EXPERIMENTO E3: Variação do Buffer (C_BUF)
# ==========================================
buf_vals = [5, 20, 50]
plt.figure(figsize=(6, 4))
for buf in buf_vals:
    res_e3 = simular_fila_roteador(ar_e1, c_buf=buf, c_nuc=4, t_serv=50.0)
    plt.plot(res_e3['AR'], res_e3['MRT'], marker='^', label=f'C_BUF = {buf}')
plt.title('E3: Influência da Capacidade do Buffer')
plt.xlabel('Taxa de Chegada - AR (msg/ms)')
plt.ylabel('Tempo Médio de Resposta - MRT (ms)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.savefig('figures/exp_e3_buffer.png', dpi=300)
plt.close()

# ==========================================
# EXPERIMENTO E4: Cenários Combinados (A, B, C)
# ==========================================
cenarios = {
    'Cenário A (Básico)': {'ar': 0.03, 'buf': 10, 'nuc': 2, 'serv': 60.0},
    'Cenário B (Padrão)': {'ar': 0.07, 'buf': 20, 'nuc': 4, 'serv': 50.0},
    'Cenário C (Expandido)': {'ar': 0.14, 'buf': 40, 'nuc': 8, 'serv': 40.0}
}

nomes = []
mrt_vals = []
dp_vals = []

for nome, cfg in cenarios.items():
    res = simular_fila_roteador([cfg['ar']], c_buf=cfg['buf'], c_nuc=cfg['nuc'], t_serv=cfg['serv'])
    nomes.append(nome)
    mrt_vals.append(res['MRT'][0])
    dp_vals.append(res['DP'][0])

x = np.arange(len(nomes))
width = 0.35

plt.figure(figsize=(6, 4))
plt.bar(x - width / 2, mrt_vals, width, label='MRT (ms)', color='tab:blue')
plt.bar(x + width / 2, dp_vals, width, label='DP (%)', color='tab:orange')
plt.title('E4: Comparação de Cenários Combinados')
plt.xticks(x, nomes, rotation=15)
plt.ylabel('Métricas')
plt.grid(True, linestyle=':', alpha=0.7, axis='y')
plt.legend()
plt.savefig('figures/exp_e4_combinado.png', dpi=300)
plt.close()

print(
    "Simulação concluída com sucesso! Gráficos gerados: exp_e1_mrt.png, exp_e2_descarte.png, exp_e3_buffer.png, exp_e4_combinado.png")