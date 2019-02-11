import numpy as np
import matplotlib.pyplot as plt

"""
integrate and fire network
20 excitatory 5 inhibitory
simulate 10s of activity
show network has some properties
"""

class NetworkModel():
    def __init__(self, dt):

        # simulation params
        self.dt = dt
        self.vRe = 0
        self.vTh = 1

        # excitatory
        self.n_exc = 20
        self.tau_m_exc = 15 * 10**-3
        self.mu_exc = 1.1
        self.tau1_syn_exc = 1 * 10**-3
        self.tau2_syn_exc = 3 * 10**-3

        # inhibitory
        self.n_inh = 5
        self.tau_m_inh = 10 * 10**-3
        self.mu_inh = 1
        self.tau1_syn_inh = 1 * 10**-3
        self.tau2_syn_inh = 2 * 10**-3

        # connection probabilities
        self.pEE = 0.2
        self.pEI = 0.5
        self.pIE = 0.5
        self.pII = 0.5

        # synaptic strengths
        self.jEE = 0.024
        self.jEI = -0.045
        self.jIE = 0.014
        self.jII = -0.057

        # make neuron filter vectors
        self.Fe = self.make_F(dt, self.tau1_syn_exc, self.tau2_syn_exc, self.n_exc)
        self.Fi = self.make_F(dt, self.tau1_syn_inh, self.tau2_syn_inh, self.n_inh)

        # make connectivity matrices
        self.Jee = self.make_J(self.n_exc, self.n_exc, self.pEE, self.jEE)
        self.Jei = self.make_J(self.n_exc, self.n_inh, self.pEI, self.jEI)
        self.Jie = self.make_J(self.n_inh, self.n_exc, self.pIE, self.jIE)
        self.Jii = self.make_J(self.n_inh, self.n_inh, self.pII, self.jII)

        # make voltage vectors
        self.vE = np.zeros((1, self.n_exc))
        self.vI = np.zeros((1, self.n_inh))

    # neuron filter matrices
    def make_F(self, t, tau1, tau2, n):

        # make neuron filter vector
        filt = (1/(tau2 - tau1)) * (np.exp(-t/tau2) - np.exp(-t/tau1)) 
        mat = np.ones((1, n)) * filt

        return mat

    # make connectivity matrix/weight matrix
    def make_J(self, n_x, n_y, pXY, jXY):

        # make weight matrix
        mat = np.ones((n_x, n_y)) * jXY

        # spars ify matrix according to random selection
        rand_matrix = np.random.rand(n_x, n_y) < pXY

        return mat * rand_matrix

    # update voltage matrix, add bias, return spike vector
    def update_V(self, V, spike, F, J, vRe, vTh, mu):

        # get total amount of synaptic input from exc and inh
        syn = self.get_syn_input()

        # update V with synaptic input and Iinput
        V = 1/tau * (mu - V) + syn + Iinput

        # update spike
        spike = V > vTh

        # reset voltages over threshold
        V[V >= vTh] = vRe

        # refractory? some internal state structure?



    def get_syn_input():

        pass



# simulation
dt = 0.1 * 10**-3
stim = 0.07         # increased mu during "stim" 
s_to_plot = 10
t_vec = np.arange(0, s_to_plot, dt)
np.random.seed(123)

model = NetworkModel(dt)