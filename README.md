## Conceitos de Física e Modelo Matemático:
### Lançamento Oblíquo

Dado um objeto teste, de massa $m$, dotado de uma velocidade inicial $\vec{v_o}$ , lançado com certo ângulo $\theta$, formado com a horizontal, ele estará sujeito uma força graviracional $\vec{F_g}$, em que a aceleração da gravidade é uma constante $g$, e uma força viscosa de resistencia $\vec{F_v}$.
Nesse contexto, o nosso experimeto forma uma trajetória plana, podendo ser colocada no eixo XY, em que o objeto está sujeito a duas forças, que farão uma trajetória de acordo com o seguinte modelo matemático:

---

#### Definindo o referencial
  O movimento ocorrerá no plano XY. Assim, os vetores posição, velocidade, aceleração e forças podem ser descritos nos versores \($\hat{i}\$) e \($\hat{j}\$). Temos:

$$
\vec{r} = x(t) \hat{i} + y(t) \hat{j}
$$

$$
\vec{v} = \dot{\vec{r}} = v_x(t) \hat{i} + v_y(t) \hat{j}
$$

$$
\vec{a} = \ddot{\vec{r}} = a_x(t) \hat{i} + a_y(t) \hat{j}
$$

$$
\vec{F_g} = -m g \hat{j}
$$

$$
\vec{F_v} = -b \vec{v}
$$

Em que $b$ é um parâmetro positivo que depende do meio.

---

#### Segunda Lei de Newton

Aplicando a segunda lei de Newton ao movimento, obtemos as seguintes EDOs:

$$
m \vec{a} = \vec{F_g} + \vec{F_v}
$$

$$
m (a_x(t)\hat{i} + a_y(t)\hat{j}) = -mg\hat{j} - b(v_x(t)\hat{i} + v_y(t)\hat{j})
$$

EDO em X:

$$
m \ddot{x(t)} = - b \dot{x(t)}
$$

No caso especial para $b = 0$

$$
m \ddot{x(t)} = 0
$$

EDOS em Y:

$$
m \ddot{y(t)} = -mg -b\dot{y(t)}
$$

No caso especial para $b = 0$

$$
m \ddot{y(t)} = - m g
$$

---

#### Equações Horárias do movimento
Resolvendo as EDO's adquiridas acima, encontramos as seguintes equações horárias:
Seja $\alpha = b/m $, e $v_{0x} = v_0 \cos{\theta}$, $v_{0y} = v_0 \sin{\theta}$

$$
x(t) = x(0) + \frac{v_{0x}}{\alpha}(1 - e^{-\alpha t})
$$

$$
v_x(t) = v_{0x} e^{- \alpha t}
$$

$$
y(t) = y(0) - \frac{g t}{\alpha} + \big(\frac{\alpha v_{0y} + g}{\alpha^2}\big)(1 - e^{-\alpha t})
$$

$$
v_y(t) = - \frac{g}{\alpha} + \big(\frac{\alpha v_{0y} + g}{\alpha}\big) e^{- \alpha t}
$$

Para o caso em que $b = 0$

$$
x(t) = x(0) + v_{0x}
$$

$$
v_x(t) = v_{0x}
$$

$$
y(t) = y(0) + v_{0y} t - \frac{g t^2}{2}
$$

$$
v_y(t) = v_{0y} - gt
$$
