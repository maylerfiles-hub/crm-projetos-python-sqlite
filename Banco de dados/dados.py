import matplotlib
matplotlib.use('WebAgg')  # Abre a animação interativa direto no seu navegador!

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# ... o restante do seu código continua igual
# Configuração da figura
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6))
fig.suptitle("Simulação do Fluxo do Modulador PSDM e Multiplicador Bypassing", fontsize=12, fontweight='bold')

# Dados para a senoide (Sinal Analógico)
x = np.linspace(0, 4 * np.pi, 200)
y = np.sin(x)

# Plot 1: Modulador Pseudo-Paralelo
ax1.set_xlim(0, 4 * np.pi)
ax1.set_ylim(-1.5, 1.5)
ax1.set_title("1. Amostragem Pseudo-Paralela (PSDM) - 2 Amostras por Ciclo")
line_analog, = ax1.plot(x, y, color='gray', alpha=0.5, label='Sinal Analógico V/I')
pt_sample1, = ax1.plot([], [], 'ro', markersize=8, label='Amostra 1 (Paralela)')
pt_sample2, = ax1.plot([], [], 'bo', markersize=8, label='Amostra 2 (Paralela)')
ax1.legend(loc='upper right')
ax1.grid(True)

# Plot 2: Multiplicador com Bypassing
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 4)
ax2.set_axis_off()
ax2.set_title("2. Multiplicador Digital (Estratégia de Bypassing)")

# Blocos do Multiplicador
rect1 = plt.Rectangle((1, 1.5), 2, 1, facecolor='lightgreen', edgecolor='black')
rect2 = plt.Rectangle((4, 1.5), 2, 1, facecolor='lightgreen', edgecolor='black')
rect3 = plt.Rectangle((7, 1.5), 2, 1, facecolor='lightgreen', edgecolor='black')
ax2.add_patch(rect1)
ax2.add_patch(rect2)
ax2.add_patch(rect3)

t1 = ax2.text(2, 2, "Somador 1\n(Ativo)", ha='center', va='center', fontweight='bold')
t2 = ax2.text(5, 2, "Somador 2\n(Ativo)", ha='center', va='center', fontweight='bold')
t3 = ax2.text(8, 2, "Somador 3\n(Ativo)", ha='center', va='center', fontweight='bold')

def update(frame):
    # Atualiza amostras do PSDM
    idx1 = (frame * 4) % len(x)
    idx2 = (idx1 + 2) % len(x)
    
    pt_sample1.set_data([x[idx1]], [y[idx1]])
    pt_sample2.set_data([x[idx2]], [y[idx2]])
    
    # Simula o Bypassing (Desliga blocos aleatoriamente com base em termos nulos)
    val = y[idx1]
    if abs(val) < 0.3: # Produto parcial próximo de zero -> Desliga somadores
        rect2.set_facecolor('lightgray')
        t2.set_text("Somador 2\n(BYPASSED/OFF)")
        rect3.set_facecolor('lightgray')
        t3.set_text("Somador 3\n(BYPASSED/OFF)")
    else:
        rect2.set_facecolor('lightgreen')
        t2.set_text("Somador 2\n(Ativo)")
        rect3.set_facecolor('lightgreen')
        t3.set_text("Somador 3\n(Ativo)")
        
    return pt_sample1, pt_sample2, rect2, rect3

ani = FuncAnimation(fig, update, frames=100, interval=150, blit=False)
plt.tight_layout()
plt.show()