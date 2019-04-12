
% load probabilities
prob_rwd_1 = csvread('prob_rwd_1.csv');
prob_rwd_2 = csvread('prob_rwd_2.csv');

% initialize
num_trials = 361;
a = 0.2;
b = 3;

% vars for qs/outputs
rand_nums = rand(1, num_trials);
qs_1 = zeros(1, num_trials + 1);
qs_2 = zeros(1, num_trials + 1);
qs_1(1) = 0.5;
qs_2(1) = 0.5;
prob_choice_1 = zeros(1, num_trials);
prob_choice_2 = zeros(1, num_trials);

%% run simulation
% iterate trials
for i = 1:num_trials
    
    % get qs
    q1 = qs_1(i);
    q2 = qs_2(i);
    
    % calculate probabilities of choosing
    prob_1 = 1 / (1 + exp(-b *(q1-q2)));
    prob_2 = 1 - prob_1;
    
    % save prob of choice
    prob_choice_1(i) = prob_1;
    prob_choice_2(i) = prob_2;
    
    % get p_reward and update qs if necessary
    rand_num = rand_nums(i);
    if prob_1 > prob_2
        p_reward = prob_rwd_1(i);
        rewarded = rand_num <= p_reward;
        rpe = rewarded - q1;
        new_q = q1 + (a * rpe);
        qs_1(i+1) = new_q;
        qs_2(i+1) = q2;
    else
        p_reward = prob_rwd_2(i);
        rewarded = rand_num <= p_reward;
        rpe = rewarded - q2;
        new_q = q2 + (a * rpe);
        qs_1(i+1) = q1;
        qs_2(i+1) = new_q;
    end
end

%% plot results of simulation
figure
hold on
plot(prob_rwd_1)
plot(qs_1)
plot(prob_choice_1)
title('qs for 1')
legend('prob_rwd', 'qs', 'prob_chc')

figure
hold on
plot(prob_rwd_2)
plot(qs_2)
plot(prob_choice_2)
title('qs for 2')
legend('prob', 'qs', 'prob_choice_2')


